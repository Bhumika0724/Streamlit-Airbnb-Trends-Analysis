from Datacoll_dataclean import a

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Airbnb Market Intelligence",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* ---------- Main Background ---------- */

    .stApp {
        background: #f8f7fb;
    }

    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #241638 0%,
            #3d245b 50%,
            #5b326f 100%
        );
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* ---------- Selectbox Fix ---------- */

    section[data-testid="stSidebar"] div[data-baseweb="select"] {
        color: #241638 !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: white !important;
        border-radius: 12px !important;
        color: #241638 !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #241638 !important;
    }

    div[data-baseweb="menu"] {
        background-color: white !important;
    }

    div[data-baseweb="menu"] * {
        color: #241638 !important;
    }

    div[data-baseweb="menu"] [role="option"]:hover {
        background-color: #f4edff !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
        fill: #241638 !important;
    }

    /* ---------- Hero Section ---------- */

    .hero {
        background: linear-gradient(
            135deg,
            #ff5a7a,
            #ff7b72,
            #9b5de5
        );

        padding: 42px 35px;
        border-radius: 25px;
        color: white;
        text-align: center;

        box-shadow:
            0px 10px 30px rgba(92, 55, 120, 0.18);

        margin-bottom: 28px;
    }

    .hero h1 {
        font-size: 45px;
        font-weight: 800;
        margin: 0;
    }

    .hero p {
        font-size: 18px;
        margin-top: 10px;
        opacity: 0.95;
    }


    /* ---------- Section Titles ---------- */

    .section-title {
        font-size: 28px;
        font-weight: 750;
        color: #30213f;
        margin-top: 15px;
        margin-bottom: 15px;
    }


    /* ---------- KPI Cards ---------- */

    .metric-card {
        background: white;
        padding: 23px 18px;
        border-radius: 20px;

        box-shadow:
            0px 5px 20px rgba(0,0,0,0.07);

        border: 1px solid #eee;

        min-height: 135px;
        text-align: center;
    }

    .metric-icon {
        font-size: 31px;
        margin-bottom: 4px;
    }

    .metric-title {
        font-size: 14px;
        color: #777;
        font-weight: 600;
    }

    .metric-value {
        font-size: 27px;
        font-weight: 800;
        color: #ff5a7a;
        margin-top: 4px;
    }


    /* ---------- Insight Cards ---------- */

    .insight-card {
        background: linear-gradient(
            135deg,
            #ffffff,
            #fff5f8
        );

        border-left: 5px solid #ff5a7a;

        padding: 20px;

        border-radius: 15px;

        margin-bottom: 12px;

        box-shadow:
            0px 4px 15px rgba(0,0,0,0.05);
    }

    .insight-card h4 {
        margin-top: 0;
        color: #3b264d;
    }


    /* ---------- Filter Card ---------- */

    .filter-card {
        background: white;
        padding: 22px;
        border-radius: 18px;

        box-shadow:
            0px 5px 18px rgba(0,0,0,0.06);

        margin-bottom: 20px;
    }


    /* ---------- Info Card ---------- */

    .info-card {
        background: linear-gradient(
            135deg,
            #f4edff,
            #fff0f4
        );

        padding: 25px;
        border-radius: 20px;

        margin: 20px 0;

        border: 1px solid #eee;
    }


    /* ---------- Footer ---------- */

    .footer {
        text-align: center;
        padding: 30px;
        color: #777;
        font-size: 13px;
    }


    /* ---------- Buttons ---------- */

    .stButton > button {
        border-radius: 12px;
        border: none;
        font-weight: 600;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATA PREPARATION
# =========================================================

df = a.copy()


# Price conversion

df["price"] = (
    df["price"]
    .astype(str)
    .str.replace(" dollars", "", regex=False)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["price"] = pd.to_numeric(
    df["price"],
    errors="coerce"
)


# Review date

df["last_review"] = pd.to_datetime(
    df["last_review"],
    errors="coerce"
)


# City extraction

df["city"] = (
    df["nbhood_full"]
    .fillna("")
    .astype(str)
    .str.split(",")
    .str[0]
    .str.strip()
)


# Neighborhood extraction

df["neighborhood"] = (
    df["nbhood_full"]
    .fillna("")
    .astype(str)
    .str.split(",", n=1)
    .str[1]
    .str.strip()
)


# Description length

df["description_length"] = (
    df["description"]
    .fillna("")
    .astype(str)
    .str.len()
)


# Review year

df["review_year"] = (
    df["last_review"].dt.year
)


# Review month

df["review_month"] = (
    df["last_review"].dt.month
)


# Remove invalid prices

df = df.dropna(
    subset=["price"]
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center;">
            <h1>🏠</h1>
            <h2>Airbnb Intelligence</h2>
            <p>Market Analytics Dashboard</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 🎛️ Dashboard Filters")

    sidebar_city = st.selectbox(
        "📍 City",
        ["All Cities"] +
        sorted(
            df["city"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    sidebar_room = st.selectbox(
        "🛏️ Room Type",
        ["All Room Types"] +
        sorted(
            df["room_type"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    max_available_price = int(
        df["price"].max()
    )

    sidebar_price = st.slider(
        "💰 Maximum Price",
        min_value=0,
        max_value=max_available_price,
        value=max_available_price
    )

    st.divider()

    st.markdown(
        """
        ### 📌 About this dashboard

        This application analyzes Airbnb listings,
        pricing patterns, room types, hosts,
        cities and neighborhoods.
        """
    )


# =========================================================
# APPLY GLOBAL FILTERS
# =========================================================

filtered_df = df.copy()


if sidebar_city != "All Cities":

    filtered_df = filtered_df[
        filtered_df["city"] == sidebar_city
    ]


if sidebar_room != "All Room Types":

    filtered_df = filtered_df[
        filtered_df["room_type"] == sidebar_room
    ]


filtered_df = filtered_df[
    filtered_df["price"] <= sidebar_price
]


# =========================================================
# HERO SECTION
# =========================================================

# =========================================================
# HERO SECTION
# =========================================================

st.title("🏠 Airbnb Market Intelligence")

st.write(
    "Discover Airbnb pricing, listings, room types, "
    "hosts and neighborhood trends"
)

st.divider()


# =========================================================
# NAVIGATION TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "🏠 Overview",
        "📍 Locations",
        "🔎 Listings",
        "📊 Statistics",
        "🧠 Insights",
        "📈 Visualizations"
    ]
)


# =========================================================
# TAB 1 - OVERVIEW
# =========================================================
# =========================================================
# TAB 1 - OVERVIEW
# =========================================================

with tab1:

    st.header("📊 Market Overview")

    # KPI CARDS

    col1, col2, col3, col4 = st.columns(4)

    total_listings = filtered_df[
        "listing_id"
    ].nunique()

    average_price = filtered_df[
        "price"
    ].mean()

    total_cities = filtered_df[
        "city"
    ].nunique()

    total_room_types = filtered_df[
        "room_type"
    ].nunique()


    with col1:

        st.metric(
            label="🏠 Total Listings",
            value=f"{total_listings:,}"
        )


    with col2:

        st.metric(
            label="💰 Average Price",
            value=f"${average_price:,.2f}"
        )


    with col3:

        st.metric(
            label="📍 Cities",
            value=f"{total_cities}"
        )


    with col4:

        st.metric(
            label="🛏️ Room Types",
            value=f"{total_room_types}"
        )


    st.write("")

    # -----------------------------------------------------
    # INTRODUCTION
    # -----------------------------------------------------

    st.subheader("✨ Explore the Airbnb Market")

    st.info(
        "Use the filters on the left to explore Airbnb listings "
        "based on city, room type and price. The dashboard provides "
        "insights into pricing, location, room-type distribution "
        "and host activity."
    )


    # -----------------------------------------------------
    # TWO CHARTS
    # -----------------------------------------------------

    chart_col1, chart_col2 = st.columns(2)


    # Listing by city

    with chart_col1:

        city_count = (
            filtered_df
            .groupby("city")["listing_id"]
            .count()
            .reset_index()
            .sort_values(
                "listing_id",
                ascending=False
            )
            .head(10)
        )

        fig = px.bar(
            city_count,
            x="city",
            y="listing_id",
            color="listing_id",
            color_continuous_scale="Plasma",
            title="🏙️ Top Cities by Listings"
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Average price room type

    with chart_col2:

        room_price = (
            filtered_df
            .groupby("room_type")["price"]
            .mean()
            .reset_index()
            .sort_values(
                "price",
                ascending=False
            )
        )

        fig = px.bar(
            room_price,
            x="room_type",
            y="price",
            color="room_type",
            title="💰 Average Price by Room Type"
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # -----------------------------------------------------
    # KEY MARKET INSIGHTS
    # -----------------------------------------------------

    st.header("💡 Key Market Insights")


    if len(filtered_df) > 0:

        top_city = (
            filtered_df["city"]
            .value_counts()
            .idxmax()
        )

        top_room = (
            filtered_df["room_type"]
            .value_counts()
            .idxmax()
        )

        expensive_room = (
            filtered_df
            .groupby("room_type")["price"]
            .mean()
            .idxmax()
        )

        expensive_city = (
            filtered_df
            .groupby("city")["price"]
            .mean()
            .idxmax()
        )


        insight1, insight2 = st.columns(2)


        with insight1:

            st.subheader("🏙️ Popular Location")

            st.info(
                f"{top_city} has the highest number of "
                "listings in the current selection."
            )


            st.subheader("🛏️ Most Common Room Type")

            st.success(
                f"{top_room} is the most frequently "
                "listed room type."
            )


        with insight2:

            st.subheader("💎 Highest-Priced Room Type")

            st.warning(
                f"{expensive_room} has the highest "
                "average listing price."
            )


            st.subheader("📍 Highest Average Price")

            st.info(
                f"{expensive_city} has the highest "
                "average price among available cities."
            )

    else:

        st.warning(
            "No listings match the selected filters."
        )
# =========================================================
# TAB 2 - LOCATION ANALYSIS
# =========================================================

with tab2:

    st.markdown(
        '<div class="section-title">📍 Location Intelligence</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Explore listing concentration and pricing patterns "
        "across cities and neighborhoods."
    )


    col1, col2 = st.columns(2)


    # Listings by city

    with col1:

        city_listing = (
            filtered_df
            .groupby("city")["listing_id"]
            .count()
            .reset_index()
            .sort_values(
                "listing_id",
                ascending=False
            )
            .head(10)
        )

        fig = px.bar(
            city_listing,
            x="listing_id",
            y="city",
            orientation="h",
            color="listing_id",
            color_continuous_scale="Turbo",
            title="🏙️ Top 10 Cities by Listings"
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Average price city

    with col2:

        city_average = (
            filtered_df
            .groupby("city")["price"]
            .mean()
            .reset_index()
            .sort_values(
                "price",
                ascending=False
            )
            .head(10)
        )

        fig = px.bar(
            city_average,
            x="price",
            y="city",
            orientation="h",
            color="price",
            color_continuous_scale="Plasma",
            title="💰 Top Cities by Average Price"
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Neighborhoods

    st.markdown(
        '<div class="section-title">🏘️ Neighborhood Analysis</div>',
        unsafe_allow_html=True
    )


    neighborhood_count = (
        filtered_df
        .groupby("neighborhood")["listing_id"]
        .count()
        .reset_index()
        .sort_values(
            "listing_id",
            ascending=False
        )
        .head(10)
    )


    fig = px.bar(
        neighborhood_count,
        x="listing_id",
        y="neighborhood",
        orientation="h",
        color="listing_id",
        color_continuous_scale="Viridis",
        title="Top 10 Neighborhoods by Number of Listings"
    )


    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        coloraxis_showscale=False
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# TAB 3 - LISTING EXPLORER
# =========================================================

with tab3:

    st.markdown(
        '<div class="section-title">🔎 Listing Explorer</div>',
        unsafe_allow_html=True
    )


    st.write(
        "Search and explore individual Airbnb listings."
    )


    col1, col2 = st.columns(2)


    with col1:

        explorer_city = st.selectbox(
            "📍 Select City",
            ["All"] +
            sorted(
                df["city"]
                .dropna()
                .unique()
                .tolist()
            ),
            key="explorer_city"
        )


    with col2:

        explorer_room = st.selectbox(
            "🛏️ Select Room Type",
            ["All"] +
            sorted(
                df["room_type"]
                .dropna()
                .unique()
                .tolist()
            ),
            key="explorer_room"
        )


    explorer_df = df.copy()


    if explorer_city != "All":

        explorer_df = explorer_df[
            explorer_df["city"] == explorer_city
        ]


    if explorer_room != "All":

        explorer_df = explorer_df[
            explorer_df["room_type"] == explorer_room
        ]


    # Price range

    if len(explorer_df) > 0:

        min_price = int(
            explorer_df["price"].min()
        )

        max_price = int(
            explorer_df["price"].max()
        )

        price_range = st.slider(
            "💰 Price Range",
            min_price,
            max_price,
            (min_price, max_price),
            key="explorer_price"
        )

        explorer_df = explorer_df[
            explorer_df["price"].between(
                price_range[0],
                price_range[1]
            )
        ]


    st.write(
        f"### 🏠 {len(explorer_df):,} listings found"
    )


    # Display table

    display_columns = [
        "listing_id",
        "price",
        "city",
        "neighborhood",
        "host_name",
        "room_type",
        "last_review"
    ]


    st.dataframe(
        explorer_df[
            display_columns
        ],
        use_container_width=True,
        hide_index=True
    )


    # Selected listing

    if len(explorer_df) > 0:

        st.markdown(
            '<div class="section-title">🏡 Listing Details</div>',
            unsafe_allow_html=True
        )


        selected_id = st.selectbox(
            "Select a listing",
            explorer_df[
                "listing_id"
            ].tolist()
        )


        listing = explorer_df[
            explorer_df["listing_id"] == selected_id
        ].iloc[0]


        detail1, detail2 = st.columns(2)


        with detail1:

            st.markdown(
                f"""
                <div class="info-card">

                <h3>🏠 Listing Information</h3>

                <p><b>Listing ID:</b>
                {listing["listing_id"]}</p>

                <p><b>Price:</b>
                ${listing["price"]:,.2f}</p>

                <p><b>Room Type:</b>
                {listing["room_type"]}</p>

                <p><b>City:</b>
                {listing["city"]}</p>

                <p><b>Neighborhood:</b>
                {listing["neighborhood"]}</p>

                <p><b>Host:</b>
                {listing["host_name"]}</p>

                </div>
                """,
                unsafe_allow_html=True
            )


        with detail2:

            st.markdown(
                f"""
                <div class="info-card">

                <h3>📝 Description</h3>

                <p>
                {listing["description"]}
                </p>

                <p>
                <b>Last Review:</b>
                {listing["last_review"]}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# TAB 4 - STATISTICS
# =========================================================

with tab4:

    st.markdown(
        '<div class="section-title">📊 Statistical Analysis</div>',
        unsafe_allow_html=True
    )


    # Descriptive statistics

    st.subheader("📋 Price Statistics")


    price_values = filtered_df[
        "price"
    ].dropna()


    if len(price_values) > 0:

        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)


        with stat_col1:

            st.metric(
                "Minimum Price",
                f"${price_values.min():,.2f}"
            )


        with stat_col2:

            st.metric(
                "Maximum Price",
                f"${price_values.max():,.2f}"
            )


        with stat_col3:

            st.metric(
                "Median Price",
                f"${price_values.median():,.2f}"
            )


        with stat_col4:

            st.metric(
                "Price Std. Dev.",
                f"${price_values.std():,.2f}"
            )


    # Price distribution

    st.subheader("📈 Price Distribution")


    fig = px.histogram(
        filtered_df,
        x="price",
        nbins=50,
        color_discrete_sequence=["#ff5a7a"],
        title="Distribution of Airbnb Listing Prices"
    )


    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # Correlation

    st.subheader("🔗 Correlation Analysis")


    correlation_df = filtered_df[
        [
            "price",
            "description_length"
        ]
    ].corr()


    fig = px.imshow(
        correlation_df,
        text_auto=True,
        color_continuous_scale="RdPu",
        title="Price and Description Length Correlation"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# TAB 5 - INSIGHTS
# =========================================================

with tab5:

    st.markdown(
        '<div class="section-title">🧠 Business Insights</div>',
        unsafe_allow_html=True
    )


    st.write(
        "Automatically generated observations from the Airbnb dataset."
    )


    if len(filtered_df) > 0:

        # Top city

        city_counts = (
            filtered_df["city"]
            .value_counts()
        )

        top_city = city_counts.index[0]

        top_city_count = city_counts.iloc[0]


        # Most common room

        room_counts = (
            filtered_df["room_type"]
            .value_counts()
        )

        top_room = room_counts.index[0]

        top_room_count = room_counts.iloc[0]


        # Highest price city

        city_prices = (
            filtered_df
            .groupby("city")["price"]
            .mean()
            .sort_values(
                ascending=False
            )
        )

        highest_price_city = (
            city_prices.index[0]
        )

        highest_price_value = (
            city_prices.iloc[0]
        )


        # Highest price room

        room_prices = (
            filtered_df
            .groupby("room_type")["price"]
            .mean()
            .sort_values(
                ascending=False
            )
        )

        highest_price_room = (
            room_prices.index[0]
        )

        highest_room_price = (
            room_prices.iloc[0]
        )


        # Most active host

        host_counts = (
            filtered_df["host_name"]
            .value_counts()
        )

        top_host = host_counts.index[0]

        top_host_count = host_counts.iloc[0]


        # Review percentage

        reviewed = (
            filtered_df["last_review"]
            .notna()
            .sum()
        )

        total = len(filtered_df)

        review_percentage = (
            reviewed / total * 100
        )


        # Insight cards

        c1, c2 = st.columns(2)


        with c1:

            st.markdown(
                f"""
                <div class="insight-card">

                <h4>🏙️ Listing Concentration</h4>

                <p>
                <b>{top_city}</b> contains
                <b>{top_city_count:,}</b> listings,
                making it the most represented city
                in the selected data.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                f"""
                <div class="insight-card">

                <h4>🛏️ Room Type Preference</h4>

                <p>
                <b>{top_room}</b> is the most common
                room type with
                <b>{top_room_count:,}</b> listings.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                f"""
                <div class="insight-card">

                <h4>👤 Active Host</h4>

                <p>
                <b>{top_host}</b> has
                <b>{top_host_count:,}</b> listings
                in the selected dataset.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        with c2:

            st.markdown(
                f"""
                <div class="insight-card">

                <h4>💰 Highest-Priced City</h4>

                <p>
                <b>{highest_price_city}</b> has the highest
                average price of
                <b>${highest_price_value:,.2f}</b>.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                f"""
                <div class="insight-card">

                <h4>💎 Premium Room Type</h4>

                <p>
                <b>{highest_price_room}</b> has the highest
                average price at
                <b>${highest_room_price:,.2f}</b>.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                f"""
                <div class="insight-card">

                <h4>⭐ Review Coverage</h4>

                <p>
                Approximately
                <b>{review_percentage:.1f}%</b>
                of the selected listings have a recorded
                last review date.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# TAB 6 - VISUALIZATIONS
# =========================================================

with tab6:

    st.markdown(
        '<div class="section-title">📈 Interactive Visualizations</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # ROOM TYPE DISTRIBUTION
    # -----------------------------------------------------

    st.subheader("🛏️ Room Type Distribution")


    room_distribution = (
        filtered_df["room_type"]
        .value_counts()
        .reset_index()
    )


    room_distribution.columns = [
        "room_type",
        "count"
    ]


    fig = px.pie(
        room_distribution,
        values="count",
        names="room_type",
        hole=0.48,
        title="Airbnb Listings by Room Type"
    )


    fig.update_layout(
        paper_bgcolor="white"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -----------------------------------------------------
    # PRICE TREND
    # -----------------------------------------------------

    st.subheader("📅 Average Price Trend by Month")


    trend_df = filtered_df.dropna(
        subset=["last_review"]
    ).copy()

    trend_df["month"] = trend_df[
        "last_review"
    ].dt.month

    monthly_price = (
        trend_df
        .groupby("month")["price"]
        .mean()
        .reset_index()
    )


    monthly_price.columns = [
        "month",
        "average_price"
    ]


    month_names = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }


    monthly_price["month_name"] = (
        monthly_price["month"]
        .map(month_names)
    )


    fig = px.line(
        monthly_price,
        x="month_name",
        y="average_price",
        markers=True,
        title="Average Airbnb Price by Review Month",
        color_discrete_sequence=["#9b5de5"]
    )


    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -----------------------------------------------------
    # TOP HOSTS
    # -----------------------------------------------------

    st.subheader("👤 Top Hosts")


    top_hosts = (
        filtered_df
        .groupby("host_name")["listing_id"]
        .count()
        .reset_index()
        .sort_values(
            "listing_id",
            ascending=False
        )
        .head(10)
    )


    fig = px.bar(
        top_hosts,
        x="host_name",
        y="listing_id",
        color="listing_id",
        color_continuous_scale="Plasma",
        title="Top 10 Hosts by Number of Listings"
    )


    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        coloraxis_showscale=False
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -----------------------------------------------------
    # PRICE BY ROOM TYPE
    # -----------------------------------------------------

    st.subheader("💰 Price Comparison by Room Type")


    room_price_chart = (
        filtered_df
        .groupby("room_type")["price"]
        .mean()
        .reset_index()
        .sort_values(
            "price",
            ascending=False
        )
    )


    fig = px.bar(
        room_price_chart,
        x="room_type",
        y="price",
        color="room_type",
        title="Average Price by Room Type"
    )


    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -----------------------------------------------------
    # PRICE VS DESCRIPTION LENGTH
    # -----------------------------------------------------

    st.subheader("📝 Description Length vs Price")


    scatter_df = filtered_df[
        [
            "description_length",
            "price",
            "room_type"
        ]
    ].dropna()


    # Limit points only for browser performance
    # while preserving the overall dataset
    if len(scatter_df) > 5000:

        scatter_df = scatter_df.sample(
            5000,
            random_state=42
        )


    fig = px.scatter(
        scatter_df,
        x="description_length",
        y="price",
        color="room_type",
        opacity=0.65,
        title="Relationship Between Description Length and Price",
        labels={
            "description_length":
                "Description Length (characters)",
            "price":
                "Price"
        }
    )


    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

    🏠 <b>Airbnb Market Intelligence</b>

    <br>

    Built with Python • Pandas • Plotly • Streamlit

    <br>

    Interactive analytics for Airbnb market exploration

    </div>
    """,
    unsafe_allow_html=True
)
