import pandas as pd


df = pd.read_csv('/Users/marinnagy/Documents/GitHub/m2_enedis/web/application/datasets/communes-france-2025-light.csv')
print(df.shape)


def categoriser_altitude(altitude):
    """
    Affecte chaque logement à une tranche d'altitude
    
    Cette fonction permet de regrouper les logements selon leur altitude
    pour faciliter les analyses comparatives entre vallées et montagnes.
    
    Args:
        altitude (float): Altitude du logement en mètres
        
    Returns:
        str: Label de la tranche d'altitude correspondante
    """
    # Gestion des valeurs manquantes
    if pd.isna(altitude):
        return pd.NA
    
    # Attribution de la tranche selon les seuils définis
    if altitude < 600:
        return "0-600"
    elif altitude < 1200:
        return "600-1200"
    elif altitude < 1800:
        return "1200-1800"
    elif altitude < 2500:
        return "1800-2500"
    else:
        return ">2500m"
    

df['classe_altitude'] = df['altitude_maximale'].apply(categoriser_altitude)

print(df.shape)

df.to_csv('/Users/marinnagy/Documents/GitHub/m2_enedis/web/application/datasets/communes-france-2025-light.csv', index=False)