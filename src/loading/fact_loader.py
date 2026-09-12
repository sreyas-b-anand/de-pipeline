from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from src.utils.logger import logger
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)

def load_fact_table(fact_df):

    try:
        logger.info("Starting fact table loading")

        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT order_id FROM fact_orders")
            )

            existing_ids = set(result.scalars().all())

        new_orders = fact_df[
            ~fact_df["order_id"].isin(existing_ids)
        ]

        if len(new_orders) > 0:
            new_orders.to_sql(
                "fact_orders",
                engine,
                if_exists="append",
                index=False
            )

        logger.info(
            f"New orders loaded: {len(new_orders)}"
        )

    except Exception as e:
        logger.error(f"{e} occurred while loading fact table")
        raise