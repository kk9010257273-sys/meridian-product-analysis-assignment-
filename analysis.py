"""
Phyllo Product Analyst Assignment - supporting validation script.

This script expects the candidate-pack response files to be placed in:
data/orders_page1.json
data/orders_page2.json
data/order_ord_9999.json

It checks:
- documented total arithmetic
- documented monetary representation
- documented customer email requirement
- documented status values
"""

import json
from pathlib import Path

DATA = Path("data")

ALLOWED_STATUSES = {"pending", "shipped", "delivered", "cancelled"}


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def check_order(order, source):
    findings = []
    subtotal = order.get("subtotal")
    tax = order.get("tax")
    shipping = order.get("shipping")
    total = order.get("total")

    # Contract: total = subtotal + tax + shipping
    if all(isinstance(x, (int, float)) for x in (subtotal, tax, shipping, total)):
        expected = subtotal + tax + shipping
        if round(expected, 2) != round(total, 2):
            findings.append(
                f"{source}: {order['id']} total mismatch: "
                f"expected {expected}, actual {total}"
            )

    # Contract: monetary amounts are integers in smallest currency unit
    for field in ("subtotal", "tax", "shipping", "total"):
        value = order.get(field)
        if not isinstance(value, int) or isinstance(value, bool):
            findings.append(
                f"{source}: {order['id']}.{field} is {value!r}; "
                "expected an integer smallest-unit amount"
            )

    # Contract: status must be one of the documented values
    if order.get("status") not in ALLOWED_STATUSES:
        findings.append(
            f"{source}: {order['id']}.status={order.get('status')!r}; "
            f"not in documented values {sorted(ALLOWED_STATUSES)}"
        )

    # Contract: customer email is always present
    email = order.get("customer", {}).get("email")
    if email is None:
        findings.append(
            f"{source}: {order['id']}.customer.email is null; "
            "documentation says it is always present"
        )

    return findings


def main():
    findings = []

    for filename in ("orders_page1.json", "orders_page2.json"):
        payload = load(filename)
        for order in payload.get("data", []):
            findings.extend(check_order(order, filename))

    missing = load("order_ord_9999.json")
    if missing.get("order") is None:
        findings.append(
            "order_ord_9999.json: captured HTTP status is 200, "
            "but documentation says a nonexistent order should return 404."
        )

    print("Findings:")
    for item in findings:
        print("-", item)


if __name__ == "__main__":
    main()
