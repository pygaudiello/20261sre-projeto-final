-- Criação das tabelas da camada RAW para o dataset Olist
-- Todas as tabelas usam MergeTree e possuem colunas de auditoria

CREATE DATABASE IF NOT EXISTS olist_db;

USE olist_db;

-- 1. Orders
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

-- 2. Order Items
CREATE TABLE IF NOT EXISTS raw_order_items (
    order_id String,
    order_item_id UInt8,
    product_id String,
    seller_id String,
    shipping_limit_date DateTime,
    price Float64,
    freight_value Float64,
    ingested_at DateTime DEFAULT now(),
    source_file String
) ENGINE = MergeTree()
ORDER BY (order_id, order_item_id);

-- 3. Products
CREATE TABLE IF NOT EXISTS raw_products (
    product_id String,
    product_category_name Nullable(String),
    product_name_lenght Nullable(UInt16),
    product_description_lenght Nullable(UInt16),
    product_photos_qty Nullable(UInt8),
    product_weight_g Nullable(UInt32),
    product_length_cm Nullable(UInt16),
    product_height_cm Nullable(UInt16),
    product_width_cm Nullable(UInt16),
    ingested_at DateTime DEFAULT now(),
    source_file String
) ENGINE = MergeTree()
ORDER BY product_id;

-- 4. Customers
CREATE TABLE IF NOT EXISTS raw_customers (
    customer_id String,
    customer_unique_id String,
    customer_zip_code_prefix String,
    customer_city String,
    customer_state String,
    ingested_at DateTime DEFAULT now(),
    source_file String
) ENGINE = MergeTree()
ORDER BY customer_id;

-- 5. Payments
CREATE TABLE IF NOT EXISTS raw_order_payments (
    order_id String,
    payment_sequential UInt8,
    payment_type String,
    payment_installments UInt8,
    payment_value Float64,
    ingested_at DateTime DEFAULT now(),
    source_file String
) ENGINE = MergeTree()
ORDER BY order_id;

-- 6. Reviews
CREATE TABLE IF NOT EXISTS raw_order_reviews (
    review_id String,
    order_id String,
    review_score UInt8,
    review_comment_title Nullable(String),
    review_comment_message Nullable(String),
    review_creation_date DateTime,
    review_answer_timestamp DateTime,
    ingested_at DateTime DEFAULT now(),
    source_file String
) ENGINE = MergeTree()
ORDER BY review_id;

-- 7. Sellers
CREATE TABLE IF NOT EXISTS raw_sellers (
    seller_id String,
    seller_zip_code_prefix String,
    seller_city String,
    seller_state String,
    ingested_at DateTime DEFAULT now(),
    source_file String
) ENGINE = MergeTree()
ORDER BY seller_id;

-- 8. Geolocation
CREATE TABLE IF NOT EXISTS raw_geolocation (
    geolocation_zip_code_prefix String,
    geolocation_lat Float64,
    geolocation_lng Float64,
    geolocation_city String,
    geolocation_state String,
    ingested_at DateTime DEFAULT now(),
    source_file String
) ENGINE = MergeTree()
ORDER BY geolocation_zip_code_prefix;
