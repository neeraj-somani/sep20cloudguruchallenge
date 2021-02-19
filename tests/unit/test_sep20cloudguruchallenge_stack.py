import json
import pytest

from aws_cdk import core
from sep20cloudguruchallenge.sep20cloudguruchallenge_stack import Sep20CloudguruchallengeStack


def get_template():
    app = core.App()
    Sep20CloudguruchallengeStack(app, "sep20cloudguruchallenge")
    return json.dumps(app.synth().get_stack("sep20cloudguruchallenge").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
