import json
import boto3
import os
from decimal import Decimal
import pandas as pd


# set environment variable
TABLE_NAME = os.environ['DDB_TABLE_NAME']
#FILE_NAME = os.environ['FILE_NAME']

# Get the service resource.
dynamodb_client = boto3.resource("dynamodb")

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)
        
def scan_operation_dynamodb(event, context) -> str:
    print('request: {}'.format(json.dumps(event)))
    ## below command is used to fetch dynamodb table name that was set by stack in frontend lambda
    #ddb_table_name = event.referenced_dynamodb_table.table_name
    
    ## passing above fetch dynamodb table name to boto3 dynamodb client object
    dynamodb_client_table = dynamodb_client.Table(TABLE_NAME)
    
    #dynamodb_client_table = dynamodb_client.Table.from_table_arn(self, "ImportedTable", os.environ['DDB_TABLE_ARN'])
    
    # using boto3 client to run scan operation on dynamodb table
    resp = dynamodb_client_table.scan()
    return{
        'statusCode': 200,
        'body': json.dumps(resp["Items"], cls=DecimalEncoder),
        'headers': {
		"Access-Control-Allow-Origin": "*"
	    }
    }
    

    ## Need to understand how can we pass this data to api gateway response