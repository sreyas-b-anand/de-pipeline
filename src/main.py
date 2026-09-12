from src.extraction.extract import extract_data
from src.transformation.transform import transform_data
from src.modeling.dimensions import (
    create_restaurant_dimension,
    create_customer_dimension,
    create_location_dimension,
    create_date_dimension
)
from src.loading.dimension_loader import (
    load_restaurant_dimension,
    load_customer_dimension,
    load_location_dimension,
    load_date_dimension
)
from src.modeling.fact import create_fact_table
from src.loading.fact_loader import load_fact_table
from src.utils.logger import logger


def main():

    logger.info("Pipeline started")

    df = extract_data()

    transformed_df = transform_data(df)

    restaurant_df = create_restaurant_dimension(transformed_df)
    customer_df = create_customer_dimension(transformed_df)
    location_df = create_location_dimension(transformed_df)
    date_df = create_date_dimension(transformed_df)
    
    load_restaurant_dimension(restaurant_df)
    load_customer_dimension(customer_df)
    load_location_dimension(location_df)
    load_date_dimension(date_df)
    
    fact_df = create_fact_table(transformed_df)
    load_fact_table(fact_df)
    

    logger.info("Loading completed")
    logger.info("Pipeline execution completed successfully")


if __name__ == "__main__":
    main()
