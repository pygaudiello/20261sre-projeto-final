with source as (
    select * from {{ source('olist_db', 'raw_orders') }}
),

cleaned as (
    select
        order_id,
        customer_id,
        order_status,
        order_purchase_timestamp,
        order_approved_at,
        order_delivered_carrier_date,
        order_delivered_customer_date,
        order_estimated_delivery_date,
        ingested_at,
        source_file,

        dateDiff('hour', order_purchase_timestamp, order_approved_at) as approval_hours,
        dateDiff('hour', order_purchase_timestamp, order_delivered_customer_date) as delivery_hours,
        dateDiff('day', order_purchase_timestamp, order_estimated_delivery_date) as estimated_delivery_days
    from source
)

select * from cleaned
