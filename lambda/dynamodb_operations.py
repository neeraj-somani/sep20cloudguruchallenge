import json
import boto3
import os
from decimal import Decimal
import pandas as pd
from s3_operations import retrieve_from_data_bucket, MissingFileError

# set environment variable
TABLE_NAME = os.environ['TABLE_NAME']
FILE_NAME = os.environ['FILE_NAME']

# Get the service resource.
dynamodb_client_table = boto3.resource("dynamodb").Table(TABLE_NAME)

def load_operation(latest_data: pd.DataFrame):
    try:
        old_data = retrieve_from_data_bucket(FILE_NAME)
    except MissingFileError:
        df = latest_data
    else:
        print('old_data cases: ', old_data.shape) # (395,2)

        print('latest_data cases: ',latest_data.shape) # (395,2)
        df = (
            old_data.merge(
                latest_data,
                how="outer",
                on=["date", "cases", "deaths", "recoveries"],
                indicator=True,
            )
            .loc[lambda x: x["_merge"] == "right_only"]
            .drop("_merge", axis=1)
        )


    new_cases_list = []

    for row in df.itertuples():
        new_cases = {"pk": 'CASES', "date": row.Index.strftime("%Y-%m-%d") , "cases": row.cases, "deaths": row.deaths, "recoveries": row.recoveries}
        new_cases_list.append(new_cases)

        
    with dynamodb_client_table.batch_writer(overwrite_by_pkeys=['pk', 'date']) as batch:
        for new_case_item in new_cases_list:
            batch.put_item(Item=new_case_item)
        
    print('load new_cases completed')



    