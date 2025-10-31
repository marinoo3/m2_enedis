import pandas as pd
from scipy.spatial.distance import cdist
from datetime import datetime

from ..volume import Volume
from .format import MapFormater, PlotFormater
from .pipeline import LogementsPipe



# Decorators

def update_volume_date(func:callable) -> callable:

        """Decorator that sets Volume's `update` date to current date
        
        Arguments:
            func {callable} -- The function to be decorated

        Returns:
            callable: The wrapped function update the date and then calls the original function
        """

        def wrapper(*args, **kwargs):

            volume:Volume = args[0].volume # ough that's not pretty

            properties = volume.read_properties()
            properties['update'] = datetime.now().strftime('%d-%m-%Y')
            volume.write_properties(properties)

            return func(*args, **kwargs)
        
        return wrapper




# Data interface

class Data():

    def __init__(self):
        self.volume = Volume()
        self.communes = self.__load_communes()
        self.cities = self.__load_cities()
        self.logements = self.__load_logements()
        self.logements_pipe = LogementsPipe(self.cities)
        self.map_formater = MapFormater(self.communes, self.cities)
        self.plot_formater = PlotFormater(self.logements)

    def __load_communes(self) -> pd.DataFrame:
        return self.volume.read_communes()
    
    def __load_cities(self) -> pd.DataFrame:
        df = pd.read_csv('application/datasets/communes-france-2025-light.csv', dtype={0: str, 1: float, 2: float})
        return df
    
    def __load_logements(self) -> pd.DataFrame:
        # TODO: load from volume
        df = pd.read_csv('application/datasets/logement-74-light.csv', dtype={4: str, 5: str})
        return df
    

    def get_property(self, key) -> str:

        """Return a property value from Koyeb volume

        Returns:
            str: Volume property value
        """

        properties = self.volume.read_properties()
        return properties[key]
    

    def get_communes(self) -> pd.DataFrame:

        """Returns raw communes.csv data

        Returns:
            pd.DataFrame: Raw communes data
        """

        return self.communes
    
    def get_logements(self) -> pd.DataFrame:

        """Returns raw logements_74.csv data

        Returns:
            pd.DataFrame: Raw logements 74 data
        """

        return self.logements
    

    @update_volume_date
    def update_communes(self, communes:list[dict]) -> None:

        """Update the communes dataset on Koyeb volume and reload communes"""

        df = pd.DataFrame(communes)
        self.volume.write_communes(df)

        # Reload communes
        self.communes = self.__load_communes()
        # Update MapFormater
        self.map_formater.set_communes(self.communes)

    def update_logements(self, existing_logements:list[dict], new_logements:list[dict]) -> None:

        existing_df = pd.DataFrame(existing_logements)
        new_df = pd.DataFrame(new_logements)
        formatted_df = self.logements_pipe.process(existing_df, new_df)

        concated = pd.concat([self.logements, formatted_df], ignore_index=True) # TODO: remove duplicates
        self.volume.write_logements(concated)

        # Reload logements
        self.logements = self.__load_logements()
        # Update plot formater
        self.plot_formater.set_logements(self.logements)
    
    def get_map(self, filters:list[dict]=None, sort:dict=None) -> list[dict]:

        """Format the data to display on the map

        Keyword Arguments:
            filters {list[dict]} -- List of filter rules (default None)
            sort {dict} -- How to sort the data (default None)

        Returns:
            list[dict]: Formatted data for the map
        """

        data = self.map_formater.get_global(filters, sort)
        return data
    
    def get_zoomed_map(self, streets:list[dict], iris:list[dict]) -> list[dict]:

        """Format the data to display on the zoomed view of the map

        Arguments:
            streets {list[dict]} -- List of streets data from Ademe
            iris {list[dict]} -- List of iris data from Enedis

        Returns:
            list[dict]: Formatted data for the map
        """

        data = self.map_formater.get_zoomed(streets, iris)
        return data
    
    def get_plot(self, filters:list[dict]=None) -> pd.DataFrame:

        """Format the data to send to the plots

        Keywords Arguments:
            filters {list[dict]} -- List of filter rules (default None)

        Returns:
            pd.DataFrame: A selection of columns for the plots
        """

        data = self.plot_formater.get_selected(filters)
        return data
    
    def get_nearest_insee(self, latitude:float, longitude:float) -> int:

        """Find the nearest insee code from `communes-france-2025` dataset by latitude and longitude

        Arguments:
            latitude {float} -- Target latitude
            longitude {float} -- Target longitude

        Returns:
            int: Nearest insee code
        """

        # Skip communes with missing coordinates
        cities = self.cities.dropna(subset=['latitude_centre', 'longitude_centre'])

        # Extract coordinates from DataFrame
        coords = cities[['latitude_centre', 'longitude_centre']].values
        # Calculate distances
        distances = cdist([(latitude, longitude)], coords, metric='euclidean')

        # Find the index of the nearest point
        min_index = distances.argmin()
        # Get the insee code of the nearest point
        nearest_code = cities.iloc[min_index]['code_insee']

        return int(nearest_code)
    
    def get_from_insee(self, insee:int) -> dict:

        """Retrieve data from `communes-france-2025` dataset by insee code

        Arguments:
            insee {int} -- Target insee code

        Returns:
            dict: Data of the insee code
        """

        serie = self.cities[self.cities['code_insee'] == str(insee)]
        return serie.to_dict(orient='records')[0]
    
    def compute_perdiode_class(self, year:int) -> str:

        """Classify a year into a periode
        
        Arguments:
            year {int} -- Year to classify

        Returns:
            str: The perdiode
        """

        # Avant 1975 (première réglementation thermique)
        if year < 1975:
            return 'Avant 1975' 
        # 1975-2000 (RT 1974, 1988, 2000)
        elif year <= 2000:
            return '1975-2000'
        # 2001-2012 (RT 2005, 2012)
        elif year <= 2012:
            return '2001-2012'
        # Après 2012 (RT 2012, RE 2020)
        else:
            return 'Après 2012'
        
    def compute_altitude_class(self, altitude:int) -> str:

        """
        Affecte chaque logement à une tranche d'altitude
        
        Cette fonction permet de regrouper les logements selon leur altitude
        pour faciliter les analyses comparatives entre vallées et montagnes.
        
        Args:
            altitude (float): Altitude du logement en mètres
            
        Returns:
            str: Label de la tranche d'altitude correspondante
        """
        # Gestion des valeurs manquantes
        if pd.isna(altitude):
            return pd.NA
        
        # Attribution de la tranche selon les seuils définis
        if altitude < 600:
            return "0-600"
        elif altitude < 1200:
            return "600-1200"
        elif altitude < 1800:
            return "1200-1800"
        elif altitude < 2500:
            return "1800-2500"
        else:
            return ">2500m"