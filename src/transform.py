import boto3
import logging
from io import BytesIO
from utils import upload_file, download_file, currency_code_converter
import polars as pl
import pyarrow as pa
from datetime import date



def lambda_handler(event, context):
    s3_client = boto3.client("s3")
    response = transform_data(s3_client, event["key"], event["batch_id"])
    return response


def transform_data(
    s3_client,
    key,
    batch_id,
    source_bucket="ainsdale-ingestion-bucket",
    destination_bucket="ainsdale-processed-bucket",
):
    """takes data from source bucket transforms into parquet format in starschema and uploads to destination bucket

    Args:
        s3_client (_type_): _description_
        key (str): key of folder containing most recent upload
        sourcebucket (str, optional): name of source bucket. Defaults to "ainsdale-ingestion-bucket".
        destinationbucket (str, optional): name of destination bucket. Defaults to "ainsdale-processed-bucket".

    Returns:
        dict:dictionary containing status code and key
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    table_name_list = [
        "counterparty",
        "currency",
        "department",
        "design",
        "staff",
        "sales_order",
        "address",
        "payment",
        "purchase_order",
        "payment_type",
        "transaction",
    ]

    df_dict = {
        "counterparty": "",
        "currency": "",
        "department": "",
        "design": "",
        "staff": "",
        "sales_order": "",
        "address": "",
        "payment": "",
        "purchase_order": "",
        "payment_type": "",
        "transaction": "",
    }

    processed_dict = {
        "fact_sales_order": "",
        "dim_date": "",
        "dim_staff": "",
        "dim_location": "",
        "dim_design": "",
        "dim_currency": "",
        "dim_counterparty": "",
    }

    try:
        for table in table_name_list:

            file = download_file(
                s3_client, source_bucket, f"{key}{batch_id}_{table}test.csv"
            )
            print(file)

            df_dict[table] = pl.read_csv(file["body"], try_parse_dates=True)
        processed_dict["fact_sales_order"] = make_fact_sales_order(
            df_dict["sales_order"]
        )

        processed_dict["dim_date"] = make_dim_date()
        processed_dict["dim_staff"] = make_dim_staff(
            df_dict["staff"], df_dict["department"]
        )
        processed_dict["dim_location"] = make_dim_location(df_dict["address"])
        processed_dict["dim_design"] = make_dim_design(df_dict["design"])
        processed_dict["dim_currency"] = make_dim_currency(df_dict["currency"])
        processed_dict["dim_counterparty"] = make_dim_counterparty(
            df_dict["counterparty"], df_dict["address"]
        )

        for table, value in processed_dict.items():
            out_buffer = BytesIO()
            value.write_parquet(out_buffer)

            upload_file(
                s3_client,
                file=out_buffer.getvalue(),
                bucket_name=destination_bucket,
                key=f"{key}{batch_id}_{table}.parquet",
            )
            logger.info(
                f"{batch_id}_{table}.parquet successfully uploaded to processed bucket"
            )
        logger.info("all tables successfully uploaded")
        return {"status": "Success", "code": 200, "key": key, "batch_id": batch_id}

    except Exception as e:
        logger.error({"status": "Failure", "message": e})
        return {"status": "Failure", "message": e}


def make_fact_sales_order(sales_order_table):
    """creates a fact table centred on sales orders: star schema

    Args:
        sales_order_table (dataframe): ingested table

    Returns:
        dataframe: a newly transformed dataframe for sales orders
    """

    fact_sales_order = sales_order_table.with_row_index("sales_record_id", offset=1)
    fact_sales_order = fact_sales_order.with_columns(
        (pl.col("created_at").dt.date()).alias("created_date"),
        (pl.col("created_at").dt.time()).alias("created_time"),
        (pl.col("last_updated").dt.date()).alias("last_updated_date"),
        (pl.col("last_updated").dt.time()).alias("last_updated_time"),
    )
    fact_sales_order = fact_sales_order.rename({"staff_id": "sales_staff_id"})

    fact_sales_order = fact_sales_order.select(
        [
            "sales_record_id",
            "sales_order_id",
            "created_date",
            "created_time",
            "last_updated_date",
            "last_updated_time",
            "sales_staff_id",
            "counterparty_id",
            "units_sold",
            "unit_price",
            "currency_id",
            "design_id",
            "agreed_payment_date",
            "agreed_delivery_date",
            "agreed_delivery_location_id",
        ]
    )

    return fact_sales_order


def make_dim_date():
    """creates a dim table centred on dates: star schema

    Returns:
        dataframe: a newly transformed dataframe for dates
    """
    start_date = date(1960, 1, 1)
    end_date = date(2060, 1, 1)
    interval = "1d"

    dim_date = pl.DataFrame(
        {
            "date_id": pl.date_range(
                start=start_date, end=end_date, interval=interval, eager=True
            )
        }
    )

    dim_date = dim_date.with_columns(
        (pl.col("date_id").dt.year()).alias("year"),
        (pl.col("date_id").dt.month()).alias("month"),
        (pl.col("date_id").dt.day()).alias("day"),
        (pl.col("date_id").dt.weekday()).alias("day_of_week"),
        (pl.col("date_id").dt.strftime("%A")).alias("day_name"),
        (pl.col("date_id").dt.strftime("%B")).alias("month_name"),
        (pl.col("date_id").dt.quarter()).alias("quarter"),
    )

    return dim_date


def make_dim_staff(staff_table, department_table):
    """creates a dim table centred on staff: star schema

    Args:
        staff_table, department (dataframe): ingested table

    Returns:
        dataframe: a newly transformed dataframe for staff details
        , location and email address
    """
    dim_staff = staff_table.join(department_table, on="department_id")
    dim_staff = dim_staff.select(
        [
            "staff_id",
            "first_name",
            "last_name",
            "department_name",
            "location",
            "email_address",
        ]
    )

    return dim_staff


def make_dim_location(address_table):
    """creates a dim table centred on location: star schema

    Args:
        address_table (dataframe): ingested table

    Returns:
        dataframe: a newly transformed dataframe for customer details (address)
    """
    dim_location = address_table.drop(["created_at", "last_updated"])
    dim_location = dim_location.rename({"address_id": "location_id"})

    return dim_location


def make_dim_currency(currency_table):
    """creates a dim table centred on purchase currency: star schema

    Args:
        currency_table (dataframe): ingested table

    Returns:
        dataframe: a newly transformed dataframe for purchase currency
    """

    dim_currency = currency_table.drop(["created_at", "last_updated"])
    columns = pl.col("currency_code")
    dim_currency = dim_currency.with_columns(
        pl.col("currency_code")
        .map_elements(currency_code_converter, return_dtype=str)
        .alias("currency_name")
    )

    return dim_currency


def make_dim_design(design_table):
    """creates a dim table centred on product design: star schema

    Args:
        design_table (dataframe): ingested table

    Returns:
        dataframe: a newly transformed dataframe for product designs
    """
    dim_design = design_table.drop(["created_at", "last_updated"])

    return dim_design


def make_dim_counterparty(counterparty_table, address_table):
    """creates a dim table centred on counterparty (customer) details: star schema

    Args:
        counterparty_table, address_table (dataframe): ingested table

    Returns:
        dataframe: a newly transformed dataframe for counterparties
    """
    dim_counterparty = counterparty_table.join(
        address_table, left_on="legal_address_id", right_on="address_id"
    )
    dim_counterparty = dim_counterparty.rename(
        {
            "address_line_1": "counterparty_legal_address_line_1",
            "address_line_2": "counterparty_legal_address_line_2",
            "district": "counterparty_legal_district",
            "city": "counterparty_legal_city",
            "postal_code": "counterparty_legal_postal_code",
            "country": "counterparty_legal_country",
            "phone": "counterparty_legal_phone_number",
        }
    )
    dim_counterparty = dim_counterparty.drop(
        [
            "legal_address_id",
            "commercial_contact",
            "delivery_contact",
            "created_at",
            "last_updated",
            "created_at_right",
            "last_updated_right",
        ]
    )

    return dim_counterparty

lambda_handler({
  "status": "Success",
  "code": 200,
  "key": "data/2025/6/9/2025-06-09_17:07:04/",
  "batch_id": "2025-06-09_17:07:04"
},"")