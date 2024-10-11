"""
The purpose of this script is to update S3 server access logging settings.

Version: 1.1

's3_server_access_logs' solution in the repo, https://github.com/aws-samples/aws-security-reference-architecture-examples

Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0
"""
import boto3
import json

s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    bucket_name = event['detail']['requestParameters']['bucketName']
    aws_account_id = event['account']
    region = event['region']

    # Check if the bucket has the "sra-server-access-logging-enabled" tag
    try:
        response = s3.get_bucket_tagging(Bucket=bucket_name)
        tags = response['TagSet']
        logging_enabled = any(tag['Key'] == 'sra-server-access-logging-enabled' and tag['Value'] == 'true' for tag in tags)
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchTagSet':
            # If the bucket has no tags, logging is disabled
            logging_enabled = False
        else:
            raise e
        
    # Bucket Tag filtering for logging
    if logging_enabled:
        # Enable s3 access logging
        try:
            s3.put_bucket_logging(
                Bucket=bucket_name,
                BucketLoggingStatus={
                    'LoggingEnabled': {
                        'TargetBucket': f"sra-server-access-log-{aws_account_id}-{region}-region",
                        'TargetPrefix': f"{aws_account_id}/{region}/{bucket_name}/"
                    }
                }
            )
            print(f"Server access logging enabled for bucket {bucket_name} in {region}")
        except s3.exceptions.ClientError as e:
            print(f"Error enabling server access logging for bucket {bucket_name}: {e}")
    
    else:
        # Disable server access logging
        try:
            s3.put_bucket_logging(
                Bucket=bucket_name,
                BucketLoggingStatus={}
            )
            print(f"Server access logging disabled for bucket {bucket_name}")
        except s3.exceptions.ClientError as e:
            print(f"Error disabling server access logging for bucket {bucket_name}: {e}")


    return {
        'statusCode': 200,
        'body': json.dumps('Lambda filtered the buckets successfully!')
    }