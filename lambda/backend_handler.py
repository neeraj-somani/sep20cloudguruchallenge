import json
#from typing import Any, Mapping , Dict, Union
from extract import extract_data_from_sources
from transform import merge_cases_with_recoveries
from dynamodb_operations import load_operation
from s3_operations import save_data_to_s3
from sns_operations import notify

def refresh_data_from_sources(event, context) -> str:
    
    print('request: {}'.format(json.dumps(event)))

    extracted = extract_data_from_sources()

    transformed = merge_cases_with_recoveries(**extracted)
    print('I am inside handler and shape of transformed dataframe is: ', transformed.shape)

    print('I am loading data into dynamodb')
    load_operation(transformed)
    
    print('I am saving data into s3')
    save_data_to_s3(transformed)

    print('trying to print event before passing it to SNS event notification')

    event_json = json.dumps(event)
    
    print('I am notify users after todays ETL run')
    notify(event_json)