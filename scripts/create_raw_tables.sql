CREATE DATABASE IF NOT EXISTS olist_db;

USE olist_db;

CREATE TABLE IF NOT EXISTS raw_orders (
    order_id String,
    customer_id String,
    order_status String,
    order_purchase_timestamp DateTime,
    order_approved_at Nullable(DateTime),
    order_delivered_carrier_date Nullable(DateTime),
    order_delivered_customer_date Nullable(DateTime),
    order_estimated_delivery_date DateTime,
    ingested_at DateTime DEFAULT now(),
    source_file String
) ENGINE = MergeTree()
ORDER BY order_id;
