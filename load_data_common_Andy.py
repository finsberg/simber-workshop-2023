import urllib.request
import time
import pandas as pd
import numpy as np
from pathlib import Path


def download_data(path, case):
    if case == "features":
        print("Download features.csv")
        link = "https://www.dropbox.com/s/8ph19rsrgnj1k1j/features.csv?dl=1"
    elif case == "traces_avg":
        print("Download traces_avg.csv")
        link = "https://www.dropbox.com/s/yrf9uxtacpv0gi5/traces_avg.csv?dl=1"
    else:
        raise ValueError(f"Unknown case {case}. Expected 'features' or 'traces_avg'")
    urllib.request.urlretrieve(link, path)
    time.sleep(1.0)
    print("Done downloading data")


# Set path to data files "features.csv", "traces_avg.csv", and "traces_full.csv"
path_to_data = Path("data_curated")
path_to_data.mkdir(exist_ok=True)

features_path = path_to_data / "features.csv"
if not features_path.is_file():
    download_data(features_path, "features")

traces_avg_path = path_to_data / "traces_avg.csv"
if not traces_avg_path.is_file():
    download_data(traces_avg_path, "traces_avg")

for p in path_to_data.iterdir():
    print(p)

df_features = pd.read_csv(features_path, index_col=0)
df_traces = pd.read_csv(traces_avg_path, index_col=0)

# Convert list strings to numpy.ndarray for time series columns
cols_array = [
    "voltage_time",
    "voltage_trace",
    "calcium_time",
    "calcium_trace",
    "displacement_time",
    "displacement_trace",
    "velocity_time",
    "velocity_trace",
]

for col_name in cols_array:
    df_traces[col_name] = df_traces[col_name].apply(eval)
    df_traces[col_name] = df_traces[col_name].apply(
        lambda x: np.array(x, dtype=np.float32)
    )

# Example filtering dataframe by drug and well
df_CisD7 = df_features[
    (df_features["drug"].values == "Cisapride") & (df_features["well"].values == "D7")
]
