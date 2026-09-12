import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from src.utils.logger import logger
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)

def add_dimension_ids(fact_df):

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT location_id, city, subzone FROM dim_location")
        )

        location_data = result.fetchall()

    location_df = pd.DataFrame(
        location_data,
        columns=["location_id", "city", "subzone"]
    )

    fact_df = fact_df.merge(
        location_df,
        on=["city", "subzone"],
        how="left"
    )

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT date_id, date FROM dim_date")
        )

        date_data = result.fetchall()

    date_df = pd.DataFrame(
        date_data,
        columns=["date_id", "date"]
    )

    fact_df = fact_df.merge(
        date_df,
        on="date",
        how="left"
    )

    return fact_df

def validate_fact_data(fact_df):

    if fact_df.empty:
        raise ValueError("Fact table is empty")

    if fact_df["order_id"].duplicated().any():
        raise ValueError("Duplicate order_id found")

    if fact_df["location_id"].isna().any():
        raise ValueError("Missing location_id found")

    if fact_df["date_id"].isna().any():
        raise ValueError("Missing date_id found")

    logger.info(
        f"Fact table validation passed: {len(fact_df)} rows"
    )

def create_fact_table(df: pd.DataFrame):
    fact_df = df[
        [
            "Order ID",
            "Restaurant ID",
            "Customer ID",
            "City",
            "Subzone",
            "Order Placed At",
            "Order Status",
            "Total",
            "Bill subtotal",
            "Packaging charges",
            "distance_km",
            "Rating",
            "KPT duration (minutes)",
            "Rider wait time (minutes)",
            "item_count",
            "total_item_quantity",
            "is_delivered"
        ]
    ].copy()

    fact_df = fact_df.rename(
        columns={
            "Order ID": "order_id",
            "Restaurant ID": "restaurant_id",
            "Customer ID": "customer_id",
            "Order Placed At": "order_placed_at",
            "Order Status": "order_status",
            "Total": "total",
            "City" : "city" , 
            "Subzone" : "subzone" , 
            "Bill subtotal": "bill_subtotal",
            "Packaging charges": "packaging_charges",
            "Rating": "rating",
            "KPT duration (minutes)": "kpt_duration",
            "Rider wait time (minutes)": "rider_wait_time"
        }
    )

    fact_df["date"] = fact_df["order_placed_at"].dt.date

    fact_df = add_dimension_ids(fact_df)

    fact_df = fact_df[
        [
            "order_id",
            "restaurant_id",
            "customer_id",
            "location_id",
            "date_id",
            "order_status",
            "order_placed_at",
            "total",
            "bill_subtotal",
            "packaging_charges",
            "distance_km",
            "rating",
            "kpt_duration",
            "rider_wait_time",
            "item_count",
            "total_item_quantity",
            "is_delivered"
        ]
    ]

    validate_fact_data(fact_df=fact_df)
    
    return fact_df