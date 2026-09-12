from datetime import datetime , timedelta
import pandas as pd
from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
from src.extraction.extract import extract_data
from src.transformation.transform import transform_data
from src.modeling.dimensions import (
    create_restaurant_dimension,
    create_customer_dimension,
    create_location_dimension,
    create_date_dimension,
)
from src.loading.dimension_loader import (
    load_restaurant_dimension,
    load_customer_dimension,
    load_location_dimension,
    load_date_dimension,
)
from src.modeling.fact import create_fact_table
from src.loading.fact_loader import load_fact_table


TRANSFORMED_DF_PATH = "data/intermediate/transformed.csv"


def extract_transform_task(**context):
    df = extract_data()

    transformed_df = transform_data(df)

    transformed_df.to_csv(
        TRANSFORMED_DF_PATH,
        index=False
    )

    context["ti"].xcom_push(
        key="transformed_df_path",
        value=TRANSFORMED_DF_PATH
    )


def get_transformed_df(context):
    path = context["ti"].xcom_pull(
        task_ids="extract_transform",
        key="transformed_df_path"
    )

    return pd.read_csv(path)


def restaurant_task(**context):
    df = get_transformed_df(context)

    restaurant_df = create_restaurant_dimension(df)

    load_restaurant_dimension(restaurant_df)


def customer_task(**context):
    df = get_transformed_df(context)

    customer_df = create_customer_dimension(df)

    load_customer_dimension(customer_df)


def location_task(**context):
    df = get_transformed_df(context)

    location_df = create_location_dimension(df)

    load_location_dimension(location_df)


def date_task(**context):
    df = get_transformed_df(context)

    df["Order Placed At"] = pd.to_datetime(df["Order Placed At"])
    
    date_df = create_date_dimension(df)

    load_date_dimension(date_df)


def fact_task(**context):
    df = get_transformed_df(context)
    
    df["Order Placed At"] = pd.to_datetime(df["Order Placed At"])

    fact_df = create_fact_table(df)

    load_fact_table(fact_df)
    
default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="food_delivery_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args
    
) as dag:

    extract_transform = PythonOperator(
        task_id="extract_transform",
        python_callable=extract_transform_task,
    )

    restaurant = PythonOperator(
        task_id="restaurant",
        python_callable=restaurant_task,
    )

    customer = PythonOperator(
        task_id="customer",
        python_callable=customer_task,
    )

    location = PythonOperator(
        task_id="location",
        python_callable=location_task,
    )

    date = PythonOperator(
        task_id="date",
        python_callable=date_task,
    )

    fact = PythonOperator(
        task_id="fact",
        python_callable=fact_task,
    )

    extract_transform >> [
        restaurant,
        customer,
        location,
        date,
    ]

    [
        restaurant,
        customer,
        location,
        date,
    ] >> fact