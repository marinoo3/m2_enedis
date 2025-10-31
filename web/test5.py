import requests
import pandas as pd


base_url = 'https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/values_agg'

data = []


def get_zone_climat(params):
    response = requests.get(base_url, params=params)
    content = response.json()
    return content['aggs']


def zones(departement):
    
    params = {
        'agg_size': 1000,
        'field': 'code_insee_ban',
        'qs': f'code_departement_ban:{departement}',
        'select': 'zone_climatique',
        'size': 1
    }


    agg = get_zone_climat(params)

    climat_general = None

    for result in agg:
        code_insee = result['value']
        zone_climatique = result['results'][0].get('zone_climatique')

        if not zone_climatique:
            if not climat_general:
                print('no general')
            data.append({'code_insee': code_insee, 'zone_climatique': climat_general})
        else:
            data.append({'code_insee': code_insee, 'zone_climatique': zone_climatique})
            if not climat_general:
                climat_general = zone_climatique
    


for i in range(99):

    departement = f"{i+1:02}"
    print(departement)
    zones(departement)

df = pd.DataFrame(data)
df.to_csv('/Users/marinnagy/Documents/GitHub/m2_enedis/test.csv', index=False)