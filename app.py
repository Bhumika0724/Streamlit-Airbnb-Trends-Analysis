import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import scipy.stats as stats


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
# DATA COLLECTION
# =========================================================

def data_collection():

    # Relative path for deployment
    path = "data/merged_airbnb_data.csv"

    df1 = pd.read_csv(path)

    return df1


# =========================================================
# DATA CLEANING
# =========================================================

def data_cleaning(df1):

    # Clean price column
    df1["price"] = (
        df1["price"]
        .astype(str)
        .str.replace(" dollars", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
    )

    df1["price"] = pd.to_numeric(
        df1["price"],
        errors="coerce"
    )

    # Convert last_review to datetime
    df1["last_review"] = pd.to_datetime(
        df1["last_review"],
        errors="coerce"
    )

    # Extract city
    df1["city"] = (
        df1["nbhood_full"]
        .fillna("")
        .astype(str)
        .str.split(",")
        .str[0]
        .str.strip()
    )

    # Extract neighborhood
    df1["neighborhood"] = (
        df1["nbhood_full"]
        .fillna("")
        .astype(str)
        .str.split(",", n=1)
        .str[1]
        .str.strip()
    )

    # Description length
    df1["description_length"] = (
        df1["description"]
        .fillna("")
        .astype(str)
        .str.len()
    )

    # Review year
    df1["review_year"] = (
        df1["last_review"].dt.year
    )

    # Review month
    df1["review_month"] = (
        df1["last_review"].dt.month
    )

    # Remove duplicate listings
    df1 = df1.drop_duplicates(
        subset="listing_id"
    )

    # Remove invalid prices
    df1 = df1.dropna(
        subset=["price"]
    )

    return df1


# =========================================================
# KRUSKAL-WALLIS TEST
# =========================================================

def kruskal_test(data, category_column):

    groups = []

    for category in data[category_column].dropna().unique():

        values = data[
            data[category_column] == category
        ]["price"].dropna()

        if len(values) >= 2:
            groups.append(values)

    if len(groups) < 2:
        return np.nan

    statistic, p_value = stats.kruskal(*groups)

    return p_value


# =========================================================
# LOAD DATA
# =========================================================

try:

    df = data_collection()
    df = data_cleaning(df)

except Exception as e:

    st.error(
        "Unable to load the Airbnb dataset."
    )

    st.write(
        "Please make sure the file exists at:"
    )

    st.code(
        "data/merged_airbnb_data.csv"
    )

    st.stop()


# =========================================================
# ADDITIONAL STATISTICAL DATA
# =========================================================

df["description_length_category"] = pd.cut(
    df["description_length"],
    bins=[-1, 100, 300, 600, np.inf],
    labels=[
        "Short",
        "Medium",
        "Long",
        "Very Long"
    ]
)

df["room_city"] = (
    df["room_type"].astype(str)
    + " - "
    + df["city"].astype(str)
)

df["review_status"] = np.where(
    df["last_review"].isna(),
    "No Review",
    "Has Review"
)

df["price_category"] = pd.cut(
    df["price"],
    bins=[-1, 50, 100, 200, 500, np.inf],
    labels=[
        "Under $50",
        "$50-$100",
        "$100-$200",
        "$200-$500",
        "Above $500"
    ]
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #f8f7fb;
    }

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

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] > div {

        background-color: white !important;
        border-radius: 12px !important;
    }

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] * {

        color: #241638 !important;
    }

    div[data-baseweb="menu"] {
        background-color: white !important;
    }

    div[data-baseweb="menu"] * {
        color: #241638 !important;
    }

    div[data-baseweb="menu"]
    [role="option"]:hover {

        background-color: #f4edff !important;
    }

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] svg {

        fill: #241638 !important;
    }

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

    .footer {

        text-align: center;
        padding: 30px;
        color: #777;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True
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

    st.markdown(
        "### 🎛️ Dashboard Filters"
    )

    sidebar_city = st.selectbox(
        "📍 City",
        ["All Cities"]
        + sorted(
            df["city"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    sidebar_room = st.selectbox(
        "🛏️ Room Type",
        ["All Room Types"]
        + sorted(
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
# MAIN TITLE
# =========================================================

st.title(
    "🏠 Airbnb Market Intelligence"
)

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

with tab1:

    st.header(
        "📊 Market Overview"
    )

    col1, col2, col3, col4 = st.columns(4)

    total_listings = (
        filtered_df["listing_id"]
        .nunique()
    )

    average_price = (
        filtered_df["price"].mean()
        if len(filtered_df) > 0
        else 0
    )

    total_cities = (
        filtered_df["city"].nunique()
    )

    total_room_types = (
        filtered_df["room_type"].nunique()
    )

    with col1:

        st.metric(
            "🏠 Total Listings",
            f"{total_listings:,}"
        )

    with col2:

        st.metric(
            "💰 Average Price",
            f"${average_price:,.2f}"
        )

    with col3:

        st.metric(
            "📍 Cities",
            f"{total_cities}"
        )

    with col4:

        st.metric(
            "🛏️ Room Types",
            f"{total_room_types}"
        )

    st.subheader(
        "✨ Explore the Airbnb Market"
    )

    st.info(
        "Use the filters on the left to explore Airbnb "
        "listings based on city, room type and price. "
        "The dashboard provides insights into pricing, "
        "location, room-type distribution and host activity."
    )

    chart_col1, chart_col2 = st.columns(2)

    # Listings by city

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

    # Average price by room type

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

    st.header(
        "💡 Key Market Insights"
    )

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

            st.subheader(
                "🏙️ Popular Location"
            )

            st.info(
                f"{top_city} has the highest number "
                "of listings in the current selection."
            )

            st.subheader(
                "🛏️ Most Common Room Type"
            )

            st.success(
                f"{top_room} is the most frequently "
                "listed room type."
            )

        with insight2:

            st.subheader(
                "💎 Highest-Priced Room Type"
            )

            st.warning(
                f"{expensive_room} has the highest "
                "average listing price."
            )

            st.subheader(
                "📍 Highest Average Price"
            )

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

    st.header(
        "📍 Location Intelligence"
    )

    st.write(
        "Explore listing concentration and pricing "
        "patterns across cities and neighborhoods."
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

    st.header(
        "🏘️ Neighborhood Analysis"
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

    st.header(
        "🔎 Listing Explorer"
    )

    st.write(
        "Search and explore individual Airbnb listings."
    )

    col1, col2 = st.columns(2)

    with col1:

        explorer_city = st.selectbox(
            "📍 Select City",
            ["All"]
            + sorted(
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
            ["All"]
            + sorted(
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

    if len(explorer_df) > 0:

        min_price = int(
            explorer_df["price"].min()
        )

        max_price = int(
            explorer_df["price"].max()
        )

        if min_price < max_price:

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

        else:

            st.info(
                f"All available listings have a price of "
                f"${min_price:,.2f}."
            )

    st.write(
        f"### 🏠 {len(explorer_df):,} listings found"
    )

    display_columns = [
        "listing_id",
        "price",
        "city",
        "neighborhood",
        "host_name",
        "room_type",
        "last_review"
    ]

    available_columns = [
        col for col in display_columns
        if col in explorer_df.columns
    ]

    st.dataframe(
        explorer_df[available_columns],
        use_container_width=True,
        hide_index=True
    )

    if len(explorer_df) > 0:

        st.header(
            "🏡 Listing Details"
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

            st.subheader(
                "🏠 Listing Information"
            )

            st.write(
                f"**Listing ID:** {listing['listing_id']}"
            )

            st.write(
                f"**Price:** ${listing['price']:,.2f}"
            )

            st.write(
                f"**Room Type:** {listing['room_type']}"
            )

            st.write(
                f"**City:** {listing['city']}"
            )

            st.write(
                f"**Neighborhood:** "
                f"{listing['neighborhood']}"
            )

            st.write(
                f"**Host:** {listing['host_name']}"
            )

        with detail2:

            st.subheader(
                "📝 Description"
            )

            description = listing["description"]

            if pd.isna(description):

                description = "No description available."

            st.write(
                description
            )

            st.write(
                f"**Last Review:** "
                f"{listing['last_review']}"
            )


# =========================================================
# TAB 4 - STATISTICAL ANALYSIS
# =========================================================

with tab4:

    st.header(
        "📊 Statistical Analysis"
    )

    st.subheader(
        "📋 Price Statistics"
    )

    price_values = (
        filtered_df["price"].dropna()
    )

    if len(price_values) > 0:

        stat_col1, stat_col2, stat_col3, stat_col4 = (
            st.columns(4)
        )

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

    st.subheader(
        "📈 Price Distribution"
    )

    if len(filtered_df) > 0:

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

    st.subheader(
        "🔗 Correlation Analysis"
    )

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

    # -----------------------------------------------------
    # KRUSKAL-WALLIS TESTS
    # -----------------------------------------------------

    st.subheader(
        "🧪 Kruskal-Wallis Statistical Tests"
    )

    analysis_df = filtered_df.copy()

    if len(analysis_df) > 0:

        # Room Type vs Price

        p_room = kruskal_test(
            analysis_df,
            "room_type"
        )

        # City vs Price

        p_city = kruskal_test(
            analysis_df,
            "city"
        )

        # Neighborhood vs Price

        neighborhood_counts = (
            analysis_df["neighborhood"]
            .value_counts()
        )

        valid_neighborhoods = (
            neighborhood_counts[
                neighborhood_counts >= 5
            ].index
        )

        df_neighborhood = analysis_df[
            analysis_df["neighborhood"]
            .isin(valid_neighborhoods)
        ]

        p_neighborhood = kruskal_test(
            df_neighborhood,
            "neighborhood"
        )

        # Host vs Price

        host_counts = (
            analysis_df["host_name"]
            .value_counts()
        )

        valid_hosts = (
            host_counts[
                host_counts >= 5
            ].index
        )

        df_host = analysis_df[
            analysis_df["host_name"]
            .isin(valid_hosts)
        ]

        p_host = kruskal_test(
            df_host,
            "host_name"
        )

        # Review Year vs Price

        df_year = analysis_df.dropna(
            subset=["review_year"]
        )

        p_year = kruskal_test(
            df_year,
            "review_year"
        )

        # Review Month vs Price

        df_month = analysis_df.dropna(
            subset=["review_month"]
        )

        p_month = kruskal_test(
            df_month,
            "review_month"
        )

        # Description Length vs Price

        p_description = kruskal_test(
            analysis_df,
            "description_length_category"
        )

        # Room Type + City vs Price

        room_city_counts = (
            analysis_df["room_city"]
            .value_counts()
        )

        valid_room_city = (
            room_city_counts[
                room_city_counts >= 5
            ].index
        )

        df_room_city = analysis_df[
            analysis_df["room_city"]
            .isin(valid_room_city)
        ]

        p_room_city = kruskal_test(
            df_room_city,
            "room_city"
        )

        # Review Availability vs Price

        p_review_status = kruskal_test(
            analysis_df,
            "review_status"
        )

        # Price Category

        price_room = analysis_df.dropna(
            subset=[
                "price_category",
                "room_type"
            ]
        )

        p_price_category = kruskal_test(
            price_room,
            "price_category"
        )

        test_results = pd.DataFrame(
            {
                "Analysis": [
                    "Room Type vs Price",
                    "City vs Price",
                    "Neighborhood vs Price",
                    "Host vs Price",
                    "Review Year vs Price",
                    "Review Month vs Price",
                    "Description Length vs Price",
                    "Room Type + City vs Price",
                    "Review Availability vs Price",
                    "Price Category vs Price"
                ],
                "P-Value": [
                    p_room,
                    p_city,
                    p_neighborhood,
                    p_host,
                    p_year,
                    p_month,
                    p_description,
                    p_room_city,
                    p_review_status,
                    p_price_category
                ]
            }
        )

        st.dataframe(
            test_results,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "A p-value below 0.05 indicates a statistically "
            "significant difference between groups."
        )


# =========================================================
# TAB 5 - BUSINESS INSIGHTS
# =========================================================

with tab5:

    st.header(
        "🧠 Business Insights"
    )

    st.write(
        "Automatically generated observations from "
        "the Airbnb dataset."
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

        c1, c2 = st.columns(2)

        with c1:

            st.subheader(
                "🏙️ Listing Concentration"
            )

            st.info(
                f"{top_city} contains "
                f"{top_city_count:,} listings, "
                "making it the most represented city "
                "in the selected data."
            )

            st.subheader(
                "🛏️ Room Type Preference"
            )

            st.success(
                f"{top_room} is the most common "
                f"room type with "
                f"{top_room_count:,} listings."
            )

            st.subheader(
                "👤 Active Host"
            )

            st.info(
                f"{top_host} has "
                f"{top_host_count:,} listings "
                "in the selected dataset."
            )

        with c2:

            st.subheader(
                "💰 Highest-Priced City"
            )

            st.warning(
                f"{highest_price_city} has the highest "
                f"average price of "
                f"${highest_price_value:,.2f}."
            )

            st.subheader(
                "💎 Premium Room Type"
            )

            st.warning(
                f"{highest_price_room} has the highest "
                f"average price at "
                f"${highest_room_price:,.2f}."
            )

            st.subheader(
                "⭐ Review Coverage"
            )

            st.info(
                f"Approximately "
                f"{review_percentage:.1f}% "
                "of the selected listings have a "
                "recorded last review date."
            )

    else:

        st.warning(
            "No listings match the selected filters."
        )


# =========================================================
# TAB 6 - VISUALIZATIONS
# =========================================================

with tab6:

    st.header(
        "📈 Interactive Visualizations"
    )

    # Room Type Distribution

    st.subheader(
        "🛏️ Room Type Distribution"
    )

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

    # Average Price Trend

    st.subheader(
        "📅 Average Price Trend by Month"
    )

    trend_df = filtered_df.dropna(
        subset=["last_review"]
    ).copy()

    trend_df["month"] = (
        trend_df["last_review"].dt.month
    )

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

    if len(monthly_price) > 0:

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

    else:

        st.info(
            "There is not enough review-date data "
            "to display the monthly trend."
        )

    # Top Hosts

    st.subheader(
        "👤 Top Hosts"
    )

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

    # Price by Room Type

    st.subheader(
        "💰 Price Comparison by Room Type"
    )

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

    # Description Length vs Price

    st.subheader(
        "📝 Description Length vs Price"
    )

    scatter_df = filtered_df[
        [
            "description_length",
            "price",
            "room_type"
        ]
    ].dropna()

    if len(scatter_df) > 5000:

        scatter_df = scatter_df.sample(
            5000,
            random_state=42
        )

    if len(scatter_df) > 0:

        fig = px.scatter(
            scatter_df,
            x="description_length",
            y="price",
            color="room_type",
            opacity=0.65,
            title=(
                "Relationship Between Description "
                "Length and Price"
            ),
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

    else:

        st.info(
            "Not enough data available for the scatter plot."
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
