import logging
import boto3
#from botocore.exceptions import ClientError
from io import BytesIO
from utils import upload_file, get_db_secret
import polars as pl
from datetime import datetime


def lambda_handler(event, context):
    s3_client = boto3.client("s3")
    response = extract_data(s3_client)
    return response


def extract_data(s3_client=None, bucket="ainsdale-ingestion-bucket"):
    """Extracts data from database and places in ingestion bucket

    Args:
        s3_client (_type_, optional): amazon s3.client resource. Defaults to None.
        bucket (str, optional):name of ingestion bucket  . Defaults to "ainsdale-ingestion-bucket".

    Returns:
        dict: status message
    """

    logger = logging.getLogger(__name__)

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
    secrets= get_db_secret()
    user=secrets["user"]
    password=secrets["password"]
    database=secrets["database"]
    host=secrets["host"]
    port=secrets["port"]
   
    conn = f"postgresql://{user}:{password}@{host}:{port}/{database}"

    try:
        time_now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_day = datetime.now().day
        for table in table_name_list:
            df = pl.read_database_uri("SELECT * FROM " + table, conn)
            out_buffer = BytesIO()
            
            df.write_csv(out_buffer)

            upload_file(
                s3_client,
                file=out_buffer.getvalue(),
                bucket_name=bucket,
                key=f"data/{current_year}/{current_month}/{current_day}/{time_now}/{time_now}_{table}test.csv",
            )

        logger.info("File successfully uploaded to ingestion bucket")
        return {
            "status": "Success",
            "code": 200,
            "key": f"data/{current_year}/{current_month}/{current_day}/{time_now}/",
            "batch_id": time_now,
        }
    except Exception as e:
        print(e)
        logger.error(e)
        return {"status": "Failure", "error": e}
   

extract_data(boto3.client("s3"))