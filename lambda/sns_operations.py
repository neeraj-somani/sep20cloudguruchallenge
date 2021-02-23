import os
import boto3
# from us_covid_stats.config.settings import FRONTEND_URL, NOTIFICATION_TOPIC

# set environment variable
NOTIFICATION_TOPIC_ARN = os.environ['NOTIFICATION_TOPIC_ARN']

sns = boto3.resource("sns")
topic = sns.Topic(NOTIFICATION_TOPIC_ARN)


def notify(event_json):
    message = event_json
    '''(
        event["responsePayload"]
        if isinstance(event["responsePayload"], str)
        else json.dumps(event["responsePayload"].get("errorMessage"))
    )
    '''

    topic.publish(
        Message='This is just a test message after ETL job completed', ##" ".join([message, f"View dashboard at {FRONTEND_URL}."]),
        Subject="Data refresh successful.",
        MessageAttributes={
            "condition": {
                "DataType": "String",
                "StringValue": event_json #'This is just a test message', ## event_json ## ["requestContext"]["condition"],
            }
        },
    )

'''
def on_refresh_data_from_sources(event: DestinationEvent, context: Any) -> None:
    message = (
        event["responsePayload"]
        if isinstance(event["responsePayload"], str)
        else json.dumps(event["responsePayload"].get("errorMessage"))
    )
    notify(
        message=message,
        condition=event["requestContext"]["condition"],
    )
'''