# SECTION 8 RENTALS AND MORE LLC
## AWS Enterprise Cloud Architecture & HUD/HIPAA Data Protection Framework
**Document Version:** 2026.1.0  
**Target Infrastructure:** AWS GovCloud / Commercial US-East / Cloudflare Edge  
**Entity:** Section 8 Rentals and More LLC (Dr. Albert Ray LaMotte, President / CEO)  

---

### 1. Data Classification & Scope
The platform processes sensitive records across Minnesota and Western Wisconsin voucher operations:
* **HUD Housing Assistance Data:** Vouchers (HUD-52646), RFTA Packets (HUD-52517), HAP contracts (HUD-52641).
* **Protected Health Information (PHI / HIPAA):** Reasonable Accommodation medical verifications, disability assistance animal letters, and medical expense deduction verifications.
* **Personally Identifiable Information (PII):** Social Security Numbers, banking ACH records, and government identification.

---

### 2. Multi-Tier AWS Infrastructure Architecture

[ User / Landlord / PHA ]
          |
  (Cloudflare Edge) ---- SSL/TLS 1.3 Termination, WAF, DDoS Mitigation
          |
  [ AWS API Gateway ] -- Strict IAM Token Authentication
          |
  [ AWS Lambda / ECS Fargate ] -- Isolated Microservices (RFTA, Legal Notices)
          |
     +----+----+
     |         |
[ AWS S3 ]  [ AWS RDS PostgreSQL ]
(Encrypted)  (Multi-AZ KMS Encrypted)

---

### 3. Encryption Standards & Key Management

* **Data at Rest:** 
  * Storage volumes (Amazon S3 buckets and RDS databases) encrypted via **AWS Key Management Service (KMS)** using dedicated customer-managed keys (CMKs) running **AES-256**.
  * Automated annual key rotation enabled.
* **Data in Transit:**
  * Strict **TLS 1.3** enforcement across all endpoints.
  * HSTS (HTTP Strict Transport Security) enabled with max-age=63072000; includeSubDomains; preload.

---

### 4. Identity & Access Management (IAM) & 2-Level RBAC

| Role Level | AWS IAM Policy | Application Scope | Audit Frequency |
| :--- | :--- | :--- | :--- |
| **Executive Admin** | `S8ExecutiveAdminPolicy` | Full system access, ledger sync, purge triggers, key rotation. | Quarterly |
| **Property Manager** | `S8ManagerScopedPolicy` | Scoped read/write to assigned units and PHA cases only. No export of raw PII/PHI. | Monthly |

---

### 5. Automated Data Retention & Sample Purge Failsafe

* **Production Lead Data:** Retained for 3 years post-lease termination in compliance with HUD 24 CFR § 982.158 retention mandates.
* **Local Storage / Edge Cache:** Client-side queues automatically purge sensitive tokens upon payload dispatch.
* **Testing Failsafe:** Zero test data retention on production tables. Automated sanitization script enforced via `purgeSampleData()` protocol.
