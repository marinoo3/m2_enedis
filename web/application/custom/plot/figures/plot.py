from abc import ABC, abstractmethod

import pandas as pd
import plotly.graph_objects as go
from plotly import utils

import json



class Plot(ABC):

    COULEURS_DPE = {
        'A': '#00A651',
        'B': '#50B847',
        'C': '#C8D220',
        'D': '#FDEE00',
        'E': '#FEB700',
        'F': '#F0832A',
        'G': '#ED1C24'
    }

    SEUILS_ALTITUDE = [600, 1200, 1800, 2500]

    LABELS_ALTITUDE = [
        "0-600m (Vallée)",
        "600-1200m (Colline)",
        "1200-1800m (Montagne)",
        "1800-2500m (Haute montagne)",
        ">2500m (Très haute montagne)"
    ]

    COULEURS_ALTITUDE = {
        "0-600m (Vallée)": '#27ae60',
        "600-1200m (Colline)": '#f39c12',
        "1200-1800m (Montagne)": '#e74c3c',
        "1800-2500m (Haute montagne)": '#9b59b6',
        ">2500m (Très haute montagne)": '#34495e'
    }

    TAILLE_ECHANTILLON = 10000
    PRIX_ELECTRICITE = 0.20  # €/kWh
    SURFACE_REFERENCE = 70  # m²


    def __init__(self, df):
        self.df = self._validate_data(df)
        self.fig = self._create_plot()


    @abstractmethod
    def _validate_data(self, df:pd.DataFrame) -> pd.DataFrame:
        ...

    @abstractmethod
    def _create_plot(self) -> go.Figure:
        ...


    def get_json(self) -> str:
        fig_json = json.dumps(self.fig, cls=utils.PlotlyJSONEncoder)
        return fig_json

