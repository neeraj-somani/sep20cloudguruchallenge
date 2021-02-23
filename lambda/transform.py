from pandas import DataFrame


def merge_cases_with_recoveries(cases: DataFrame, recoveries: DataFrame) -> DataFrame:

    print('I am inside merge function')
    
    return (
        cases.join(recoveries, how="inner", on="date")
        .fillna(0)
        .rename(columns={"Recovered": "recoveries"})
        .astype({"recoveries": "int"})
        .drop("country_region", axis=1)
    )