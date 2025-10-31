import pandas as pd


df = pd.read_csv('/Users/marinnagy/Documents/GitHub/m2_enedis/web/application/datasets/communes-france-2025-light.csv', dtype={20: str})

print(df['zone_climatique'].unique())