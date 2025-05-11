
import overpy
import geopandas as gpd
from shapely.geometry import Polygon
from tqdm import tqdm


class OverpassAPI:
    def __init__(self) -> None:
        self._api = overpy.Overpass()
    
    def _get_bbox_landuse(self, bbox: tuple[float, float, float, float]) -> overpy.Result:
        """Fetches all ways and relations with a landuse tag within bounding box.
        
        Args:
            bbox (tuple[float, float, float, float]): Tuple containing (x,y) coordinate pairs for the bbox.
        
        Returns:
            overpy.Result: Result object response to the query.
        """
        print("Querying Overpass API...")
        query = f"""
            wr["landuse"]({bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]});
            (._;>;);
            out body;
            """
        return self._api.query(query)
    
    def _overpass_result_to_gdf(self, result: overpy.Result) -> gpd.GeoDataFrame:
        """Parses and cleans the overpy.Result object into a GeoDataFrame.
        
        Args:
            result (overpy.Result): Result of query to Overpass API.

        Returns:
            gpd.GeoDataFrame: Polygons from the overpy.Result and their landuse tag.
        """
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
        """Queries and cleans landuse results from the Overpass API.
        
        Args:
            bbox (tuple[float, float, float, float]): Tuple containing (x,y) pairs for the bounding box.
        
        Returns:
            gpd.GeoDataFrame: Polygons from the overpy.Result and their landuse tag.
        """
        result = self._get_bbox_landuse(bbox)
        return self._overpass_result_to_gdf(result)


if __name__ == "__main__":
    overpass_api = OverpassAPI()

    bbox = (55.66731601212282, 12.560585920836248, 55.699960803118294, 12.607727632258538)
    gdf = overpass_api.get_land_use_gdf(bbox)
    gdf.explore("landuse").save("assets/map.html")