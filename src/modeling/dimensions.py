import pandas as pd


def create_restaurant_dimension(df: pd.DataFrame):

    restaurant_df = df[
        ["Restaurant ID", "Restaurant name"]
    ].drop_duplicates(
        subset=["Restaurant ID"]
    )

    restaurant_df = restaurant_df.rename(
        columns={
            "Restaurant ID": "restaurant_id",
            "Restaurant name": "restaurant_name"
        }
    )

    return restaurant_df


def create_customer_dimension(df: pd.DataFrame):

    customer_df = df[
        ["Customer ID"]
    ].drop_duplicates()

    customer_df = customer_df.rename(
        columns={
            "Customer ID": "customer_id"
        }
    )

    return customer_df


def create_location_dimension(df: pd.DataFrame):

    location_df = df[
        ["City", "Subzone"]
    ].drop_duplicates()

    location_df = location_df.rename(
        columns={
            "City": "city",
            "Subzone": "subzone"
        }
    )

    return location_df


def create_date_dimension(df: pd.DataFrame):

    date_df = df[
        ["Order Placed At"]
    ].copy()

    date_df["date"] = date_df["Order Placed At"].dt.date

    date_df = date_df[
        ["date"]
    ].drop_duplicates()

    date_df["day"] = pd.to_datetime(
        date_df["date"]
    ).dt.day

    date_df["month"] = pd.to_datetime(
        date_df["date"]
    ).dt.month

    date_df["year"] = pd.to_datetime(
        date_df["date"]
    ).dt.year

    date_df["date_id"] = (
        date_df["year"] * 10000
        + date_df["month"] * 100
        + date_df["day"]
    )

    return date_df[
        ["date_id", "date", "day", "month", "year"]
    ]