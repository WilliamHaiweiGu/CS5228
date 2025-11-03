import os

import numpy as np
import pandas as pd
from numpy import ndarray
from pandas import DataFrame, Series

from paths import auxiliary_data_dir

if __name__ == "__main__":
    src_df = pd.read_csv(os.path.join(auxiliary_data_dir, "sg-hdb-block-details.csv"))
    out_file: str = "hdb-block-walking-distance.csv"
    for dest_file in os.listdir():
        if not (dest_file.startswith("sg-") and dest_file.endswith("_mat.npy")):
            continue
        distance_matrix: ndarray = np.load(dest_file)
        if dest_file == "sg-mrt-stations_mat.npy": # remove closed MRT stations
            df: DataFrame = pd.read_csv(os.path.join(auxiliary_data_dir, "sg-mrt-stations.csv"))
            distance_matrix = distance_matrix[:, df["STATUS"] == "open"]
            print("Processed:", distance_matrix.shape)
        src_df["dist-to" + dest_file[2: -8]] = Series(distance_matrix.min(axis=1))
    src_df.to_csv(os.path.join(auxiliary_data_dir, out_file))
