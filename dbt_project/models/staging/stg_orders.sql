with source as (
    select * from {{ source('northwind_db', 'raw_orders') }}
),

cleaned as (
    select
        order_id,
        customer_id,
        employee_id,
        order_date,
        required_date,
        shipped_date,
        ship_via,
        freight,
        ship_name,
        ship_address,
        ship_city,
        ship_region,
        ship_postal_code,
        ship_country,
        ingested_at,
        source_file,

        dateDiff('day', order_date, shipped_date) as days_to_ship,
        dateDiff('day', order_date, required_date) as required_days
    from source
)

select * from cleaned
