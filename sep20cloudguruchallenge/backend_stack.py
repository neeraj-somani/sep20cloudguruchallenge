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
    core,
)


class backendStack(core.Stack):
    
    @property
    def dynamodb_table_arn(self):
        return self._ddb_table_arn

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        
        # Defines an AWS Lambda resource
        my_backend_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='backend_handler.refresh_data_from_sources',
            #layers=[my_layer],
            timeout=core.Duration.seconds(300),
        )
        
        # Run every day at 4PM UTC
        # See https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(
                minute='45',
                hour='18',
                month='*',
                week_day='*',
                year='*'),
        )
        rule.add_target(targets.LambdaFunction(my_backend_lambda))
        
        # create dynamo table
        demotable = dynamodb.Table(
            self, "sep20cloudguruchallenge_table",
            table_name='sep20cloudguruchallenge_covid',
            partition_key=dynamodb.Attribute(
                name="pk",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="date",
                type=dynamodb.AttributeType.STRING
            ),
            # The default removal policy is RETAIN, which means that cdk
            # destroy will not attempt to delete the new table, and it will
            # remain in your account until manually deleted. By setting the
            # policy to DESTROY, cdk destroy will delete the table (even if it
            # has data in it)
            removal_policy=core.RemovalPolicy.DESTROY # NOT recommended for production code   
        )

        my_backend_lambda.add_environment("TABLE_NAME", demotable.table_name)

        # grant permission to lambda to write to demo table
        demotable.grant_write_data(my_backend_lambda)
        
        self._ddb_table_arn = demotable.table_arn
        

        # create s3 bucket
        s3 = _s3.Bucket(self, "s3bucket",
            bucket_name='sep20cloudguruchallenge-previous-load-data',
            removal_policy=core.RemovalPolicy.DESTROY
        )
        # set bukcket name at environment level to use it across project
        my_backend_lambda.add_environment("BUCKET_NAME", s3.bucket_name)

        # set s3 file name at environment level to use it across project
        my_backend_lambda.add_environment("FILE_NAME", 'last_save_data.csv')

        # Grant lambda function access to the s3 bucket created earlier
        s3.grant_read_write(my_backend_lambda)


        topic = sns.Topic(
            self, "sep20cloudguruchallenge-sns-topic",
            topic_name='sep20cloudguruchallenge-sns-topic'
        )

        topic.add_subscription(subs.EmailSubscription('neerajsomani04@gmail.com'))

        topic.grant_publish(my_backend_lambda)

        my_backend_lambda.add_environment("NOTIFICATION_TOPIC_ARN", topic.topic_arn)
