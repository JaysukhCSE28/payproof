# Judge Q&A (scaffold)

- **Who writes the numbers?** Dual calc engines (`Decimal` + integer paise), not the LLM.
- **Verdicts?** `MATCH`, `DISCREPANCY`, `CANNOT_DETERMINE`.
- **When do we abstain?** Low OCR, missing fields, engine disagreement, or injection-like input.
- **What is executable policy?** Only `status=reviewed` rule cards.

TODO: add failure-mode answers after eval metrics exist.
