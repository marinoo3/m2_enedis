import pandas as pd
import numpy as np

from ..filter import Filter



class Format:

    def _compute_score(self, serie:pd.Series, scale='original') -> pd.Series:

        if serie.size == 1:
            return serie

        if scale == 'log':
            serie = np.log1p(serie)

        score:pd.Series = ((serie - serie.min()) / (serie.max() - serie.min())) * 100

        return score
    
    def _iso_transform(self, serie:pd.Series, as_str=False) -> pd.Series:

        if as_str:
            serie = serie.astype(str)

        serie = serie.apply(lambda x: x.lower().replace(' ', '_'))
        return serie
    
    def _filter(self, df:pd.DataFrame, rules:list[dict]) -> pd.DataFrame:

        df = Filter.apply(df, rules)
        return df