# Food Delivery Data Engineering Pipeline

A Python-based data engineering pipeline that extracts food delivery order data from a CSV dataset, performs data cleaning and transformation, validates the data, models it using a star schema, and incrementally loads it into PostgreSQL hosted on Supabase.

## Project Overview

This project demonstrates a complete ETL workflow for food delivery data.

The pipeline:

1. Extracts raw order data from CSV
2. Cleans and transforms the data using Pandas
3. Validates the transformed data
4. Creates dimension and fact tables using a star schema
5. Loads the dimensions and fact table into PostgreSQL
6. Performs incremental loading to prevent duplicate records
7. Provides SQL queries for analytical use cases

## Architecture

```text
                 Raw CSV Data
                      |
                      v
                +-----------+
                |  Extract  |
                +-----------+
                      |
                      v
                +----------------+
                | Transform &    |
                | Validate       |
                +----------------+
                      |
                      v
              +-----------------+
              | Data Modeling   |
              |   Star Schema   |
              +-----------------+
                 /    |    |    \
                /     |    |     \
               v      v    v      v
          Restaurant Customer Location Date
          Dimension  Dimension Dimension Dimension
                \      |    |      /
                 \     |    |     /
                  \    |    |    /
                   v   v    v   v
                   +-----------+
                   | Fact Orders|
                   +-----------+
                        |
                        v
                PostgreSQL / Supabase
                        |
                        v
                   SQL Analytics

```
## Tech Stack

- **Python** – Pipeline development
- **Pandas** – Data processing and transformation
- **SQLAlchemy** – Database connectivity
- **PostgreSQL** – Relational database
- **Supabase** – Hosted PostgreSQL
- **SQL** – Database schema and analytics
- **Git** – Version control

## Dataset

The project uses a food delivery order history dataset containing **21,321 orders** and **29 attributes**.

The dataset includes information about:

- Restaurants and customers
- Order status and timestamps
- Order values and discounts
- Delivery distance
- Ratings and reviews
- Cancellation and rejection details
- Delivery performance metrics

## Project Structure

```text
food-delivery-data-pipeline/
│
├── data/
│   └── raw/
│       └── order_history_kaggle_data.csv
│
├── docs/
│   └── schema.png
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── extraction/
│   │   └── extract.py
│   │
│   ├── transformation/
│   │   └── transform.py
│   │
│   ├── modeling/
│   │   ├── dimensions.py
│   │   └── fact.py
│   │
│   ├── loading/
│   │   ├── dimension_loader.py
│   │   └── fact_loader.py
│   │
│   └── utils/
│       └── logger.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## ETL Pipeline

The pipeline follows an **Extract, Transform, Load (ETL)** approach.

### Extract

Raw food delivery data is extracted from a CSV file using Pandas.

### Transform

The extracted data is cleaned, validated, and transformed. Derived fields such as delivery distance, discount type, item count, total item quantity, and delivery status are generated.

The transformed data is then organized into a **star schema** consisting of fact and dimension tables.

### Load

The dimension and fact tables are incrementally loaded into PostgreSQL hosted on Supabase. Existing records are identified using their keys, and only new records are inserted.

## Data Modeling

The project uses a star schema for analytical data modeling.

The central fact table contains order-level transactional data, while dimension tables contain descriptive information about entities such as restaurants, customers, locations, and dates.

## Star Schema

![Star Schema](docs/schema.png)
              
## Setup

### 1. Clone the repository

```bash
git clone https://github.com/sreyas-b-anand/de-project.git
cd de-project
```
### 2. Create a virtual environment
```bash
python -m venv .venv
```
### 3. Activate the virtual environment

Windows PowerShell
```bash
.venv\Scripts\Activate.ps1
```

Linux / macOS
```bash
source .venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a .env file in the project root:
```bash
DATABASE_URL=your_postgresql_connection_string
```
### 6. Add the dataset

Place the raw CSV file at:

data/raw/order_history_kaggle_data.csv

### 7. Run the pipeline

From the project root:
```bash
python -m src.main
```