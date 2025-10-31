import pandas as pd


df = pd.read_csv('/Users/marinnagy/Downloads/communes-france-2025.csv', dtype={20: str})

selected_columns = ['code_insee',
                    'latitude_centre',
                    'longitude_centre',
                    'altitude_maximale',
                    'nom_standard',
                    'densite',
                    'superficie_km2',
                    'population',
                    'superficie_km2',
                    'grille_densite_texte'
]

df = df[selected_columns]

df.to_csv('/Users/marinnagy/Downloads/communes-france-2025-light.csv')