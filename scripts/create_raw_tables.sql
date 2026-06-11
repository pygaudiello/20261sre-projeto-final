CREATE DATABASE IF NOT EXISTS northwind_db;

USE northwind_db;

CREATE TABLE IF NOT EXISTS raw_orders (
    order_id Int64,
    customer_id String,
    employee_id Int64,
    order_date Date,
    required_date Date,
    shipped_date Nullable(Date),
    ship_via Int64,
    freight Float64,
    ship_name String,
    ship_address String,
    ship_city String,
    ship_region Nullable(String),
    ship_postal_code Nullable(String),
    ship_country String,
    ingested_at DateTime DEFAULT now(),
    source_file String
) ENGINE = MergeTree()
ORDER BY order_id;

CREATE TABLE IF NOT EXISTS raw_order_details (
    order_id Int64,
    product_id Int64,
    unit_price Float64,
    quantity Int64,
    discount Float64,
    ingested_at DateTime DEFAULT now(),
    source_file String
) ENGINE = MergeTree()
ORDER BY (order_id, product_id);
