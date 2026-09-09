from Datacoll_dataclean import a
import scipy.stats as stats
import pandas as pd
import numpy as np


# --------------------------------------------------
# Prepare the data
# --------------------------------------------------

df1 = a.copy()

# Make sure price is numeric
df1["price"] = (
    df1["price"]
    .astype(str)
    .str.replace(" dollars", "", regex=False)
)

df1["price"] = pd.to_numeric(df1["price"], errors="coerce")

# Convert review date
df1["last_review"] = pd.to_datetime(
    df1["last_review"],
    errors="coerce"
)

# Extract city
df1["city"] = (
    df1["nbhood_full"]
    .str.split(",")
    .str[0]
    .str.strip()
)

# Extract neighborhood
df1["neighborhood"] = (
    df1["nbhood_full"]
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
df1["review_year"] = df1["last_review"].dt.year

# Review month
df1["review_month"] = df1["last_review"].dt.month


# --------------------------------------------------
# Function for Kruskal-Wallis test
# --------------------------------------------------

def kruskal_test(data, category_column):

    groups = []

    for category in data[category_column].dropna().unique():

        values = data[
            data[category_column] == category
        ]["price"].dropna()

        # Need at least 2 values in a group
        if len(values) >= 2:
            groups.append(values)

    # Need at least 2 groups
    if len(groups) < 2:
        return np.nan

    statistic, p_value = stats.kruskal(*groups)

    return p_value


# --------------------------------------------------
# 1. Room Type vs Price
# --------------------------------------------------

p = kruskal_test(
    df1,
    "room_type"
)


# --------------------------------------------------
# 2. City vs Price
# --------------------------------------------------

p1 = kruskal_test(
    df1,
    "city"
)


# --------------------------------------------------
# 3. Neighborhood vs Price
# --------------------------------------------------

# Use only neighborhoods having enough listings
neighborhood_counts = (
    df1["neighborhood"]
    .value_counts()
)

valid_neighborhoods = neighborhood_counts[
    neighborhood_counts >= 5
].index

df_neighborhood = df1[
    df1["neighborhood"].isin(valid_neighborhoods)
]

p2 = kruskal_test(
    df_neighborhood,
    "neighborhood"
)


# --------------------------------------------------
# 4. Host vs Price
# --------------------------------------------------

# Use hosts with at least 5 listings
host_counts = (
    df1["host_name"]
    .value_counts()
)

valid_hosts = host_counts[
    host_counts >= 5
].index

df_host = df1[
    df1["host_name"].isin(valid_hosts)
]

p3 = kruskal_test(
    df_host,
    "host_name"
)


# --------------------------------------------------
# 5. Review Year vs Price
# --------------------------------------------------

df_year = df1.dropna(
    subset=["review_year"]
)

p4 = kruskal_test(
    df_year,
    "review_year"
)


# --------------------------------------------------
# 6. Review Month vs Price
# --------------------------------------------------

df_month = df1.dropna(
    subset=["review_month"]
)

p5 = kruskal_test(
    df_month,
    "review_month"
)


# --------------------------------------------------
# 7. Description Length Category vs Price
# --------------------------------------------------

df1["description_length_category"] = pd.cut(
    df1["description_length"],
    bins=[-1, 100, 300, 600, np.inf],
    labels=[
        "Short",
        "Medium",
        "Long",
        "Very Long"
    ]
)

p6 = kruskal_test(
    df1,
    "description_length_category"
)


# --------------------------------------------------
# 8. Room Type + City vs Price
# --------------------------------------------------

df1["room_city"] = (
    df1["room_type"].astype(str)
    + " - "
    + df1["city"].astype(str)
)

# Only use combinations with at least 5 listings
room_city_counts = (
    df1["room_city"].value_counts()
)

valid_room_city = room_city_counts[
    room_city_counts >= 5
].index

df_room_city = df1[
    df1["room_city"].isin(valid_room_city)
]

p7 = kruskal_test(
    df_room_city,
    "room_city"
)


# --------------------------------------------------
# 9. Review Availability vs Price
# --------------------------------------------------

df1["review_status"] = np.where(
    df1["last_review"].isna(),
    "No Review",
    "Has Review"
)

p8 = kruskal_test(
    df1,
    "review_status"
)


# --------------------------------------------------
# 10. Price Category vs Room Type
# --------------------------------------------------

# Create price categories
df1["price_category"] = pd.cut(
    df1["price"],
    bins=[-1, 50, 100, 200, 500, np.inf],
    labels=[
        "Under $50",
        "$50-$100",
        "$100-$200",
        "$200-$500",
        "Above $500"
    ]
)

# Compare room types across price categories
price_room = (
    df1.dropna(
        subset=["price_category", "room_type"]
    )
)

p9 = kruskal_test(
    price_room,
    "price_category"
)


# --------------------------------------------------
# 11. Create final output
# --------------------------------------------------

p10 = p9
