import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Nassau Candy | Profitability Intelligence", page_icon="🍬", layout="wide")

DATA_URL = "https://raw.githubusercontent.com/Prasannasegabandi36/Nassau-Candy-Distributor/main/Nassau%20Candy%20Distributor.csv"

FACTORY_MAP = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar - Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Kazookles": "The Other Factory",
}

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    df.columns = [c.strip() for c in df.columns]
    for c in ["Division","Region","Product Name","Ship Mode","City","State/Province","Country/Region"]:
        if c in df:
            df[c] = df[c].astype(str).str.strip()
    # Normalize known product-name spacing variation.
    df["Product Name"] = df["Product Name"].str.replace(r"\s*-\s*", " - ", regex=True)
    df["Product Name"] = df["Product Name"].str.replace(r"\s+", " ", regex=True).str.strip()
    for c in ["Sales","Units","Gross Profit","Cost"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True, errors="coerce")
    df = df.drop_duplicates().copy()
    df = df[(df["Sales"] > 0) & (df["Units"] > 0) & (df["Cost"] >= 0)].copy()
    df["Gross Margin %"] = np.where(df["Sales"] != 0, df["Gross Profit"]/df["Sales"]*100, np.nan)
    df["Profit per Unit"] = np.where(df["Units"] != 0, df["Gross Profit"]/df["Units"], np.nan)
    df["Revenue per Unit"] = np.where(df["Units"] != 0, df["Sales"]/df["Units"], np.nan)
    df["Cost per Unit"] = np.where(df["Units"] != 0, df["Cost"]/df["Units"], np.nan)
    df["Cost Ratio %"] = np.where(df["Sales"] != 0, df["Cost"]/df["Sales"]*100, np.nan)
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Quarter"] = df["Order Date"].dt.to_period("Q").astype(str)
    df["Factory"] = df["Product Name"].map(FACTORY_MAP).fillna("Unmapped")
    return df

df = load_data()

st.title("🍬 Nassau Candy — Product Profitability & Margin Intelligence")
st.caption("Interactive analytics dashboard aligned to the Unified Mentor project brief.")

with st.sidebar:
    st.header("Filters")
    divisions = st.multiselect("Division", sorted(df["Division"].dropna().unique()), default=sorted(df["Division"].dropna().unique()))
    regions = st.multiselect("Region", sorted(df["Region"].dropna().unique()), default=sorted(df["Region"].dropna().unique()))
    products = st.multiselect("Product", sorted(df["Product Name"].dropna().unique()))
    margin_threshold = st.slider("Margin threshold (%)", 0, 100, 60)
    min_date = df["Order Date"].min()
    max_date = df["Order Date"].max()
    date_range = st.date_input("Order date range", (min_date.date(), max_date.date()))

f = df[df["Division"].isin(divisions) & df["Region"].isin(regions)].copy()
if products:
    f = f[f["Product Name"].isin(products)]
if isinstance(date_range, tuple) and len(date_range)==2:
    f = f[(f["Order Date"].dt.date >= date_range[0]) & (f["Order Date"].dt.date <= date_range[1])]

sales = f["Sales"].sum()
profit = f["Gross Profit"].sum()
cost = f["Cost"].sum()
units = f["Units"].sum()
margin = profit/sales*100 if sales else 0

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Revenue", f"${sales:,.0f}")
c2.metric("Gross Profit", f"${profit:,.0f}")
c3.metric("Cost", f"${cost:,.0f}")
c4.metric("Gross Margin", f"{margin:.1f}%")
c5.metric("Units", f"{units:,.0f}")

tabs = st.tabs(["Overview","Product Profitability","Division Performance","Cost Diagnostics","Pareto & Geography"])

with tabs[0]:
    st.subheader("Revenue, Cost & Profit")
    monthly = f.groupby("Month", as_index=False)[["Sales","Cost","Gross Profit"]].sum()
    if len(monthly):
        st.plotly_chart(px.line(monthly, x="Month", y=["Sales","Cost","Gross Profit"], markers=True), use_container_width=True)
    st.subheader("Product revenue vs profit")
    p = f.groupby(["Product Name","Division"], as_index=False)[["Sales","Gross Profit"]].sum()
    if len(p):
        st.plotly_chart(px.scatter(p, x="Sales", y="Gross Profit", color="Division", size="Sales",
                                   hover_name="Product Name", title="Revenue vs Gross Profit"), use_container_width=True)

with tabs[1]:
    st.subheader("Product-level profitability")
    p = f.groupby(["Product Name","Division"], as_index=False).agg(
        Sales=("Sales","sum"), Cost=("Cost","sum"), Gross_Profit=("Gross Profit","sum"), Units=("Units","sum"))
    p["Gross Margin %"] = p["Gross_Profit"]/p["Sales"]*100
    p["Profit per Unit"] = p["Gross_Profit"]/p["Units"]
    p["Revenue Contribution %"] = p["Sales"]/p["Sales"].sum()*100
    p["Profit Contribution %"] = p["Gross_Profit"]/p["Gross_Profit"].sum()*100
    p["Margin Health"] = np.select(
        [p["Gross Margin %"]>=45, p["Gross Margin %"]>=30],
        ["Healthy","Acceptable"], default="At Risk")
    st.dataframe(p.sort_values("Gross_Profit", ascending=False).style.format({
        "Sales":"${:,.2f}","Cost":"${:,.2f}","Gross_Profit":"${:,.2f}",
        "Gross Margin %":"{:.1f}%","Profit per Unit":"${:.2f}",
        "Revenue Contribution %":"{:.1f}%","Profit Contribution %":"{:.1f}%"
    }), use_container_width=True, hide_index=True)
    st.plotly_chart(px.bar(p.sort_values("Gross Margin %"), x="Gross Margin %", y="Product Name",
                           color="Division", orientation="h", title="Gross Margin by Product"),
                    use_container_width=True)

with tabs[2]:
    st.subheader("Division performance")
    d = f.groupby("Division", as_index=False).agg(Sales=("Sales","sum"), Cost=("Cost","sum"), Gross_Profit=("Gross Profit","sum"))
    d["Gross Margin %"] = d["Gross_Profit"]/d["Sales"]*100
    d["Cost Ratio %"] = d["Cost"]/d["Sales"]*100
    st.dataframe(d.style.format({"Sales":"${:,.2f}","Cost":"${:,.2f}","Gross_Profit":"${:,.2f}",
                                 "Gross Margin %":"{:.1f}%","Cost Ratio %":"{:.1f}%"}), use_container_width=True, hide_index=True)
    st.plotly_chart(px.bar(d, x="Division", y=["Sales","Gross_Profit","Cost"], barmode="group"),
                    use_container_width=True)
    st.plotly_chart(px.box(f, x="Division", y="Gross Margin %", points=False, title="Margin distribution by division"),
                    use_container_width=True)

with tabs[3]:
    st.subheader("Cost structure diagnostics")
    p = f.groupby(["Product Name","Division"], as_index=False).agg(Sales=("Sales","sum"), Cost=("Cost","sum"), Gross_Profit=("Gross Profit","sum"))
    p["Gross Margin %"] = p["Gross_Profit"]/p["Sales"]*100
    p["Cost Ratio %"] = p["Cost"]/p["Sales"]*100
    avg_margin = profit/sales*100 if sales else 0
    avg_cost_ratio = cost/sales*100 if sales else 0
    p["Diagnostic"] = np.select(
        [(p["Cost Ratio %"]>avg_cost_ratio)&(p["Gross Margin %"]<avg_margin),
         (p["Cost Ratio %"]>avg_cost_ratio)&(p["Gross Margin %"]>=avg_margin),
         (p["Cost Ratio %"]<=avg_cost_ratio)&(p["Gross Margin %"]<avg_margin)],
        ["Cost-Heavy / Margin-Poor","Cost-Heavy / Margin-OK","Lean-Cost / Margin-Poor"],
        default="Lean-Cost / High-Margin")
    st.plotly_chart(px.scatter(p, x="Cost Ratio %", y="Gross Margin %", color="Diagnostic",
                               text="Product Name", title="Cost Ratio vs Gross Margin",
                               hover_data=["Sales","Gross_Profit"]), use_container_width=True)
    st.info(f"Current filtered portfolio thresholds: average gross margin = {avg_margin:.1f}%, average cost ratio = {avg_cost_ratio:.1f}%.")

with tabs[4]:
    st.subheader("Pareto concentration")
    p = f.groupby("Product Name", as_index=False)["Gross Profit"].sum().sort_values("Gross Profit", ascending=False)
    p["Cumulative Profit %"] = p["Gross Profit"].cumsum()/p["Gross Profit"].sum()*100
    fig = go.Figure()
    fig.add_bar(x=p["Product Name"], y=p["Gross Profit"], name="Gross Profit")
    fig.add_scatter(x=p["Product Name"], y=p["Cumulative Profit %"], name="Cumulative Profit %", yaxis="y2", mode="lines+markers")
    fig.update_layout(yaxis2=dict(title="Cumulative %", overlaying="y", side="right", range=[0,105]),
                      title="Product Profit Pareto")
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Geographic revenue concentration")
    state = f.groupby("State/Province", as_index=False).agg(Sales=("Sales","sum"), Gross_Profit=("Gross Profit","sum"))
    state["Revenue Share %"] = state["Sales"]/state["Sales"].sum()*100
    st.dataframe(state.sort_values("Sales", ascending=False).head(15).style.format({"Sales":"${:,.2f}","Gross_Profit":"${:,.2f}","Revenue Share %":"{:.1f}%"}),
                 use_container_width=True, hide_index=True)

st.divider()
st.caption("Source dataset is publicly referenced in the project documentation; dashboard calculations are recomputed from the transaction-level CSV.")
