import pandas as pd



class Filter():

    @staticmethod
    def __equal(df, col:str, value:str) -> pd.DataFrame:
        return df[df[col] == value]
    
    @staticmethod
    def __startwith(df:pd.DataFrame, col:str, value:str) -> pd.DataFrame:
        return df[df[col].astype(str).str.startswith(value)]
    
    @staticmethod
    def __inrange(df:pd.DataFrame, col:str, value:list) -> pd.DataFrame:
        low = float(value[0])
        hight = float(value[1])
        return df[(df[col] >= low) & (df[col] <= hight)]

    @staticmethod
    def __create_filters(rules:list[dict]) -> list[callable]:

        ffuncs = []
        for r in rules:

            c = r['column']
            v = r['value']

            if not v:
                continue
            
            if r['type'] == 'equal':
                filter = lambda df, col=c, value=v: Filter.__equal(df, col, value)
            elif r['type'] == 'startwith':
                filter = lambda df, col=c, value=v: Filter.__startwith(df, col, value)
            elif r['type'] == 'inrange':
                filter = lambda df, col=c, value=v: Filter.__inrange(df, col, value)

            ffuncs.append(filter)

        return ffuncs
    
    @staticmethod
    def apply(df:pd.DataFrame, rules:list[dict]) -> pd.DataFrame:

        """Filters the dataframe

        Arguments:
            df {pd.DataFrame} -- DataFrame to filter
            rules {list[dict]} -- Filter rules to apply

        Returns:
            pd.DataFrame: Filtered dataframe
        """

        ffuncs = Filter.__create_filters(rules)

        for filter in ffuncs:
            df = filter(df)

        return df