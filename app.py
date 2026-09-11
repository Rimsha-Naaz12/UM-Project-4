from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SkyCity Auckland | Channel Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL APP
       ======================================================== */

    .stApp {
        background: linear-gradient(
            135deg,
            #f7f9fc 0%,
            #eef3f9 50%,
            #f8f7fc 100%
        );
        color: #172033 !important;
    }

    .main {
        padding-top: 0.5rem;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* Force readable text everywhere */

    html,
    body,
    [class*="css"],
    .stApp,
    .stMarkdown,
    p,
    span,
    label,
    div {
        color: #172033;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #111827 0%,
                #172554 45%,
                #312e81 100%
            ) !important;

        border-right: 1px solid rgba(255,255,255,0.12);
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] p {
        color: #dbeafe !important;
    }

    [data-testid="stSidebar"] label {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] .stMultiSelect div,
    [data-testid="stSidebar"] .stSelectbox div {
        color: #172033 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: #ffffff !important;
        border-radius: 8px !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #172033 !important;
    }

    [data-testid="stSidebar"] .stMultiSelect span {
        color: #172033 !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.15) !important;
    }


    /* ========================================================
       MAIN HEADINGS
       ======================================================== */

    h1 {
        color: #172554 !important;
        font-weight: 800 !important;
        font-size: 2.35rem !important;
        letter-spacing: -0.5px;
    }

    h2 {
        color: #1e3a8a !important;
        font-weight: 750 !important;
        margin-top: 1.5rem !important;
    }

    h3 {
        color: #312e81 !important;
        font-weight: 700 !important;
    }


    /* ========================================================
       TITLE AREA
       ======================================================== */

    .dashboard-title {
        background:
            linear-gradient(
                135deg,
                #172554 0%,
                #1d4ed8 45%,
                #7c3aed 100%
            );

        padding: 30px 35px;
        border-radius: 18px;
        margin-bottom: 22px;

        box-shadow:
            0 10px 30px rgba(30, 64, 175, 0.18);
    }

    .dashboard-title h1 {
        color: #ffffff !important;
        margin: 0;
        font-size: 2.4rem !important;
    }

    .dashboard-title p {
        color: #dbeafe !important;
        margin-top: 8px;
        font-size: 1.05rem;
    }


    /* ========================================================
       INFO BOX
       ======================================================== */

    .info-box {
        padding: 20px 22px;
        border-radius: 14px;

        background:
            linear-gradient(
                135deg,
                #eff6ff,
                #eef2ff
            ) !important;

        border: 1px solid #bfdbfe !important;

        box-shadow:
            0 5px 18px rgba(30,64,175,0.08);

        margin-bottom: 25px;

        color: #172033 !important;
    }

    .info-box strong {
        color: #1d4ed8 !important;
        font-size: 1.05rem;
    }

    .info-box p,
    .info-box span,
    .info-box div {
        color: #263449 !important;
    }


    /* ========================================================
       KPI CARDS
       ======================================================== */

    [data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                #ffffff 0%,
                #f8fafc 100%
            ) !important;

        border: 1px solid #dbe3ef !important;

        padding: 20px !important;

        border-radius: 15px !important;

        min-height: 125px;

        box-shadow:
            0 7px 22px rgba(15,23,42,0.08) !important;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);

        box-shadow:
            0 12px 28px rgba(30,64,175,0.13) !important;
    }

    [data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricLabel"] * {
        color: #475569 !important;
    }

    [data-testid="stMetricValue"] {
        color: #172554 !important;
        font-weight: 800 !important;
    }

    [data-testid="stMetricValue"] * {
        color: #172554 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #2563eb !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricDelta"] * {
        color: #2563eb !important;
    }


    /* ========================================================
       SECTION DIVIDERS
       ======================================================== */

    hr {
        border: none !important;
        height: 2px !important;

        background:
            linear-gradient(
                90deg,
                transparent,
                #93c5fd,
                #a78bfa,
                transparent
            ) !important;

        margin: 35px 0 !important;
    }


    /* ========================================================
       STREAMLIT TEXT
       ======================================================== */

    .stMarkdown p,
    .stMarkdown li {
        color: #263449 !important;
    }

    .stCaption {
        color: #64748b !important;
    }


    /* ========================================================
       SELECTBOX / MULTISELECT
       ======================================================== */

    [data-testid="stMultiSelect"] label,
    [data-testid="stSelectbox"] label {
        color: #334155 !important;
        font-weight: 600 !important;
    }

    [data-baseweb="select"] {
        border-radius: 9px !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton button {
        background:
            linear-gradient(
                135deg,
                #2563eb,
                #7c3aed
            ) !important;

        color: #ffffff !important;

        border: none !important;

        border-radius: 9px !important;

        font-weight: 700 !important;

        padding: 8px 18px !important;

        box-shadow:
            0 5px 15px rgba(37,99,235,0.22);
    }

    .stButton button:hover {
        background:
            linear-gradient(
                135deg,
                #1d4ed8,
                #6d28d9
            ) !important;

        color: #ffffff !important;
    }


    /* ========================================================
       DATAFRAMES
       ======================================================== */

    [data-testid="stDataFrame"] {
        border-radius: 12px !important;
        border: 1px solid #dbe3ef !important;

        box-shadow:
            0 5px 18px rgba(15,23,42,0.06);
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    [data-testid="stExpander"] {
        background: #ffffff !important;

        border: 1px solid #dbe3ef !important;

        border-radius: 12px !important;

        box-shadow:
            0 4px 15px rgba(15,23,42,0.05);
    }

    [data-testid="stExpander"] summary {
        color: #1e3a8a !important;
        font-weight: 700 !important;
    }

    [data-testid="stExpander"] summary p {
        color: #1e3a8a !important;
        font-weight: 700 !important;
    }

    [data-testid="stExpander"] div {
        color: #263449 !important;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    [data-testid="stAlert"] {
        border-radius: 11px !important;
    }

    [data-testid="stAlert"] p {
        color: #263449 !important;
    }


    /* ========================================================
       RISK CARDS
       ======================================================== */

    .risk-high {
        padding: 18px;
        border-radius: 12px;

        background:
            linear-gradient(
                135deg,
                #fff1f2,
                #ffe4e6
            ) !important;

        border-left: 6px solid #e11d48;

        color: #881337 !important;

        box-shadow:
            0 5px 15px rgba(225,29,72,0.10);
    }

    .risk-high p,
    .risk-high strong {
        color: #881337 !important;
    }


    .risk-medium {
        padding: 18px;
        border-radius: 12px;

        background:
            linear-gradient(
                135deg,
                #fffbeb,
                #fef3c7
            ) !important;

        border-left: 6px solid #f59e0b;

        color: #78350f !important;

        box-shadow:
            0 5px 15px rgba(245,158,11,0.10);
    }

    .risk-medium p,
    .risk-medium strong {
        color: #78350f !important;
    }


    .risk-low {
        padding: 18px;
        border-radius: 12px;

        background:
            linear-gradient(
                135deg,
                #f0fdf4,
                #dcfce7
            ) !important;

        border-left: 6px solid #16a34a;

        color: #14532d !important;

        box-shadow:
            0 5px 15px rgba(22,163,74,0.10);
    }

    .risk-low p,
    .risk-low strong {
        color: #14532d !important;
    }


    /* ========================================================
       PLOTLY CONTAINERS
       ======================================================== */

    .stPlotlyChart {
        background: #ffffff;

        border-radius: 14px;

        padding: 8px;

        box-shadow:
            0 5px 18px rgba(15,23,42,0.06);

        border: 1px solid #e2e8f0;
    }


    /* ========================================================
       DATASET INFO CARDS
       ======================================================== */

    .dataset-card {
        background: #ffffff;

        padding: 20px;

        border-radius: 14px;

        border: 1px solid #dbe3ef;

        box-shadow:
            0 5px 18px rgba(15,23,42,0.06);
    }


    /* ========================================================
       RECOMMENDATIONS
       ======================================================== */

    .recommendation {
        background:
            linear-gradient(
                135deg,
                #ffffff,
                #f8fafc
            );

        border-left: 5px solid #6366f1;

        padding: 14px 18px;

        margin: 9px 0;

        border-radius: 9px;

        box-shadow:
            0 3px 12px rgba(15,23,42,0.05);

        color: #263449 !important;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-box {
        text-align: center;

        padding: 20px;

        background:
            linear-gradient(
                135deg,
                #172554,
                #312e81
            );

        border-radius: 14px;

        margin-top: 30px;
    }

    .footer-box p {
        color: #dbeafe !important;
        margin: 4px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_PATHS = [
    BASE_DIR / "data" / "skycity_auckland_restaurants_bars.csv",
    BASE_DIR / "skycity_auckland_restaurants_bars.csv",
    BASE_DIR / "data" / "SkyCity Auckland Restaurants & Bars (1).csv",
    BASE_DIR / "SkyCity Auckland Restaurants & Bars (1).csv",
]


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    for path in DATA_PATHS:

        if path.exists():

            data = pd.read_csv(path)

            data = data.loc[
                :,
                ~data.columns.str.contains(
                    "^Unnamed",
                    case=False
                )
            ]

            return data

    searched_paths = "\n".join(
        str(path)
        for path in DATA_PATHS
    )

    raise FileNotFoundError(
        "Dataset not found.\n\n"
        "The application searched these locations:\n\n"
        f"{searched_paths}\n\n"
        "Please make sure the CSV file is inside the "
        "'data' folder of your GitHub repository."
    )


df = load_data()


# ============================================================
# HELPER FUNCTION
# ============================================================

def find_column(possible_names):

    for name in possible_names:

        if name in df.columns:
            return name

    return None


# ============================================================
# IDENTIFY IMPORTANT COLUMNS
# ============================================================

restaurant_id_col = find_column(
    [
        "RestaurantID",
        "Restaurant Id",
        "Restaurant_ID",
    ]
)

restaurant_name_col = find_column(
    [
        "RestaurantName",
        "Restaurant Name",
        "Restaurant_Name",
    ]
)

cuisine_col = find_column(
    [
        "CuisineType",
        "Cuisine Type",
        "Cuisine_Type",
    ]
)

segment_col = find_column(
    [
        "Segment",
    ]
)

subregion_col = find_column(
    [
        "Subregion",
        "SubRegion",
        "Sub Region",
    ]
)

growth_col = find_column(
    [
        "GrowthFactor",
        "Growth Factor",
        "Growth_Factor",
    ]
)

aov_col = find_column(
    [
        "AOV",
        "AverageOrderValue",
        "Average Order Value",
    ]
)

monthly_orders_col = find_column(
    [
        "MonthlyOrders",
        "Monthly Orders",
        "Monthly_Orders",
    ]
)


# ============================================================
# CHANNEL DEFINITIONS
# ============================================================

CHANNELS = {

    "In-Store": {
        "orders": [
            "InStoreOrders",
            "In-Store Orders",
            "InStore Order Count",
        ],

        "revenue": [
            "InStoreRevenue",
            "In-Store Revenue",
        ],

        "profit": [
            "InStoreNetProfit",
            "In-Store Net Profit",
        ],
    },


    "Uber Eats": {
        "orders": [
            "UberEatsOrders",
            "Uber Eats Orders",
            "UberEats Order Count",
        ],

        "revenue": [
            "UberEatsRevenue",
            "Uber Eats Revenue",
        ],

        "profit": [
            "UberEatsNetProfit",
            "Uber Eats Net Profit",
        ],
    },


    "DoorDash": {
        "orders": [
            "DoorDashOrders",
            "DoorDash Orders",
            "DoorDash Order Count",
        ],

        "revenue": [
            "DoorDashRevenue",
            "DoorDash Revenue",
        ],

        "profit": [
            "DoorDashNetProfit",
            "DoorDash Net Profit",
        ],
    },


    "Self-Delivery": {
        "orders": [
            "SelfDeliveryOrders",
            "Self Delivery Orders",
            "SelfDelivery Order Count",
        ],

        "revenue": [
            "SelfDeliveryRevenue",
            "Self Delivery Revenue",
        ],

        "profit": [
            "SelfDeliveryNetProfit",
            "Self Delivery Net Profit",
        ],
    },
}


# ============================================================
# RESOLVE CHANNEL COLUMNS
# ============================================================

def resolve_channel_column(possible_names):

    for name in possible_names:

        if name in df.columns:
            return name

    return None


for channel in CHANNELS:

    CHANNELS[channel]["orders"] = resolve_channel_column(
        CHANNELS[channel]["orders"]
    )

    CHANNELS[channel]["revenue"] = resolve_channel_column(
        CHANNELS[channel]["revenue"]
    )

    CHANNELS[channel]["profit"] = resolve_channel_column(
        CHANNELS[channel]["profit"]
    )


# ============================================================
# CONVERT NUMERIC COLUMNS
# ============================================================

numeric_columns = [
    growth_col,
    aov_col,
    monthly_orders_col,
]


for channel in CHANNELS:

    numeric_columns.extend(
        [
            CHANNELS[channel]["orders"],
            CHANNELS[channel]["revenue"],
            CHANNELS[channel]["profit"],
        ]
    )


for column in numeric_columns:

    if column and column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        ).fillna(0)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        text-align:center;
        padding:10px 0 18px 0;
    ">
        <div style="
            font-size:2.2rem;
        ">
            📊
        </div>

        <div style="
            font-size:1.35rem;
            font-weight:800;
            color:white !important;
        ">
            SkyCity Analytics
        </div>

        <div style="
            color:#bfdbfe !important;
            font-size:0.85rem;
            margin-top:4px;
        ">
            Auckland Restaurant Intelligence
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    <div style="
        color:#e0e7ff !important;
        font-weight:700;
        font-size:1.05rem;
        margin-bottom:8px;
    ">
        🎛️ Dashboard Filters
    </div>
    """,
    unsafe_allow_html=True,
)


st.sidebar.markdown(
    """
    <div style="
        color:#cbd5e1 !important;
        font-size:0.88rem;
        margin-bottom:15px;
    ">
        Explore order-channel performance across
        SkyCity Auckland restaurants and bars.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SUBREGION FILTER
# ============================================================

if subregion_col:

    subregions = sorted(
        df[subregion_col]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_subregions = st.sidebar.multiselect(
        "📍 Subregion",
        subregions,
        default=subregions,
    )

else:

    selected_subregions = []


# ============================================================
# CUISINE FILTER
# ============================================================

if cuisine_col:

    cuisines = sorted(
        df[cuisine_col]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_cuisines = st.sidebar.multiselect(
        "🍽️ Cuisine",
        cuisines,
        default=cuisines,
    )

else:

    selected_cuisines = []


# ============================================================
# SEGMENT FILTER
# ============================================================

if segment_col:

    segments = sorted(
        df[segment_col]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_segments = st.sidebar.multiselect(
        "🏪 Segment",
        segments,
        default=segments,
    )

else:

    selected_segments = []


# ============================================================
# CHANNEL FILTER
# ============================================================

selected_channels = st.sidebar.multiselect(
    "📦 Channels",
    list(CHANNELS.keys()),
    default=list(CHANNELS.keys()),
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if subregion_col and selected_subregions:

    filtered_df = filtered_df[
        filtered_df[subregion_col]
        .astype(str)
        .isin(selected_subregions)
    ]


if cuisine_col and selected_cuisines:

    filtered_df = filtered_df[
        filtered_df[cuisine_col]
        .astype(str)
        .isin(selected_cuisines)
    ]


if segment_col and selected_segments:

    filtered_df = filtered_df[
        filtered_df[segment_col]
        .astype(str)
        .isin(selected_segments)
    ]


# ============================================================
# CALCULATE CHANNEL METRICS
# ============================================================

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


    if order_col:

        filtered_channel_orders[channel] = (
            filtered_df[order_col].sum()
        )

    else:

        filtered_channel_orders[channel] = 0


    if revenue_col:

        filtered_channel_revenue[channel] = (
            filtered_df[revenue_col].sum()
        )

    else:

        filtered_channel_revenue[channel] = 0


    if profit_col:

        filtered_channel_profit[channel] = (
            filtered_df[profit_col].sum()
        )

    else:

        filtered_channel_profit[channel] = 0


filtered_total_orders = sum(
    filtered_channel_orders.values()
)

filtered_total_revenue = sum(
    filtered_channel_revenue.values()
)

filtered_total_profit = sum(
    filtered_channel_profit.values()
)


# ============================================================
# CALCULATE KPIs
# ============================================================

aggregator_orders = (
    filtered_channel_orders.get("Uber Eats", 0)
    + filtered_channel_orders.get("DoorDash", 0)
)


if filtered_total_orders > 0:

    aggregator_dependence = (
        aggregator_orders
        / filtered_total_orders
        * 100
    )

else:

    aggregator_dependence = 0


delivery_orders = (
    filtered_channel_orders.get("Uber Eats", 0)
    + filtered_channel_orders.get("DoorDash", 0)
    + filtered_channel_orders.get("Self-Delivery", 0)
)


if filtered_total_orders > 0:

    delivery_share = (
        delivery_orders
        / filtered_total_orders
        * 100
    )

else:

    delivery_share = 0


in_store_orders = filtered_channel_orders.get(
    "In-Store",
    0
)


if filtered_total_orders > 0:

    in_store_share = (
        in_store_orders
        / filtered_total_orders
        * 100
    )

else:

    in_store_share = 0


if filtered_total_orders > 0:

    calculated_aov = (
        filtered_total_revenue
        / filtered_total_orders
    )

else:

    calculated_aov = 0


if growth_col:

    average_growth = filtered_df[
        growth_col
    ].mean()

else:

    average_growth = 0


projected_orders = (
    filtered_total_orders
    * (1 + average_growth / 100)
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="dashboard-title">

        <h1>
            📊 SkyCity Auckland Restaurants & Bars
        </h1>

        <p>
            Order Channel Performance & Market Share Analytics
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="info-box">

        <strong>✨ Dashboard Overview</strong>

        <p>
            This interactive analytics dashboard analyses
            order volume, channel market share, revenue,
            profitability, geographic preferences,
            cuisine patterns and aggregator dependency
            across SkyCity Auckland's restaurant and bar market.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# KPI SECTION
# ============================================================

st.header("📌 Key Performance Indicators")


kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.metric(
        "📦 Monthly Orders",
        f"{filtered_total_orders:,.0f}",
    )


with kpi2:

    st.metric(
        "💰 Revenue",
        f"${filtered_total_revenue:,.0f}",
    )


with kpi3:

    st.metric(
        "💵 Net Profit",
        f"${filtered_total_profit:,.0f}",
    )


with kpi4:

    st.metric(
        "⚠️ Aggregator Dependence",
        f"{aggregator_dependence:.1f}%",
    )


# ============================================================
# SECOND KPI ROW
# ============================================================

st.subheader("📈 Additional Indicators")


kpi5, kpi6, kpi7, kpi8 = st.columns(4)


with kpi5:

    st.metric(
        "🚚 Delivery Order Share",
        f"{delivery_share:.1f}%",
    )


with kpi6:

    st.metric(
        "🏪 In-Store Reliance",
        f"{in_store_share:.1f}%",
    )


with kpi7:

    st.metric(
        "💳 Calculated AOV",
        f"${calculated_aov:,.2f}",
    )


with kpi8:

    st.metric(
        "🚀 Next-Month Order Scenario",
        f"{projected_orders:,.0f}",
        f"{average_growth:.1f}% growth",
    )


# ============================================================
# CHANNEL OVERVIEW
# ============================================================

st.markdown("---")

st.header("1. 📦 Channel Overview")


channel_data = pd.DataFrame(
    {
        "Channel": selected_channels,

        "Orders": [
            filtered_channel_orders[channel]
            for channel in selected_channels
        ],

        "Revenue": [
            filtered_channel_revenue[channel]
            for channel in selected_channels
        ],

        "Net Profit": [
            filtered_channel_profit[channel]
            for channel in selected_channels
        ],
    }
)


col1, col2 = st.columns(2)


with col1:

    fig_orders = px.bar(
        channel_data,
        x="Channel",
        y="Orders",
        title="Monthly Orders by Channel",
        text_auto=".2s",
        color="Channel",
        color_discrete_sequence=[
            "#2563EB",
            "#7C3AED",
            "#EC4899",
            "#14B8A6",
        ],
    )

    fig_orders.update_layout(
        xaxis_title="Order Channel",
        yaxis_title="Orders",
        template="plotly_white",
        legend_title="Channel",
    )

    st.plotly_chart(
        fig_orders,
        use_container_width=True,
    )


with col2:

    fig_share = px.pie(
        channel_data,
        names="Channel",
        values="Orders",
        title="Channel Order Share",
        hole=0.48,
        color_discrete_sequence=[
            "#2563EB",
            "#7C3AED",
            "#EC4899",
            "#14B8A6",
        ],
    )

    fig_share.update_layout(
        template="plotly_white",
    )

    st.plotly_chart(
        fig_share,
        use_container_width=True,
    )


# ============================================================
# REVENUE AND PROFIT
# ============================================================

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
        color_discrete_sequence=[
            "#3B82F6",
            "#8B5CF6",
            "#F472B6",
            "#2DD4BF",
        ],
    )

    fig_revenue.update_layout(
        template="plotly_white",
        yaxis_title="Revenue ($)",
    )

    st.plotly_chart(
        fig_revenue,
        use_container_width=True,
    )


with col4:

    fig_profit = px.bar(
        channel_data,
        x="Channel",
        y="Net Profit",
        title="Net Profit by Channel",
        text_auto=".2s",
        color="Channel",
        color_discrete_sequence=[
            "#22C55E",
            "#06B6D4",
            "#6366F1",
            "#A855F7",
        ],
    )

    fig_profit.update_layout(
        template="plotly_white",
        yaxis_title="Net Profit ($)",
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True,
    )


# ============================================================
# PROFIT MARGIN
# ============================================================

st.subheader("📊 Profit Margin by Channel")


channel_data["Profit Margin %"] = np.where(
    channel_data["Revenue"] > 0,

    (
        channel_data["Net Profit"]
        / channel_data["Revenue"]
        * 100
    ),

    0,
)


fig_margin = px.bar(
    channel_data,
    x="Channel",
    y="Profit Margin %",
    title="Net Profit Margin by Channel",
    text_auto=".1f",
    color="Profit Margin %",
    color_continuous_scale=[
        "#DBEAFE",
        "#6366F1",
        "#7C3AED",
    ],
)


fig_margin.update_layout(
    template="plotly_white",
    yaxis_title="Profit Margin (%)",
)


st.plotly_chart(
    fig_margin,
    use_container_width=True,
)


# ============================================================
# SUBREGION ANALYSIS
# ============================================================

st.markdown("---")

st.header("2. 🗺️ Geographic / Subregion Analysis")


if subregion_col:

    available_channels = [
        channel
        for channel in selected_channels
        if CHANNELS[channel]["orders"]
    ]


    aggregation_dict = {}

    for channel in available_channels:

        aggregation_dict[channel] = (
            CHANNELS[channel]["orders"],
            "sum",
        )


    subregion_channel = (
        filtered_df
        .groupby(subregion_col)
        .agg(**aggregation_dict)
        .reset_index()
    )


    if not subregion_channel.empty:

        st.subheader(
            "📍 Channel Order Volume by Subregion"
        )


        melted_subregion = (
            subregion_channel
            .melt(
                id_vars=[subregion_col],
                value_vars=available_channels,
                var_name="Channel",
                value_name="Orders",
            )
        )


        fig_subregion = px.bar(
            melted_subregion,
            x=subregion_col,
            y="Orders",
            color="Channel",
            barmode="group",
            title="Orders by Subregion and Channel",
            color_discrete_sequence=[
                "#2563EB",
                "#7C3AED",
                "#EC4899",
                "#14B8A6",
            ],
        )


        fig_subregion.update_layout(
            template="plotly_white",
            xaxis_title="Subregion",
            yaxis_title="Orders",
        )


        st.plotly_chart(
            fig_subregion,
            use_container_width=True,
        )


        st.subheader(
            "🔥 Subregion Channel Heatmap"
        )


        heatmap_data = (
            subregion_channel
            .set_index(subregion_col)
            [available_channels]
        )


        fig_heatmap = px.imshow(
            heatmap_data,
            text_auto=".2s",
            aspect="auto",
            title="Subregion Channel Heatmap",
            color_continuous_scale=[
                "#EFF6FF",
                "#93C5FD",
                "#4F46E5",
                "#312E81",
            ],
        )


        fig_heatmap.update_layout(
            template="plotly_white",
        )


        st.plotly_chart(
            fig_heatmap,
            use_container_width=True,
        )


        st.subheader(
            "🏆 Dominant Channel by Subregion"
        )


        dominance = heatmap_data.idxmax(
            axis=1
        )


        dominance_table = pd.DataFrame(
            {
                "Subregion": dominance.index,
                "Dominant Channel": dominance.values,
                "Orders": heatmap_data.max(
                    axis=1
                ).values,
            }
        )


        st.dataframe(
            dominance_table,
            use_container_width=True,
            hide_index=True,
        )

else:

    st.warning(
        "Subregion column was not found in the dataset."
    )


# ============================================================
# CUISINE ANALYSIS
# ============================================================

st.markdown("---")

st.header("3. 🍽️ Cuisine vs Channel Analysis")


if cuisine_col:

    available_channels = [
        channel
        for channel in selected_channels
        if CHANNELS[channel]["orders"]
    ]


    aggregation_dict = {}

    for channel in available_channels:

        aggregation_dict[channel] = (
            CHANNELS[channel]["orders"],
            "sum",
        )


    cuisine_channel = (
        filtered_df
        .groupby(cuisine_col)
        .agg(**aggregation_dict)
        .reset_index()
    )


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
        color_discrete_sequence=[
            "#2563EB",
            "#7C3AED",
            "#EC4899",
            "#14B8A6",
        ],
    )


    fig_cuisine.update_layout(
        template="plotly_white",
        xaxis_title="Cuisine",
        yaxis_title="Orders",
    )


    st.plotly_chart(
        fig_cuisine,
        use_container_width=True,
    )


    cuisine_pivot = (
        cuisine_channel
        .set_index(cuisine_col)
    )


    cuisine_dominance = (
        cuisine_pivot
        .idxmax(axis=1)
    )


    cuisine_table = pd.DataFrame(
        {
            "Cuisine": cuisine_dominance.index,
            "Dominant Channel": cuisine_dominance.values,
            "Orders": cuisine_pivot.max(
                axis=1
            ).values,
        }
    )


    st.subheader(
        "🏆 Dominant Channel by Cuisine"
    )


    st.dataframe(
        cuisine_table,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.warning(
        "Cuisine column was not found in the dataset."
    )


# ============================================================
# SEGMENT ANALYSIS
# ============================================================

st.markdown("---")

st.header("4. 🏪 Restaurant Segment Analysis")


if segment_col:

    available_channels = [
        channel
        for channel in selected_channels
        if CHANNELS[channel]["orders"]
    ]


    aggregation_dict = {}

    for channel in available_channels:

        aggregation_dict[channel] = (
            CHANNELS[channel]["orders"],
            "sum",
        )


    segment_channel = (
        filtered_df
        .groupby(segment_col)
        .agg(**aggregation_dict)
        .reset_index()
    )


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
        color_discrete_sequence=[
            "#2563EB",
            "#7C3AED",
            "#EC4899",
            "#14B8A6",
        ],
    )


    fig_segment.update_layout(
        template="plotly_white",
        xaxis_title="Restaurant Segment",
        yaxis_title="Orders",
    )


    st.plotly_chart(
        fig_segment,
        use_container_width=True,
    )

else:

    st.warning(
        "Segment column was not found in the dataset."
    )


# ============================================================
# AGGREGATOR DEPENDENCY
# ============================================================

st.markdown("---")

st.header("5. ⚠️ Aggregator Dependency Risk")


st.markdown(
    """
    <div class="info-box">

        <strong>Risk Classification</strong>

        <p>
            A restaurant is classified as
            <strong>High Risk</strong> when Uber Eats +
            DoorDash account for <strong>70% or more</strong>
            of total monthly orders.
        </p>

        <p>
            <strong>High:</strong> ≥ 70%
            &nbsp;&nbsp; | &nbsp;&nbsp;
            <strong>Medium:</strong> 50–69.9%
            &nbsp;&nbsp; | &nbsp;&nbsp;
            <strong>Low:</strong> &lt; 50%
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


dependency_df = filtered_df.copy()


uber_col = CHANNELS["Uber Eats"]["orders"]

doordash_col = CHANNELS["DoorDash"]["orders"]


if (
    uber_col
    and doordash_col
    and monthly_orders_col
):

    dependency_df["AggregatorOrders"] = (
        dependency_df[uber_col]
        + dependency_df[doordash_col]
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

        [
            "High",

            "Medium",
        ],

        default="Low",
    )


    high_risk_count = int(
        (
            dependency_df["Risk"]
            == "High"
        ).sum()
    )


    medium_risk_count = int(
        (
            dependency_df["Risk"]
            == "Medium"
        ).sum()
    )


    low_risk_count = int(
        (
            dependency_df["Risk"]
            == "Low"
        ).sum()
    )


    r1, r2, r3 = st.columns(3)


    with r1:

        st.metric(
            "🔴 High Risk",
            f"{high_risk_count:,}",
        )


    with r2:

        st.metric(
            "🟠 Medium Risk",
            f"{medium_risk_count:,}",
        )


    with r3:

        st.metric(
            "🟢 Low Risk",
            f"{low_risk_count:,}",
        )


    risk_counts = pd.DataFrame(
        {
            "Risk": [
                "High",
                "Medium",
                "Low",
            ],

            "Restaurants": [
                high_risk_count,
                medium_risk_count,
                low_risk_count,
            ],
        }
    )


    fig_risk = px.bar(
        risk_counts,
        x="Risk",
        y="Restaurants",
        title="Restaurant Dependency Risk Distribution",
        text_auto=True,
        color="Risk",
        color_discrete_map={
            "High": "#E11D48",
            "Medium": "#F59E0B",
            "Low": "#16A34A",
        },
    )


    fig_risk.update_layout(
        template="plotly_white",
    )


    st.plotly_chart(
        fig_risk,
        use_container_width=True,
    )


    # ========================================================
    # RESTAURANT RISK TABLE
    # ========================================================

    st.subheader(
        "🔎 Restaurants with Highest Aggregator Dependence"
    )


    display_columns = []


    if restaurant_id_col:

        display_columns.append(
            restaurant_id_col
        )


    if restaurant_name_col:

        display_columns.append(
            restaurant_name_col
        )


    if cuisine_col:

        display_columns.append(
            cuisine_col
        )


    if segment_col:

        display_columns.append(
            segment_col
        )


    if subregion_col:

        display_columns.append(
            subregion_col
        )


    display_columns.extend(
        [
            monthly_orders_col,
            "AggregatorOrders",
            "AggregatorDependence",
            "Risk",
        ]
    )


    display_columns = [
        column
        for column in display_columns
        if column
        and column in dependency_df.columns
    ]


    risk_table = (
        dependency_df[
            display_columns
        ]
        .sort_values(
            "AggregatorDependence",
            ascending=False,
        )
    )


    st.dataframe(
        risk_table.head(100),
        use_container_width=True,
        hide_index=True,
    )

else:

    st.warning(
        "Required columns for aggregator dependency "
        "analysis were not found."
    )


# ============================================================
# CHANNEL DIVERSIFICATION
# ============================================================

st.markdown("---")

st.header("6. 🔀 Channel Diversification")


st.markdown(
    """
    <div class="info-box">

        <strong>📐 Diversification Method</strong>

        <p>
            The Channel Diversification Score uses normalized
            Shannon entropy across the four order channels.
        </p>

        <p>
            <strong>0 = highly concentrated</strong>
            &nbsp;&nbsp; | &nbsp;&nbsp;
            <strong>100 = highly diversified</strong>
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


diversification_df = filtered_df.copy()


order_columns = {
    channel: CHANNELS[channel]["orders"]
    for channel in CHANNELS
    if CHANNELS[channel]["orders"]
}


if (
    len(order_columns) >= 2
    and monthly_orders_col
):

    channel_values = np.column_stack(
        [
            diversification_df[column].values
            for column in order_columns.values()
        ]
    )


    totals = channel_values.sum(
        axis=1
    )


    proportions = np.divide(
        channel_values,
        totals[:, None],
        out=np.zeros_like(
            channel_values,
            dtype=float,
        ),
        where=totals[:, None] != 0,
    )


    entropy = -np.sum(
        np.where(
            proportions > 0,
            proportions
            * np.log(proportions),
            0,
        ),
        axis=1,
    )


    max_entropy = np.log(
        len(order_columns)
    )


    diversification_df[
        "DiversificationScore"
    ] = np.where(
        max_entropy > 0,

        entropy
        / max_entropy
        * 100,

        0,
    )


    average_diversification = (
        diversification_df[
            "DiversificationScore"
        ].mean()
    )


    st.metric(
        "🌐 Average Channel Diversification Score",
        f"{average_diversification:.1f}/100",
    )


    fig_diversification = px.histogram(
        diversification_df,
        x="DiversificationScore",
        nbins=20,
        title="Distribution of Channel Diversification Scores",
        color_discrete_sequence=[
            "#6366F1"
        ],
    )


    fig_diversification.update_layout(
        template="plotly_white",
        xaxis_title="Diversification Score",
        yaxis_title="Number of Restaurants",
    )


    st.plotly_chart(
        fig_diversification,
        use_container_width=True,
    )

else:

    st.warning(
        "Not enough channel order columns are available "
        "for diversification analysis."
    )


# ============================================================
# GROWTH SCENARIO
# ============================================================

st.markdown("---")

st.header("7. 📈 Growth Scenario")


if growth_col:

    growth_summary = pd.DataFrame(
        {
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
        }
    )


    st.dataframe(
        growth_summary,
        use_container_width=True,
        hide_index=True,
    )


    st.info(
        "The dataset does not contain a time dimension. "
        "Therefore, this is a one-month growth scenario "
        "using the supplied GrowthFactor, not a true "
        "historical time-series forecast."
    )

else:

    st.info(
        "GrowthFactor was not found in the dataset."
    )


# ============================================================
# DATA QUALITY VALIDATION
# ============================================================

st.markdown("---")

st.header("8. ✅ Data Quality Validation")


validation_results = []


missing_values = int(
    df.isna().sum().sum()
)


validation_results.append(
    {
        "Validation": "Missing Values",
        "Result": missing_values,
        "Status": (
            "PASS"
            if missing_values == 0
            else "CHECK"
        ),
    }
)


duplicate_rows = int(
    df.duplicated().sum()
)


validation_results.append(
    {
        "Validation": "Duplicate Rows",
        "Result": duplicate_rows,
        "Status": (
            "PASS"
            if duplicate_rows == 0
            else "CHECK"
        ),
    }
)


if monthly_orders_col:

    available_order_columns = [
        column
        for column in order_columns.values()
        if column in df.columns
    ]


    if available_order_columns:

        calculated_orders = (
            df[available_order_columns]
            .sum(axis=1)
        )


        mismatches = int(
            (
                calculated_orders
                != df[monthly_orders_col]
            ).sum()
        )


        validation_results.append(
            {
                "Validation":
                    "Channel Orders = Monthly Orders",

                "Result": mismatches,

                "Status": (
                    "PASS"
                    if mismatches == 0
                    else "CHECK"
                ),
            }
        )


validation_table = pd.DataFrame(
    validation_results
)


st.dataframe(
    validation_table,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# EXECUTIVE INSIGHTS
# ============================================================

st.markdown("---")

st.header("9. 💡 Executive Insights & Recommendations")


if filtered_channel_orders:

    dominant_channel = max(
        filtered_channel_orders,
        key=filtered_channel_orders.get,
    )

    dominant_orders = (
        filtered_channel_orders[
            dominant_channel
        ]
    )

else:

    dominant_channel = "N/A"
    dominant_orders = 0


st.subheader("🔎 Key Findings")


st.markdown(
    f"""
    <div class="recommendation">
        <strong>📦 Dominant Channel:</strong>
        {dominant_channel}, with approximately
        <strong>{dominant_orders:,.0f} orders</strong>.
    </div>

    <div class="recommendation">
        <strong>🚚 Delivery Contribution:</strong>
        Delivery channels account for approximately
        <strong>{delivery_share:.1f}%</strong> of orders.
    </div>

    <div class="recommendation">
        <strong>⚠️ Aggregator Dependence:</strong>
        Uber Eats and DoorDash together account for
        approximately <strong>{aggregator_dependence:.1f}%</strong>
        of orders.
    </div>

    <div class="recommendation">
        <strong>🏪 In-Store Reliance:</strong>
        In-Store contributes approximately
        <strong>{in_store_share:.1f}%</strong> of orders.
    </div>

    <div class="recommendation">
        <strong>🚀 Projected Orders:</strong>
        Using the supplied GrowthFactor, the next-month
        scenario is approximately
        <strong>{projected_orders:,.0f} orders</strong>.
    </div>
    """,
    unsafe_allow_html=True,
)


st.subheader(
    "🎯 Strategic Recommendations"
)


recommendations = [
    "Diversify order channels to reduce dependence on a small number of aggregators.",
    "Monitor restaurants where Uber Eats and DoorDash together exceed the 70% dependency threshold.",
    "Strengthen direct and self-delivery capabilities where delivery economics support it.",
    "Use subregion-level channel preferences to tailor marketing and operational strategies.",
    "Use cuisine-level channel patterns when allocating promotional budgets.",
    "Protect profitable in-store demand while using digital channels to expand customer reach.",
    "Track profitability alongside order volume because the largest channel may not be the most profitable.",
]


for recommendation in recommendations:

    st.markdown(
        f"""
        <div class="recommendation">
            💡 {recommendation}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# DATASET INFORMATION
# ============================================================

st.markdown("---")

st.header("10. 📋 Dataset Information")


info1, info2, info3 = st.columns(3)


with info1:

    st.metric(
        "🏪 Restaurant Records",
        f"{len(df):,}",
    )


with info2:

    st.metric(
        "🧾 Dataset Columns",
        f"{len(df.columns):,}",
    )


with info3:

    st.metric(
        "🔎 Filtered Records",
        f"{len(filtered_df):,}",
    )


with st.expander(
    "🔍 View Dataset Columns"
):

    st.write(
        list(df.columns)
    )


with st.expander(
    "📄 View Filtered Data"
):

    st.dataframe(
        filtered_df.head(500),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-box">

        <p>
            <strong>
                📊 SkyCity Auckland Restaurants & Bars
            </strong>
        </p>

        <p>
            Order Channel Performance and Market Share Analytics
        </p>

        <p>
            Unified Mentor Project • Interactive Streamlit Analytics Dashboard
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)
