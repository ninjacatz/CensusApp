class DCAPICall:
    # API url for US Census Decennial Census (2010)
    host = "https://api.census.gov/data"
    year = "2010"
    data = "dec/sf1"
    dc_base_url = "/".join([host, year, data])

    # total_pop_var is always "P001001"
    total_pop_var = "P001001"