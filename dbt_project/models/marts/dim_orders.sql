with stg_orders as (
    select * from {{ ref('stg_pedidos') }}
)

select
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp,
    order_approved_at,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    order_estimated_delivery_date,
    approval_hours,
    delivery_hours,
    estimated_delivery_days,

    case
        when order_status = 'delivered' and order_delivered_customer_date <= order_estimated_delivery_date
            then 'on_time'
        when order_status = 'delivered' and order_delivered_customer_date > order_estimated_delivery_date
            then 'late'
        when order_status = 'delivered'
            then 'unknown'
        else 'not_delivered'
    end as delivery_performance,

    date_diff('day', order_purchase_timestamp, order_delivered_customer_date) as actual_delivery_days,

    now() as updated_at
from stg_orders
