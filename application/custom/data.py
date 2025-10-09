import pandas as pd
import numpy as np


class Data():

    def __init__(self):
        self.communes = self.__load_communes()
        self.cities = self.__load_cities()

    def __load_communes(self) -> pd.DataFrame:
        df = pd.read_csv('application/data/communes.csv')
        df['code_commune'] = df['code_commune'].astype(str)
        return df
    
    def __load_cities(self) -> pd.DataFrame:
        df = pd.read_csv('application/data/20230823-communes-departement-region.csv')
        df['code_commune_INSEE'] = df['code_commune_INSEE'].astype(str)
        return df
    
    def __compute_score(self, serie:pd.Series, scale='original') -> pd.Series:

        if serie.size == 1:
            return serie

        if scale == 'log':
            serie = np.log1p(serie)

        score:pd.Series = ((serie - serie.min()) / (serie.max() - serie.min())) * 100

        return score


    def get_map_data(self) -> list:

        """
        Completes communes data from Enedis API with data from cities dataset (coordinates and names)
        Returns a list of commune formatted for the map
        """

        # Copy self.communes
        communes = self.communes

        # Keep only unique `code_commune_INSEE` as index
        cities = self.cities.drop_duplicates('code_commune_INSEE').set_index('code_commune_INSEE')

        # Retrieve coordinates from cities dataset and drop not found cities
        communes['latitude'] = communes.code_commune.map(cities.latitude)
        communes['longitude'] = communes.code_commune.map(cities.longitude)
        communes.dropna(subset=['latitude', 'longitude'], inplace=True) # if a place coordinates cannot be found in the dataset, then drop
        # Retrieve cities name
        communes['nom_commune'] = communes.code_commune.map(cities.nom_commune_postal)

        # Compute average consumption per inhabitant.
        communes['conso_moyenne_mwh'] = communes['conso_total_mwh'] / communes['nombre_de_logements']
        # Compute scores
        communes['score_moyenne_conso'] = self.__compute_score(communes['conso_moyenne_mwh'], scale='log')
        communes['score_total_conso'] = self.__compute_score(communes['conso_total_mwh'], scale='log')

        # Format and return output
        formatted = communes.to_dict(orient='records')
        return formatted
    
    def zoomed_map_data(self, streets:list[dict], iris:list[dict]) -> list:

        """
        Completes iris data from Enedis API with insee data from edeme API (coordinates and postal codes)
        Returns a list of iris formatted for the map
        """

        def iso_transform(s):
            return s.lower().replace(' ', '_')

        # Convert list to DataFrames
        streets:pd.DataFrame = pd.DataFrame(streets)
        iris:pd.DataFrame = pd.DataFrame(iris)

        streets['voie_iso'] = streets['nom_rue_ban'].astype(str).apply(iso_transform)
        # Keep only unique `insee_code` as index
        streets = streets.drop_duplicates('voie_iso').set_index('voie_iso')
        # Split latitudes and longitudes
        streets[['latitude', 'longitude']] = streets['_geopoint'].str.split(',', expand=True)

        # Create voie_iso column from code_iris
        iris['voie_iso'] = iris['type_de_voie'].astype(str) + ' ' + iris['libelle_de_voie'].astype(str)
        iris['voie_iso'] = iris['voie_iso'].apply(iso_transform)
        # Add coordinates to iris DataFrame
        iris['latitude'] = iris.voie_iso.map(streets.latitude)
        iris['longitude'] = iris.voie_iso.map(streets.longitude)
        # Add postal code to iris DataFrame
        iris['code_postal'] = iris.voie_iso.map(streets.code_postal_ban)

        # Drop NAs
        _not_na = iris['voie_iso'].notna().sum()
        #print(f'{_not_na}/{iris.shape[0]} found, increase requests size to improve')
        iris.dropna(subset=['latitude', 'longitude', 'conso_total_mwh', 'nombre_de_logements'], inplace=True)

        # Compute average consumption per inhabitant.
        iris['conso_moyenne_mwh'] = iris['conso_total_mwh'] / iris['nombre_de_logements']
        # Compute scores
        iris['score_moyenne_conso'] = self.__compute_score(iris['conso_moyenne_mwh'], scale='log')
        iris['score_total_conso'] = self.__compute_score(iris['conso_total_mwh'], scale='log')

        if iris['score_moyenne_conso'].isna().any():
            print("is NaN")
            print(iris['conso_moyenne_mwh'].values)
            print(iris['score_moyenne_conso'].values)

        # Format and return output
        formatted = iris.to_dict(orient='records')
        return formatted


