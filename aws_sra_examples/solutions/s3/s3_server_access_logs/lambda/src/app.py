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
cloudtrail = boto3.client('cloudtrail')

def lambda_handler(event, context):
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }