with stg_orders as (
    select * from {{ ref('stg_orders') }}
),

status_fact as (
    select
        order_id,
        customer_id,
        order_date,
        shipped_date,
        required_date,

        case
            when shipped_date is not null then 1
            else 0
        end as is_shipped,

        case
            when shipped_date <= required_date then 1
            else 0
        end as is_on_time,

        case
            when shipped_date > required_date then 1
            else 0
        end as is_late
    from stg_orders
)

select * from status_fact
