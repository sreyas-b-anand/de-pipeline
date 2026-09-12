import pandas as pd

from src.utils.logger import logger


def transform_discount(x):
    if str(x).startswith("Buy 1"):
        return "buy_1_get_1"
    elif "%" in str(x):
        return "percentage"
    elif "Flat" in str(x):
        return "flat"
    else:
        return "none"


def extract_discount_percent(x):
    if "%" in str(x):
        return float(str(x).split("%")[0].split()[-1])
    return None


def extract_discount_cap(x):
    x = str(x)

    if "upto Rs." in x:
        return float(x.split("upto Rs.")[1])
    elif "Flat Rs." in x:
        return float(x.split("Flat Rs.")[1].split(" ")[0])

    return None


def calculate_total_quantity(x):
    items = str(x).split(",")
    total = 0

    for item in items:
        quantity = int(item.strip().split(" x ")[0])
        total += quantity

    return total


def validate_data(df: pd.DataFrame):

    logger.info("Starting data validation")

    if len(df) == 0:
        raise ValueError("DataFrame contains no rows")

    logger.info(f"Row count validation passed: {len(df)} rows")

    if df["Order ID"].duplicated().any():
        raise ValueError("Duplicate Order IDs found")

    logger.info("Duplicate Order ID validation passed")

    required_columns = [
        "Order ID",
        "Order Status",
        "Order Placed At",
        "distance_km",
        "total_item_quantity"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    logger.info("Required column validation passed")

    if (df["distance_km"] < 0).any():
        raise ValueError("Negative distance found")
    
    logger.info("Distance validation passed")
    
    if (df["Total"] < 0).any():
            raise ValueError("Negative total found")
        
    logger.info("Order Total validation passed")


    if (df["total_item_quantity"] <= 0).any():
        raise ValueError("Invalid item quantity found")

    logger.info("Item quantity validation passed")

    logger.info("Data validation completed successfully")


def transform_data(df: pd.DataFrame):
    try:
        
        logger.info("Starting data transformation")

        df["distance_km"] = df["Distance"].str.replace("km", "")
        df["distance_km"] = df["distance_km"].str.replace("<1", "0.5")
        df["distance_km"] = df["distance_km"].astype(float)

        df["discount_type"] = df["Discount construct"].apply(
            lambda x: transform_discount(x)
        )

        df["discount_percent"] = df["Discount construct"].apply(
            lambda x: extract_discount_percent(x)
        )

        df["discount_cap"] = df["Discount construct"].apply(
            lambda x: extract_discount_cap(x)
        )

        df["Order Placed At"] = pd.to_datetime(
            df["Order Placed At"],
            format="%I:%M %p, %B %d %Y"
        )

        df["item_count"] = df["Items in order"].str.split(",").str.len()

        df["total_item_quantity"] = df["Items in order"].apply(
            lambda x: calculate_total_quantity(x)
        )

        df["is_delivered"] = df["Order Status"] == "Delivered"

        logger.info(
            f"Data transformation completed: {len(df)} rows transformed"
        )
        
        validate_data(df)

        return df
    except Exception as e:
        logger.error(f"{e} occurred during transformation")
        raise