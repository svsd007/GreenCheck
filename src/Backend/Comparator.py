import rasterio
import numpy as np

class Comparator:

    def __init__(self, img1, img2):
        url = img1.assets["red"].href
