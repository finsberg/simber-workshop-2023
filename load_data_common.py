import pandas as pd
import numpy as np
from pathlib import Path


def load_data():
    path_to_data = Path("data_curated")
    
    df_features = pd.read_csv(path_to_data.joinpath("features.csv"), index_col=0)
    df_features.replace(["0nM", "0uM"], "baseline", inplace=True)
    df_features.sort_values(["drug", "experiment", "well", "tissue", "dose"], ascending=[True, True, True, True, False], inplace=True)
    drop_rows = np.where(pd.isnull(df_features["voltage_apd30"])|
                         pd.isnull(df_features["voltage_apd90"])|
                         pd.isnull(df_features["voltage_beating_frequencies"])
                        )
    df_features.drop(index=df_features.iloc[drop_rows].index.tolist(), inplace=True)
    df_features.reset_index(drop=True, inplace=True)

    df_traces = pd.read_csv(path_to_data.joinpath("traces_avg.csv"), index_col=0)

    cols_array = ["voltage_time", "voltage_trace",
                  "calcium_time", "calcium_trace",
                  "displacement_time", "displacement_trace",
                  "velocity_time", "velocity_trace"]

    for col_name in cols_array:
        df_traces[col_name] = df_traces[col_name].apply(eval)
        df_traces[col_name] = df_traces[col_name].apply(lambda x: np.array(x, dtype=np.float32))


    # convert dose strings to float
    unit_dict = {"baseline":0.0,
                 '0.1nM':0.1e-9, '1nM':1e-9, '10nM':10e-9, '100nM':100e-9, '1000nM':1000e-9, '10000nM':10000e-9,
                 '3nM':3e-9, '30nM':30e-9, '300nM':300e-9, '3000nM':3000e-9,
                 '3uM':3e-6, '30uM':30e-6, '0.3uM':0.3-6, '300uM':300e-6,
                 '1uM':1e-6, '10uM':10e-6, '100uM':100e-6, '0.1uM':0.1e-6,
                 '0.6%':0.0, '0.06%':0.0, '0.006%':0.0, '0.0006%':0.0
                }

    df_features.insert(loc=5, column="dose_float", value=[unit_dict[d] for d in df_features["dose"]])
        
    return df_features, df_traces
