from .base_api import BaseAPI



class ADEME(BaseAPI):

    def __init__(self):
        # Pass base_url argument to the parent class
        super().__init__('https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/lines')

    
    def insee_from_bbox(self, 
                             lon_min:float, 
                             lat_min:float, 
                             lon_max:float, 
                             lat_max:float,
                             size=200) -> list[dict]:
        
        """
        Retrieve the list of insee codes from a specific bounding box.
        * Bounding box 4 variables: minimum longitude, minimum latitude, maximum longitude, maximum latitude
        Returns data about each insee code: `code_insee_ban`, `_geopoint`, `code_postal_ban`
        """
        
        params = {
            'bbox': ','.join([lon_min, lat_min, lon_max, lat_max]),
            'select': 'code_insee_ban,code_postal_ban,nom_rue_ban,_geopoint',
            'collapse': 'nom_rue_ban',
            'size': 300
        }

        content = self._get_requests(params=params)

        return content['results']