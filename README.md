# Compute shortest waling distances from HDBs to amenities
The running environment for this part is Linux.
1. Turn on Docker.
2. Install the OSRM server and turn it on:
```
cd "OSRM server"
./install.sh
./run.sh
```
3. Do not close the server. Compute distance matrix:
```
python "compute dist mat.py"
```
4. Compute the shortest distance from HDBs:
```
python "compute min dist.py"
```
# Distance Matrix Notes
Each `[amenity_name]_mat.npy` is a distance matrix computed from  `[sg-hdb-block-details.csv]` and `[amenity_name].csv`.

Each distance matrix can be loaded with `distance_mat: np.ndarray = np.load("my_array.npy")`. The array is 2D with size `(N_HDB, N_amenity)`

If there are no walking path between two points, the walking distance is recorded as $+\infty$.