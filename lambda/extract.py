import json
import pandas as pd
#from typing import Any, Mapping, Dict, Union

RAW_GITHUB_HOST = "https://raw.githubusercontent.com"

# New York Times Data
US_CASES_URL = f"{RAW_GITHUB_HOST}/nytimes/covid-19-data/master/us.csv"

# John Hopkins Data
WORLD_RECOVERIES_URL = (
    f"{RAW_GITHUB_HOST}/datasets/covid-19/master/data/time-series-19-covid-combined.csv"
)


class ExtractedData():
        cases: pd.DataFrame
        recoveries: pd.DataFrame
        
def extract_data_from_sources() -> ExtractedData :
        print("I'm running inside extract function! ")


        us_cases = pd.read_csv(US_CASES_URL, index_col="date",
                parse_dates=True)


        us_recoveries = pd.read_csv(WORLD_RECOVERIES_URL, usecols=['Date', 'Country/Region', 'Recovered'],
                index_col='Date',
                parse_dates=True)

        us_recoveries = us_recoveries.rename({'Country/Region': 'country_region'}, axis=1)

        us_recoveries = us_recoveries[us_recoveries['country_region']=='US']

        print('(386,2) total us cases: ', us_cases.shape) # (386,2)

        print('(385,2) total us recoveries: ',us_recoveries.shape) # (385,2)

        return {
                "cases": us_cases,
                "recoveries": us_recoveries,
        }