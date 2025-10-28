from .figures import Scatter, Box, Bar, BarDPE, HeatMap


import pandas as pd




class PlotsManager():

    scatter:Scatter = None
    box:Box = None
    bar:Bar = None
    bar_dpe: BarDPE = None
    heatmap:HeatMap = None

    def __load(self, df:pd.DataFrame) -> None:
        self.scatter = Scatter(df)
        self.box = Box(df)
        self.bar = Bar(df)
        self.bar_dpe = BarDPE(df)
        self.heatmap = HeatMap(df)

    def load_plots(self, df) -> None:

        """Load the plots from a dataframe
        
        Arguments:
            df {pd.DataFrame} -- DataFrame to load the plots from
        """

        self.__load(df)

    def get_jsons(self, df:pd.DataFrame=None) -> dict:

        """Returns a formatted dict containing plot jsons to display on HTML

        Keyword Arguments:
            df {pd.DataFrame} -- a DataFrame to load the plots from if provided (default: None)

        Returns:
            dict: Json plots
        """

        if df is not None:
            self.__load(df)

        jsons = {
            'scatterPlot': self.scatter.get_json(),
            'boxPlot': self.box.get_json(),
            'barPlot': self.bar.get_json(),
            'barDPEPlot': self.bar_dpe.get_json(),
            'heatmapPlot': self.heatmap.get_json()
        }

        return jsons