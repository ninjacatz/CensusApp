from ACSAPICall.acsapicall import ACSAPICall


# Household: A household includes all the people who occupy a housing unit.
# A housing unit is a house, an apartment, a mobile home, a group of rooms, or a single room.

# examples:
# DP02 = households by type
# _0001E = total
# _0002E = family
# _0003E = family (with children under 18)
# _0004E = family (married couple)
# _0005E = family (married with children under 18)
# _0006E = family (male no wife)
# etc.. etc..


class ACSHouseHoldTypeCall(ACSAPICall):
    def __init__(self, household_type_var: str, is_county: bool):
        self.is_county = is_county

        # for household data, must include "profile" at end of base url
        self.acs_base_url += "/profile"

        # setting up variables for API request
        self.total_household_var = "DP02_0001E"
        self.household_type_var = "DP02_" + household_type_var

        # var_for_request to be used in calling API
        self.var_for_request = [self.total_household_var,
                                self.household_type_var,
                                "NAME",
                                "GEO_ID"
                                ]

        # column names to be used in pandas data frame
        self.column_names = ["total_households",
                             "household_type_pop",
                             "name",
                             "geo_id"
                             ]

        ACSAPICall.__init__(self, is_county, self.var_for_request, self.column_names)

        self.calculate_household_percentages()

    def calculate_household_percentages(self):
        # convert population values to int for calculations
        for i in range(2):
            self.dataset[self.dataset.columns[i]] = self.dataset[self.dataset.columns[i]].apply(lambda x: int(x) if x is not None else 1)

        # fixing "None" values that were replaced with "1" (puerto rico is the culprit)
        if self.is_county:
            # 2473 - 2494 AND 896 - 951
            for i in range(2473, 2495):
                self.dataset.iat[i, 0] = 30
            for i in range(896, 952):
                self.dataset.iat[i, 0] = 30
        else:
            self.dataset.iat[28, 0] = 30


        # create column in dataset for percent "household_type_var"
        self.dataset.insert(loc=0, column="%_household_type", value='')
        self.dataset["%_household_type"] = 100 * self.dataset["household_type_pop"] / self.dataset["total_households"]


# for more... https://api.census.gov/data/2018/acs/acs5/profile/groups/DP02.html
households = {"family": "0002E",
              "family_with_children": "0003E",
              "married": "0004E",
              "married_with_children": "0005E",
              "male_no_wife": "0006E",
              "male_no_wife_with_children": "0007E",
              "female_no_husband": "0008E",
              "female_no_husband_with_children": "0009E",
              "non-family": "0010E",
              "non-family_living_alone": "0011E",
              "non-family_living_alone_over_65": "0012E",
              }
