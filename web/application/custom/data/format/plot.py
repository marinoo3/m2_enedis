import pandas as pd

from .format import Format



class PlotFormater(Format):

    logements:pd.DataFrame = None

    def __init__(self, logements):
        self.set_logements(logements)

    def set_logements(self, logements) -> None:
        self.logements = logements

    def get_selected(self, filters:list[dict]=None) -> pd.DataFrame:

        selected_columns = [
            'numero_dpe',                          # Identifiant unique du DPE
            'code_insee_ban',                      # Code commune
            'nom_commune_ban',                     # Nom de la commune
            'etiquette_dpe',                       # Classe énergétique (A à G)
            'conso_5_usages_par_m2_ep',            # Consommation en kWh/m²/an
            'surface_habitable_logement',          # Surface en m² (pour calculs de coûts)
            'type_batiment',                       # Maison ou appartement
            'periode_construction',                # Époque de construction
            'periode_categorie',                   # Categorie de periode de construction
            'type_energie_principale_chauffage',   # Type de chauffage utilisé
            'altitude_moyenne',                    # Altitude moyenne (déjà dans le DPE)
            'classe_altitude',                     # Classe d'altitude
            'categorie_dpe'                        # Categorie DPE simplifiées
        ]

        return self.logements[selected_columns]