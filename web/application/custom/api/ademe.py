from .api import API
from datetime import datetime



class ADEME(API):

    existing_endpoint = '/dpe03existant/lines'
    new_endpoint = '/dpe02neuf/lines'

    def __init__(self):
        # Pass base_url argument to the parent class
        super().__init__('https://data.ademe.fr/data-fair/api/v1/datasets')

    
    def __loop_API(self, endpoint, params:dict, yield_progress=False) -> list[dict]:
        
        data = []

        content = self._get_requests(endpoint, params=params)
        progress = len(data) / content['total']
        yield f"data:{progress*100}\n\n"
        data.extend(content['results'])

        while content.get('next'):

            content = self._get_requests(endpoint, custom_url=content['next'])

            # yield progress
            progress = len(data) / content['total']
            print(progress*100)
            # yield f"data:{progress*100}\n\n"

            data.extend(content['results'])

        return data

    
    def addresses_from_date(self, date:datetime, size=300, yield_progress=False) -> dict:

        """Requests 74 data from a specific date

        Arguments:
            date {datetime} -- The date to request the data from

        Keywords Arguments:
            size {int} -- The size of each request (default: 300)
            yield_progress {bool} -- Whether to yield the progress (in percent) or not

        Returns:
            tuple[list[dict], list[dict]]: The existing and new data collected from the ADEME API
        """

        date_str = datetime.strftime(date, '%Y-%m-%d')

        params = {
            'size': size,
            'qs': f'code_departement_ban:74 AND date_derniere_modification_dpe:[{date_str} TO *]'
        }

        existing = self.__loop_API(self.existing_endpoint, params, yield_progress=yield_progress)
        new = self.__loop_API(self.new_endpoint, params, yield_progress=yield_progress)
        data = {'existing': existing, 'new': new} # doesn't work cause `existing` and `new` are generators...

        return data

    
    def insee_from_bbox(self, 
                             lon_min:float, 
                             lat_min:float, 
                             lon_max:float, 
                             lat_max:float,
                             size=300) -> list[dict]:
        
        """
        Retrieve the list of insee codes from a specific bounding box.
        * Bounding box 4 variables: minimum longitude, minimum latitude, maximum longitude, maximum latitude
        Returns data about each insee code: `code_insee_ban`, `_geopoint`, `code_postal_ban`
        """
        
        params = {
            'bbox': ','.join([lon_min, lat_min, lon_max, lat_max]),
            'select': 'code_insee_ban,code_postal_ban,nom_rue_ban,_geopoint',
            'collapse': 'nom_rue_ban',
            'size': size
        }

        content = self._get_requests(self.existing_endpoint, params=params)

        return content['results']