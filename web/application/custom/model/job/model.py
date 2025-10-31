from abc import ABC, abstractmethod
from sklearn.pipeline import Pipeline
import pandas as pd
import joblib
import os




class Model(ABC):

    models_path = 'application/models'
    features:dict = None

    def __init__(self, pickle_name:str) -> None:
        self.model = self.__load_pickle(pickle_name)

    def __load_pickle(self, pickle_name) -> Pipeline:
        pickle_path = os.path.join(self.models_path, pickle_name)
        model = joblib.load(pickle_path)
        return model
    
    def _validate_values(self, values:dict) -> dict:

        valid = self.features # sets default values

        for key, value in values.items():
            if key in self.features:
                valid[key] = value

        return pd.DataFrame([valid])
    
    @abstractmethod
    def predict(self, values:dict) -> dict:
        ...