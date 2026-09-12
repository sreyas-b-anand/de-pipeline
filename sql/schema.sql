-- dimension table

CREATE TABLE dim_restaurant (
    restaurant_id BIGINT PRIMARY KEY,
    restaurant_name TEXT
);

CREATE TABLE dim_customer (
    customer_id TEXT PRIMARY KEY
);

CREATE TABLE dim_location (
    location_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    city TEXT,
    subzone TEXT,
    UNIQUE (city, subzone)
);

CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    date DATE,
    day INTEGER,
    month INTEGER,
    year INTEGER
);

-- facts table

CREATE TABLE fact_orders (
    order_id BIGINT PRIMARY KEY,

    restaurant_id BIGINT REFERENCES dim_restaurant(restaurant_id),
    customer_id TEXT REFERENCES dim_customer(customer_id),
    location_id INTEGER REFERENCES dim_location(location_id),
    date_id INTEGER REFERENCES dim_date(date_id),

    order_status TEXT,
    order_placed_at TIMESTAMP,

    total NUMERIC,
    bill_subtotal NUMERIC,
    packaging_charges NUMERIC,
    distance_km NUMERIC,
    rating NUMERIC,
    kpt_duration NUMERIC,
    rider_wait_time NUMERIC,
    item_count INTEGER,
    total_item_quantity INTEGER,
    is_delivered BOOLEAN
);