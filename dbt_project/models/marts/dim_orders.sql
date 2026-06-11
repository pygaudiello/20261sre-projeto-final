with stg_orders as (
    select * from {{ ref('stg_orders') }}
),

stg_details as (
    select
        order_id,
        sum(quantity) as total_items,
        sum(total_price) as total_revenue
    from {{ ref('stg_order_details') }}
    group by order_id
)

select
    o.order_id,
    o.customer_id,
    o.employee_id,
    o.order_date,
    o.required_date,
    o.shipped_date,
    o.ship_country,
    o.freight,
    o.days_to_ship,
    o.required_days,
    d.total_items,
    d.total_revenue,

    case
        when o.shipped_date <= o.required_date then 'on_time'
        when o.shipped_date > o.required_date then 'late'
        else 'not_shipped'
    end as shipping_performance,

    now() as updated_at
from stg_orders o
left join stg_details d on o.order_id = d.order_id
