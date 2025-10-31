from .model import Model



class PassoireModel(Model):

    pickle_name = 'classification_randomforest_20251031_191718.pkl'

    features = {
        'surface_habitable_logement': None,
        'periode_construction': None,
        'type_batiment': None,
        'qualite_isolation_enveloppe': None,
        'type_energie_principale_chauffage': None,
        'logement_traversant': None,
        'protection_solaire_exterieure': None,
        'zone_climatique': None,
        'classe_altitude': None
    }

    def load(self):
        self._load(self.pickle_name)

    def predict(self, values):
        valid_values = self._validate_values(values)

        result = self.model.predict(valid_values)
        return {'result': result[0]}