#!/usr/bin/env python3

from aws_cdk import core

from sep20cloudguruchallenge.backend_stack import backendStack 
from sep20cloudguruchallenge.frontend_stack import frontendStack


app = core.App()
backend = backendStack(app, "sep20cloudguruchallenge-backend", env={'region': 'us-west-2'})
frontend = frontendStack(app, "sep20cloudguruchallenge-frontend", referenced_dynamodb_table_arn=backend.dynamodb_table_arn , env={'region': 'us-west-2'})

app.synth()
