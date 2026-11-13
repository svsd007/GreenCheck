import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling

# creates an image of the specified place and compares the change in vegetation between the given red and nir08 images
class Comparator:
    # REQUIRES: date of imgs1 < date of imgs2
    def __init__(self, imgs1, imgs2):
        self.imgs1 = imgs1
        self.imgs2 = imgs2        

    # EFFECTS: returns the change in 2d matrix of NDVI values between the old and new image
    def getNDVI(self):
        image1Red, image1NIR = self.imgs1[0], self.imgs1[1]
        image2Red, image2NIR = self.imgs2[0], self.imgs2[1]

        ndvi1, change1 = self.calculateNDVI(image1Red, image1NIR)
        ndvi2, change2 = self.calculateNDVI(image2Red, image2NIR)

        percentChange = ( (change2 - change1) / change1 ) * 100

        denominator2 = image2NIR + image2Red

        return ndvi2 - ndvi1, ndvi2, ndvi1, percentChange
    
    # EFFECTS: takes composite red and nir and returns composite ndvi img and NDVI change amount in number of pixels
    #          Filters invalid denominator values and filters large ndvi pixel values 
    def calculateNDVI(self, imgRed, imgNIR):
        ndvi = np.full(imgRed.shape, np.nan, dtype=np.float32)

        numerator = imgNIR - imgRed
        denominator = imgNIR + imgRed
        valid = (denominator != 0) & (denominator > 0.001) & (np.isfinite(denominator))

        ndvi[valid] = numerator[valid]/denominator[valid]

        changeMatrix = (ndvi <= -0.10) | (ndvi >= 0.10)
        changeAmount = np.count_nonzero(changeMatrix)

        return ndvi, changeAmount


