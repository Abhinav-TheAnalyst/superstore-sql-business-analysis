**Executive Summary — Superstore Analysis**

Author: Abhinav Verma — https://github.com/Abhinav-TheAnalyst / https://www.linkedin.com/in/abhinav-theanalyst/
Dataset: Sample — Superstore (Kaggle)

Key findings

- Profit is concentrated in a small number of categories and customers. A short list of profitable customers drives a large share of total profit — these accounts are high-priority for retention and expansion.
- Deep discounts (roughly >20%) often correspond with negative or very low profit margins. Revisit blanket discounts on low-margin SKUs.
- Some states show high sales but negative profit, suggesting product mix or promotional issues at a state level. Prioritize corrective actions where sales are large but margins are poor.
- A small set of SKUs produce repeated losses — consider removing them from promotions or renegotiating costs.

Recommended next steps

1. Run a promotions audit focused on SKUs and campaigns with discounts > 20% and quantify profit impact per SKU.
2. Build a compact dashboard with KPI cards (Sales, Profit, Margin), Region × Category performance, and a Discount vs Profit scatter plot.
3. Produce a top-20 profitable-customer list and draft targeted retention offers.
4. Run small, controlled discount experiments to measure elasticity before scaling promotions.

Notes for interviews

- Briefly describe the cleaning approach: standardised names/dates, coerced numeric types, and added year/month for aggregation.
- Walk through 2–3 SQL queries that directly answer business questions (e.g., discount impact, top customers, regions with losses).
- Use the executive summary to present the business recommendations and show the supporting SQL for technical depth.
**Executive Summary — Superstore Analysis**

- **Author:** Abhinav Verma — https://github.com/Abhinav-TheAnalyst / https://www.linkedin.com/in/abhinav-theanalyst/
- **Dataset:** Sample — Superstore (Kaggle)

Key findings (concise):

- **Profit concentrated in a few categories and customers.** A small set of customers and product groups contribute a large share of profit. These customers are good candidates for loyalty and expansion programs.
- **Deep discounts often coincide with losses.** Orders with discounts above ~20% frequently show negative or low profit margins — revisit discounting policy for low-margin products.
- **Regional mix matters.** Some regions have high sales but low margins, indicating either product mix issues or excessive discounting. Prioritize state-level fixes where large sales still produce negative profits.
- **Product assortment optimization.** Identify loss-making SKUs and either reduce discounting on them, renegotiate supplier costs, or remove them from promotions.

Recommended next steps:

1. Run a promotions audit: identify campaigns and SKUs where discounts exceed margin thresholds and produce a short remediation plan.
2. Build a dashboard (Power BI / Tableau) showing Sales, Profit, Margin by Region × Category and a Discount vs Profit scatter plot.
3. Create a short list of top 20 profitable customers and design targeted retention offers.
4. Monitor discount elasticity: run controlled experiments where discount levels are varied and measure profit lift.

How to cite these outputs in interviews:

- Briefly explain the cleaning approach (standardize names/dates, add year/month, ensure numeric types).
- Walk through 2–3 SQL queries that answer a business question (e.g., discount impact, top customers, region losses).
- Show the executive summary and recommend specific next actions backed by numbers.
