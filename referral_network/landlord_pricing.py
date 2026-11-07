"""Approved introductory landlord subscription catalog.

Pricing is display-only until a separate, reviewed Stripe Checkout integration
is deployed. Never activate subscriptions or collect payment details here.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Plan:
    code: str
    name: str
    monthly_usd: int
    description: str

PLANS = (
    Plan("starter", "Landlord Starter", 0, "Free registration, one listing, anonymous preliminary matches"),
    Plan("plus", "Landlord Plus", 29, "Multiple listings, matching alerts and vacancy tools when available"),
    Plan("professional", "Landlord Professional", 79, "Portfolio matching, document workflows and reporting when available"),
    Plan("property_management", "Property Management", 199, "Starting price; multi-user portfolio services subject to agreement"),
)

BILLING_ENABLED = False
# Activation prerequisites: reviewed subscription terms, clear recurring-charge
# consent, cancellation flow, Stripe products/prices/webhooks, and end-to-end tests.
