import os

import numpy as np
import pandas as pd
import requests


def get_coords(file_name: str) -> list[tuple[float, float]]:
    csv_path: str = os.path.join("data", "auxiliary-data", file_name)
    df: pd.DataFrame = pd.read_csv(csv_path)
    print(f"Number of rows in {file_name}: {len(df)}")
    return df[["LONGITUDE", "LATITUDE"]].values.tolist()


if __name__ == "__main__":
    # https://project-osrm.org/docs/v5.5.1/api/?language=cURL#table-service
    homes: list[tuple[float, float]] = get_coords("sg-hdb-block-details.csv")
    n_homes: int = len(homes)
    src_idxs_str: str = ";".join(map(str, range(n_homes)))

    coords: list[tuple[float, float]] = homes + get_coords("sg-gov-hawkers.csv")
    dest_idxs_str: str = ';'.join(map(str, range(n_homes, len(coords))))
    url = f"http://localhost:5000/table/v1/foot/{';'.join([f"{lon},{lat}" for lon, lat in coords])}"

    params = {
        "sources": src_idxs_str,
        "destinations": dest_idxs_str,
        "annotations": "distance"
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    tbl = res.json()
    # [N_SRC, N_DEST]
    distance_matrix: np.ndarray = np.array(tbl["distances"])
    print(distance_matrix)
