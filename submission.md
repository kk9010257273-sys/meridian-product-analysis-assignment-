# Product Analyst Intern Assignment 

## Task 1 — API/documentation mismatches

I found five meaningful mismatches:

1. **Incorrect order total — `ord_1004`**  
   The documentation says `total = subtotal + tax + shipping`. The response gives 6200 + 511 + 599 = **7310**, but returns `total: 6810`. This can directly cause incorrect financial reporting.

2. **Undocumented status — `ord_1003`**  
   The documented statuses are `pending`, `shipped`, `delivered`, and `cancelled`, but the API returns `refunded`. Consumers validating against the documented enum could reject or mishandle the order.

3. **Missing required email — `ord_1005`**  
   The documentation says `customer.email` is always present, but the response contains `null`. Applications assuming a string may fail or require undocumented null handling.

4. **Incorrect monetary representation — `ord_1006`**  
   The documentation specifies integer amounts in the smallest currency unit. This order instead returns decimal dollar values (`53.62` rather than `5362`). This could cause incorrect financial calculations for consumers following the documented contract.

5. **Incorrect HTTP status for a missing order**  
   `GET /v1/orders/ord_9999` returns HTTP 200 with `{"order": null}`, while the documentation says a nonexistent order returns 404. This can break clients relying on HTTP status codes for error handling.

**Most serious:** the monetary representation issue is particularly risky because it can cause downstream financial systems to interpret the same value incorrectly.

## Task 2 — Total revenue

I normalized the monetary values to dollars before summing. I excluded `ord_1003` because its status is `refunded`; however, the documentation does not explicitly define whether refunded orders should be included in revenue.

**Revenue = $225.70**

If the intended definition is to include refunded orders, the gross order-total amount is **$328.03**. The supplied documentation does not provide enough information to determine the refund treatment definitively.

## Task 3A — Reply to Priya

**Subject: Re: Revenue reconciliation**

Hi Priya,

Thanks for flagging this. I reviewed the orders returned by the Meridian API and found several data issues that can explain the discrepancy.

`ord_1004` has a total that does not equal its subtotal, tax and shipping. `ord_1006` also uses a different monetary format from the documented API contract. There is additionally a refunded order, although the API documentation does not specify how refunds should be treated in revenue.

Assuming refunded orders are excluded, the revenue from the available orders is **$225.70**.

I've documented the underlying API issue separately for engineering investigation.

Best,
KiranKumar Borigarla

## Task 3B — Bug report

**Title:** `GET /v1/orders` returns monetary values in inconsistent units

**Issue:** `ord_1006` returns `subtotal`, `tax`, `shipping`, and `total` as decimal dollar values, despite the API contract specifying integer smallest-unit amounts.

**Actual:** `total: 53.62`  
**Expected:** `total: 5362`

**Impact:** Consumers following the documented contract may calculate incorrect financial values.

**Evidence:** `orders_page2.json`, `ord_1006`.

**Fix:** Return monetary values consistently in the documented smallest-unit format, or update the contract if decimal major-unit values are intentional.
