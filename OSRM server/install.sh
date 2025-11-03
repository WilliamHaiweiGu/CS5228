curl -o city.osm.pbf https://download.geofabrik.de/asia/malaysia-singapore-brunei-251102.osm.pbf
curl -o foot.lua https://raw.githubusercontent.com/Project-OSRM/osrm-backend/master/profiles/foot.lua
docker pull osrm/osrm-backend
docker run -t -v "$(pwd):/data" osrm/osrm-backend osrm-extract -p /data/foot.lua /data/city.osm.pbf
docker run -t -v "$(pwd):/data" osrm/osrm-backend osrm-partition /data/city.osrm
docker run -t -v "$(pwd):/data" osrm/osrm-backend osrm-customize /data/city.osrm