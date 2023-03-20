import pandas as pd
import numpy as np
import imp
import decorators.decorator as dec
from scr import script_2 as f
imp.reload(dec)


@dec.log_execution("df_1", "df_2")
def drop_na(df_1, df_2):
    df_1 = df_1.dropna()
    df_2 = df_2.dropna()
    return df_1, df_2

@dec.log_execution("df")
def col_to_pep8(df):
    df.columns = df.columns.str.replace(' ','_')
    df.columns = df.columns.str.lower()
    return df

@dec.log_execution("df_1")
def delimiter_sepal_length(df_1, sepal_length_cm):
    df_1 = df_1[df_1['sepal_length_(cm)'] >= sepal_length_cm]
    return df_1

@dec.log_execution("df_1", "df_2", "df_3")
def delimiter_petal_width(df_1, df_2, df_3, petal_width):
    
    df_1 = df_1[df_1['petal_width_(cm)'] <= petal_width]
    df_3 = df_3[df_3['petal_width_(cm)'] <= petal_width]
    
    df_1 = pd.concat([df_1, df_2, df_3], ignore_index=True)
    
    return df_1, df_2

def execute(df_1, df_2, df_3, sepal_length_cm, petal_width):
    df_1 = col_to_pep8(df_1)
    df_2 = col_to_pep8(df_2)
    df_3 = col_to_pep8(df_3)
    df_1, df_2 = drop_na(df_1, df_2)
    df_1 = delimiter_sepal_length(df_1, sepal_length_cm)
    df_1, df_2 = delimiter_petal_width(df_1, df_2, df_3, petal_width)
    
    
    