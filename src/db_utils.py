from pg8000 import dbapi
import boto3
from botocore.exceptions import ClientError
import json


def get_db_secret(client=None):

    secret_name = "toteys_db_credentials"
    region_name = "eu-west-2"

    # Create a Secrets Manager client
    if not client:
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response["SecretString"]
    return secret


def get_db_warehouse_secret(client=None):

    secret_name = "toteys_db_warehouse_credentials"
    region_name = "eu-west-2"

    # Create a Secrets Manager client
    if not client:
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response["SecretString"]
    return secret


def connect_to_db(secret_name="toteys_db_credentials"):
    if secret_name == "toteys_db_credentials":
        secrets = json.loads(get_db_secret())
    elif secret_name == "toteys_db_warehouse_credentials":
        secrets = json.loads(get_db_warehouse_secret())

    return dbapi.connect(
        user=secrets["user"],
        password=secrets["password"],
        database=secrets["database"],
        host=secrets["host"],
        port=secrets["port"],
        timeout=15,
    )


def close_db_connection(conn):
    conn.close()
