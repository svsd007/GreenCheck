import planetary_computer as pc
from pystac_client import Client

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
            modifier=pc.sign_inplace,
        )

        self.datetime = datetime

    # MODIFIES: items
    # EFFECTS: this seraches images based on c2-l2, longitutde and latitude, and date range
    def searchImg(self, min_longitude : float, min_latitude : float, max_longitude : float, max_latitude : float):
        search = self.catalog.search(
            collections = ["landsat-c2-l2"],
            bbox = [min_longitude, min_latitude, max_longitude, max_latitude],
            datetime = self.datetime,
            query = {"eo:cloud_cover": {"lt": 20}},     # filters images with les than 20% cld coverage
            max_items = 10,
        )
        
        self.items = list(search.items())

    # EFFECTS: filter and get imgs
    def getImg(self):
        if not self.items:
            raise RuntimeError("No suitable images found. Try a wider date range.")
        
        item = min(
            self.items,
            key=lambda x: x.properties.get("eo:cloud_cover", 100),
        )
        return item


