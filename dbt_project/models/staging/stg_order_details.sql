with source as (
    select * from {{ source('northwind_db', 'raw_order_details') }}
),

cleaned as (
    select
        order_id,
        product_id,
        unit_price,
        quantity,
        discount,
        (unit_price * quantity) * (1 - discount) as total_price,
        ingested_at,
        source_file
    from source
)

select * from cleaned
