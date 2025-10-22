import pandas as pd
import os
import json




class Volume:


    mount_path = '/volume'
    properties = 'properties.json'


    def __init__(self):
        self.__init_mount()


    def __init_mount(self):

        # Use environment varibale `MOUNT_PATH` if user wants to use a custom path for the volume
        custom_mount = os.environ.get('MOUNT_PATH')
        if custom_mount:
            self.mount_path = custom_mount

        # Create `properties.json` if doesn't exists
        properties_path = os.path.join(self.mount_path, self.properties)
        if not os.path.isfile(properties_path):
            dummy_prop = {'update': 'NA'}
            self.write_properties(dummy_prop)



    def read_properties(self) -> dict:

        """Read volumes properties / infos

        Returns:
            dict: Volumes properties and info
        """

        properties_path = os.path.join(self.mount_path, self.properties)
        with open(properties_path, 'r') as f:
            content = json.load(f)
            
        return content
    
    def write_properties(self, properties:dict) -> dict:

        """Write new volumes properties

        Arguments:
            dict: New properties to write on Koyeb Volume
        """

        properties_path = os.path.join(self.mount_path, self.properties)
        with open(properties_path, 'w') as f:
            json.dump(properties, f)

    def read_communes(self) -> pd.DataFrame:

        """Load the latest communes data from Koyeb volume. 
        Fallback to original dataset communes if fails

        Returns:
            pd.DataFrame: Communes data
        """

        communes_path = os.path.join(self.mount_path, 'communes.csv')
        
        try:
            df = pd.read_csv(communes_path)
        except FileNotFoundError:
            print('FileNotFoundError: "communes.csv" not found on volume. Loading from dataset instead')
            df = pd.read_csv('application/datasets/communes.csv')
        finally:
            df['code_commune'] = df['code_commune'].astype(str)

        return df
    
    def write_communes(self, communes:pd.DataFrame) -> None:

        """Update the communes dataset in Koyeb Volume

        Arguments:
            communes {pd.DataFrame} -- The new communes dataframe to write in volume
        """

        communes_path = os.path.join(self.mount_path, 'communes.csv')
        communes.to_csv(communes_path, index=False)