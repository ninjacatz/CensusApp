from ACSAPICall.acsapicall import ACSAPICall

# Travel time to work:
# This question was asked of people who reported
# that they worked outside their home.

# examples:
# B08303 = travel time to work
# _001E = total
# _002E = less than 10 minutes
# _003E = 10-14
# _004E = 15-19
# _005E = 20-24
# _006E = 25-29
# _007E = 30-34
# _008E = 35-44
# _009E = 45-59
# _010E = >60


class ACSTravelTimeCall(ACSAPICall):
    # dataset order after calculations:
    # 0: % under 10
    # 1: % 10-14
    # 2: % 15-19
    # 3: % 20-24
    # 4: % 25-29
    # 5: % 30-34
    # 6: % 35-44
    # 7: % 45-59
    # 8: % over 60
    # 9: total travel time
    # 10: under 10
    # 11: 10-14
    # 12: 15-19
    # 13: 20-24
    # 14: 25-29
    # 15: 30-34
    # 16: 35-44
    # 17: 45-59
    # 18: over 60
    # 19: name
    # 20: geo id
    # 21: state code
    # 22: county code (possibly)
    def __init__(self, is_county: bool):
        # required for "None" problem found below in calculations
        self.is_county = is_county

        # setting up variables for API request
        travel_time = "B08303_"
        self.travel_time_total = travel_time + "001E"
        self.travel_time_under_10 = travel_time + "002E"
        self.travel_time_10_14 = travel_time + "003E"
        self.travel_time_15_19 = travel_time + "004E"
        self.travel_time_20_24 = travel_time + "005E"
        self.travel_time_25_29 = travel_time + "006E"
        self.travel_time_30_34 = travel_time + "007E"
        self.travel_time_35_44 = travel_time + "008E"
        self.travel_time_45_59 = travel_time + "009E"
        self.travel_time_over_60 = travel_time + "010E"

        # var_for_request to be used in calling API
        self.var_for_request = [self.travel_time_total,
                                self.travel_time_under_10,
                                self.travel_time_10_14,
                                self.travel_time_15_19,
                                self.travel_time_20_24,
                                self.travel_time_25_29,
                                self.travel_time_30_34,
                                self.travel_time_35_44,
                                self.travel_time_45_59,
                                self.travel_time_over_60,
                                "NAME",
                                "GEO_ID"
                                ]

        # column names to be used in pandas data frame
        self.column_names = ["travel_time_total",
                             "travel_time_under_10",
                             "travel_time_10_14",
                             "travel_time_15_19",
                             "travel_time_20_24",
                             "travel_time_25_29",
                             "travel_time_30_34",
                             "travel_time_35_44",
                             "travel_time_45_59",
                             "travel_time_over_60",
                             "name",
                             "geo_id"
                             ]

        ACSAPICall.__init__(
            self, is_county, self.var_for_request, self.column_names)

        self.calculate_travel_percentages()

    def calculate_travel_percentages(self):
        # convert population values to int for calculations
        # NOTE: had to use lambda here because of incomplete county data from api (none values)
        for i in range(10):
            self.dataset[self.dataset.columns[i]] = self.dataset[self.dataset.columns[i]].apply(lambda x: int(x) if x is not None else 1)

        # NOTE: had to change index 291, column 0 to 20 because it shows up as "None" from api
        # and changing it to 30 doesn't mess with the map shades too much
        if self.is_county:
            self.dataset.iat[291, 0] = 30

        self.dataset.insert(loc=0, column="%_travel_time_under_10", value='')
        self.dataset["%_travel_time_under_10"] = 100 * self.dataset["travel_time_under_10"] / self.dataset[
            "travel_time_total"]

        self.dataset.insert(loc=1, column="%_travel_time_10_14", value='')
        self.dataset["%_travel_time_10_14"] = 100 * self.dataset["travel_time_10_14"] / self.dataset[
            "travel_time_total"]

        self.dataset.insert(loc=2, column="%_travel_time_15_19", value='')
        self.dataset["%_travel_time_15_19"] = 100 * self.dataset["travel_time_15_19"] / self.dataset[
            "travel_time_total"]

        self.dataset.insert(loc=3, column="%_travel_time_20_24", value='')
        self.dataset["%_travel_time_20_24"] = 100 * self.dataset["travel_time_20_24"] / self.dataset[
            "travel_time_total"]

        self.dataset.insert(loc=4, column="%_travel_time_25_29", value='')
        self.dataset["%_travel_time_25_29"] = 100 * self.dataset["travel_time_25_29"] / self.dataset[
            "travel_time_total"]

        self.dataset.insert(loc=5, column="%_travel_time_30_34", value='')
        self.dataset["%_travel_time_30_34"] = 100 * self.dataset["travel_time_30_34"] / self.dataset[
            "travel_time_total"]

        self.dataset.insert(loc=6, column="%_travel_time_35_44", value='')
        self.dataset["%_travel_time_35_44"] = 100 * self.dataset["travel_time_35_44"] / self.dataset[
            "travel_time_total"]

        self.dataset.insert(loc=7, column="%_travel_time_45_59", value='')
        self.dataset["%_travel_time_45_59"] = 100 * self.dataset["travel_time_45_59"] / self.dataset[
            "travel_time_total"]

        self.dataset.insert(loc=8, column="%_travel_time_over_60", value='')
        self.dataset["%_travel_time_over_60"] = 100 * self.dataset["travel_time_over_60"] / self.dataset[
            "travel_time_total"]
