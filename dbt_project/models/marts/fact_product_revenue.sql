with stg_order_details as (
    select * from {{ ref('stg_order_details') }}
),

stg_orders as (
    select * from {{ ref('stg_orders') }}
),

joined as (
    select
        od.order_id,
        od.product_id,
        od.unit_price,
        od.quantity,
        od.discount,
        od.total_price as net_revenue,
        o.order_date,
        toStartOfMonth(o.order_date) as order_month
    from stg_order_details od
    inner join stg_orders o on od.order_id = o.order_id
)

select * from joined
