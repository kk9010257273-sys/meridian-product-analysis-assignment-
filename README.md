# Phyllo Product Analyst Internship Assignment

This repository contains my submission for the Product Analyst Intern take-home assignment.

## Contents

- `submission.md` — final write-up (under 800 words)
- `analysis.py` — supporting Python validation script
- `data/` — local-only folder for the candidate-pack JSON responses

## How to run the analysis

1. Place the three candidate-pack JSON files in `data/`:
   - `orders_page1.json`
   - `orders_page2.json`
   - `order_ord_9999.json`
2. Run:

```bash
python analysis.py
```

The script checks the response data against the documented API contract.

## Note

Do not publish confidential candidate-pack/source files unless the assignment explicitly permits redistribution. The final submission and supporting script are intended to be the public-facing contents.
