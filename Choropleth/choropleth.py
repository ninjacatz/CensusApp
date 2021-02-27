import pandas as pd
import plotly.express as px


class Choropleth:
    def __init__(self, dataset: pd.DataFrame, geojson_list: [dict], is_county: bool, data_index: int):
        self.dataset = dataset
        self.geojson_list = geojson_list
        self.is_county = is_county
        self.data_index = data_index
        self.fig = px.choropleth

        # select geojson to use in __plot_map
        if is_county:
            self.geojson = geojson_list[1]
        else:
            self.geojson = geojson_list[0]

        self.__plot_map()

    def __plot_map(self):
        self.fig = px.choropleth(data_frame=self.dataset,
                                 locations='geo_id',
                                 geojson=self.geojson,
                                 featureidkey='properties.GEO_ID',
                                 color=self.dataset[self.dataset.columns[self.data_index]],
                                 hover_name='name',
                                 scope='usa')
