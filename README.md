# Nassau Candy — Product Line Profitability & Margin Performance Analysis

## Project objective
Analyze Nassau Candy Distributor transaction data to identify product-level profit drivers, margin risks, division performance, cost inefficiencies, and profit concentration.

## Deliverables
- Interactive Streamlit dashboard (`app.py`)
- Research paper (`reports/research_paper.pdf`)
- Executive summary (`reports/executive_summary.md`)
- Video feedback script (`reports/video_feedback_script.md`)
- Reproducible analysis notebook (`src/analysis_notebook.ipynb`)
- Requirements file for deployment

## Dataset
The dashboard reads the publicly accessible Nassau Candy Distributor transaction CSV used in multiple published project analyses. The source contains 10,194 transaction rows and fields for order/shipment dates, customer geography, division, region, product, sales, units, gross profit and cost.

Source repository:
https://github.com/Prasannasegabandi36/Nassau-Candy-Distributor

Raw CSV:
https://raw.githubusercontent.com/Prasannasegabandi36/Nassau-Candy-Distributor/main/Nassau%20Candy%20Distributor.csv

## Analytical framework
1. Data cleaning and validation
2. Gross margin and profit-per-unit calculations
3. Product-level ranking
4. Division-level performance
5. Cost-ratio diagnostics
6. Pareto profit concentration
7. Geographic revenue concentration
8. Interactive filters and dashboard views

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit deployment
Create a GitHub repository, upload the project files, then deploy `app.py` through Streamlit Community Cloud.

## Important data-quality note
Published analyses of this dataset report that the Order Date and Ship Date ranges are not operationally realistic. This dashboard therefore treats shipping dates only as source fields and does not use lead-time findings as evidence of real-world delivery performance.

## Technology
Python, pandas, NumPy, Plotly, Streamlit.
