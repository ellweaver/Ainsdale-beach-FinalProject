import logging
import boto3
from utils.db_utils import connect_to_db, close_db_connection
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import shutil 
from datetime import datetime

client = 'b'

logger = logging.getLogger(__name__)

# with ZipFile('spam.zip', 'w') as myzip:
#     myzip.write('eggs.txt')



def extract_data(client):
    
    table_name_list = ["counterparty",
                        "currency",
                        "department",
                        "design",
                        "staff",
                        "sales_order",
                        "address",
                        "payment",
                        "purchase_order",
                        "payment_type",
                        "transaction"]
    
    conn = connect_to_db()
    time_now = datetime.now()

   
    for table in table_name_list:
        df = pd.read_sql("SELECT * FROM " + table, conn)
        pyarrow_table = pa.Table.from_pandas(df)
        pq.write_table(pyarrow_table, f'data/{time_now}{table}.parquet')
        #creates each parquet file in data directory

  

extract_data(client)




    # try:
    #     transformer_func(*table_name_list)
        
    # except:


    # finally:
    #     close_db_connection(conn)
    
    # return 



# get info from db
# reformat db data 
# to parquet 
# file upload using util 
# return



