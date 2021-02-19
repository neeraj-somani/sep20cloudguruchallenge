#!/usr/bin/env python3

from aws_cdk import core

from sep20cloudguruchallenge.sep20cloudguruchallenge_stack import Sep20CloudguruchallengeStack


app = core.App()
Sep20CloudguruchallengeStack(app, "sep20cloudguruchallenge", env={'region': 'us-west-2'})

app.synth()
