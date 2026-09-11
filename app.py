from pathlib import Path

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SkyCity Auckland | Channel Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
        .main {
            padding-top: 1rem;
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        h1 {
            font-weight: 700;
        }

        h2, h3 {
            font-weight: 600;
        }

        [data-testid="stMetric"] {
            background-color: #f8f9fa;
            border: 1px solid #e5e7eb;
            padding: 15px;
            border-radius: 10px;
        }

        .info-box {
            padding: 15px;
            border-radius: 10px;
            background-color: #f3f6fa;
            border: 1px solid #d9e2ec;
            margin-bottom: 15px;
        }

        .risk-high {
            padding: 12px;
            border-radius: 8px;
            background-color: #ffe5e5;
            border-left: 5px solid #d62728;
        }

        .risk-medium {
            padding: 12px;
            border-radius: 8px;
            background-color: #fff4d6;
            border-left: 5px solid #ff9900;
        }

        .risk-low {
            padding: 12px;
            border-radius: 8px;
            background-color: #e6f7e6;
            border-left: 5px solid #2ca02c;
        }
    </style>
    """,
    unsafe_allow_html=True
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

            df = pd.read_csv(path)

            # Remove accidental unnamed columns
            df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

            return df

    searched_paths = "\n".join(str(path) for path in DATA_PATHS)

    raise FileNotFoundError(
        "Dataset not found.\n\n"
        "The application searched these locations:\n\n"
        f"{searched_paths}\n\n"
        "Please make sure the CSV file is uploaded to GitHub "
        "inside the data folder."
    )


df = load_data()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_column(possible_names):

    """
    Finds a column from a list of possible column names.
    """

    for name in possible_names:

        if name in df.columns:
            return name

    return None


def numeric_sum(column):

    if column and column in df.columns:
        return pd.to_numeric(df[column], errors="coerce").fillna(0).sum()

    return 0


def safe_percentage(value):

    return f"{value:.1f}%"


# ============================================================
# COLUMN DETECTION
# ============================================================

restaurant_id_col = find_column(
    ["RestaurantID", "Restaurant Id", "Restaurant_ID"]
)

restaurant_name_col = find_column(
    ["RestaurantName", "Restaurant Name", "Restaurant_Name"]
)

cuisine_col = find_column(
    ["CuisineType", "Cuisine Type", "Cuisine_Type"]
)

segment_col = find_column(
    ["Segment"]
)

subregion_col = find_column(
    ["Subregion", "SubRegion", "Sub Region"]
)

growth_col = find_column(
    ["GrowthFactor", "Growth Factor", "Growth_Factor"]
)

aov_col = find_column(
    ["AOV", "AverageOrderValue", "Average Order Value"]
)

monthly_orders_col = find_column(
    ["MonthlyOrders", "Monthly Orders", "Monthly_Orders"]
)

delivery_radius_col = find_column(
    ["DeliveryRadiusKM", "Delivery Radius KM"]
)

delivery_cost_col = find_column(
    ["DeliveryCostOrder", "Delivery Cost Order"]
)


# ============================================================
# CHANNEL COLUMN DEFINITIONS
# ============================================================

CHANNELS = {
    "In-Store": {
        "orders": "InStoreOrders",
        "revenue": "InStoreRevenue",
        "profit": "InStoreNetProfit",
    },
    "Uber Eats": {
        "orders": "UberEatsOrders",
        "revenue": "UberEatsRevenue",
        "profit": "UberEatsNetProfit",
    },
    "DoorDash": {
        "orders": "DoorDashOrders",
        "revenue": "DoorDashRevenue",
        "profit": "DoorDashNetProfit",
    },
    "Self-Delivery": {
        "orders": "SelfDeliveryOrders",
        "revenue": "SelfDeliveryRevenue",
        "profit": "SelfDeliveryNetProfit",
    },
}


# Try alternative column names if required
COLUMN_ALIASES = {

    "InStoreOrders": [
        "InStoreOrders",
        "In-Store Orders",
        "InStore Order Count",
        "InStore_Order_Count",
    ],

    "UberEatsOrders": [
        "UberEatsOrders",
        "Uber Eats Orders",
        "UberEats Order Count",
    ],

    "DoorDashOrders": [
        "DoorDashOrders",
        "DoorDash Orders",
        "DoorDash Order Count",
    ],

    "SelfDeliveryOrders": [
        "SelfDeliveryOrders",
        "Self Delivery Orders",
        "SelfDelivery Order Count",
    ],

    "InStoreRevenue": [
        "InStoreRevenue",
        "In-Store Revenue",
        "InStore Revenue",
    ],

    "UberEatsRevenue": [
        "UberEatsRevenue",
        "Uber Eats Revenue",
    ],

    "DoorDashRevenue": [
        "DoorDashRevenue",
        "DoorDash Revenue",
    ],

    "SelfDeliveryRevenue": [
        "SelfDeliveryRevenue",
        "Self Delivery Revenue",
    ],

    "InStoreNetProfit": [
        "InStoreNetProfit",
        "In-Store Net Profit",
    ],

    "UberEatsNetProfit": [
        "UberEatsNetProfit",
        "Uber Eats Net Profit",
    ],

    "DoorDashNetProfit": [
        "DoorDashNetProfit",
        "DoorDash Net Profit",
    ],

    "SelfDeliveryNetProfit": [
        "SelfDeliveryNetProfit",
        "Self Delivery Net Profit",
    ],
}


def resolve_column(column_name):

    if column_name in df.columns:
        return column_name

    for alternative in COLUMN_ALIASES.get(column_name, []):

        if alternative in df.columns:
            return alternative

    return None


# Resolve actual columns
for channel in CHANNELS:

    CHANNELS[channel]["orders"] = resolve_column(
        CHANNELS[channel]["orders"]
    )

    CHANNELS[channel]["revenue"] = resolve_column(
        CHANNELS[channel]["revenue"]
    )

    CHANNELS[channel]["profit"] = resolve_column(
        CHANNELS[channel]["profit"]
    )


# ============================================================
# NUMERIC CONVERSION
# ============================================================

numeric_columns = [
    monthly_orders_col,
    growth_col,
    aov_col,
    delivery_radius_col,
    delivery_cost_col,
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
# CHANNEL ORDER TOTALS
# ============================================================

channel_order_totals = {}

for channel, columns in CHANNELS.items():

    order_col = columns["orders"]

    if order_col:

        channel_order_totals[channel] = df[order_col].sum()

    else:

        channel_order_totals[channel] = 0


total_orders = sum(channel_order_totals.values())


# ============================================================
# CHANNEL REVENUE TOTALS
# ============================================================

channel_revenue_totals = {}

for channel, columns in CHANNELS.items():

    revenue_col = columns["revenue"]

    if revenue_col:

        channel_revenue_totals[channel] = df[revenue_col].sum()

    else:

        channel_revenue_totals[channel] = 0


total_revenue = sum(channel_revenue_totals.values())


# ============================================================
# CHANNEL PROFIT TOTALS
# ============================================================

channel_profit_totals = {}

for channel, columns in CHANNELS.items():

    profit_col = columns["profit"]

    if profit_col:

        channel_profit_totals[channel] = df[profit_col].sum()

    else:

        channel_profit_totals[channel] = 0


total_profit = sum(channel_profit_totals.values())


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎛️ Dashboard Filters")

st.sidebar.markdown(
    "Use the filters below to explore SkyCity Auckland's "
    "restaurant and bar order-channel performance."
)


# Subregion filter
if subregion_col:

    subregions = sorted(
        df[subregion_col].dropna().astype(str).unique()
    )

    selected_subregions = st.sidebar.multiselect(
        "Subregion",
        subregions,
        default=subregions
    )

else:

    selected_subregions = []


# Cuisine filter
if cuisine_col:

    cuisines = sorted(
        df[cuisine_col].dropna().astype(str).unique()
    )

    selected_cuisines = st.sidebar.multiselect(
        "Cuisine",
        cuisines,
        default=cuisines
    )

else:

    selected_cuisines = []


# Segment filter
if segment_col:

    segments = sorted(
        df[segment_col].dropna().astype(str).unique()
    )

    selected_segments = st.sidebar.multiselect(
        "Segment",
        segments,
        default=segments
    )

else:

    selected_segments = []


selected_channels = st.sidebar.multiselect(
    "Channels",
    list(CHANNELS.keys()),
    default=list(CHANNELS.keys())
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if subregion_col and selected_subregions:

    filtered_df = filtered_df[
        filtered_df[subregion_col].astype(str).isin(
            selected_subregions
        )
    ]


if cuisine_col and selected_cuisines:

    filtered_df = filtered_df[
        filtered_df[cuisine_col].astype(str).isin(
            selected_cuisines
        )
    ]


if segment_col and selected_segments:

    filtered_df = filtered_df[
        filtered_df[segment_col].astype(str).isin(
            selected_segments
        )
    ]


# ============================================================
# FILTERED CHANNEL METRICS
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
# HEADER
# ============================================================

st.title(
    "📊 SkyCity Auckland Restaurants & Bars"
)

st.subheader(
    "Order Channel Performance & Market Share Analytics"
)

st.markdown(
    """
    <div class="info-box">
    This interactive dashboard analyses order volume, channel share,
    revenue, profitability, geographic preferences, cuisine patterns,
    and dependency risk across In-Store, Uber Eats, DoorDash,
    and Self-Delivery channels.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# KPI SECTION
# ============================================================

st.markdown("## 📌 Key Performance Indicators")


kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.metric(
        "Monthly Orders",
        f"{filtered_total_orders:,.0f}"
    )


with kpi2:

    st.metric(
        "Revenue",
        f"${filtered_total_revenue:,.0f}"
    )


with kpi3:

    st.metric(
        "Net Profit",
        f"${filtered_total_profit:,.0f}"
    )


# Aggregator dependence
aggregator_orders = (
    filtered_channel_orders.get("Uber Eats", 0)
    + filtered_channel_orders.get("DoorDash", 0)
)

if filtered_total_orders > 0:

    aggregator_dependence = (
        aggregator_orders / filtered_total_orders * 100
    )

else:

    aggregator_dependence = 0


with kpi4:

    st.metric(
        "Aggregator Dependence",
        f"{aggregator_dependence:.1f}%"
    )


# ============================================================
# SECOND KPI ROW
# ============================================================

st.markdown("## 📈 Additional Indicators")


kpi5, kpi6, kpi7, kpi8 = st.columns(4)


# Delivery share
delivery_orders = (
    filtered_channel_orders.get("Uber Eats", 0)
    + filtered_channel_orders.get("DoorDash", 0)
    + filtered_channel_orders.get("Self-Delivery", 0)
)

if filtered_total_orders:

    delivery_share = (
        delivery_orders / filtered_total_orders * 100
    )

else:

    delivery_share = 0


with kpi5:

    st.metric(
        "Delivery Order Share",
        f"{delivery_share:.1f}%"
    )


# In-store share
in_store_orders = filtered_channel_orders.get(
    "In-Store",
    0
)

if filtered_total_orders:

    in_store_share = (
        in_store_orders / filtered_total_orders * 100
    )

else:

    in_store_share = 0


with kpi6:

    st.metric(
        "In-Store Reliance",
        f"{in_store_share:.1f}%"
    )


# Average order value
if filtered_total_orders > 0:

    calculated_aov = (
        filtered_total_revenue /
        filtered_total_orders
    )

else:

    calculated_aov = 0


with kpi7:

    st.metric(
        "Calculated AOV",
        f"${calculated_aov:,.2f}"
    )


# Next month scenario
if growth_col:

    average_growth = filtered_df[growth_col].mean()

else:

    average_growth = 0


projected_orders = (
    filtered_total_orders *
    (1 + average_growth / 100)
)


with kpi8:

    st.metric(
        "Next-Month Order Scenario",
        f"{projected_orders:,.0f}",
        f"{average_growth:.1f}% growth"
    )


# ============================================================
# CHANNEL OVERVIEW
# ============================================================

st.markdown("---")

st.header("1. Channel Overview")


channel_data = pd.DataFrame(
    {
        "Channel": list(selected_channels),
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
        text_auto=".2s"
    )

    fig_orders.update_layout(
        xaxis_title="Order Channel",
        yaxis_title="Orders",
        showlegend=False
    )

    st.plotly_chart(
        fig_orders,
        use_container_width=True
    )


with col2:

    fig_share = px.pie(
        channel_data,
        names="Channel",
        values="Orders",
        title="Channel Order Share",
        hole=0.4
    )

    st.plotly_chart(
        fig_share,
        use_container_width=True
    )


# ============================================================
# REVENUE AND PROFIT
# ============================================================

st.subheader("Revenue and Net Profit by Channel")


col3, col4 = st.columns(2)


with col3:

    fig_revenue = px.bar(
        channel_data,
        x="Channel",
        y="Revenue",
        title="Revenue by Channel",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_revenue,
        use_container_width=True
    )


with col4:

    fig_profit = px.bar(
        channel_data,
        x="Channel",
        y="Net Profit",
        title="Net Profit by Channel",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )


# ============================================================
# CHANNEL PROFITABILITY
# ============================================================

channel_data["Profit Margin %"] = np.where(
    channel_data["Revenue"] > 0,
    channel_data["Net Profit"]
    / channel_data["Revenue"] * 100,
    0
)


fig_margin = px.bar(
    channel_data,
    x="Channel",
    y="Profit Margin %",
    title="Net Profit Margin by Channel",
    text_auto=".1f"
)

fig_margin.update_layout(
    yaxis_title="Profit Margin (%)"
)

st.plotly_chart(
    fig_margin,
    use_container_width=True
)


# ============================================================
# SUBREGION ANALYSIS
# ============================================================

st.markdown("---")

st.header("2. Geographic / Subregion Analysis")


if subregion_col:

    subregion_channel = (
        filtered_df
        .groupby(subregion_col)
        .agg(
            **{
                channel: (
                    CHANNELS[channel]["orders"],
                    "sum"
                )
                for channel in selected_channels
                if CHANNELS[channel]["orders"]
            }
        )
        .reset_index()
    )


    if not subregion_channel.empty:

        st.subheader(
            "Channel Order Volume by Subregion"
        )

        melt_columns = [
            channel
            for channel in selected_channels
            if channel in subregion_channel.columns
        ]

        melted_subregion = subregion_channel.melt(
            id_vars=[subregion_col],
            value_vars=melt_columns,
            var_name="Channel",
            value_name="Orders"
        )


        fig_subregion = px.bar(
            melted_subregion,
            x=subregion_col,
            y="Orders",
            color="Channel",
            barmode="group",
            title="Orders by Subregion and Channel"
        )

        fig_subregion.update_layout(
            xaxis_title="Subregion",
            yaxis_title="Orders"
        )

        st.plotly_chart(
            fig_subregion,
            use_container_width=True
        )


        # Heatmap
        heatmap_data = subregion_channel.set_index(
            subregion_col
        )[melt_columns]


        fig_heatmap = px.imshow(
            heatmap_data,
            text_auto=".2s",
            aspect="auto",
            title="Subregion Channel Heatmap"
        )

        st.plotly_chart(
            fig_heatmap,
            use_container_width=True
        )


        # Dominant channel
        dominance = heatmap_data.idxmax(axis=1)

        dominance_table = pd.DataFrame(
            {
                "Subregion": dominance.index,
                "Dominant Channel": dominance.values,
                "Orders": heatmap_data.max(axis=1).values
            }
        )

        st.subheader(
            "Dominant Channel by Subregion"
        )

        st.dataframe(
            dominance_table,
            use_container_width=True,
            hide_index=True
        )


else:

    st.warning(
        "Subregion column was not found in the dataset."
    )


# ============================================================
# CUISINE ANALYSIS
# ============================================================

st.markdown("---")

st.header("3. Cuisine vs Channel Analysis")


if cuisine_col:

    cuisine_channel = (
        filtered_df
        .groupby(cuisine_col)
        .agg(
            **{
                channel: (
                    CHANNELS[channel]["orders"],
                    "sum"
                )
                for channel in selected_channels
                if CHANNELS[channel]["orders"]
            }
        )
        .reset_index()
    )


    cuisine_melt = cuisine_channel.melt(
        id_vars=[cuisine_col],
        var_name="Channel",
        value_name="Orders"
    )


    fig_cuisine = px.bar(
        cuisine_melt,
        x=cuisine_col,
        y="Orders",
        color="Channel",
        barmode="stack",
        title="Cuisine Channel Mix"
    )

    fig_cuisine.update_layout(
        xaxis_title="Cuisine",
        yaxis_title="Orders"
    )

    st.plotly_chart(
        fig_cuisine,
        use_container_width=True
    )


    # Cuisine dominant channel
    cuisine_pivot = cuisine_channel.set_index(
        cuisine_col
    )

    cuisine_dominance = cuisine_pivot.idxmax(
        axis=1
    )


    cuisine_table = pd.DataFrame(
        {
            "Cuisine": cuisine_dominance.index,
            "Dominant Channel": cuisine_dominance.values,
            "Orders": cuisine_pivot.max(axis=1).values
        }
    )


    st.subheader(
        "Dominant Channel by Cuisine"
    )

    st.dataframe(
        cuisine_table,
        use_container_width=True,
        hide_index=True
    )


else:

    st.warning(
        "Cuisine column was not found in the dataset."
    )


# ============================================================
# SEGMENT ANALYSIS
# ============================================================

st.markdown("---")

st.header("4. Restaurant Segment Analysis")


if segment_col:

    segment_channel = (
        filtered_df
        .groupby(segment_col)
        .agg(
            **{
                channel: (
                    CHANNELS[channel]["orders"],
                    "sum"
                )
                for channel in selected_channels
                if CHANNELS[channel]["orders"]
            }
        )
        .reset_index()
    )


    segment_melt = segment_channel.melt(
        id_vars=[segment_col],
        var_name="Channel",
        value_name="Orders"
    )


    fig_segment = px.bar(
        segment_melt,
        x=segment_col,
        y="Orders",
        color="Channel",
        barmode="group",
        title="Order Channels by Restaurant Segment"
    )

    st.plotly_chart(
        fig_segment,
        use_container_width=True
    )


else:

    st.warning(
        "Segment column was not found in the dataset."
    )


# ============================================================
# DEPENDENCY RISK
# ============================================================

st.markdown("---")

st.header("5. Aggregator Dependency Risk")


st.markdown(
    """
    **Risk threshold:** a restaurant is flagged as high dependency
    when Uber Eats + DoorDash account for **70% or more of total
    monthly orders**.
    """
)


dependency_df = filtered_df.copy()


uber_col = CHANNELS["Uber Eats"]["orders"]
doordash_col = CHANNELS["DoorDash"]["orders"]


if uber_col and doordash_col and monthly_orders_col:

    dependency_df["AggregatorOrders"] = (
        dependency_df[uber_col]
        + dependency_df[doordash_col]
    )


    dependency_df["AggregatorDependence"] = np.where(
        dependency_df[monthly_orders_col] > 0,
        dependency_df["AggregatorOrders"]
        / dependency_df[monthly_orders_col] * 100,
        0
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
        default="Low"
    )


    high_risk_count = (
        dependency_df["Risk"] == "High"
    ).sum()


    medium_risk_count = (
        dependency_df["Risk"] == "Medium"
    ).sum()


    low_risk_count = (
        dependency_df["Risk"] == "Low"
    ).sum()


    r1, r2, r3 = st.columns(3)


    with r1:

        st.metric(
            "High Risk",
            f"{high_risk_count:,}"
        )


    with r2:

        st.metric(
            "Medium Risk",
            f"{medium_risk_count:,}"
        )


    with r3:

        st.metric(
            "Low Risk",
            f"{low_risk_count:,}"
        )


    # Risk chart
    risk_counts = pd.DataFrame(
        {
            "Risk": [
                "High",
                "Medium",
                "Low"
            ],
            "Restaurants": [
                high_risk_count,
                medium_risk_count,
                low_risk_count
            ]
        }
    )


    fig_risk = px.bar(
        risk_counts,
        x="Risk",
        y="Restaurants",
        title="Restaurant Dependency Risk Distribution",
        text_auto=True
    )


    st.plotly_chart(
        fig_risk,
        use_container_width=True
    )


    # Restaurant-level risk table

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
            "Risk"
        ]
    )


    display_columns = [
        column
        for column in display_columns
        if column and column in dependency_df.columns
    ]


    risk_table = dependency_df[
        display_columns
    ].sort_values(
        "AggregatorDependence",
        ascending=False
    )


    st.subheader(
        "Restaurants with Highest Aggregator Dependence"
    )


    st.dataframe(
        risk_table.head(100),
        use_container_width=True,
        hide_index=True
    )


else:

    st.warning(
        "Required order columns for dependency analysis "
        "were not found."
    )


# ============================================================
# CHANNEL DIVERSIFICATION
# ============================================================

st.markdown("---")

st.header("6. Channel Diversification")


st.markdown(
    """
    The Channel Diversification Score uses normalized Shannon entropy
    across the four order channels.

    **0 = highly concentrated**  
    **100 = highly diversified**
    """
)


diversification_df = filtered_df.copy()


order_columns = {
    channel: CHANNELS[channel]["orders"]
    for channel in CHANNELS
    if CHANNELS[channel]["orders"]
}


if len(order_columns) >= 2 and monthly_orders_col:

    channel_values = np.column_stack(
        [
            diversification_df[column].values
            for column in order_columns.values()
        ]
    )


    totals = channel_values.sum(axis=1)


    proportions = np.divide(
        channel_values,
        totals[:, None],
        out=np.zeros_like(
            channel_values,
            dtype=float
        ),
        where=totals[:, None] != 0
    )


    entropy = -np.sum(
        np.where(
            proportions > 0,
            proportions * np.log(proportions),
            0
        ),
        axis=1
    )


    max_entropy = np.log(
        len(order_columns)
    )


    diversification_df[
        "DiversificationScore"
    ] = np.where(
        max_entropy > 0,
        entropy / max_entropy * 100,
        0
    )


    average_diversification = (
        diversification_df[
            "DiversificationScore"
        ].mean()
    )


    st.metric(
        "Average Channel Diversification Score",
        f"{average_diversification:.1f}/100"
    )


    fig_diversification = px.histogram(
        diversification_df,
        x="DiversificationScore",
        nbins=20,
        title="Distribution of Channel Diversification Scores"
    )


    st.plotly_chart(
        fig_diversification,
        use_container_width=True
    )


else:

    st.warning(
        "Not enough channel order columns available "
        "for diversification analysis."
    )


# ============================================================
# GROWTH PROJECTION
# ============================================================

st.markdown("---")

st.header("7. Growth Scenario")


if growth_col:

    growth_summary = pd.DataFrame(
        {
            "Metric": [
                "Average Growth Factor",
                "Current Monthly Orders",
                "Projected Monthly Orders"
            ],
            "Value": [
                f"{average_growth:.2f}%",
                f"{filtered_total_orders:,.0f}",
                f"{projected_orders:,.0f}"
            ]
        }
    )


    st.dataframe(
        growth_summary,
        use_container_width=True,
        hide_index=True
    )


    st.info(
        "Important: the dataset does not contain a time dimension. "
        "Therefore, this is a one-month growth scenario using the "
        "supplied GrowthFactor, not a true historical time-series forecast."
    )


else:

    st.info(
        "GrowthFactor was not found in the dataset."
    )


# ============================================================
# DATA VALIDATION
# ============================================================

st.markdown("---")

st.header("8. Data Quality Validation")


validation_results = []


# Missing values
missing_values = int(
    df.isna().sum().sum()
)


validation_results.append(
    {
        "Validation": "Missing Values",
        "Result": missing_values,
        "Status": "PASS" if missing_values == 0 else "CHECK"
    }
)


# Duplicate rows
duplicate_rows = int(
    df.duplicated().sum()
)


validation_results.append(
    {
        "Validation": "Duplicate Rows",
        "Result": duplicate_rows,
        "Status": "PASS" if duplicate_rows == 0 else "CHECK"
    }
)


# Monthly order reconciliation
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
                "Validation": "Channel Orders = Monthly Orders",
                "Result": mismatches,
                "Status": (
                    "PASS"
                    if mismatches == 0
                    else "CHECK"
                )
            }
        )


validation_table = pd.DataFrame(
    validation_results
)


st.dataframe(
    validation_table,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# EXECUTIVE INSIGHTS
# ============================================================

st.markdown("---")

st.header("9. Executive Insights & Recommendations")


# Determine dominant channel
if filtered_channel_orders:

    dominant_channel = max(
        filtered_channel_orders,
        key=filtered_channel_orders.get
    )

    dominant_orders = filtered_channel_orders[
        dominant_channel
    ]

else:

    dominant_channel = "N/A"
    dominant_orders = 0


st.subheader("Key Findings")


st.markdown(
    f"""
    - **Dominant channel:** {dominant_channel}, with
      approximately **{dominant_orders:,.0f} orders** in the selected data.
    - **Delivery contribution:** delivery channels account for
      approximately **{delivery_share:.1f}%** of selected orders.
    - **Aggregator dependence:** Uber Eats and DoorDash together
      account for approximately **{aggregator_dependence:.1f}%**
      of selected orders.
    - **In-store reliance:** In-Store contributes approximately
      **{in_store_share:.1f}%** of selected orders.
    - **Projected orders:** using the supplied GrowthFactor,
      the next-month scenario is approximately
      **{projected_orders:,.0f} orders**.
    """
)


st.subheader("Strategic Recommendations")


recommendations = [
    "Diversify order channels to reduce dependence on a small number of aggregators.",
    "Monitor restaurants where Uber Eats and DoorDash together exceed the 70% dependency threshold.",
    "Strengthen direct/self-delivery capabilities where economics and delivery radius support it.",
    "Use subregion-level channel preferences to tailor marketing and operational strategies.",
    "Review cuisine-level channel patterns before allocating promotional budgets.",
    "Protect profitable in-store demand while using digital channels to expand customer reach.",
    "Track channel profitability alongside order volume because the largest order channel may not be the most profitable.",
]


for recommendation in recommendations:

    st.markdown(
        f"• {recommendation}"
    )


# ============================================================
# DATASET INFORMATION
# ============================================================

st.markdown("---")

st.header("10. Dataset Information")


info1, info2, info3 = st.columns(3)


with info1:

    st.metric(
        "Restaurant Records",
        f"{len(df):,}"
    )


with info2:

    st.metric(
        "Dataset Columns",
        f"{len(df.columns):,}"
    )


with info3:

    st.metric(
        "Filtered Records",
        f"{len(filtered_df):,}"
    )


with st.expander("View Dataset Columns"):

    st.write(
        list(df.columns)
    )


with st.expander("View Filtered Data"):

    st.dataframe(
        filtered_df.head(500),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "SkyCity Auckland Restaurants & Bars — "
    "Order Channel Performance and Market Share Analytics"
)

st.caption(
    "Developed for Unified Mentor Project | "
    "Interactive Streamlit Analytics Dashboard"
)
