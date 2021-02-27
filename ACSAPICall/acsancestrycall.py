from ACSAPICall.acsapicall import ACSAPICall


# Ancestry:
# The ancestry question allowed respondents to report
# one or more ancestry groups. Generally, only the
# first two responses reported were coded.

# variables from ACS examples:
# B04006 = people reporting ancestry
# B04004 = people reporting single ancestry
# B04005 = people reporting multiple ancestry
# 089E = swedish
# B04004_089E = people reporting swedish as a single ancestry

# NOTE: initialize with ancestry variable (ex. for swedish: "089E")
# ^^^ use dictionary found at bottom of file


class ACSAncestryCall(ACSAPICall):
    # dataset order after calculations:
    # 0: % total
    # 1: % single
    # 2: % multiple
    # 3: total pop
    # 4: total ancestry
    # 5: total single
    # 6: total multiple
    # 7: name
    # 8: geo id
    # 9: state code
    # 10: county code (possibly)
    def __init__(self, ancestry_var: str, is_county: bool):
        # setting up variables for API request
        self.total_ancestry = "B04006_" + ancestry_var
        self.single_ancestry = "B04004_" + ancestry_var
        self.multiple_ancestry = "B04005_" + ancestry_var

        # var_for_request to be used in calling API
        self.var_for_request = [self.total_pop_var,
                                self.total_ancestry,
                                self.single_ancestry,
                                self.multiple_ancestry,
                                "NAME",
                                "GEO_ID"
                                ]

        # column names to be used in pandas data frame
        self.column_names = ["total_pop",
                             "total_ancestry_pop",
                             "single_ancestry_pop",
                             "multiple_ancestry_pop",
                             "name",
                             "geo_id"
                             ]

        ACSAPICall.__init__(self, is_county, self.var_for_request, self.column_names)

        self.calculate_ancestry_percentages()

    def calculate_ancestry_percentages(self):
        # convert population values to int for calculations
        for i in range(4):
            self.dataset[self.dataset.columns[i]] = self.dataset[self.dataset.columns[i]].astype(int)

        # create column in dataset for percent total ancestry
        self.dataset.insert(loc=0, column="%_total_ancestry", value='')
        self.dataset["%_total_ancestry"] = 100 * self.dataset["total_ancestry_pop"] / self.dataset["total_pop"]

        # create column in dataset for percent single ancestry
        self.dataset.insert(loc=1, column="%_single_ancestry", value='')
        self.dataset["%_single_ancestry"] = 100 * self.dataset["single_ancestry_pop"] / self.dataset["total_pop"]

        # create column in dataset for percent multiple ancestry
        self.dataset.insert(loc=2, column="%_multiple_ancestry", value='')
        self.dataset["%_multiple_ancestry"] = 100 * self.dataset["multiple_ancestry_pop"] / self.dataset["total_pop"]


# simple dictionary for easily accessing ancestry variables by name
ancestry = {"total": "001E",
            "afghan": "002E",
            "albanian": "003E",
            "alsatian": "004E",
            "american": "005E",
            "arab_total": "006E",
            "arab_egyptian": "007E",
            "arab_iraqi": "008E",
            "arab_jordanian": "009E",
            "arab_lebanese": "010E",
            "arab_moroccan": "011E",
            "arab_palestinian": "012E",
            "arab_syrian": "013E",
            "arab_arab": "014E",
            "arab_other": "015E",
            "armenian": "016E",
            "assyrian/chaldean/syriac": "017E",
            "australian": "018E",
            "austrian": "019E",
            "basque": "020E",
            "belgian": "021E",
            "brazilian": "022E",
            "british": "023E",
            "bulgarian": "024E",
            "cajun": "025E",
            "canadian": "026E",
            "carpatho_rusyn": "027E",
            "celtic": "028E",
            "croatian": "029E",
            "cypriot": "030E",
            "czech": "031E",
            "czechoslovakian": "032E",
            "danish": "033E",
            "dutch": "034E",
            "eastern_european": "035E",
            "english": "036E",
            "estonian": "037E",
            "european": "038E",
            "finnish": "039E",
            "french_except_basque": "040E",
            "french_canadian": "041E",
            "german": "042E",
            "german_russian": "043E",
            "greek": "044E",
            "guyanese": "045E",
            "hungarian": "046E",
            "icelander": "047E",
            "iranian": "048E",
            "irish": "049E",
            "israeli": "050E",
            "italian": "051E",
            "latvian": "052E",
            "lithuanian": "053E",
            "luxembourger": "054E",
            "macedonian": "055E",
            "maltese": "056E",
            "new_zealander": "057E",
            "northern_european": "058E",
            "norwegian": "059E",
            "pennsylvania_german": "060E",
            "polish": "061E",
            "portuguese": "062E",
            "romanian": "063E",
            "russian": "064E",
            "scandinavian": "065E",
            "scotch-irish": "066E",
            "scottish": "067E",
            "serbian": "068E",
            "slavic": "069E",
            "slovak": "070E",
            "slovene": "071E",
            "soviet_union": "072E",
            "subsaharan_african_total": "072E",
            "subsaharan_african_cape_verdean": "074E",
            "subsaharan_african_ethiopian": "075E",
            "subsaharan_african_ghanian": "076E",
            "subsaharan_african_kenyan": "077E",
            "subsaharan_african_liberian": "078E",
            "subsaharan_african_nigerian": "079E",
            "subsaharan_african_senegalese": "080E",
            "subsaharan_african_sierra_leonean": "081E",
            "subsaharan_african_somali": "082E",
            "subsaharan_african_south_african": "083E",
            "subsaharan_african_sudanese": "084E",
            "subsaharan_african_ugandan": "085E",
            "subsaharan_african_zimbabwean": "086E",
            "subsaharan_african_african": "087E",
            "subsaharan_african_other_subsaharan_african": "088E",
            "swedish": "089E",
            "swiss": "090E",
            "turkish": "091E",
            "ukranian": "092E",
            "welsh": "093E",
            "west_indian_except_hispanic_groups_total": "094E",
            "west_indian_except_hispanic_groups_bahamian": "095E",
            "west_indian_except_hispanic_groups_barbadian": "096E",
            "west_indian_except_hispanic_groups_belizean": "097E",
            "west_indian_except_hispanic_groups_bermudan": "098E",
            "west_indian_except_hispanic_groups_british_west_indian": "099E",
            "west_indian_except_hispanic_groups_dutch_west_indian": "100E",
            "west_indian_except_hispanic_groups_haitian": "101E",
            "west_indian_except_hispanic_groups_jamaican": "102E",
            "west_indian_except_hispanic_groups_trinidadian_and_tobagonian": "103E",
            "west_indian_except_hispanic_groups_us_virgin_islander": "104E",
            "west_indian_except_hispanic_groups_west_indian": "105E",
            "west_indian_except_hispanic_groups_other_west_indian": "106E",
            "yugoslavian": "107E",
            "other_groups": "108E",
            "unclassified_or_not_reported": "109E",
            }
