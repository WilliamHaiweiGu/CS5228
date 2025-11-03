# Distance Matrix Notes
Each `[amenity_name]_mat.npy` is a distance matrix computed from  `[sg-hdb-block-details.csv]` and `[amenity_name].csv`.

Each distance matrix can be loaded with `distance_mat: np.ndarray = np.load("my_array.npy")`. The array is 2D with size `(N_HDB, N_amenity)`

If there are no walking path between two points, the walking distance is recorded as $+\infty$.