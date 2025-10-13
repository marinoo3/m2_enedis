import plotly.express as px
from plotly import utils
import pandas as pd

import json





class Plots():

    def __init__(self):
        pass

    def test_plot(self, df:pd.DataFrame) -> dict:
        fig = px.scatter(df, x='nombre_de_logements', y='conso_total_mwh', 
                 title='Nombre de Logements vs Conso Total MWh', 
                 labels={'nombre_de_logements': 'Nombre de Logements', 
                         'conso_total_mwh': 'Conso Total (MWh)'})
        fig_json = json.dumps(fig, cls=utils.PlotlyJSONEncoder)
        return fig_json