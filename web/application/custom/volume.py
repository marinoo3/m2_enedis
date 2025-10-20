import pandas as pd




class Volume:

    @staticmethod
    def read_communes() -> pd.DataFrame:

        """Loads the latest communes data from Koyeb volume. 
        Fallback to original dataset communes if fails

        Returns:
            pd.DataFrame: Communes data
        """
        
        try:
            df = pd.read_csv('enedis/communes.csv')
        except FileNotFoundError:
            print('FileNotFoundError: "communes.csv" not found on volume. Loading from dataset instead')
            df = pd.read_csv('application/datasets/communes.csv')
        finally:
            df['code_commune'] = df['code_commune'].astype(str)

        return df
    
    @staticmethod
    def write_communes(communes:pd.DataFrame) -> None:
        communes.to_csv('enedis/communes.csv', index=False)