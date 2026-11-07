"""Opt-in transactional Resend delivery. Keep API keys in Railway secrets."""
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SENDERS = {
    "notifications": "notifications@section8rentalsandmore.com",
    "referrals": "referrals@section8rentalsandmore.com",
    "support": "support@section8rentalsandmore.com",
    "admin": "admin@section8rentalsandmore.com",
    "no-reply": "no-reply@section8rentalsandmore.com",
}

class EmailDeliveryError(RuntimeError):
    pass

def send_email(to, subject, text, *, sender="notifications", reply_to=None):
    """Send a single transactional email; disabled until explicitly configured.

    Never put sensitive tenant documents, SSNs or financial details in email.
    """
    if os.getenv("EMAIL_ENABLED", "").lower() != "true":
        raise EmailDeliveryError("Email sending is disabled")
    key = os.getenv("RESEND_API_KEY")
    if not key:
        raise EmailDeliveryError("RESEND_API_KEY is not configured")
    if sender not in SENDERS:
        raise ValueError("Unknown sender")
    if not isinstance(to, str) or not to.strip() or not subject or not text:
        raise ValueError("Recipient, subject and message are required")
    payload = {"from": SENDERS[sender], "to": [to], "subject": subject, "text": text}
    if reply_to:
        payload["reply_to"] = reply_to
    req = Request("https://api.resend.com/emails",
                  data=json.dumps(payload).encode("utf-8"),
                  headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
                  method="POST")
    try:
        with urlopen(req, timeout=15) as response:
            return json.load(response)["id"]
    except HTTPError as exc:
        raise EmailDeliveryError("Email provider rejected request: HTTP " + str(exc.code)) from exc
    except (URLError, TimeoutError, KeyError, ValueError) as exc:
        raise EmailDeliveryError("Email provider request failed") from exc
