```sql
--tranformation created_date created_time last_updated_date last_updated_time
Table "fact_sales_order" {
  "sales_record_id" SERIAL [pk, increment]
  "sales_order_id" int [not null] --(sales_order sales_order_id)
  "created_date" date [not null] --(sales_order created_at) dim_date
  "created_time" time [not null] --(sales_order created_at)
  "last_updated_date" date [not null] --(sales_order last_updated) dim_date
  "last_updated_time" time [not null] --(sales_order last_updated)
  "sales_staff_id" int [not null] --(sales_order staff_id) dim_staff
  "counterparty_id" int [not null] --(sales_order counter_party_id) dim_counterparty
  "units_sold" int [not null] --(sales_order units_sold)
  "unit_price" "numeric(10, 2)" [not null]--(sales_order unit_price)
  "currency_id" int [not null] --(sales_order currency_id) dim_currency
  "design_id" int [not null] --(sales_order design_id) dim_design
  "agreed_payment_date" date [not null] -- (sales_order agreed_payment_date) dim_date
  "agreed_delivery_date" date [not null]--(sales_order agreed_delivery_date) dim_date
  "agreed_delivery_location_id" int [not null] --(sales_order agreed_delivery_location_id)dim_location
}

Table dim_date as DT { --Dates
  date_id date [pk, not null] 
  year int [not null]
  month int [not null]
  day int [not null]
  day_of_week int [not null]
  day_name varchar [not null]
  month_name varchar [not null]
  quarter int [not null]
}


--Transformation: department_name location
Table dim_staff as S {
  staff_id int [pk, not null] --(staff staff_id)
  first_name varchar [not null]--(staff first_name)
  last_name varchar [not null]--(staff last_name)
  department_name varchar [not null]--(department department_name)
  location varchar [not null] --(department location)
  email_address email_address [not null] --(staff email_address)
}

--no transformation
Table dim_location as LOC {
  location_id int [pk, not null] --(address address_id)
  address_line_1 varchar [not null] --(address address_line_1)
  address_line_2 varchar --(address address_line_2)
  district varchar --(address district)
  city varchar [not null] --(address city)
  postal_code varchar [not null]--(address postal_code)
  country varchar [not null] --(address country)
  phone varchar [not null] --(address phone)
}

--Transformation(currency_name)
Table dim_currency as C {
  currency_id int [pk, not null] --(currency currency_id)
  currency_code varchar [not null]--(currency currency_code)
  currency_name varchar [not null] --(currency currency_code)
}

--no transformation
Table dim_design as D{
  design_id int [pk, not null] --(design design_id)
  design_name varchar [not null] --(design design_name)
  file_location varchar [not null] --(design file_location)
  file_name varchar [not null] --(design file_name)
}

--Transformation(counterparty_address_line_1 counterparty_address_line_2 counterparty_legal_district counterparty_city counterparty_postal_code counterparty_country counterparty_phone)
Table dim_counterparty as CO {
  counterparty_id int [pk, not null] --(counterparty counterparty_id)
  counterparty_legal_name varchar [not null] --(counterparty counterparty_legal_name)
  counterparty_legal_address_line_1 varchar [not null] --(address address_line_1)
  counterparty_legal_address_line_2 varchar --(address address_line_2)
  counterparty_legal_district varchar--(address district)
  counterparty_legal_city varchar [not null] --(address city)
  counterparty_legal_postal_code varchar [not null] --(address postal_code)
  counterparty_legal_country varchar [not null] --(address country)
  counterparty_legal_phone_number varchar [not null] --(address phone)
}

Ref:"dim_date"."date_id" < "fact_sales_order"."created_date"

Ref:"dim_date"."date_id" < "fact_sales_order"."last_updated_date"

Ref:"dim_staff"."staff_id" < "fact_sales_order"."sales_staff_id"

Ref:"dim_counterparty"."counterparty_id" < "fact_sales_order"."counterparty_id"

Ref:"dim_currency"."currency_id" < "fact_sales_order"."currency_id"

Ref:"dim_design"."design_id" < "fact_sales_order"."design_id"

Ref:"dim_date"."date_id" < "fact_sales_order"."agreed_payment_date"

Ref:"dim_date"."date_id" < "fact_sales_order"."agreed_delivery_date"

Ref:"dim_location"."location_id" < "fact_sales_order"."agreed_delivery_location_id"
```