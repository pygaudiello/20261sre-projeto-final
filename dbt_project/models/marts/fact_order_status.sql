with stg_orders as (
    select * from {{ ref('stg_pedidos') }}
),

status_fact as (
    select
        order_id,
        customer_id,
        order_status as current_status,
        order_purchase_timestamp,
        order_approved_at,
        order_delivered_carrier_date,
        order_delivered_customer_date,
        order_estimated_delivery_date,
        ingested_at as batch_timestamp,

        case
            when order_status = 'delivered' then 1
            else 0
        end as is_delivered,

        case
            when order_approved_at is not null then 1
            else 0
        end as is_approved,

        case
            when order_delivered_carrier_date is not null then 1
            else 0
        end as is_with_carrier
    from stg_orders
)

select * from status_fact
