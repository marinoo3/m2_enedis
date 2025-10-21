import pandas as pd
import os
import json




class Volume:

    mount_path = '/volume'

    @staticmethod
    def read_properties() -> dict:

        """Read volumes properties / infos

        Returns:
            dict: Volumes properties and info
        """

        properties_path = os.path.join(Volume.mount_path, 'properties.json')
        with open(properties_path, 'r') as f:
            content = json.load(f)
            
        return content
    
    @staticmethod
    def write_properties(properties:dict) -> dict:

        """Write new volumes properties

        Arguments:
            dict: New properties to write on Koyeb Volume
        """

        properties_path = os.path.join(Volume.mount_path, 'properties.json')
        with open(properties_path, 'w') as f:
            json.dump(properties, f)

    @staticmethod
    def read_communes() -> pd.DataFrame:

        """Load the latest communes data from Koyeb volume. 
        Fallback to original dataset communes if fails

        Returns:
            pd.DataFrame: Communes data
        """

        communes_path = os.path.join(Volume.mount_path, 'communes.csv')
        
        try:
            df = pd.read_csv(communes_path)
        except FileNotFoundError:
            print('FileNotFoundError: "communes.csv" not found on volume. Loading from dataset instead')
            df = pd.read_csv('application/datasets/communes.csv')
        finally:
            df['code_commune'] = df['code_commune'].astype(str)

        return df
    
    @staticmethod
    def write_communes(communes:pd.DataFrame) -> None:

        """Update the communes dataset in Koyeb Volume

        Arguments:
            communes {pd.DataFrame} -- The new communes dataframe to write in volume
        """

        communes_path = os.path.join(Volume.mount_path, 'communes.csv')
        communes.to_csv(communes_path, index=False)