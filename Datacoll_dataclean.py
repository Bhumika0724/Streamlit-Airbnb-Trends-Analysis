import pandas as pd
import numpy as np


def data_collection():

    path = r"C:\Users\admin\Desktop\Airbnb_Market_Intelligence\data\merged_airbnb_data.csv"

    df1 = pd.read_csv(path)

    return df1


def data_cleaning(df1):

    # Clean price column
    df1["price"] = (
        df1["price"]
        .astype(str)
        .str.replace(" dollars", "", regex=False)
    )

    df1["price"] = pd.to_numeric(df1["price"], errors="coerce")

    # Convert last_review to datetime
    df1["last_review"] = pd.to_datetime(
        df1["last_review"],
        errors="coerce"
    )

    # Extract city from neighborhood
    df1["city"] = df1["nbhood_full"].str.split(",").str[0].str.strip()

    # Extract neighborhood
    df1["neighborhood"] = (
        df1["nbhood_full"]
        .str.split(",", n=1)
        .str[1]
        .str.strip()
    )

    # Remove duplicate listings
    df1 = df1.drop_duplicates(subset="listing_id")

    return df1


# Load data
a = data_collection()

# Clean data
a = data_cleaning(a)
