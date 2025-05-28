def upload_file(client, file_name, bucket,key):

    response =client.put_object(Body=file_name,Bucket=bucket, Key=key)
    response = {"status":response["ResponseMetadata"]["HTTPStatusCode"]}
    return response

def download_file(client,filename,bucket):
    pass
    