# going with S3 access logging [Ievgeniiaa]
import boto3
import json

s3 = boto3.client('s3')
cloudtrail = boto3.client('cloudtrail')

def lambda_handler(event, context):
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }