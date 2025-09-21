import os
import time
from typing import Optional

import numpy as np
import pandas as pd
import requests
from pandas import DataFrame, Series


def get_coords(file_name: str) -> tuple[list[tuple[float, float]], DataFrame]:
    csv_path: str = os.path.join("data", "auxiliary-data", file_name)
    df: DataFrame = pd.read_csv(csv_path)
    print(f"Number of rows in {file_name}: {len(df)}")
    return df[["LONGITUDE", "LATITUDE"]].values.tolist(), df


if __name__ == "__main__":
    # https://project-osrm.org/docs/v5.5.1/api/?language=cURL#table-service
    src_file: str = "sg-hdb-block-details.csv"
    out_file: str = "hdb-block-walking-distance.csv"
    src_coords, df = get_coords(src_file)
    n_homes: int = len(src_coords)
    src_idxs_str: str = ";".join(map(str, range(n_homes)))
    for dest_file in os.listdir(os.path.join("data", "auxiliary-data")):
        if dest_file in [src_file, out_file]:
            continue
        print("Processing", dest_file, "...")
        t: float = time.time()

        dest_coords, _ = get_coords(dest_file)
        coords: list[tuple[float, float]] = src_coords + dest_coords
        dest_idxs_str: str = ';'.join(map(str, range(n_homes, len(coords))))
        url: str = f"http://localhost:5000/table/v1/foot/{';'.join([f"{lon},{lat}" for lon, lat in coords])}"
        params: dict[str, str] = {
            "sources": src_idxs_str,
            "destinations": dest_idxs_str,
            "annotations": "distance"
        }
        res: requests.Response = requests.get(url, params=params)
        res.raise_for_status()
        tbl: dict = res.json()
        # [N_SRC, N_DEST]
        distance_matrix: list[list[Optional[float]]] = tbl["distances"]
        for row in distance_matrix:
            for i, val in enumerate(row):
                if val is None:
                    row[i] = np.nan
        df["dist-to-" + dest_file[3: -4]] = Series(np.nanmin(distance_matrix, axis=1))
        print("Completed in", round(time.time() - t, 3), "seconds")
    df.to_csv(os.path.join("data", "auxiliary-data", out_file))
