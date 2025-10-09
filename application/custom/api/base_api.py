import requests
import pandas as pd
import time



class BaseAPI():

    def __init__(self, base_url) -> None:
        self.base_url = base_url
        self.temp_data = None


    def _append_data(df:pd.DataFrame, data:list[dict]) -> pd.DataFrame:

        """
        Append a list of data to a DataFrame of the same structure
        Returns concatened DataFrame
        """
    
        data_df = pd.DataFrame(data)
        return pd.concat([df, data_df], ignore_index=True)
    

    def _get_requests(self, custom_url:str = None, params:dict = {}, tic=0) -> dict:

        """
        Make a get requests and catchs exceptions. 
        * Uses the base url if no custom url provided
        * Optional parameters passed to the requests
        Returns the response json object
        """

        try:

            if custom_url:
                response = requests.get(custom_url)
            else:
                response = requests.get(self.base_url, params=params)

        except ConnectionError:

            print(f'ConnectionError, network failed to request API ({tic+1}/3)')

            if(tic == 3):
                print('Failed to fetch')
                return None
            
            print('Trying again in 1 second')
            time.sleep(1)
            return self._get_requests(params=params, custom_url=custom_url, tic=tic+1)
            
        if response.status_code != 200:

            if(tic == 3):
                print(f'Failed')
                return None
            
            print(f'Error code {response.status_code}')
            time.sleep(1)
            return self._get_requests(params=params, custom_url=custom_url, tic=tic+1)
    
        return response.json()