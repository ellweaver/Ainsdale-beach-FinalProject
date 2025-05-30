import logging
import boto3
from botocore.exceptions import ClientError
from io import BytesIO
from utils.db_utils import connect_to_db, close_db_connection
from utils.utils import upload_file
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime

def lamda_handler(event, context):
    s3_client = boto3.client("s3")
    response = extract_data(s3_client)
    return response
    
def extract_data(s3_client=None, bucket="ainsdale-ingestion-bucket"):

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


            out_buffer = BytesIO()
            pq.write_table(pyarrow_table, out_buffer)

            upload_file(s3_client, file=out_buffer.getvalue(), bucket_name=bucket, key=f"data/{time_now}/{time_now}_{table}.parquet")

        logger.info(
            "File successfully uploaded to ingestion bucket"
        )  
        return {"status": "Success", "code": 200, "key": f"data/{time_now}"}
    except Exception as e:
        print(e)
        logger.error(e)
        return {"status": "Failure", "error": e}
    finally:
        close_db_connection(conn)

# remove this going forward
if __name__ == '__main__':
    lamda_handler(None, None)