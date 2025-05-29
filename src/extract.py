import logging
import boto3
from botocore.exceptions import ClientError

from utils.db_utils import connect_to_db, close_db_connection
from utils.utils import upload_file

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from datetime import datetime


def extract_data(client=None):
    if not client:
        client = boto3.client("s3")

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

    conn = connect_to_db()

    try:
        time_now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

        for table in table_name_list:
            df = pd.read_sql("SELECT * FROM " + table, conn)
            pyarrow_table = pa.Table.from_pandas(df)
            pq.write_table(
                pyarrow_table, f"data/{time_now}{table}.parquet"
            )  # creates each parquet file in data directory
            upload_file(
                client,
                file=f"data/{time_now}{table}.parquet",
                bucket_name="ainsdale-ingestion-bucket",
                key=f"{time_now}/{time_now}{table}.parquet",
            )
        logger.info(
            "File successfully uploaded to ingestion bucket"
        )  
        return {"status": "Success", "code": 200}
    except ClientError as e:
        logger.error(e)
        return {"status": "failure", "error": e}
    finally:
        close_db_connection()
