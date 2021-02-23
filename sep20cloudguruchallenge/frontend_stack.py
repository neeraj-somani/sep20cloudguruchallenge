from aws_cdk import (
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    aws_dynamodb as dynamodb,
    aws_s3 as _s3,
    aws_apigateway as apigw,
    core,
)

from spa_deploy import SPADeploy
import boto3
import os

#ddb = boto3.resource('dynamodb')


class frontendStack(core.Stack):
    
    # Using this property I am exposing table that can be used in lambda

    def __init__(self, scope: core.Construct, construct_id: str, referenced_dynamodb_table_arn: str , **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Defines an AWS Lambda resource
        my_frontend_lambda = _lambda.Function(
            self, 'frontendHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='frontend_handler.scan_operation_dynamodb',
            #layers=[my_layer],
            timeout=core.Duration.seconds(300),
        )
        
        
        reference_ddb_table = dynamodb.Table.from_table_arn(self, "ImportedDDBTable", referenced_dynamodb_table_arn)
        my_frontend_lambda.add_environment("DDB_TABLE_NAME", reference_ddb_table.table_name)
        # now you can just call methods on the table
        reference_ddb_table.grant_read_data(my_frontend_lambda)
        
        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=my_frontend_lambda,
        )
        
        SPADeploy(self, 'spaDeploy').create_basic_site(
            index_doc='index.html',
            website_folder='../sep20cloudguruchallenge/S3_website',
            )
        
        
        
        
        
        
        