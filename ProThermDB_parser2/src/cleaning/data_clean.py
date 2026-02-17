import pandas as pd


def data_clean(df):
    ''' Удалить дубликаты строк, вывести их число,
     заменить все пропуски на None'''

    df = df.drop_duplicates()
    df = df.replace('-', None)

    return df
