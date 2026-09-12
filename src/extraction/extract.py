import pandas as pd
from src.utils.logger import logger

def extract_data():
    try:
        logger.info("Starting data extraction")

        df = pd.read_csv(
            "data/raw/order_history_kaggle_data.csv"
        )

        logger.info(
            f"Data extraction completed: {len(df)} rows extracted"
        )

        return df

    except Exception as e:
        logger.error(f"{e} occurred while extracting csv")
        raise