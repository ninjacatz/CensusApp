import requests
import pandas as pd


class ACSAPICall:
    # API url for US Census American Community Survey 5-Year Data (2009-2018)
    host = "https://api.census.gov/data"
    year = "2018"
    data = "acs/acs5"
    acs_base_url = "/".join([host, year, data])

    # total_pop_var is always "B00001_001E"
    total_pop_var = "B01001_001E"

    # TODO: DELETE LATER: getting pandas to print entire dataset
    pd.set_option("display.max_rows", None, "display.max_columns", None)

    def __init__(self, is_county: bool, var_for_request: [], column_names: []):
        self.var_for_request = var_for_request
        self.column_names = column_names

        self.dataset = pd.DataFrame()
        self.parameters = {}

        # call appropriate methods based on is_county boolean value
        if is_county:
            self.set_data_by_county("*", "*")
        else:
            self.set_data_by_state("*")

        self.request_data_from_API()

    # ---set_data_by_county---
    # parameters:
    # county_var: can be county code or "*" wildcard
    # state_var: can be state code or "*" wildcard
    # NOTE: county_var and state_var can both be wildcards,
    # but state cannot be wildcard if county is defined
    def set_data_by_county(self, county_var: str, state_var: str):
        # set up dictionary containing parameters for API request
        self.parameters = {"get": ",".join(self.var_for_request),
                           "for": "county:" + county_var,
                           "in": "state:" + state_var
                           }

        # set column_names to include state and county codes
        self.column_names.append("state_code")
        self.column_names.append("county_code")

    # ---set_data_by_county---
    # parameters:
    # state_var: can be state code or "*" wildcard
    def set_data_by_state(self, state_var: str):
        # set up dictionary containing parameters for API request
        self.parameters = {"get": ",".join(self.var_for_request),
                           "for": "state:" + state_var
                           }

        # create column to include state_code
        self.column_names.append("state_code")

    # ---request_data_from_API---
    # simply requests the data from the API using the url and parameters given
    # and passes the data into the DataFrame ([1:] used to ignore headers)
    def request_data_from_API(self):
        r = requests.get(self.acs_base_url, params=self.parameters)
        self.dataset = pd.DataFrame(data=r.json()[1:], columns=self.column_names)
