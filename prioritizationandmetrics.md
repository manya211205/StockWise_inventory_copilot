# Phase 4: Feature Prioritization and Success Metrics

## 1. Objective

The objective of this phase is to identify which features StockWise should prioritize next and define how their impact should be measured.

StockWise is an Inventory Decision Copilot designed to help inventory and operations managers at small D2C brands identify inventory risks, prioritize replenishment decisions, and manage purchasing within budget constraints.

The current prototype supports inventory risk identification, reorder recommendations, prioritized action lists, budget-aware replenishment, and CSV-based data input and export.

The next step is to determine which improvements would deliver the greatest user value while balancing business objectives, implementation effort, and feasibility.

**Important:** The priorities and metrics in this document are initial product hypotheses. They have not yet been validated through user interviews or real-world usage data.

## 2. Feature Prioritization Framework

The IIMA Product Mindset Casebook discusses evaluating features using factors such as user value, business value, strategic fit, effort, and feasibility.

For StockWise, the following factors will guide prioritization:

- **User value:** How significantly does the feature address an inventory-management problem?
- **Business value:** Could the feature improve product adoption, retention, or the perceived usefulness of StockWise?
- **Strategic fit:** Does it strengthen StockWise's core purpose of helping users make better replenishment decisions?
- **Effort and feasibility:** How much development work, data, and technical complexity would implementation require?
- **Confidence:** How much evidence supports the assumption that users need the feature?

These factors will be reassessed after user research and prototype testing.

## 3. Features Under Consideration

### Feature A: Improve Recommendation Transparency

**Problem hypothesis:** Users may hesitate to trust a reorder recommendation if they cannot understand why a product has been classified as high risk or why a particular quantity has been recommended.

**Proposed improvement:**
- Explain the reason behind each inventory-risk classification.
- Display relevant inputs, such as days of cover, lead time, and projected stock.
- Show how the suggested reorder quantity was calculated.

**Expected value:** Could make recommendations easier to understand and evaluate.

**Effort:** Low to medium, depending on the changes required to the existing interface and calculation logic.

**Validation required:** Test whether users understand the recommendations and whether explanations increase their confidence in the tool.

### Feature B: Improve Budget-Based Prioritization

**Problem hypothesis:** Inventory managers may have to choose between replenishing multiple products when their available purchasing budget is insufficient to cover every recommended order.

**Proposed improvement:**
- Rank replenishment decisions by urgency and potential business impact.
- Allow users to specify a purchasing budget.
- Explain which orders are prioritized and which are deferred.

**Expected value:** Could help users make more informed purchasing decisions when budgets are constrained.

**Effort:** Medium, depending on how supplier constraints, minimum order quantities, and other purchasing requirements are handled.

**Validation required:** Understand how frequently users face budget constraints and how they currently prioritize competing replenishment needs.

### Feature C: Improve CSV Data Validation

**Problem hypothesis:** Missing, inconsistent, or invalid input data may result in misleading inventory calculations and recommendations.

**Proposed improvement:**
- Detect missing required columns and values.
- Validate numeric fields and reject impossible or invalid inputs.
- Flag suspicious values, such as negative stock or non-positive lead times.
- Display actionable error messages before generating recommendations.

**Expected value:** Could improve the reliability of the existing workflow and reduce the risk of decisions based on incorrect inputs.

**Effort:** Low to medium, depending on the range of validations implemented.

**Validation required:** Test common input errors and determine how often data-quality problems occur in users' actual workflows.

### Feature D: Add Demand Forecasting

**Problem hypothesis:** Average daily sales may not adequately represent future demand when sales patterns change due to seasonality, promotions, or other factors.

**Proposed improvement:**
- Use historical, time-stamped sales data to estimate future demand.
- Compare forecast-based demand estimates with the current average-daily-sales approach.
- Incorporate validated demand estimates into replenishment recommendations only if they improve decision quality.

**Expected value:** Could improve replenishment decisions when historical demand patterns provide useful predictive information.

**Effort:** High relative to the other proposed features because it requires suitable historical data, forecasting logic, and evaluation against a baseline.

**Validation required:** Establish whether users have access to historical sales data, identify relevant demand patterns, and test whether forecasts outperform a simple baseline.

Demand forecasting is a proposed future direction, not a confirmed user requirement.

## 4. Comparative Evaluation

| Feature | Potential user value | Relative effort | Key uncertainty |
|---|---|---|---|
| A. Recommendation transparency | Medium to high | Low–medium | Whether explanations improve understanding and trust |
| B. Budget-based prioritization | Medium to high | Medium | How frequently purchasing budgets constrain decisions |
| C. CSV data validation | Medium to high | Low–medium | Frequency and impact of input-data errors |
| D. Demand forecasting | Potentially high | High | Data availability and measurable forecast improvement |

These are qualitative assessments, not measured results. Actual value and effort may differ after research and technical evaluation.

## 5. Provisional Prioritization Decision

Based on the current prototype and implementation feasibility, **CSV data validation and recommendation transparency are the initial candidates for prioritization**.

The reasoning is:

1. **Data validation:** Reliable input data is necessary for meaningful inventory calculations. Preventing invalid inputs may reduce avoidable errors in existing recommendations.
2. **Recommendation transparency:** Users should be able to understand how the tool reaches its recommendations before relying on them for purchasing decisions.
3. **Budget-based prioritization:** This remains a strong candidate if research confirms that users frequently face competing replenishment needs under a limited budget.
4. **Demand forecasting:** This should be evaluated after confirming the availability of historical sales data and establishing a reliable baseline for comparison.

This is a provisional, feasibility-led decision rather than a conclusion about which feature users value most. User research may change the order.

## 6. Applying the RICE Framework

The RICE framework evaluates features using:

**RICE Score = (Reach × Impact × Confidence) / Effort**

- **Reach:** Number of users or decisions affected during a defined period.
- **Impact:** Expected effect on the user or business outcome.
- **Confidence:** Strength of the evidence supporting the estimates.
- **Effort:** Estimated implementation work, expressed consistently, such as in person-months.

A numerical RICE score has not been assigned because reliable estimates for reach, impact, confidence, and effort are not yet available. Assigning precise numbers now would create false confidence.

The following evidence is needed before scoring:

- **Transparency:** Usability-test results and feedback about recommendation explanations.
- **Budget prioritization:** Interview evidence about purchasing constraints and examples of competing replenishment decisions.
- **Data validation:** Frequency and consequences of invalid or incomplete inventory inputs.
- **Demand forecasting:** Availability of historical sales data, forecast accuracy against a simple baseline, and evidence of the business impact of forecast errors.

Once this evidence is collected, each feature can be scored using consistent assumptions and compared more rigorously.

## 7. Success Metrics

The metrics below are proposed for future evaluation. No improvement has yet been measured.

### North Star Metric

**Proposed North Star Metric: Number of replenishment decisions completed with a documented rationale and no critical data-quality issues.**

This metric aims to capture whether StockWise helps users move from inventory information to a more informed decision.

It is provisional and should be tested against actual user workflows before being adopted as the final North Star Metric.

### Supporting Metrics

**1. Time to complete a replenishment review**

- Measures the time users need to review inventory and decide what to replenish.
- A reduction may indicate a more efficient workflow.
- Compare against a baseline using the same tasks and similar users.

**2. Recommendation acceptance and override rate**

- Measures how often users accept, modify, or reject recommendations.
- Record the reasons for overrides to identify gaps in the recommendation logic.
- A high acceptance rate alone should not be treated as proof of recommendation quality.

**3. Data validation failure rate**

- Measures the proportion of uploaded files that contain validation errors.
- Track the most common error types and whether users successfully resolve them.
- Interpret changes carefully because a lower failure rate could reflect better input quality or changes in the users uploading files.

### Guardrail Metrics

**1. Recommendation error rate**

Track cases where a recommendation is materially misleading because of incorrect inputs, calculations, or assumptions.

**2. Stockout and excess-inventory outcomes**

If real operational data becomes available, monitor stockouts and excess inventory to check whether recommendations support better inventory outcomes. These outcomes are affected by factors beyond StockWise, so avoid attributing every change to the product.

**3. Budget constraint violations**

For budget-aware recommendations, track whether proposed purchasing decisions exceed the user's specified budget or ignore known purchasing constraints.

## 8. Validation Plan

Before committing to a feature roadmap, the following steps are proposed:

1. Conduct interviews with inventory or operations managers at small D2C brands.
2. Ask participants to describe their most recent replenishment decision, including the data used, constraints faced, and problems encountered.
3. Test the existing StockWise prototype to understand whether users can interpret its recommendations.
4. Collect examples of CSV input problems and assess the value of additional validation.
5. Determine whether suitable historical sales data is available for demand forecasting.
6. Estimate reach, impact, confidence, and effort for each feature.
7. Revisit prioritization using the RICE framework and the qualitative evaluation.
8. Establish baseline measurements before claiming that StockWise improves decision speed or inventory outcomes.

Until this research is completed, feature priorities and expected benefits remain hypotheses.

## 9. Conclusion

StockWise should prioritize improvements that make its existing replenishment workflow more reliable and understandable while investigating which problems matter most to target users.

CSV data validation and recommendation transparency are the initial candidates because they strengthen the reliability and explainability of the current prototype. Budget-based prioritization may become the leading candidate if research confirms that limited purchasing budgets are a frequent and important problem.

Demand forecasting remains a promising future direction, but it should be introduced only when appropriate historical data is available and testing demonstrates value beyond the current average-daily-sales approach.

The final roadmap should be based on user evidence, feasibility, and measurable outcomes rather than assumptions alone.
