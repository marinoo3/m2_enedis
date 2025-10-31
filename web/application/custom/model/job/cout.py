from .model import Model



class CoutModel(Model):

    pickle_name = 'regression_gradientboosting_20251029_145215.pkl'

    features = {
        'surface_habitable_logement': '1975-1989',
        'periode_construction': None,
        'type_batiment': None,
        'qualite_isolation_enveloppe': None,
        'type_energie_principale_chauffage': None,
        'logement_traversant': None,
        'protection_solaire_exterieure': None,
        'zone_climatique': None,
        'classe_altitude': None,
        'apport_interne_saison_chauffe': 200
    }

    def __init__(self):
        super().__init__(self.pickle_name)

    def predict(self, values):
        valid_values = self._validate_values(values)

        result = self.model.predict(valid_values)
        return {'result': result[0]}