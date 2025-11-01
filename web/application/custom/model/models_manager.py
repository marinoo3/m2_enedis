from .job import ConsommationModel, PassoireModel

import time



"""

Dev comment:
Docstrings in this class endup epic

"""




class ModelsManager():

    consommation = ConsommationModel()
    passoire = PassoireModel()

    def load_consommation(self) -> None:

        """Load ConsommationModel is not loaded yet"""

        if self.consommation.model is None:
            self.consommation.load()

    def load_passoire(self) -> None:

        """Load PassoireModel is not loaded yet"""

        if self.passoire.model is None:
            self.passoire.load()

    def get_features(self, model) -> dict:

        """Retrive a dict of features from a model

        Arguments:
            model {str} -- the name of the model ['consommation', 'passoire']

        Returns:
            dict: Features of the model
        """

        if model == 'consommation':
            return self.consommation.features.copy()
        elif model == 'passoire':
            return self.passoire.features.copy()

    def predict_consommation(self, values) -> tuple[float, float]:

        """Predict the consumption of the accomodation

        Arguments:
            values {dict} -- The accomodation values to pass to the model

        Returns:
            float: Predicted consumption
            float: Inference duration
        """

        # Load ConsommationModel if not loaded yet
        self.load_consommation()

        start_time = time.perf_counter()
        response = self.consommation.predict(values)
        total_time = round(time.perf_counter() - start_time, 3)

        return response['result'], total_time
    
    def predict_passoire(self, values) -> tuple[bool, float]:

        """Predict the wether the accomodation is a passoire or not

        Arguments:
            values {dict} -- The accomodation values to pass to the model

        Returns:
            bool: Is a passoire
            float: Inference duration
        """

        # Load PassoireModel if not loaded yet
        self.load_passoire()

        start_time = time.perf_counter()
        response = self.passoire.predict(values)
        total_time = round(time.perf_counter() - start_time, 3)

        return bool(response['result']), total_time

