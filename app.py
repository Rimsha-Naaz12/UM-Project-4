import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="SkyCity Auckland Channel Analytics", page_icon="🍽️", layout="wide")

DATA_PATH = Path(__file__).parent / "data" / "skycity_auckland_restaurants_bars.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    order_cols = ["InStoreOrders","UberEatsOrders","DoorDashOrders","SelfDeliveryOrders"]
    df["DeliveryOrders"] = df[["UberEatsOrders","DoorDashOrders","SelfDeliveryOrders"]].sum(axis=1)
    df["AggregatorOrders"] = df[["UberEatsOrders","DoorDashOrders"]].sum(axis=1)
    df["AggregatorDependence"] = df["AggregatorOrders"] / df["MonthlyOrders"]
    shares = df[order_cols].div(df["MonthlyOrders"], axis=0)
    df["ChannelDiversificationScore"] = (-(shares.replace(0,np.nan)*np.log(shares.replace(0,np.nan))).sum(axis=1)/np.log(4)*100)
    df["NextMonthProjectedOrders"] = df["MonthlyOrders"] * df["GrowthFactor"]
    return df

df = load_data()
order_cols = ["InStoreOrders","UberEatsOrders","DoorDashOrders","SelfDeliveryOrders"]
channel_labels = {"InStoreOrders":"In-Store","UberEatsOrders":"Uber Eats","DoorDashOrders":"DoorDash","SelfDeliveryOrders":"Self-Delivery"}

st.title("🍽️ Order Channel Performance & Market Share Analytics")
st.caption("SkyCity Auckland Restaurants & Bars • Unified Mentor project")

with st.sidebar:
    st.header("Filters")
    subregions = st.multiselect("Subregion", sorted(df["Subregion"].unique()), default=sorted(df["Subregion"].unique()))
    cuisines = st.multiselect("Cuisine", sorted(df["CuisineType"].unique()), default=sorted(df["CuisineType"].unique()))
    segments = st.multiselect("Segment", sorted(df["Segment"].unique()), default=sorted(df["Segment"].unique()))
    selected_channels = st.multiselect("Channels", list(channel_labels.values()), default=list(channel_labels.values()))
    st.divider()
    st.info("Risk threshold: 70% combined dependence on Uber Eats + DoorDash. A single-aggregator 70% threshold is also checked in the methodology.")

f = df[df["Subregion"].isin(subregions) & df["CuisineType"].isin(cuisines) & df["Segment"].isin(segments)].copy()

# KPI cards
total_orders = int(f["MonthlyOrders"].sum())
total_rev = sum(f[c].sum() for c in ["InStoreRevenue","UberEatsRevenue","DoorDashRevenue","SelfDeliveryRevenue"])
total_profit = sum(f[c].sum() for c in ["InStoreNetProfit","UberEatsNetProfit","DoorDashNetProfit","SelfDeliveryNetProfit"])
agg_dep = (f["UberEatsOrders"].sum()+f["DoorDashOrders"].sum()) / total_orders if total_orders else 0
proj_orders = f["NextMonthProjectedOrders"].sum()

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Monthly orders", f"{total_orders:,.0f}")
c2.metric("Revenue", f"${total_rev:,.0f}")
c3.metric("Net profit", f"${total_profit:,.0f}")
c4.metric("Aggregator dependence", f"{agg_dep:.1%}")
c5.metric("Next-month projection", f"{proj_orders:,.0f}")

st.subheader("1. Channel Mix Overview")
channel_df = pd.DataFrame({
    "Channel":[channel_labels[c] for c in order_cols if channel_labels[c] in selected_channels],
    "Orders":[f[c].sum() for c in order_cols if channel_labels[c] in selected_channels]
})
fig = px.bar(channel_df, x="Channel", y="Orders", text_auto=".3s", title="Order volume by channel")
st.plotly_chart(fig, use_container_width=True)

col1,col2 = st.columns(2)
with col1:
    fig2 = px.pie(channel_df, names="Channel", values="Orders", hole=.45, title="Channel order share")
    st.plotly_chart(fig2, use_container_width=True)
with col2:
    st.markdown("**Interpretation**")
    st.write("Uber Eats is the largest order channel in the supplied dataset. Delivery channels collectively dominate the order mix, while in-store remains strategically important for higher-margin direct sales.")
    st.write("The projection shown here is a one-month scenario using each restaurant's GrowthFactor. Because the dataset has no time-series dates, this is not a trained time-series forecast.")

st.subheader("2. Subregion Channel Heatmap")
g = f.groupby("Subregion")[order_cols].sum()
g_share = g.div(g.sum(axis=1), axis=0)
g_share.columns = [channel_labels[c] for c in order_cols]
heat = px.imshow(g_share, text_auto=".1%", aspect="auto", title="Channel share by subregion")
st.plotly_chart(heat, use_container_width=True)

st.subheader("3. Cuisine vs Channel")
cg = f.groupby("CuisineType")[order_cols].sum()
cg_share = cg.div(cg.sum(axis=1), axis=0)
cg_share.columns = [channel_labels[c] for c in order_cols]
long = cg_share.reset_index().melt(id_vars="CuisineType", var_name="Channel", value_name="Share")
fig3 = px.bar(long, x="CuisineType", y="Share", color="Channel", barmode="stack", text_auto=".0%")
fig3.update_yaxes(tickformat=".0%")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("4. Segment Channel Patterns")
sg = f.groupby("Segment")[order_cols].sum()
sg_share = sg.div(sg.sum(axis=1), axis=0)
sg_share.columns = [channel_labels[c] for c in order_cols]
long2 = sg_share.reset_index().melt(id_vars="Segment", var_name="Channel", value_name="Share")
fig4 = px.bar(long2, x="Segment", y="Share", color="Channel", barmode="group", text_auto=".0%")
fig4.update_yaxes(tickformat=".0%")
st.plotly_chart(fig4, use_container_width=True)

st.subheader("5. Dependency Risk")
risk = f.copy()
risk["RiskBand"] = pd.cut(risk["AggregatorDependence"], [-np.inf,.50,.70,np.inf], labels=["Balanced / moderate","Aggregator-heavy","High dependency"])
risk_counts = risk["RiskBand"].value_counts().reindex(["Balanced / moderate","Aggregator-heavy","High dependency"]).fillna(0)
fig5 = px.bar(x=risk_counts.index, y=risk_counts.values, labels={"x":"Risk band","y":"Restaurants"}, title="Restaurants by combined aggregator dependence")
st.plotly_chart(fig5, use_container_width=True)

risk_cols = ["RestaurantID","RestaurantName","CuisineType","Segment","Subregion","MonthlyOrders","AggregatorDependence","ChannelDiversificationScore"]
st.dataframe(risk.sort_values("AggregatorDependence", ascending=False)[risk_cols].head(25), use_container_width=True)

st.subheader("6. Profitability by Channel")
profit_df = pd.DataFrame({
    "Channel":["In-Store","Uber Eats","DoorDash","Self-Delivery"],
    "Revenue":[f[c].sum() for c in ["InStoreRevenue","UberEatsRevenue","DoorDashRevenue","SelfDeliveryRevenue"]],
    "Net Profit":[f[c].sum() for c in ["InStoreNetProfit","UberEatsNetProfit","DoorDashNetProfit","SelfDeliveryNetProfit"]]
})
profit_long = profit_df.melt(id_vars="Channel", var_name="Metric", value_name="Value")
fig6 = px.bar(profit_long, x="Channel", y="Value", color="Metric", barmode="group", text_auto=".3s", title="Revenue and net profit by channel")
st.plotly_chart(fig6, use_container_width=True)

st.subheader("7. Recommendations")
st.markdown("""
- **Reduce aggregator concentration:** prioritise direct-order incentives and first-party retention, especially for restaurants above 70% combined Uber Eats + DoorDash dependence.
- **Protect high-margin channels:** in-store and self-delivery show materially stronger net margins in the supplied data than third-party aggregators.
- **Cuisine-specific strategy:** Pizza has the strongest self-delivery mix, while Kebabs/Mediterranean and Japanese show high Uber Eats shares; channel investment should reflect these patterns.
- **Segment-specific strategy:** Ghost Kitchens are strongly delivery/aggregator oriented, while Full-service restaurants have the strongest in-store contribution.
- **Use geography tactically:** subregional differences are relatively small overall, so cuisine and segment appear more actionable than geography alone.
""")

st.caption("Data quality note: channel order counts reconcile exactly to MonthlyOrders. The supplied UE/DD/SD share fields are delivery-channel shares, so they should not be added directly to InStoreShare.")
