from .job import CoutModel, PassoireModel



"""

Dev comment:
Docstrings in this class endup epic

"""




class ModelsManager():

    cout: CoutModel = None
    passoire: PassoireModel = None

    def load_cout(self) -> None:

        """Load CoutModel is not loaded yet"""

        if self.cout is None:
            self.cout = CoutModel()

    def load_passoire(self) -> None:

        """Load PassoireModel is not loaded yet"""

        if self.passoire is None:
            self.passoire = PassoireModel()

    def predict_cout(self, values) -> float:

        """Predict the cost of the accomodation

        Arguments:
            values {dict} -- The accomodation values to pass to the model

        Returns:
            float: Predicted cost
        """

        # Load CoutModel if not loaded yet
        self.load_cout()

        response = self.cout.predict(values)
        return response['result']
    
    def predict_passoire(self, values) -> bool:

        """Predict the wether the accomodation is a passoire or not

        Arguments:
            values {dict} -- The accomodation values to pass to the model

        Returns:
            bool: Is a passoire
        """

        # Load CoutModel if not loaded yet
        self.load_passoire()

        response = self.passoire.predict(values)
        return bool(response['result'])

