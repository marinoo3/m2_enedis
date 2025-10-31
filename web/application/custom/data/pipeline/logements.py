import pandas as pd



class LogementsPipe():

    selected_columns = [
        'nom_commune_ban',
        'etiquette_dpe',
        'conso_5_usages_par_m2_ep',
        'type_batiment',
        'periode_construction',
        'periode_categorie',
        'type_energie_principale_chauffage',
        'altitude_maximale',
        'classe_altitude',
        'categorie_dpe'
    ]

    def __init__(self, cities:pd.DataFrame):
        self.cities = cities

    def __categorize_altitude(altitude):
            
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
                return "0-600m (Vallée)"
            elif altitude < 1200:
                return "600-1200m (Colline)"
            elif altitude < 1800:
                return "1200-1800m (Montagne)"
            elif altitude < 2500:
                return "1800-2500m (Haute montagne)"
            else:
                return ">2500m (Très haute montagne)"
            
    def __categorize_dpe(etiquette):

        if etiquette in ['A', 'B']:
            return 'Bons (A-B)'
        elif etiquette in ['C', 'D']:
            return 'Moyens (C-D)'
        elif etiquette == 'E':
            return 'Médiocres (E)'
        else:  # F ou G
            return 'Passoires (F-G)'
        
    def __categorize_periode(periode):

        """Regroupe les périodes de construction en grandes époques"""

        if pd.isna(periode):
            return pd.NA
        
        periode_str = str(periode).lower()
        
        # Strings
        if any(x in periode_str for x in ['récent']):
            return 'Après 2012'
        elif any(x in periode_str for x in ['avant', 'ancien']):
            return 'Avant 1975'
        
        periode_int = int(periode_str.split('-')[0].split(' ')[-1])

        # Avant 1975 (première réglementation thermique)
        if periode_int < 1975:
            return 'Avant 1975' 
        # 1975-2000 (RT 1974, 1988, 2000)
        elif periode_int <= 2000:
            return '1975-2000'
        # 2001-2012 (RT 2005, 2012)
        elif periode_int <= 2012:
            return '2001-2012'
        # Après 2012 (RT 2012, RE 2020)
        else:
            return 'Après 2012'

    def process(self, existing:pd.DataFrame, new:pd.DataFrame) -> pd.DataFrame:

        # Add data source
        existing['data_source'] = 'existant'
        new['data_source'] = 'existant'
        print(len(existing.columns), flush=True)
        print(len(new.columns), flush=True)

        # Conact existing and new
        df = pd.concat([existing, new], ignore_index=True)
        print(df.columns, flush=True)
        print(len(df.columns), flush=True)

        # Add data from `communes-france-2025.csv`
        communes = self.cities[['code_insee', 'population', 'superficie_km2', 'densite', 'altitude_maximale', 'grille_densite_texte']]
        merged_df = pd.merge(df, communes, left_on='code_insee_ban', right_on='code_insee', how='left', indicator=True)
        unmatched_rows = merged_df[merged_df['_merge'] == 'left_only']

        # Fix old Annecy
        old_annecy_insees = unmatched_rows['code_insee_ban'].unique()
        df = df[df['code_insee_ban'] != 74187] # Drop Montmin
        df['code_insee_ban'] = df['code_insee_ban'].replace(old_annecy_insees, 74010) # replace old insee to new insee
        merged_df = pd.merge(df, communes, left_on='code_insee_ban', right_on='code_insee', how='left')
        merged_df = merged_df.drop(columns=['code_insee'])

        # Add altitude classes
        merged_df['classe_altitude'] = merged_df['altitude_maximale'].apply(self.__categorize_altitude)

        # Add DPE classes
        merged_df['categorie_dpe'] = merged_df['etiquette_dpe'].apply(self.__categorize_dpe)

        # Add passoire classe
        merged_df['passoire'] = merged_df['etiquette_dpe'].isin(['F', 'G'])

        # Add periode classes
        merged_df['periode_categorie'] = merged_df['periode_construction'].apply(self.__categorize_periode)

        # Optimize dataframe and only keep columns of interest
        merged_df = merged_df[self.selected_columns]

        return merged_df