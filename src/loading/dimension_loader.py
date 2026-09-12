from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from src.utils.logger import logger
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)


def load_restaurant_dimension(restaurant_df):

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT restaurant_id FROM dim_restaurant")
        )

        existing_ids = set(result.scalars().all())

    new_restaurants = restaurant_df[
        ~restaurant_df["restaurant_id"].isin(existing_ids)
    ]

    if len(new_restaurants) > 0:
        new_restaurants.to_sql(
            "dim_restaurant",
            engine,
            if_exists="append",
            index=False
        )

    logger.info(
        f"New restaurants loaded: {len(new_restaurants)}"
    )


def load_customer_dimension(customer_df):

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT customer_id FROM dim_customer")
        )

        existing_ids = set(result.scalars().all())

    new_customers = customer_df[
        ~customer_df["customer_id"].isin(existing_ids)
    ]

    if len(new_customers) > 0:
        new_customers.to_sql(
            "dim_customer",
            engine,
            if_exists="append",
            index=False
        )

    logger.info(
        f"New customers loaded: {len(new_customers)}"
    )


def load_location_dimension(location_df):

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT city, subzone FROM dim_location")
        )

        existing_locations = set(result.fetchall())

    new_locations = location_df[
        ~location_df.apply(
            lambda row: (row["city"], row["subzone"]) in existing_locations,
            axis=1
        )
    ]

    if len(new_locations) > 0:
        new_locations.to_sql(
            "dim_location",
            engine,
            if_exists="append",
            index=False
        )

    logger.info(
        f"New locations loaded: {len(new_locations)}"
    )


def load_date_dimension(date_df):

    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT date_id FROM dim_date")
            )

            existing_ids = set(result.scalars().all())

        new_dates = date_df[
            ~date_df["date_id"].isin(existing_ids)
        ]

        if len(new_dates) > 0:
            new_dates.to_sql(
                "dim_date",
                engine,
                if_exists="append",
                index=False
            )

        logger.info(
            f"New dates loaded: {len(new_dates)}"
        )

    except Exception as e:
        logger.error(f"{e} occurred while loading ...")
        raise