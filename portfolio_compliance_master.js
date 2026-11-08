
// portfolio_compliance_master.js - Complete Statutory & HUD Engine Registry
// Section 8 Rentals and More LLC • Twin Cities Metro & Western Wisconsin Operations

window.COMPLIANCE_ENGINES_REGISTRY = [
  { id: 'master_packet', title: '1-Click Master Lease-Up Packet', handler: 'generateMasterCompliancePacket', cat: 'Intake' },
  { id: 'rfta', title: 'Form HUD-52517 (RFTA Packet)', handler: 'generateRftaPacket', cat: 'Intake' },
  { id: 'safmr', title: 'HUD 110% SAFMR Rent Reasonableness', handler: 'generateRentReasonablenessStudy', cat: 'Financial' },
  { id: 'hap_contract', title: 'Form HUD-52641 HAP Contract Execution', handler: 'generateHapContract', cat: 'Legal' },
  { id: 'utility_allowance', title: 'Form HUD-52667 Utility Allowance Matrix', handler: 'computeUtilityAllowanceBreakdown', cat: 'Financial' },
  { id: 'lead_paint', title: 'EPA/HUD 24 CFR Part 35 Lead Paint Disclosure', handler: 'generateLeadPaintDisclosure', cat: 'Safety' },
  { id: 'nspire_audit', title: 'NSPIRE Pre-Inspection Audit & Scoring Cert', handler: 'runNspireAuditAudit', cat: 'Inspection' },
  { id: 'nspire_reinspection', title: 'Form HUD-52580 24-Hr LTF Defect Cure Cert', handler: 'generateCureCertification', cat: 'Inspection' },
  { id: 'vawa', title: 'Form HUD-5380 VAWA Occupancy Rights & Lease Bifurcation', handler: 'generateVawaNotice', cat: 'Legal' },
  { id: 'screening', title: 'Minn. Stat. § 504B.173 Screening Criteria & Adverse Action', handler: 'generateScreeningCriteriaDisclosure', cat: 'Intake' },
  { id: 'emergency_entry', title: 'Minn. Stat. § 504B.211 24-Hr Landlord Entry Notice', handler: 'generateLandlordEntryNotice', cat: 'Maintenance' },
  { id: 'emergency_dispatch', title: 'Twin Cities Emergency Trade Dispatch (P1 Work Order)', handler: 'dispatchEmergencyContractorWorkOrder', cat: 'Maintenance' },
  { id: 'rent_increase', title: 'HUD PIH 2023-27 60-Day Annual Rent Adjustment Notice', handler: 'generateRentIncreaseNotice', cat: 'Financial' },
  { id: 'legal_notices', title: 'Dual-State Cure Demand / 30-Day CARES Act Eviction Notice', handler: 'generateStatutoryNotice', cat: 'Legal' },
  { id: 'escrow_disposition', title: 'Minn. Stat. § 504B.178 21-Day Security Deposit Statement', handler: 'generateSecurityDepositDisposition', cat: 'Accounting' },
  { id: 'escrow_trust', title: 'Bank Escrow Trust Certification & 1.0% Simple Interest', handler: 'generateEscrowTrustCertificate', cat: 'Accounting' },
  { id: 'fair_housing', title: '42 U.S.C. § 3604 Reasonable Accommodation / Assistance Animal', handler: 'generateReasonableAccommodationPacket', cat: 'Legal' },
  { id: 'portability', title: 'Form HUD-52665 Inter-Agency Voucher Portability Packet', handler: 'generatePortabilityPacket', cat: 'Intake' },
  { id: 'schedule_e', title: 'IRS Schedule E & Form 1099-MISC Dual-Stream Reconciliation', handler: 'generateScheduleETaxReport', cat: 'Tax' },
  { id: 'pha_dispatch', title: 'Direct County PHA Electronic Submission Engine', handler: 'dispatchPacketToPha', cat: 'Dispatch' }
];

console.log("✔ Complete Section 8 Compliance Registry initialized: " + window.COMPLIANCE_ENGINES_REGISTRY.length + " statutory engines active.");
