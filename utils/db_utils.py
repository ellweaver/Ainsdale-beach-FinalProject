from pg8000 import dbapi
import boto3
from botocore.exceptions import ClientError
import json


def get_secret():

    secret_name = "toteys_db_credentials"
    region_name = "eu-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    return secret


def connect_to_db():
    secrets = json.loads(get_secret())
    return dbapi.connect(
        user=secrets["user"], 
        password=secrets["password"],
        database=secrets["database"],
        host=secrets["host"],
        port=secrets["port"]
    )


def close_db_connection(conn):
    conn.close()
