import pandas as pd



class Filter():

    def __init__(self, filters:dict):
        self.filter_funcs = self.__create_filters(filters)

    def __equal(self, df, col:str, value:str) -> pd.DataFrame:
        return df[df[col] == value]
    
    def __startwith(self, df:pd.DataFrame, col:str, value:str) -> pd.DataFrame:
        return df[df[col].astype(str).str.startswith(value)]
    
    def __inrange(self, df:pd.DataFrame, col:str, value:list) -> pd.DataFrame:
        low = float(value[0])
        hight = float(value[1])
        return df[(df[col] >= low) & (df[col] <= hight)]

    def __create_filters(self, filters:list[dict]):

        filter_funcs = []
        for f in filters:

            c = f['column']
            v = f['value']

            if not v:
                continue
            
            if f['type'] == 'equal':
                func = lambda df, col=c, value=v: self.__equal(df, col, value)
            elif f['type'] == 'startwith':
                func = lambda df, col=c, value=v: self.__startwith(df, col, value)
            elif f['type'] == 'inrange':
                func = lambda df, col=c, value=v: self.__inrange(df, col, value)

            filter_funcs.append(func)

        return filter_funcs
    

    def compute(self, df:pd.DataFrame) -> pd.DataFrame:

        """Filters the dataframe

        Arguments:
            df {pd.DataFrame} -- DataFrame to filter

        Returns:
            pd.DataFrame: Filtered dataframe
        """

        for func in self.filter_funcs:
            df = func(df)

        return df