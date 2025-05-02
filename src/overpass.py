
import overpy
import geopandas as gpd
from shapely.geometry import Polygon
from tqdm import tqdm


class OverpassAPI:
    def __init__(self) -> None:
        self._api = overpy.Overpass()
    
    def _get_bbox_landuse(self, bbox: tuple[float, float, float, float]) -> overpy.Result:
        print("Querying Overpass API...")
        query = f"""
            wr["landuse"]({bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]});
            (._;>;);
            out body;
            """
        return self._api.query(query)
    
    def _overpass_result_to_gdf(self, result: overpy.Result) -> gpd.GeoDataFrame:
        print("Converting to GeoDataFrame...")
        geoms = []
        land_use = []
        for way in tqdm(result.ways):
            try:
                coords = [(node.lon, node.lat) for node in way.nodes]
                
                if coords:
                    polygon = Polygon(coords)
                    geoms.append(polygon)
                    land_use.append(way.tags.get("landuse"))
            except:
                pass

        return gpd.GeoDataFrame({"geometry": geoms, "landuse": land_use}, crs="EPSG:4326")
    
    def get_land_use_gdf(self, bbox: tuple[float, float, float, float])-> gpd.GeoDataFrame:
        result = self._get_bbox_landuse(bbox)
        return self._overpass_result_to_gdf(result)


if __name__ == "__main__":
    overpass_api = OverpassAPI()

    bbox = (51.24613621117362, -0.5206335385957582, 51.697294958769845, 0.2820596718485233)
    gdf = overpass_api.get_land_use_gdf(bbox)