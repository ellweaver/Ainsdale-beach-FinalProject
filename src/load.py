import boto3
import polars as pl
import pandas as pd
import logging
from utils import download_file, get_db_secret
import pg8000
from io import BytesIO
import psycopg2






def lambda_handler(event, context):
    s3_client = boto3.client("s3")
    response = load_data(s3_client, event["key"], event["batch_id"])
    return response


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def load_data(
    s3_client, key, batch_id, sourcebucket="ainsdale-processed-bucket", test=False
):
    """takes data from transform bucket and upload to data warehoue

    Args:
        s3_client (_type_): _description_
        key (str): key of folder containing most recent upload
        sourcebucket (str, optional): name of source bucket. Defaults to "ainsdale_transform_bucket".
        test which can be set to true during testing to avoid unwanted behaviour".

    Returns:
        dict:dictionary containing status code and key
    """
    

    secrets= get_db_secret(secretname="toteys_db_warehouse_credentials")
    user=secrets["user"]
    password=secrets["password"]
    database=secrets["database"]
    host=secrets["host"]
    port=secrets["port"]
    conn = f"postgresql://{user}:{password}@{host}:{port}/{database}"

    processed_dict = {
        "dim_date": "",
        "dim_staff": "",
        "dim_location": "",
        "dim_design": "",
        "dim_currency": "",
        "dim_counterparty": "",
        "fact_sales_order": "",
    }

    try:
        for table in processed_dict:
            file = download_file(
                s3_client, sourcebucket, f"{key}{batch_id}_{table}.parquet"
            )
            if file["code"]==200:
                transformed_df = pl.read_parquet(file["body"])
                #print(transformed_df)
                db_df = pl.read_database_uri("SELECT * FROM " + table, conn)
                db__df_shape=db_df.shape[0]
                transformed_shape=transformed_df.shape[0]
                tail=db__df_shape-transformed_shape
               
                

            else: raise Exception(f"{table} not found")
                
            
            
            if not test: 
                transformed_df.tail(tail).write_database(table_name=table, connection=conn, if_table_exists= "append")
            logger.info(f"{table} successfully uploaded to data warehouse")

        logger.info("All tables successfully uploaded to data warehouse")
        return {"status": "Success", "code": 200, "key": key, "batch_id": batch_id}

    except Exception as e:
        logger.error({"status": "Failure", "code": 404, "message": str(e)})
        return {"status": "Failure", "code": 404, "message": str(e)}


if __name__ == "__main__":
    print(lambda_handler({'status': 'Success', 'code': 200, 'key': 'data/2025/6/10/2025-06-10_11:49:15/', 'batch_id': '2025-06-10_11:49:15'},""))

    
