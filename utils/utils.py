from botocore.exceptions import ClientError

def upload_file(client, file_name, bucket_name,key):
    """Provides packaged error handling and response for client.putobject function

    Args:
        client (client_object): aws s3 client
        file_name (string): name of file to be uploaded
        bucket_name (string): name of bucket
        key (string): key of item in bucket

    Returns:
        Dict: dictionary with key Status
    """
    try:
        response =client.put_object(Body=file_name,Bucket=bucket_name, Key=key)
        response = {'status':"Success","code":response["ResponseMetadata"]["HTTPStatusCode"]}
    except ClientError as e:
        response = {'status':"Failed", "code":e.response['Error']['Code']}
    
    return response

def download_file(client,filename,bucket):
    pass
    