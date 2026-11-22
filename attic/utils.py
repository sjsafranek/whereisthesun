import math
import pandas as pd
import numpy as np
import multiprocessing as mp


def split_dataframe(df, chunk_size = 10000): 
    chunks = list()
    num_chunks = len(df) // chunk_size + 1
    for i in range(num_chunks):
        chunks.append(df[i*chunk_size:(i+1)*chunk_size])
    return chunks

def parallelize_dataframe(df, func):
    num_processes = mp.cpu_count()
    if 1 == num_processes:
        return func(df)
    # df_split = np.array_split(df, num_processes)  # DEPRICATION WARNING...
    chunk_size = math.ceil(len(df)/num_processes)
    df_split = split_dataframe(df, chunk_size=chunk_size)
    with mp.Pool(num_processes) as p:
        df = pd.concat(p.map(func, df_split))
    return df

def parallelize_function(df):
    df[column_output] = df[column_input].apply(example_function)
    return df
