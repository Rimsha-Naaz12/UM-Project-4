from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="SkyCity Auckland | Channel Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 50%, #f5f3ff 100%) !important;
        color: #172033 !important;
    }
    .main .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    h1, h2, h3 {
        color: #172554 !important;
        font-weight: 800 !important;
    }
    p, li {
        color: #334155 !important;
    }
    .hero-header {
        padding: 32px 36px;
        border-radius: 22px;
        margin-bottom: 24px;
        background: linear-gradient(135deg, #0f172a 0%, #172554 40%, #4f46e5 100%);
        box-shadow: 0 16px 36px rgba(30, 41, 91, 0.20);
    }
    .hero-header h1 {
        color: #ffffff !important;
        margin: 0 0 8px 0;
        font-size: 2.35rem !important;
    }
    .hero-header p {
        color: #dbeafe !important;
        margin: 0;
        font-size: 1.08rem;
    }
    .info-box {
        padding: 20px 22px;
        border-radius: 16px;
        margin-bottom: 24px;
        background: linear-gradient(135deg, #ffffff 0%, #f5f7ff 100%) !important;
        border: 1px solid #dbe3f0 !important;
        box-shadow: 0 6px 18px rgba(31, 41, 91, 0.07);
        color: #172033 !important;
    }
    .info-box strong {
        color: #3730a3 !important;
    }
    .info-box p, .info-box li {
        color: #334155 !important;
    }
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #ffffff 0%, #f8faff 100%) !important;
        border: 1px solid #dce3f0 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        min-height: 120px;
        box-shadow: 0 7px 20px rgba(31, 41, 91, 0.08) !important;
    }
    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] * {
        color: #64748b !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {
        color: #172554 !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricDelta"],
    [data-testid="stMetricDelta"] * {
        color: #4f46e5 !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #172554 48%, #312e81 100%) !important;
        border-right: 1px solid #334155 !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] p {
        color: #cbd5e1 !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] *,
    [data-testid="stSidebar"] input {
        color: #172033 !important;
    }
    [data-testid="stSidebar"] [data-baseweb="tag"] {
        background: #dbeafe !important;
    }
    [data-testid="stSidebar"] [data-baseweb="tag"] * {
        color: #1e3a8a !important;
    }
    [data-baseweb="menu"] {
        background: #ffffff !important;
    }
    [data-baseweb="menu"] *,
    [role="option"] {
        color: #172033 !important;
    }
    [role="option"]:hover {
        background: #eef2ff !important;
    }
    [data-baseweb="select"] > div {
        background: #ffffff !important;
        border-radius: 10px !important;
    }
    [data-baseweb="select"] * {
        color: #172033 !important;
    }
    [data-baseweb="tag"] {
        background: #e0e7ff !important;
        border-radius: 6px !important;
    }
    [data-baseweb="tag"] * {
        color: #312e81 !important;
        font-weight: 600 !important;
    }
    [data-testid="stDataFrame"] {
        background: #ffffff !important;
        border: 1px solid #dce3f0 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    [data-testid="stExpander"] {
        background: #ffffff !important;
        border: 1px solid #dce3f0 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 14px rgba(31, 41, 91, 0.06);
    }
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary * {
        color: #172554 !important;
        font-weight: 700 !important;
    }
    [data-testid="stAlert"] {
        border-radius: 12px !important;
    }
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] div {
        color: #172033 !important;
    }
    .risk-high, .risk-medium, .risk-low {
        padding: 15px 18px;
        border-radius: 12px;
        margin-bottom: 16px;
    }
    .risk-high {
        background: linear-gradient(135deg, #fff1f2, #ffe4e6) !important;
        border-left: 5px solid #e11d48;
        color: #881337 !important;
    }
    .risk-medium {
        background: linear-gradient(135deg, #fffbeb, #fef3c7) !important;
        border-left: 5px solid #f59e0b;
        color: #78350f !important;
    }
    .risk-low {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7) !important;
        border-left: 5px solid #16a34a;
        color: #14532d !important;
    }
    .risk-high *, .risk-medium *, .risk-low * {
        font-weight: 600;
    }
    .stButton button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 9px !important;
        font-weight: 700 !important;
    }
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, #c7d2fe, transparent) !important;
        margin: 32px 0 !important;
    }
    .footer-box {
        text-align: center;
        padding: 22px;
        margin-top: 30px;
        border-radius: 16px;
        background: linear-gradient(135deg, #111827, #172554, #312e81);
        color: #e0e7ff !important;
        box-shadow: 0 10px 25px rgba(31, 41, 91, 0.15);
    }
    .footer-box p {
        color: #e0e7ff !important;
        margin: 5px;
    }
    @media (max-width: 900px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        .hero-header h1 {
            font-size: 1.8rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = Path(__file__).resolve().parent

DATA_PATHS = [
    BASE_DIR / "data" / "skycity_auckland_restaurants_bars.csv",
    BASE_DIR / "skycity_auckland_restaurants_bars.csv",
    BASE_DIR / "data" / "SkyCity Auckland Restaurants & Bars (1).csv",
    BASE_DIR / "SkyCity Auckland Restaurants & Bars (1).csv",
]

@st.cache_data
def load_data():
    for path in DATA_PATHS:
        if path.exists():
            data = pd.read_csv(path)
            data = data.loc[:, ~data.columns.str.contains("^Unnamed", case=False)]
            return data

    searched_paths = "\n".join(str(path) for path in DATA_PATHS)
    raise FileNotFoundError(
        "Dataset not found.\n\n"
        "The application searched these locations:\n\n"
        f"{searched_paths}\n\n"
        "Please make sure the CSV file is inside the data folder of your GitHub repository."
    )

df = load_data()

def find_column(possible_names):
    for name in possible_names:
        if name in df.columns:
            return name
    return None

restaurant_id_col = find_column(["RestaurantID", "Restaurant Id", "Restaurant_ID"])
restaurant_name_col = find_column(["RestaurantName", "Restaurant Name", "Restaurant_Name"])
cuisine_col = find_column(["CuisineType", "Cuisine Type", "Cuisine_Type"])
segment_col = find_column(["Segment"])
subregion_col = find_column(["Subregion", "SubRegion", "Sub Region"])
growth_col = find_column(["GrowthFactor", "Growth Factor", "Growth_Factor"])
aov_col = find_column(["AOV", "AverageOrderValue", "Average Order Value"])
monthly_orders_col = find_column(["MonthlyOrders", "Monthly Orders", "Monthly_Orders"])

CHANNELS = {
    "In-Store": {
        "orders": ["InStoreOrders", "In-Store Orders", "InStore Order Count"],
        "revenue": ["InStoreRevenue", "In-Store Revenue"],
        "profit": ["InStoreNetProfit", "In-Store Net Profit"],
    },
    "Uber Eats": {
        "orders": ["UberEatsOrders", "Uber Eats Orders", "UberEats Order Count"],
        "revenue": ["UberEatsRevenue", "Uber Eats Revenue"],
        "profit": ["UberEatsNetProfit", "Uber Eats Net Profit"],
    },
    "DoorDash": {
        "orders": ["DoorDashOrders", "DoorDash Orders", "DoorDash Order Count"],
        "revenue": ["DoorDashRevenue", "DoorDash Revenue"],
        "profit": ["DoorDashNetProfit", "DoorDash Net Profit"],
    },
    "Self-Delivery": {
        "orders": ["SelfDeliveryOrders", "Self Delivery Orders", "SelfDelivery Order Count"],
        "revenue": ["SelfDeliveryRevenue", "Self Delivery Revenue"],
        "profit": ["SelfDeliveryNetProfit", "Self Delivery Net Profit"],
    },
}

def resolve_channel_column(possible_names):
    for name in possible_names:
        if name in df.columns:
            return name
    return None

for channel in CHANNELS:
    CHANNELS[channel]["orders"] = resolve_channel_column(CHANNELS[channel]["orders"])
    CHANNELS[channel]["revenue"] = resolve_channel_column(CHANNELS[channel]["revenue"])
    CHANNELS[channel]["profit"] = resolve_channel_column(CHANNELS[channel]["profit"])

numeric_columns = [growth_col, aov_col, monthly_orders_col]

for channel in CHANNELS:
    numeric_columns.extend([
        CHANNELS[channel]["orders"],
        CHANNELS[channel]["revenue"],
        CHANNELS[channel]["profit"],
    ])

for column in numeric_columns:
    if column and column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

ORDER_COLUMNS = {
    channel: CHANNELS[channel]["orders"]
    for channel in CHANNELS
    if CHANNELS[channel]["orders"]
}

CHANNEL_COLORS = {
    "In-Store": "#4f46e5",
    "Uber Eats": "#06b6d4",
    "DoorDash": "#8b5cf6",
    "Self-Delivery": "#10b981",
}

def chart_layout(fig, x_title=None, y_title=None):
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="#ffffff",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#172033", family="Arial"),
        title_font=dict(color="#172554", size=20),
        legend_title_text="",
        margin=dict(l=40, r=30, t=65, b=45),
        hoverlabel=dict(font_color="#172033"),
    )
    if x_title is not None:
        fig.update_xaxes(title_text=x_title, title_font_color="#334155")
    if y_title is not None:
        fig.update_yaxes(title_text=y_title, title_font_color="#334155")
    return fig

st.sidebar.markdown(
    """
    <div style="
        padding:18px;
        border-radius:14px;
        background:rgba(255,255,255,0.10);
        margin-bottom:20px;
    ">
        <div style="font-size:1.35rem;font-weight:800;color:#ffffff;">
            🎛️ Dashboard Filters
        </div>
        <div style="margin-top:7px;font-size:0.88rem;color:#cbd5e1;">
            Explore channel performance across SkyCity Auckland.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if subregion_col:
    subregions = sorted(df[subregion_col].dropna().astype(str).unique())
    selected_subregions = st.sidebar.multiselect(
        "📍 Subregion",
        subregions,
        default=subregions,
    )
else:
    selected_subregions = []

if cuisine_col:
    cuisines = sorted(df[cuisine_col].dropna().astype(str).unique())
    selected_cuisines = st.sidebar.multiselect(
        "🍽️ Cuisine",
        cuisines,
        default=cuisines,
    )
else:
    selected_cuisines = []

if segment_col:
    segments = sorted(df[segment_col].dropna().astype(str).unique())
    selected_segments = st.sidebar.multiselect(
        "🏪 Segment",
        segments,
        default=segments,
    )
else:
    selected_segments = []

selected_channels = st.sidebar.multiselect(
    "📦 Channels",
    list(CHANNELS.keys()),
    default=list(CHANNELS.keys()),
)

filtered_df = df.copy()

if subregion_col and selected_subregions:
    filtered_df = filtered_df[
        filtered_df[subregion_col].astype(str).isin(selected_subregions)
    ]

if cuisine_col and selected_cuisines:
    filtered_df = filtered_df[
        filtered_df[cuisine_col].astype(str).isin(selected_cuisines)
    ]

if segment_col and selected_segments:
    filtered_df = filtered_df[
        filtered_df[segment_col].astype(str).isin(selected_segments)
    ]

filtered_channel_orders = {}
filtered_channel_revenue = {}
filtered_channel_profit = {}

for channel in CHANNELS:
    if channel not in selected_channels:
        filtered_channel_orders[channel] = 0
        filtered_channel_revenue[channel] = 0
        filtered_channel_profit[channel] = 0
        continue

    order_col = CHANNELS[channel]["orders"]
    revenue_col = CHANNELS[channel]["revenue"]
    profit_col = CHANNELS[channel]["profit"]

    filtered_channel_orders[channel] = (
        filtered_df[order_col].sum() if order_col else 0
    )
    filtered_channel_revenue[channel] = (
        filtered_df[revenue_col].sum() if revenue_col else 0
    )
    filtered_channel_profit[channel] = (
        filtered_df[profit_col].sum() if profit_col else 0
    )

filtered_total_orders = sum(filtered_channel_orders.values())
filtered_total_revenue = sum(filtered_channel_revenue.values())
filtered_total_profit = sum(filtered_channel_profit.values())

aggregator_orders = (
    filtered_channel_orders.get("Uber Eats", 0)
    + filtered_channel_orders.get("DoorDash", 0)
)
aggregator_dependence = (
    aggregator_orders / filtered_total_orders * 100
    if filtered_total_orders > 0 else 0
)

delivery_orders = (
    filtered_channel_orders.get("Uber Eats", 0)
    + filtered_channel_orders.get("DoorDash", 0)
    + filtered_channel_orders.get("Self-Delivery", 0)
)
delivery_share = (
    delivery_orders / filtered_total_orders * 100
    if filtered_total_orders > 0 else 0
)

in_store_orders = filtered_channel_orders.get("In-Store", 0)
in_store_share = (
    in_store_orders / filtered_total_orders * 100
    if filtered_total_orders > 0 else 0
)

calculated_aov = (
    filtered_total_revenue / filtered_total_orders
    if filtered_total_orders > 0 else 0
)

average_growth = (
    float(filtered_df[growth_col].mean())
    if growth_col and not filtered_df.empty else 0.0
)
if np.isnan(average_growth):
    average_growth = 0.0

projected_orders = filtered_total_orders * (1 + average_growth / 100)

st.markdown(
    """
    <div class="hero-header">
        <h1>📊 SkyCity Auckland Restaurants & Bars</h1>
        <p>Order Channel Performance & Market Share Analytics</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="info-box">
        <strong>✨ Dashboard Overview</strong>
        <p>
            This interactive analytics dashboard explores order volume,
            channel market share, revenue, profitability, geographic preferences,
            cuisine patterns and aggregator dependency across SkyCity Auckland's
            restaurant and bar market.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.header("📌 Key Performance Indicators")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("📦 Monthly Orders", f"{filtered_total_orders:,.0f}")
with kpi2:
    st.metric("💰 Revenue", f"${filtered_total_revenue:,.0f}")
with kpi3:
    st.metric("💎 Net Profit", f"${filtered_total_profit:,.0f}")
with kpi4:
    st.metric("⚠️ Aggregator Dependence", f"{aggregator_dependence:.1f}%")

st.subheader("📈 Additional Indicators")
kpi5, kpi6, kpi7, kpi8 = st.columns(4)

with kpi5:
    st.metric("🚚 Delivery Order Share", f"{delivery_share:.1f}%")
with kpi6:
    st.metric("🏪 In-Store Reliance", f"{in_store_share:.1f}%")
with kpi7:
    st.metric("💵 Calculated AOV", f"${calculated_aov:,.2f}")
with kpi8:
    st.metric(
        "📈 Next-Month Order Scenario",
        f"{projected_orders:,.0f}",
        f"{average_growth:.1f}% growth",
    )

st.markdown("---")
st.header("1. 📦 Channel Overview")

channel_data = pd.DataFrame({
    "Channel": selected_channels,
    "Orders": [filtered_channel_orders[channel] for channel in selected_channels],
    "Revenue": [filtered_channel_revenue[channel] for channel in selected_channels],
    "Net Profit": [filtered_channel_profit[channel] for channel in selected_channels],
})

if not channel_data.empty:
    color_sequence = [
        CHANNEL_COLORS.get(channel, "#6366f1")
        for channel in selected_channels
    ]

    col1, col2 = st.columns(2)

    with col1:
        fig_orders = px.bar(
            channel_data,
            x="Channel",
            y="Orders",
            title="Monthly Orders by Channel",
            text_auto=".2s",
            color="Channel",
            color_discrete_sequence=color_sequence,
        )
        chart_layout(fig_orders, "Order Channel", "Orders")
        st.plotly_chart(fig_orders, use_container_width=True)

    with col2:
        fig_share = px.pie(
            channel_data,
            names="Channel",
            values="Orders",
            title="Channel Order Share",
            hole=0.45,
            color="Channel",
            color_discrete_sequence=color_sequence,
        )
        chart_layout(fig_share)
        st.plotly_chart(fig_share, use_container_width=True)

    st.subheader("💰 Revenue and Net Profit by Channel")
    col3, col4 = st.columns(2)

    with col3:
        fig_revenue = px.bar(
            channel_data,
            x="Channel",
            y="Revenue",
            title="Revenue by Channel",
            text_auto=".2s",
            color="Channel",
            color_discrete_sequence=color_sequence,
        )
        chart_layout(fig_revenue, "Order Channel", "Revenue")
        st.plotly_chart(fig_revenue, use_container_width=True)

    with col4:
        fig_profit = px.bar(
            channel_data,
            x="Channel",
            y="Net Profit",
            title="Net Profit by Channel",
            text_auto=".2s",
            color="Channel",
            color_discrete_sequence=color_sequence,
        )
        chart_layout(fig_profit, "Order Channel", "Net Profit")
        st.plotly_chart(fig_profit, use_container_width=True)

    channel_data["Profit Margin %"] = np.where(
        channel_data["Revenue"] > 0,
        channel_data["Net Profit"] / channel_data["Revenue"] * 100,
        0,
    )

    fig_margin = px.bar(
        channel_data,
        x="Channel",
        y="Profit Margin %",
        title="Net Profit Margin by Channel",
        text_auto=".1f",
        color="Channel",
        color_discrete_sequence=color_sequence,
    )
    chart_layout(fig_margin, "Order Channel", "Profit Margin (%)")
    st.plotly_chart(fig_margin, use_container_width=True)
else:
    st.info("Select at least one channel from the sidebar to display channel charts.")

st.markdown("---")
st.header("2. 🗺️ Geographic / Subregion Analysis")

if subregion_col:
    available_channels = [
        channel for channel in selected_channels
        if CHANNELS[channel]["orders"]
    ]

    if available_channels and not filtered_df.empty:
        aggregation_dict = {
            channel: (CHANNELS[channel]["orders"], "sum")
            for channel in available_channels
        }

        subregion_channel = (
            filtered_df.groupby(subregion_col)
            .agg(**aggregation_dict)
            .reset_index()
        )

        if not subregion_channel.empty:
            st.subheader("Channel Order Volume by Subregion")

            melted_subregion = subregion_channel.melt(
                id_vars=[subregion_col],
                value_vars=available_channels,
                var_name="Channel",
                value_name="Orders",
            )

            fig_subregion = px.bar(
                melted_subregion,
                x=subregion_col,
                y="Orders",
                color="Channel",
                barmode="group",
                title="Orders by Subregion and Channel",
                color_discrete_map=CHANNEL_COLORS,
            )
            chart_layout(fig_subregion, "Subregion", "Orders")
            st.plotly_chart(fig_subregion, use_container_width=True)

            st.subheader("Subregion Channel Heatmap")
            heatmap_data = subregion_channel.set_index(subregion_col)[available_channels]

            fig_heatmap = px.imshow(
                heatmap_data,
                text_auto=".2s",
                aspect="auto",
                title="Subregion Channel Heatmap",
                color_continuous_scale=["#eef2ff", "#6366f1", "#312e81"],
            )
            chart_layout(fig_heatmap)
            st.plotly_chart(fig_heatmap, use_container_width=True)

            st.subheader("Dominant Channel by Subregion")
            dominance = heatmap_data.idxmax(axis=1)
            dominance_table = pd.DataFrame({
                "Subregion": dominance.index,
                "Dominant Channel": dominance.values,
                "Orders": heatmap_data.max(axis=1).values,
            })
            st.dataframe(
                dominance_table,
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.info("No subregion data is available for the current filters.")
else:
    st.warning("Subregion column was not found in the dataset.")

st.markdown("---")
st.header("3. 🍽️ Cuisine vs Channel Analysis")

if cuisine_col:
    available_channels = [
        channel for channel in selected_channels
        if CHANNELS[channel]["orders"]
    ]

    if available_channels and not filtered_df.empty:
        aggregation_dict = {
            channel: (CHANNELS[channel]["orders"], "sum")
            for channel in available_channels
        }

        cuisine_channel = (
            filtered_df.groupby(cuisine_col)
            .agg(**aggregation_dict)
            .reset_index()
        )

        if not cuisine_channel.empty:
            cuisine_melt = cuisine_channel.melt(
                id_vars=[cuisine_col],
                var_name="Channel",
                value_name="Orders",
            )

            fig_cuisine = px.bar(
                cuisine_melt,
                x=cuisine_col,
                y="Orders",
                color="Channel",
                barmode="stack",
                title="Cuisine Channel Mix",
                color_discrete_map=CHANNEL_COLORS,
            )
            chart_layout(fig_cuisine, "Cuisine", "Orders")
            st.plotly_chart(fig_cuisine, use_container_width=True)

            cuisine_pivot = cuisine_channel.set_index(cuisine_col)
            cuisine_dominance = cuisine_pivot.idxmax(axis=1)

            cuisine_table = pd.DataFrame({
                "Cuisine": cuisine_dominance.index,
                "Dominant Channel": cuisine_dominance.values,
                "Orders": cuisine_pivot.max(axis=1).values,
            })

            st.subheader("Dominant Channel by Cuisine")
            st.dataframe(
                cuisine_table,
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.info("No cuisine data is available for the current filters.")
else:
    st.warning("Cuisine column was not found in the dataset.")

st.markdown("---")
st.header("4. 🏪 Restaurant Segment Analysis")

if segment_col:
    available_channels = [
        channel for channel in selected_channels
        if CHANNELS[channel]["orders"]
    ]

    if available_channels and not filtered_df.empty:
        aggregation_dict = {
            channel: (CHANNELS[channel]["orders"], "sum")
            for channel in available_channels
        }

        segment_channel = (
            filtered_df.groupby(segment_col)
            .agg(**aggregation_dict)
            .reset_index()
        )

        if not segment_channel.empty:
            segment_melt = segment_channel.melt(
                id_vars=[segment_col],
                var_name="Channel",
                value_name="Orders",
            )

            fig_segment = px.bar(
                segment_melt,
                x=segment_col,
                y="Orders",
                color="Channel",
                barmode="group",
                title="Order Channels by Restaurant Segment",
                color_discrete_map=CHANNEL_COLORS,
            )
            chart_layout(fig_segment, "Restaurant Segment", "Orders")
            st.plotly_chart(fig_segment, use_container_width=True)
    else:
        st.info("No segment data is available for the current filters.")
else:
    st.warning("Segment column was not found in the dataset.")

st.markdown("---")
st.header("5. ⚠️ Aggregator Dependency Risk")

st.markdown(
    """
    <div class="risk-high">
        <strong>Risk Threshold</strong><br>
        A restaurant is classified as <strong>High Risk</strong> when
        Uber Eats + DoorDash account for <strong>70% or more</strong>
        of total monthly orders.
    </div>
    """,
    unsafe_allow_html=True,
)

dependency_df = filtered_df.copy()
uber_col = CHANNELS["Uber Eats"]["orders"]
doordash_col = CHANNELS["DoorDash"]["orders"]

if uber_col and doordash_col and monthly_orders_col:
    dependency_df["AggregatorOrders"] = (
        dependency_df[uber_col] + dependency_df[doordash_col]
    )

    dependency_df["AggregatorDependence"] = np.where(
        dependency_df[monthly_orders_col] > 0,
        dependency_df["AggregatorOrders"]
        / dependency_df[monthly_orders_col]
        * 100,
        0,
    )

    dependency_df["Risk"] = np.select(
        [
            dependency_df["AggregatorDependence"] >= 70,
            dependency_df["AggregatorDependence"] >= 50,
        ],
        ["High", "Medium"],
        default="Low",
    )

    high_risk_count = int((dependency_df["Risk"] == "High").sum())
    medium_risk_count = int((dependency_df["Risk"] == "Medium").sum())
    low_risk_count = int((dependency_df["Risk"] == "Low").sum())

    r1, r2, r3 = st.columns(3)
    with r1:
        st.metric("🔴 High Risk", f"{high_risk_count:,}")
    with r2:
        st.metric("🟠 Medium Risk", f"{medium_risk_count:,}")
    with r3:
        st.metric("🟢 Low Risk", f"{low_risk_count:,}")

    risk_counts = pd.DataFrame({
        "Risk": ["High", "Medium", "Low"],
        "Restaurants": [high_risk_count, medium_risk_count, low_risk_count],
    })

    fig_risk = px.bar(
        risk_counts,
        x="Risk",
        y="Restaurants",
        title="Restaurant Dependency Risk Distribution",
        text_auto=True,
        color="Risk",
        color_discrete_map={
            "High": "#e11d48",
            "Medium": "#f59e0b",
            "Low": "#16a34a",
        },
    )
    chart_layout(fig_risk, "Risk Level", "Restaurants")
    st.plotly_chart(fig_risk, use_container_width=True)

    st.subheader("Restaurants with Highest Aggregator Dependence")

    display_columns = []

    for column in [
        restaurant_id_col,
        restaurant_name_col,
        cuisine_col,
        segment_col,
        subregion_col,
        monthly_orders_col,
        "AggregatorOrders",
        "AggregatorDependence",
        "Risk",
    ]:
        if column and column in dependency_df.columns and column not in display_columns:
            display_columns.append(column)

    if display_columns:
        risk_table = (
            dependency_df[display_columns]
            .sort_values("AggregatorDependence", ascending=False)
        )
        st.dataframe(
            risk_table.head(100),
            use_container_width=True,
            hide_index=True,
        )
else:
    st.warning(
        "Required columns for aggregator dependency analysis were not found."
    )

st.markdown("---")
st.header("6. 🔀 Channel Diversification")

st.markdown(
    """
    <div class="info-box">
        The Channel Diversification Score uses normalized Shannon entropy
        across the available order channels.
        <br><br>
        <strong>0 = Highly Concentrated</strong>
        &nbsp;&nbsp;&nbsp;&nbsp;
        <strong>100 = Highly Diversified</strong>
    </div>
    """,
    unsafe_allow_html=True,
)

diversification_df = filtered_df.copy()

if len(ORDER_COLUMNS) >= 2 and not diversification_df.empty:
    channel_values = np.column_stack(
        [diversification_df[column].values for column in ORDER_COLUMNS.values()]
    )

    totals = channel_values.sum(axis=1)

    proportions = np.divide(
        channel_values,
        totals[:, None],
        out=np.zeros_like(channel_values, dtype=float),
        where=totals[:, None] != 0,
    )

    entropy = -np.sum(
        np.where(
            proportions > 0,
            proportions * np.log(proportions),
            0,
        ),
        axis=1,
    )

    max_entropy = np.log(len(ORDER_COLUMNS))

    diversification_df["DiversificationScore"] = np.where(
        max_entropy > 0,
        entropy / max_entropy * 100,
        0,
    )

    average_diversification = float(
        diversification_df["DiversificationScore"].mean()
    )

    st.metric(
        "🔀 Average Channel Diversification Score",
        f"{average_diversification:.1f}/100",
    )

    fig_diversification = px.histogram(
        diversification_df,
        x="DiversificationScore",
        nbins=20,
        title="Distribution of Channel Diversification Scores",
        color_discrete_sequence=["#6366f1"],
    )
    chart_layout(fig_diversification, "Diversification Score", "Restaurants")
    st.plotly_chart(fig_diversification, use_container_width=True)
else:
    st.warning(
        "Not enough channel order columns or filtered records are available "
        "for diversification analysis."
    )

st.markdown("---")
st.header("7. 📈 Growth Scenario")

if growth_col:
    growth_summary = pd.DataFrame({
        "Metric": [
            "Average Growth Factor",
            "Current Monthly Orders",
            "Projected Monthly Orders",
        ],
        "Value": [
            f"{average_growth:.2f}%",
            f"{filtered_total_orders:,.0f}",
            f"{projected_orders:,.0f}",
        ],
    })

    st.dataframe(
        growth_summary,
        use_container_width=True,
        hide_index=True,
    )

    st.info(
        "The dataset does not contain a time dimension. Therefore, this is "
        "a one-month growth scenario using the supplied GrowthFactor, not a "
        "true historical time-series forecast."
    )
else:
    st.info("GrowthFactor was not found in the dataset.")

st.markdown("---")
st.header("8. ✅ Data Quality Validation")

validation_results = []

missing_values = int(df.isna().sum().sum())
validation_results.append({
    "Validation": "Missing Values",
    "Result": missing_values,
    "Status": "PASS" if missing_values == 0 else "CHECK",
})

duplicate_rows = int(df.duplicated().sum())
validation_results.append({
    "Validation": "Duplicate Rows",
    "Result": duplicate_rows,
    "Status": "PASS" if duplicate_rows == 0 else "CHECK",
})

if monthly_orders_col:
    available_order_columns = [
        column for column in ORDER_COLUMNS.values()
        if column in df.columns
    ]

    if available_order_columns:
        calculated_orders = df[available_order_columns].sum(axis=1)
        mismatches = int(
            (calculated_orders != df[monthly_orders_col]).sum()
        )

        validation_results.append({
            "Validation": "Channel Orders = Monthly Orders",
            "Result": mismatches,
            "Status": "PASS" if mismatches == 0 else "CHECK",
        })

validation_table = pd.DataFrame(validation_results)

st.dataframe(
    validation_table,
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")
st.header("9. 💡 Executive Insights & Recommendations")

selected_order_values = {
    channel: filtered_channel_orders.get(channel, 0)
    for channel in selected_channels
}

if selected_order_values:
    dominant_channel = max(
        selected_order_values,
        key=selected_order_values.get,
    )
    dominant_orders = selected_order_values[dominant_channel]
else:
    dominant_channel = "N/A"
    dominant_orders = 0

st.subheader("🔎 Key Findings")

st.markdown(
    f"""
    <div class="info-box">
        <ul>
            <li>
                <strong>Dominant channel:</strong> {dominant_channel},
                with approximately <strong>{dominant_orders:,.0f} orders</strong>.
            </li>
            <li>
                <strong>Delivery contribution:</strong> delivery channels account
                for approximately <strong>{delivery_share:.1f}%</strong> of orders.
            </li>
            <li>
                <strong>Aggregator dependence:</strong> Uber Eats and DoorDash
                together account for approximately
                <strong>{aggregator_dependence:.1f}%</strong> of orders.
            </li>
            <li>
                <strong>In-store reliance:</strong> In-Store contributes
                approximately <strong>{in_store_share:.1f}%</strong> of orders.
            </li>
            <li>
                <strong>Projected orders:</strong> using the supplied GrowthFactor,
                the next-month scenario is approximately
                <strong>{projected_orders:,.0f} orders</strong>.
            </li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("🎯 Strategic Recommendations")

recommendations = [
    "Diversify order channels to reduce dependence on a small number of aggregators.",
    "Monitor restaurants where Uber Eats and DoorDash together exceed the 70% dependency threshold.",
    "Strengthen direct and self-delivery capabilities where delivery economics support it.",
    "Use subregion-level channel preferences to tailor marketing and operational strategies.",
    "Use cuisine-level channel patterns when allocating promotional budgets.",
    "Protect profitable in-store demand while using digital channels to expand customer reach.",
    "Track profitability alongside order volume because the largest channel may not be the most profitable.",
]

for index, recommendation in enumerate(recommendations, start=1):
    st.markdown(
        f"""
        <div style="
            background:#ffffff;
            border:1px solid #e0e7ff;
            border-left:4px solid #6366f1;
            padding:13px 17px;
            margin:8px 0;
            border-radius:9px;
            box-shadow:0 3px 10px rgba(31,41,91,0.05);
        ">
            <strong style="color:#4f46e5;">{index}.</strong>
            <span style="color:#172033;">{recommendation}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.header("10. 📋 Dataset Information")

info1, info2, info3 = st.columns(3)

with info1:
    st.metric("🏪 Restaurant Records", f"{len(df):,}")
with info2:
    st.metric("📊 Dataset Columns", f"{len(df.columns):,}")
with info3:
    st.metric("🔎 Filtered Records", f"{len(filtered_df):,}")

with st.expander("🔍 View Dataset Columns"):
    st.write(list(df.columns))

with st.expander("📄 View Filtered Data"):
    st.dataframe(
        filtered_df.head(500),
        use_container_width=True,
        hide_index=True,
    )

st.markdown(
    """
    <div class="footer-box">
        <p><strong>📊 SkyCity Auckland Restaurants & Bars</strong></p>
        <p>Order Channel Performance and Market Share Analytics</p>
        <p style="font-size:0.85rem;">
            Unified Mentor Project | Interactive Streamlit Analytics Dashboard
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
