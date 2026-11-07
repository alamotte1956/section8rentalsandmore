# SECTION 8 RENTALS AND MORE LLC
## Enterprise Operations Manual & Compliance Protocol
**Document Version:** 2026.1.0  
**Effective Date:** November 07, 2026  
**Jurisdiction:** Minnesota (Metro Area) & Western Wisconsin  
**Corporate Authority:** Dr. Albert Ray LaMotte, President / CEO  

---

### 1. Executive Summary & Regulatory Authority
Section 8 Rentals and More LLC operates as a specialized dual-state property management, compliance, and HAP contract facilitation platform. This operations manual codifies standard operating procedures for managing Section 8 Housing Choice Voucher (HCV) tenancies across five primary Minnesota Public Housing Authorities (PHAs) and Western Wisconsin county housing agencies.

---

### 2. Covered Housing Authority Jurisdictions (Twin Cities Metro)

| Authority Code | Agency Name | Primary Service Territory | Standard Processing Window |
| :--- | :--- | :--- | :--- |
| **MN002** | Minneapolis Public Housing Authority (MPHA) | Minneapolis / Hennepin County | 14-21 Business Days |
| **MN001** | Saint Paul Public Housing Agency | St. Paul / Ramsey County | 10-15 Business Days |
| **MN042** | Dakota County Community Development Agency (CDA) | Dakota County (Burnsville, Eagan, Lakeville) | 7-14 Business Days |
| **MN033** | Washington County CDA | Washington County (Woodbury, Cottage Grove) | 10-14 Business Days |
| **MN027** | Anoka County Housing and Redevelopment Authority | Anoka County | 10-14 Business Days |
| **WI-REG** | Western Wisconsin Housing Regional Offices | St. Croix & Pierce Counties | 14-21 Business Days |

---

### 3. Request for Tenancy Approval (HUD-52517 RFTA) Workflow

1. **Voucher Verification:** Confirm tenant voucher bedroom size, expiration date, and verified subsidy standard prior to executing lease.
2. **Rent Reasonableness Test:** Ensure proposed contract rent plus utility allowance falls within the 110% Fair Market Rent (FMR) payment standard envelope.
3. **Utility Splits Matrix:** Define explicit utility responsibilities (Gas, Electric, Water/Sewer, Trash) using current PHA schedule deductions.
4. **Submission Execution:** Dispatch signed Form HUD-52517, lead-based paint disclosure, and unexecuted lease via automated packet compiler (`generate_rfta.py`).

---

### 4. HUD NSPIRE Pre-Inspection Standards & Fail Protocols
All units must undergo mandatory pre-audit scoring (`nspire_audit.py`) prior to official PHA inspection. Any positive finding on the following conditions triggers an automatic stop-work order:

* **Life-Safety Egress:** Unobstructed secondary exit in basement and sleeping areas; operable window sash locks.
* **Electrical Safety:** GFCI protection within 6 feet of all water sources; no open junction boxes or exposed wire runs.
* **Fire & Carbon Monoxide Detection:** Operable smoke alarms inside each bedroom and hallway; dual-sensor CO detectors within 10 feet of all sleeping rooms.
* **Plumbing & Water Heating:** Pressure relief valve discharge pipes terminated within 6 inches of the floor; zero active drain traps or supply leaks.
* **Lead-Based Paint Protocol:** Certified encapsulation on all pre-1978 friction surfaces (window wells, door frames) with zero peeling or chipping paint.

---

### 5. Multi-Jurisdictional Legal Notice Protocols

#### Minnesota Statutory Nonpayment Procedure (Minn. Stat. § 504B.321)
* **Pre-Filing Waiting Period:** Strict 14-day statutory written notice required before filing any eviction action in District Court.
* **Itemization Mandate:** Specific breakdown separating subsidized HAP portions from the tenant-responsible portion.
* **PHA Notice Service:** Simultaneous written delivery to the designated PHA voucher specialist is mandatory.

#### Wisconsin Statutory Default Procedure (Wis. Stat. § 704.17)
* **Notice Classification:** 5-Day Notice to Remedy Default or Vacate (remediable nonpayment) or 14-Day Notice to Vacate without option to cure (month-to-month tenancies or recurring default).
* **Delivery Proof:** Service via certified mail or personal physical delivery with affidavit of service.

#### Federal CARES Act Compliance (15 U.S.C. § 9058)
* **Covered Properties:** Mandatory 30-day notice period applies to any dwelling unit participating in covered federal housing programs (including Section 8 vouchers).

---

### 6. Edge Lead Intake & Automated Data Routing
* **Primary Intake Endpoint:** `https://www.section8rentalsandmore.com/api/send-lead`
* **Edge Service Provider:** Cloudflare Pages Functions (`/functions/api/send-lead.js`)
* **Transmission Gateway:** Resend API integration directly to `info@section8rentalsandmore.com`
* **Client Fallback Queue:** Local browser storage (`s8_leads_database`) with automated queue sync on re-established connection.
