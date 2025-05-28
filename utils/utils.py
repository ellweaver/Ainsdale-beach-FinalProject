from botocore.exceptions import ClientError


def upload_file(client, file, bucket_name,key):
    """Provides packaged error handling and response for client.putobject function

    Args:
        client (client_object): aws s3 client
        file (bytes|string): bytes object to be uploaded or name of file 
        bucket_name (string): name of bucket
        key (string): key of item in bucket

    Returns:
        Dict: dictionary with key Status (containing Success or Failed) and Code containing response code
    """
    try:
        response =client.put_object(Body=file,Bucket=bucket_name, Key=key)
        response = {'status':"Success","code":response["ResponseMetadata"]["HTTPStatusCode"]}
    except ClientError as e:
        response = {'status':"Failed", "code":e.response['Error']['Code']}
    
    return response

def download_file(client,bucket_name,key):
    """provides Error handling and response for get_object

    Args:
        client (client_object): AWS s3 client
        bucket (string): name of bucket to be retrieved from
        key (string): key of object to be retrieved

    Returns:
        dict: dictionary containing keys 'body' containing streaming body ) 'status' (containing Failed or Success) and 'code'(containing the status code)
    """
    #TODO turn body response into file object response possibly
    try:
        response = client.get_object(Bucket=bucket_name,Key=key)
        response = {'body':response['Body'],'status':"Success","code":response["ResponseMetadata"]["HTTPStatusCode"]}
        

    except ClientError as e:
        response = {'status':"Failed", "code":e.response['Error']['Code']}
        
    return response
    