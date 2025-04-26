
import overpy
import geopandas as gpd
from shapely.geometry import Polygon


class OverpassAPI:
    def __init__(self) -> None:
        self.api = overpy.Overpass()

    def _query_overpass(self, query: str) -> overpy.Result:
        return self.api.query(query)
    
    def _get_bbox_landuse(self, bbox: tuple[float, float, float, float]) -> overpy.Result:
        query = f"""
            [out:json];
            wr["landuse"]({bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]});
            out body;
            """
        return self._query_overpass(query)
    
    def _overpass_result_to_gdf(self, result: overpy.Result) -> gpd.GeoDataFrame:
        geoms = []
        for way in result.ways:
            coords = [(node.lon, node.lat) for node in way.nodes]
            
            if coords:
                polygon = Polygon(coords)
                geoms.append(polygon)
        return gpd.GeoDataFrame(geoms, crs="EPSG:4326")
    
    def get_land_use_gdf(self, bbox: tuple[float, float, float, float])-> gpd.GeoDataFrame:
        result = self._get_bbox_landuse(bbox)
        return self._overpass_result_to_gdf(result)


if __name__ == "__main__":
    overpass_api = OverpassAPI()

    bbox = (43.73129909633757, 7.415686982253379, 43.73942132881274, 7.42613427246315)
    gdf = overpass_api.get_land_use_gdf(bbox)
    print(gdf)