import pandas as pd
import numpy as np


def preprocess(df,region_df):
    # global df,region_df
    df = df[df['Season']=='Summer']
    df = df.merge(region_df,on='NOC',how='left')
    df.drop_duplicates(inplace = True)
    df = pd.concat([df,pd.get_dummies(df['Medal']).astype(np.int8)],axis=1)
    return df
