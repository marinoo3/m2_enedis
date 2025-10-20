import pandas as pd
import numpy as np
from datetime import datetime

from .volume import Volume
from .filter import Filter




class Data():

    def __init__(self):
        self.communes = self.__load_communes()
        self.cities = self.__load_cities()

    def __load_communes(self) -> pd.DataFrame:
        return Volume.read_communes()
    
    def __load_cities(self) -> pd.DataFrame:
        df = pd.read_csv('application/datasets/communes-france-2025.csv', low_memory=False)
        df['code_insee'] = df['code_insee'].astype(str)
        return df
    
    def __compute_score(self, serie:pd.Series, scale='original') -> pd.Series:

        if serie.size == 1:
            return serie

        if scale == 'log':
            serie = np.log1p(serie)

        score:pd.Series = ((serie - serie.min()) / (serie.max() - serie.min())) * 100

        return score
    

    def get_property(self, key) -> str:

        """Read properties from Koyeb volume

        Returns:
            dict: Volume properties
        """

        properties = Volume.read_properties()
        return properties[key]
    

    def get_communes(self) -> pd.DataFrame:

        """Returns raw communes data

        Returns:
            pd.DataFrame: Raw communes data
        """

        return self.communes
    

    def update_communes(self, communes:list[dict]) -> None:

        """Update the communes dataset on Koyeb volume and reload communes"""

        df = pd.DataFrame(communes)
        Volume.write_communes(df)
        # Reload communes
        self.communes = self.__load_communes()

        # Update volume update date property
        properties = Volume.read_properties()
        properties['update'] = datetime.now().strftime('%d-%m-%Y')
        Volume.write_properties(properties)
    

    def get_map(self, filters:list[dict]=None, sort:dict=None) -> list[dict]:
        
        """Completes communes data from Enedis API with data from cities dataset (coordinates and names)

        Keyword Arguments
            filters {list[dict]} -- List of filter rules (default None)
            sort {dict} -- How to sort the data (default None)

        Returns:
            list[dict]: Communes formatted for the map
        """

        # Copy self.communes
        communes = self.communes

        # Keep only unique `code_commune_INSEE` as index
        cities = self.cities.drop_duplicates('code_insee').set_index('code_insee')

        # Retrieve coordinates from cities dataset and drop not found cities
        communes['latitude'] = communes.code_commune.map(cities.latitude_centre)
        communes['longitude'] = communes.code_commune.map(cities.longitude_centre)
        communes.dropna(subset=['latitude', 'longitude'], inplace=True) # if a place coordinates cannot be found in the dataset, then drop
        # Retrieve altitude, city names, density and superficy, from cities dataset
        communes['altitude'] = communes.code_commune.map(cities.altitude_maximale)
        communes['nom_commune'] = communes.code_commune.map(cities.nom_standard)
        communes['densite'] = communes.code_commune.map(cities.densite)
        communes['superficie_km2'] = communes.code_commune.map(cities.superficie_km2)

        # Compute average consumption per inhabitant.
        communes['conso_moyenne_mwh'] = communes['conso_total_mwh'] / communes['nombre_de_logements']
        # Compute scores
        communes['score_moyenne_conso'] = self.__compute_score(communes['conso_moyenne_mwh'], scale='log')
        communes['score_total_conso'] = self.__compute_score(communes['conso_total_mwh'], scale='log')

        # Rounding `conso_total_mwh` and `conso_moyenne_mwh` to 3 decimal places
        communes['conso_total_mwh'] = communes['conso_total_mwh'].round(3)
        communes['conso_moyenne_mwh'] = communes['conso_moyenne_mwh'].round(3)
        # Rounding average year
        communes['annee'] = communes['annee'].round()

        # Filters the data if filters provided
        if filters:
            fls = Filter(filters)
            communes = fls.compute(communes)

        # Compute scales (max and min)
        scales = {
            'altitude': {
                'max': communes['altitude'].max(),
                'min': communes['altitude'].min()
            },
            'densite': {
                'max': communes['densite'].max(),
                'min': communes['altitude'].min()
            }
        }

        # Format and return output
        formatted = communes.fillna('NA').to_dict(orient='records')

        return formatted, scales
    
    
    def get_zoomed_map(self, streets:list[dict], iris:list[dict]) -> list[dict]:

        """Completes iris data from Enedis API with insee data from Ademe API (coordinates and postal codes)

        Arguments
            streets {list[dict]} -- List of streets data from Ademe
            iris {list[dict]} -- List of iris data from Enedis

        Returns:
            list[dict]: Irises formatted for the map
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
        iris.dropna(subset=['latitude', 'longitude', 'conso_total_mwh', 'nombre_de_logements'], inplace=True)

        # Compute average consumption per inhabitant.
        iris['conso_moyenne_mwh'] = iris['conso_total_mwh'] / iris['nombre_de_logements']
        # Compute scores
        iris['score_moyenne_conso'] = self.__compute_score(iris['conso_moyenne_mwh'], scale='log')
        iris['score_total_conso'] = self.__compute_score(iris['conso_total_mwh'], scale='log')

        # Format and return output
        formatted = iris.to_dict(orient='records')
        return formatted


