import boto3
import polars as pl
import logging
from db_utils import connect_to_db, close_db_connection
from src.utils import download_file, upload_file

'''
1. Needs to download the latest data from the transform bucket
2. Latest data would pass from transform.py as event["key"] refer to key in transform s3 bucket,
   event["batch_id"] referring to current batch
3. For each table, it needs to upload to the data warehouse
4. Import is going to get key and batch_id


'''


def lambda_handler(event, context):
    s3_client = boto3.client("s3")
    response = load_data(s3_client, event["key"], event["batch_id"])
    return response
    
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def load_data(s3_client,key,batch_id,sourcebucket="ainsdale_transform_bucket"):
    conn = connect_to_db("toteys_db_warehouse_credentials")

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
        for table in processed_dict:
            file = download_file(
                    s3_client, sourcebucket, f"{key}{batch_id}_{table}.parquet"
                )
            df = pl.read_parquet(file["body"])
            df.write_database(table_name=table, connection=conn)
            logger.info(f"${table} successfully uploaded to data warehouse")

        logger.info("All tables successfully uploaded to data warehouse")
        return {"status": "Success", "code": 200, "key": key, "batch_id": batch_id}
        
    except Exception as e:
        logger.error(e)
        return {"status": "Failure", "code": e}


            
            

            
    

