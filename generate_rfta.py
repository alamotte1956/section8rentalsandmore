import os
import json
from pypdf import PdfReader, PdfWriter

PAYMENT_STANDARDS_2026 = {
    "dakota": {
        "cdacode": "MN042",
        "name": "Dakota County CDA",
        "limits": {"0": 1350, "1": 1540, "2": 1890, "3": 2420, "4": 2850}
    },
    "hennepin": {
        "cdacode": "MN002",
        "name": "Minneapolis PHA / Hennepin County",
        "limits": {"0": 1310, "1": 1490, "2": 1840, "3": 2360, "4": 2790}
    },
    "ramsey": {
        "cdacode": "MN001",
        "name": "Saint Paul PHA / Ramsey County",
        "limits": {"0": 1290, "1": 1460, "2": 1810, "3": 2320, "4": 2740}
    },
    "anoka": {
        "cdacode": "MN027",
        "name": "Anoka County HRA",
        "limits": {"0": 1280, "1": 1450, "2": 1795, "3": 2300, "4": 2720}
    },
    "washington": {
        "cdacode": "MN033",
        "name": "Washington County CDA",
        "limits": {"0": 1360, "1": 1550, "2": 1910, "3": 2450, "4": 2890}
    }
}

def generate_rfta_packet(data, output_filepath="Generated_HUD_52517_RFTA.pdf"):
    county = data.get("county", "").lower().strip()
    county_info = PAYMENT_STANDARDS_2026.get(county, {
        "cdacode": "MN-METRO",
        "name": county.title() + " Housing Authority",
        "limits": {}
    })
    
    bedrooms = str(data.get("bedrooms", "2"))
    payment_standard = county_info.get("limits", {}).get(bedrooms, "N/A")
    contract_rent = float(data.get("proposed_rent", 0.0))
    security_deposit = float(data.get("security_deposit", contract_rent))

    fields_payload = {
        "topmostSubform[0].Page1[0].Header[0].PHA_Name[0]": county_info["name"],
        "topmostSubform[0].Page1[0].Header[0].PHA_Code[0]": county_info["cdacode"],
        "topmostSubform[0].Page1[0].Section1[0].UnitAddress[0]": data.get("unit_address", ""),
        "topmostSubform[0].Page1[0].Section1[0].UnitCity[0]": data.get("city", ""),
        "topmostSubform[0].Page1[0].Section1[0].UnitState[0]": "MN",
        "topmostSubform[0].Page1[0].Section1[0].UnitZip[0]": data.get("zip", ""),
        "topmostSubform[0].Page1[0].Section1[0].Bedrooms[0]": bedrooms,
        "topmostSubform[0].Page1[0].Section1[0].YearBuilt[0]": str(data.get("year_built", "")),
        "topmostSubform[0].Page1[0].Section1[0].ProposedRent[0]": f"${contract_rent:,.2f}",
        "topmostSubform[0].Page1[0].Section1[0].SecurityDeposit[0]": f"${security_deposit:,.2f}",
        "topmostSubform[0].Page1[0].Section1[0].DateAvailable[0]": data.get("date_available", ""),
        "topmostSubform[0].Page1[0].Section1[0].StructureType[0]": data.get("structure_type", "Single Family Detached"),
        "topmostSubform[0].Page1[0].Section2[0].OwnerName[0]": data.get("landlord_legal_entity", "Section 8 Rentals and More LLC"),
        "topmostSubform[0].Page1[0].Section2[0].OwnerAddress[0]": data.get("landlord_address", "10805 173rd St W, Unit 127"),
        "topmostSubform[0].Page1[0].Section2[0].OwnerCity[0]": data.get("landlord_city", "Lakeville"),
        "topmostSubform[0].Page1[0].Section2[0].OwnerState[0]": "MN",
        "topmostSubform[0].Page1[0].Section2[0].OwnerZip[0]": data.get("landlord_zip", "55044"),
        "topmostSubform[0].Page1[0].Section2[0].OwnerPhone[0]": data.get("landlord_phone", "612-701-7064"),
        "topmostSubform[0].Page1[0].Section2[0].OwnerEmail[0]": data.get("landlord_email", "alamotte1956@gmail.com"),
        "topmostSubform[0].Page1[0].Section2[0].TenantName[0]": data.get("tenant_name", ""),
        "topmostSubform[0].Page1[0].Section2[0].TenantPhone[0]": data.get("tenant_phone", ""),
        "topmostSubform[0].Page2[0].Utilities[0].HeatingPayor[0]": data.get("heating_payor", "T"),
        "topmostSubform[0].Page2[0].Utilities[0].ElectricPayor[0]": data.get("electric_payor", "T"),
        "topmostSubform[0].Page2[0].Utilities[0].GasPayor[0]": data.get("gas_payor", "T"),
        "topmostSubform[0].Page2[0].Utilities[0].WaterPayor[0]": data.get("water_payor", "O"),
        "topmostSubform[0].Page2[0].Utilities[0].SewerPayor[0]": data.get("sewer_payor", "O"),
        "topmostSubform[0].Page2[0].Utilities[0].TrashPayor[0]": data.get("trash_payor", "O")
    }

    print("==================================================")
    print("      SECTION 8 RENTALS & MORE - RFTA ENGINE      ")
    print("==================================================")
    print(f"Target PHA:             {county_info['name']}")
    print(f"PHA Jurisdiction Code:  {county_info['cdacode']}")
    print(f"Bedroom Count:          {bedrooms} BR")
    print(f"2026 Payment Ceiling:   ${payment_standard}/month")
    print(f"Proposed Contract Rent: ${contract_rent:,.2f}/month")
    
    if isinstance(payment_standard, (int, float)):
        variance = payment_standard - contract_rent
        if variance >= 0:
            print(f"Compliance Check:       PASS (Within standard by ${variance:,.2f})")
        else:
            print(f"Compliance Check:       WARNING (Exceeds standard ceiling by ${abs(variance):,.2f})")

    template_path = "hud52517_blank.pdf"
    if os.path.exists(template_path):
        reader = PdfReader(template_path)
        writer = PdfWriter()
        writer.append(reader)
        writer.update_page_form_field_values(writer.pages[0], fields_payload)
        with open(output_filepath, "wb") as f_out:
            writer.write(f_out)
        print(f"Output File:            {output_filepath} (Form stamped successfully)")
    else:
        manifest_path = output_filepath.replace(".pdf", "_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f_out:
            json.dump({
                "status": "READY_FOR_SUBMISSION",
                "authority": county_info,
                "payment_standard": payment_standard,
                "data": fields_payload
            }, f_out, indent=2)
        print(f"Output Manifest:        {manifest_path} (Ready for submission)")
    print("==================================================")

if __name__ == "__main__":
    sample_intake = {
        "county": "dakota",
        "bedrooms": "3",
        "proposed_rent": 2250.00,
        "security_deposit": 2250.00,
        "unit_address": "10805 173rd St W, Unit 127",
        "city": "Lakeville",
        "zip": "55044",
        "year_built": 2004,
        "date_available": "2026-12-01",
        "structure_type": "Townhouse / Low-Rise",
        "landlord_legal_entity": "Section 8 Rentals and More LLC",
        "landlord_address": "10805 173rd St W, Unit 127",
        "landlord_city": "Lakeville",
        "landlord_zip": "55044",
        "landlord_phone": "612-701-7064",
        "landlord_email": "alamotte1956@gmail.com",
        "tenant_name": "Applicant Voucher Holder",
        "tenant_phone": "612-555-0192",
        "heating_payor": "T",
        "electric_payor": "T",
        "gas_payor": "T",
        "water_payor": "O",
        "sewer_payor": "O",
        "trash_payor": "O"
    }
    generate_rfta_packet(sample_intake)
