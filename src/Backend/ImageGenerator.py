from pystac_client import Client
import planetary_computer as pc


# import planetary_computer
# import pystac_client
# import geopandas
# import rich.table
# from IPython.display import Image

# print("Opening catalog...", flush=True)

# catalog = pystac_client.Client.open(    
#     "https://planetarycomputer.microsoft.com/api/stac/v1",
#     )

# print("Catalog opened!", flush=True)

# time_range = "2025-01-01/2025-12-31"
# bbox = [-122.96, 49.10, -122.88, 49.17]
# search = catalog.search(collections=["sentinel-2-l2a"], bbox=bbox, datetime=time_range)
# items = search.item_collection()
# print(len(items))
# print("Item collection!", flush=True)

# selected_item = min(
#     items,
#     key=lambda item: item.properties["eo:cloud_cover"]
# )

# print(selected_item)


# df = geopandas.GeoDataFrame.from_features(items.to_dict(), crs="epsg:4326")
# df

# table = rich.table.Table("Asset Key", "Description")
# for asset_key, asset in selected_item.assets.items():
#     table.add_row(asset_key, asset.title)


# selected_item.assets["rendered_preview"].to_dict()

# import webbrowser

# map_link = selected_item.get_single_link("preview")
# webbrowser.open(map_link.href)



# find a satillite with filtered cloudiness based on longitude and latitude
class ImageGenerator:
    datetime = ""
    items = None

    # EFFECTS: connects to satillite imagery catalog from microsoft
    # MODIFIES: datetime
    # format datetime as "YYYY-MM-DD-YYYY-MM-DD"

    def __init__(self, datetime : str):
        self.catalog = Client.open(
            "https://planetarycomputer.microsoft.com/api/stac/v1",
            # modifier=pc.sign_inplace,
        )

        self.datetime = datetime

    # MODIFIES: items
    # EFFECTS: this seraches images based on c2-l2, longitutde and latitude, and date range
    def searchImg(self, min_longitude : float, min_latitude : float, max_longitude : float, max_latitude : float):
        search = self.catalog.search(
            collections = ["landsat-c2-l2"],
            bbox = [min_longitude, min_latitude, max_longitude, max_latitude],
            datetime = self.datetime,
            query = {"eo:cloud_cover": {"lt": 20}},     # filters images with les than 20% cloud coverage
            # max_items = 10,
        )
        bbox = [min_longitude, min_latitude, max_longitude, max_latitude]
        self.items = list(search.items())
        print(f"----------------------------------------------------------------\nItems in {bbox}:\n{len(self.items)}\nIn the time: \n {self.datetime}\n----------------------------------------------------------------\n")

    # EFFECTS: filter and get imgs
    def getImg(self):
        if not self.items:
            raise RuntimeError("No suitable images found. Try a wider date range.")
        
        self.item = min(
            self.items,
            key=lambda x: x.properties.get("eo:cloud_cover", 100),
        )
        return self.item


    # EFFECTS: returns date
    def getDate(self):
        return self.item.datetime


