import pandas as pd
import numpy as np
from pathlib import Path

# Set path to data files "features.csv", "traces_avg.csv", and "traces_full.csv"
path_to_data = Path("data_curated")
for p in path_to_data.iterdir():
    print(p)
    
df_features = pd.read_csv(path_to_data.joinpath("features.csv"), index_col=0)
df_traces = pd.read_csv(path_to_data.joinpath("traces_avg.csv"), index_col=0)

# Convert list strings to numpy.ndarray for time series columns
cols_array = ["voltage_time", "voltage_trace",
              "calcium_time", "calcium_trace",
              "displacement_time", "displacement_trace",
              "velocity_time", "velocity_trace"]

for col_name in cols_array:
    df_traces[col_name] = df_traces[col_name].apply(eval)
    df_traces[col_name] = df_traces[col_name].apply(
        lambda x: np.array(x, dtype=np.float32)
        )
    
# Example filtering dataframe by drug and well
df_CisD7 = df_features[
    (df_features["drug"].values == "Cisapride")&(df_features["well"].values == "D7")
    ]


