import pandas as pd
import numpy as np
import imp
import decorators.decorator as dec
imp.reload(dec)

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