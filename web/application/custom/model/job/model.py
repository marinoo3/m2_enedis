from abc import ABC, abstractmethod


from sklearn.pipeline import Pipeline
import pandas as pd
import joblib
import os




class Model(ABC):

    models_path = 'application/models'
    model:Pipeline = None
    features:dict = None

    def _load(self, pickle_name) -> None:
        pickle_path = os.path.join(self.models_path, pickle_name)
        model = joblib.load(pickle_path)
        self.model = model
    
    def _validate_values(self, values:dict) -> dict:

        valid = self.features # sets default values

        for key, value in values.items():
            if key in self.features:
                valid[key] = value

        return pd.DataFrame([valid])
    
    @abstractmethod
    def load(self) -> None:
        ...
    
    @abstractmethod
    def predict(self, values:dict) -> dict:
        ...