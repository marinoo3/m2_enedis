import pandas as pd
from datetime import datetime

from .volume import Volume
from .format import MapFormater



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
        self.map_formater = MapFormater(self.communes, self.cities)

    def __load_communes(self) -> pd.DataFrame:
        return self.volume.read_communes()
    
    def __load_cities(self) -> pd.DataFrame:
        df = pd.read_csv('application/datasets/communes-france-2025.csv', low_memory=False)
        df['code_insee'] = df['code_insee'].astype(str)
        return df
    

    def get_property(self, key) -> str:

        """Return a property value from Koyeb volume

        Returns:
            str: Volume property value
        """

        properties = self.volume.read_properties()
        return properties[key]
    

    def get_communes(self) -> pd.DataFrame:

        """Returns raw communes data

        Returns:
            pd.DataFrame: Raw communes data
        """

        return self.communes
    

    @update_volume_date
    def update_communes(self, communes:list[dict]) -> None:

        """Update the communes dataset on Koyeb volume and reload communes"""

        df = pd.DataFrame(communes)
        self.volume.write_communes(df)

        # Reload communes
        self.communes = self.__load_communes()
        # Update MapFormater
        self.map_formater.set_communes(self.communes)

    
    def get_map(self, filters:list[dict]=None, sort:dict=None) -> list[dict]:

        """Format the data to display on the map

        Arguments:
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