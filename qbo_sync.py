import json
from datetime import datetime

class QBOSection8SyncEngine:
    def __init__(self, company_name="Section 8 Rentals and More LLC"):
        self.company_name = company_name
        self.accounts = {
            "hap_income": "4010 - HUD Section 8 HAP Direct Deposits",
            "tenant_income": "4020 - Tenant Direct Rent Collections",
            "utility_reimbursement": "5030 - Utility Allowance Pass-Through",
            "clearing_account": "1050 - Section 8 ACH Clearing",
            "undeposited_funds": "1099 - Undeposited Funds"
        }

    def process_disbursement(self, unit_id, tenant_name, pha_code, total_rent, tenant_copay):
        hap_portion = total_rent - tenant_copay
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        journal_entry = {
            "transaction_id": f"JE-{pha_code}-{unit_id}-{datetime.now().strftime('%Y%m%d%H%M')}",
            "date": timestamp,
            "entity": self.company_name,
            "unit": unit_id,
            "tenant": tenant_name,
            "pha_source": pha_code,
            "allocations": [
                {
                    "account": self.accounts["clearing_account"],
                    "type": "Debit",
                    "amount": total_rent,
                    "description": f"Monthly Rent Settlement: Unit {unit_id}"
                },
                {
                    "account": self.accounts["hap_income"],
                    "type": "Credit",
                    "amount": hap_portion,
                    "description": f"PHA ACH Subsidy Transfer ({pha_code})"
                },
                {
                    "account": self.accounts["tenant_income"],
                    "type": "Credit",
                    "amount": tenant_copay,
                    "description": f"Tenant Out-of-Pocket Share ({tenant_name})"
                }
            ],
            "balanced": True
        }
        return journal_entry

if __name__ == "__main__":
    engine = QBOSection8SyncEngine()
    test_entry = engine.process_disbursement(
        unit_id="BLM-104",
        tenant_name="Sample Section 8 Tenant",
        pha_code="MN042",
        total_rent=2150.00,
        tenant_copay=450.00
    )
    with open("qbo_ledger_export.json", "w", encoding="utf-8") as f:
        json.dump(test_entry, f, indent=2)
    print(f"[+] QBO Financial Ledger synced: qbo_ledger_export.json")
