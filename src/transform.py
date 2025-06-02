import boto3
import logging 
from io import BytesIO
from src.utils import upload_file, download_file
import polars as pl


def lambda_handler(event,context):
    s3_client = boto3.client("s3")
    response = transform_data(s3_client, event["key"], event["batch_id"])
    return response

def transform_data(s3_client,key,batch_id, sourcebucket="ainsdale-ingestion-bucket", destinationbucket="ainsdale-processed-bucket"):
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
    df_list={"counterparty":"",
        "currency":"",
        "department":"",
        "design":"",
        "staff":"",
        "sales_order":"",
        "address":"",
        "payment":"",
        "purchase_order":"",
        "payment_type":"",
        "transaction":"",}
    try:
        for table in table_name_list:
            file=download_file(s3_client,sourcebucket,f"{key}{batch_id}_{table}.csv")
            df_list[table] =pl.read_csv(file)
        

        upload_file(s3_client,file,destinationbucket,file)
        return {'status': 'Success', 'code': 200, 'key': 'data/2025/5/29/2025-05-29_00:00:00/'}
    except Exception as e:
        logger.error(e)
        return {"status":"Failure","code":e}
