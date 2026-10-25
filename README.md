# StockWise — Inventory Decision Copilot

## Overview
StockWise is a prototype inventory decision-support tool that helps retailers identify products at risk of stockouts and prioritize replenishment decisions. 

## Problem
Retailers need to balance product availability with inventory holding costs. Limited visibility into stock levels, daily sales, incoming inventory, and supplier lead times can make replenishment decisions difficult.

## Solution
StockWise analyzes inventory inputs and provides:
- Inventory risk classification: High, Medium, and Low.
- Estimated days of stock cover.
- Suggested reorder quantities.
- Estimated replenishment costs.
- Explanations and recommended next actions.

## How It Works
The prototype uses rule-based calculations based on current stock, average daily sales, supplier lead time, incoming stock, and a safety-stock assumption.

It calculates projected inventory risk and estimates reorder quantities to help users prioritize decisions.

## Product Thinking
The project explores how a decision-support product can turn raw operational data into actionable recommendations, rather than simply displaying metrics.

Key considerations include usability, explainability, prioritization, and keeping a human involved in inventory decisions.

## Tech Stack
- Python
- Pandas
- Streamlit
- Synthetic inventory data

## Current Limitations
- Uses synthetic demonstration data, not live retailer data.
- Replenishment recommendations are rule-based, not machine-learning forecasts.
- Safety stock is based on a simplified assumption.
- Recommendations require human review before real-world use.

## Future Improvements
- Upload inventory data through CSV files.
- Incorporate supplier-specific constraints and minimum order quantities.
- Allow users to adjust safety-stock assumptions.
- Track stockout and overstock outcomes.
- Evaluate recommendation quality using real operational data.

## Project Status
Working prototype built and tested with synthetic data.

**Live Demo:** [Add your Streamlit app URL here]
**GitHub Repository:** https://github.com/YOUR-USERNAME/stockwise-inventory-copilot

---

## Product Management Case Study

StockWise is not just a working inventory prototype. This repository also documents the product thinking behind it, from problem discovery to prioritization and product strategy.

### Project Phases

| Phase | Focus | Status |
|---|---|---|
| Phase 1 | Problem discovery and initial problem definition | Initial hypotheses |
| Phase 2 | User persona, Jobs to Be Done (JTBD), and research plan | Documented; research pending |
| Phase 3 | Product requirements and MVP definition | Documented; assumptions pending validation |
| Phase 4 | Feature prioritization, success metrics, and experiments | Upcoming |
| Phase 5 | Blinkit product teardown using product-management frameworks | Upcoming |

### Product Documentation

- [Phase 2: User Research, Persona & Jobs to Be Done](product-management/02-user-research-and-jtbd.md)
- [Phase 3: Product Requirements and MVP Definition](product-management/03-prd-and-mvp.md)

*Note: Proposed user needs and pain points are hypotheses until validated through research with actual users. Upcoming phases will be added as the case study develops.*
