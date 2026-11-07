# Section 8 Rentals and More — Resend sender configuration

Verified sending domain (confirm status in Resend): section8rentalsandmore.com

| Sender | Use |
| --- | --- |
| notifications@section8rentalsandmore.com | Transactional application and status notifications |
| referrals@section8rentalsandmore.com | Referral agency communications |
| support@section8rentalsandmore.com | Support correspondence and monitored replies |
| admin@section8rentalsandmore.com | Administrative operational correspondence |
| no-reply@section8rentalsandmore.com | Password reset and account verification messages |

Master administrator login: alamotte1956@gmail.com (separate from sending identities).

Production configuration in Railway (do not commit secrets):
- RESEND_API_KEY: private Resend API key.
- RESEND_FROM_EMAIL: notifications@section8rentalsandmore.com (initial default).
- RESEND_REPLY_TO: support@section8rentalsandmore.com (only after mailbox/forwarding is working).
- EMAIL_ENABLED: true **only after** verified domain and delivery testing.

Use the appropriate sender address for each message type. Configure incoming mailboxes or forwarding separately; Resend domain verification does not create inboxes. Never email sensitive tenant records, SSNs, voucher documents, or private financial information. Managers must never receive financial notifications or have access to financial APIs. Do not turn on automated sends until workflows are integrated and tested.
