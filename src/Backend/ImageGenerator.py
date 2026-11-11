import planetary_computer as pc
from pystac_client import Client

# find a satillite with filtered cloudiness based on longitude and latitude
class ImageGenerator:
    # REQUIRES: datetime as "YYYY-MM-DD-YYYY-MM-DD"
    # MODIFIES: datetime
    # EFFECTS: connects to satillite imagery catalog from microsoft
    def __init__(self, year : str, season : str):
        self.items = []
        self.datetime = ""
    
        self.seasons = {
            "winter" : ("12-01", "02-28"),
            "spring" : ("03-01", "05-31"),
            "summer" : ("06-01", "08-31"),
            "autumn" : ("09-01", "11-30")
        }

        self.catalog = Client.open(
            "https://planetarycomputer.microsoft.com/api/stac/v1",
            modifier=pc.sign_inplace,
        )

        start, end = self.seasons[season.lower()]
        if season.lower() == "winter":
            self.datetime = f"{int(year)-1}-12-01/{year}-02-28"
        else:
            self.datetime = f"{year}-{start}/{year}-{end}"

    # MODIFIES: items
    # EFFECTS: this seraches images based on c2-l2, longitutde and latitude, and date range
    def searchImg(self, minLongitude : float, minLatitude : float, maxLongitude : float, maxLatitude : float):
        search = self.catalog.search(
            collections = ["landsat-c2-l2"],
            bbox = [minLongitude, minLatitude, maxLongitude, maxLatitude],
            datetime = self.datetime,
            query = {"eo:cloud_cover": {"lt": 30}},     # filters images with less than 20% cloud coverage
            max_items = 500,
        )
        
        self.items = list(search.items())

    # EFFECTS: filter and returns a STAC item
    def getImg(self):
        if not self.items:
            raise RuntimeError("No suitable images found. Try a wider date range.")
        
        if len(self.items) < 5:
            raise RuntimeError("insufficient images from season")
        
        self.items.sort(
            key=lambda item: item.properties.get("eo:cloud_cover", 100)
        )

        return self.items[:5]
        


    # EFFECTS: returns date
    def getDate(self, img):
        return img.datetime


