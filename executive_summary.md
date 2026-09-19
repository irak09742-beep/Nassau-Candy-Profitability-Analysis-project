# Executive Summary

## Business question
Which Nassau Candy product lines generate the most economic value, where are margins weaker, and where should management focus pricing, cost and portfolio decisions?

## Dataset
The project uses the publicly documented Nassau Candy transaction dataset with 10,194 order-line records, 15 products, 3 divisions, 4 sales regions and 5 manufacturing factories.

## Key analytical measures
- Revenue = sum of Sales
- Gross Profit = sum of Gross Profit
- Gross Margin % = Gross Profit / Sales × 100
- Profit per Unit = Gross Profit / Units
- Cost Ratio % = Cost / Sales × 100
- Revenue/Profit contribution = product value ÷ portfolio value
- Pareto concentration = cumulative product profit contribution

## Reported portfolio-level findings
The published April 2026 analysis reports $141,784 revenue, $93,443 gross profit and a 65.9% portfolio gross margin. It reports Chocolate at 92.9% of revenue, four products contributing approximately 80% of gross profit, and the Other division at approximately 50.1% gross margin.

## Interpretation
The dashboard should not rely on revenue alone. A product can have high sales but a weaker margin, while a lower-volume product can have strong margin efficiency. The project therefore combines absolute profit, margin percentage, profit per unit, cost ratio and concentration measures.

## Recommended management workflow
1. Protect high-profit/high-margin products from stock-outs.
2. Investigate high-sales/low-margin products for pricing and cost structure.
3. Review products with high cost ratios before making discontinuation decisions.
4. Monitor division-level margin and revenue/profit mix.
5. Use the Pareto view to understand dependency on a small number of products.
6. Re-run the dashboard after pricing or sourcing changes to measure impact.

## Caveat
The exact values above are reported findings from the published project reference; the included Streamlit application recalculates metrics directly from the transaction CSV at runtime.
