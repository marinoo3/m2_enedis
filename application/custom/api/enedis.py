from .base_api import BaseAPI





class ENEDIS(BaseAPI):

    def __init__(self):
        # Pass base_url argument to the parent class
        super().__init__('https://data.enedis.fr/api/explore/v2.1/catalog/datasets/consommation-annuelle-residentielle-par-adresse/records')

    
    def __loop_API(self, params:dict, limit:int = 100) -> list[dict]:

        """
        Loop through pages of an API requests.
        * Parameters for the requests
        * Limit of result per requests (default = 100)
        Returns all the content as a list of dict
        """

        data = []

        stop = False
        index = 0
        while not stop:

            params['limit'] = limit
            params['offset'] = limit * index
            content = self._get_requests(params=params)

            # stop the loop if last page
            if len(content['results']) < limit:
                stop = True

            data.extend(content['results'])

            # increase index
            index += 1

        return data
    

    def __chunck_API(self, params:dict, offset:int = 0, limit:int = 50) -> list[dict]:

        params['limit'] = limit
        params['offset'] = offset
        content = self._get_requests(params=params)

        # stop the loop if last page
        stop = False
        if len(content['results']) < limit:
            stop = True

        return content['results'], stop
    

    def communes(self) -> list[dict]:

        """
        Retrieve all communes.
        Returns data about each communes: `code_commune`, `nombre_de_logements`, `conso_total_mwh`
        """

        params = {
            'select': 'code_commune, SUM(nombre_de_logements) as nombre_de_logements, SUM(consommation_annuelle_totale_de_l_adresse_mwh) as conso_total_mwh',
            'group_by': 'code_commune'
        }

        communes_data = self.__loop_API(params)

        return communes_data
    
    
    def iris_from_insee(self, insee_codes:list, offset:int = 0) -> list[dict]:

        """
        Retrive all iris from a list of insee code. The first 5 digits of iris codes are there corresponding insee code.
        * List of insee codes to parse iris from
        Returns data batch about each iris: `code_iris`, `nombre_de_logements`, `conso_total_mwh` and the next index
        """

        where_queries = [ f'startswith(code_iris, "{insee}")' for insee in insee_codes ]

        params = {
            'select': 'code_iris, type_de_voie, libelle_de_voie, SUM(nombre_de_logements) as nombre_de_logements, SUM(consommation_annuelle_totale_de_l_adresse_mwh) as conso_total_mwh',
            'group_by': 'libelle_de_voie, type_de_voie',
            'where': ' or '.join(where_queries)
        }

        iris_data, stop = self.__chunck_API(params, offset)

        next_offset = None
        if not stop:
            next_offset = offset + len(iris_data)

        return iris_data, next_offset