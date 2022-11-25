import numpy as np
import pandas as pd


def year_clean(year):
    try:
        year = int(year)
    except:
        year = np.nan
    return year

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def cleaning_data(data):
    df = pd.read_csv(data)
    df['Price$'] = df['Price$'].apply(lambda x : x if isfloat(x) else np.nan)
    df['Year'] = df['Year'].apply(year_clean)
    df.dropna(inplace=True)
    convert_dict = {
            'Year': int,
            'Price$': float,
            }
    df = df.astype(convert_dict)
    df.drop_duplicates(inplace=True)
    df.reset_index(inplace=True)
    df.drop(['index'], axis=1, inplace=True)
    return df