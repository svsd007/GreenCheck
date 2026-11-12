import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling

# creates an image of the specified place and compares the change in vegetation between the given red and nir08 images
class Comparator:
    def __init__(self, imgs1, imgs2):
        self.imgs1 = imgs1
        self.imgs2 = imgs2        

    # EFFECTS: returns the change in 2d matrix of NDVI values between the old and new image
    def getNDVI(self):
        image1Red, image1NIR = self.imgs1[0], self.imgs1[1]
        image2Red, image2NIR = self.imgs2[0], self.imgs2[1]

        ndvi1 = np.full(image1Red.shape, np.nan, dtype=np.float32)
        ndvi2 = np.full(image2Red.shape, np.nan, dtype=np.float32)

        denominator1 = image1NIR + image1Red
        validVector1 = denominator1 != 0
        ndvi1[validVector1] = (image1NIR[validVector1] - image1Red[validVector1]) / denominator1[validVector1]

        denominator2 = image2NIR + image2Red
        validVector2 = denominator2 != 0
        ndvi2[validVector2] = (image2NIR[validVector2] - image2Red[validVector2]) / denominator2[validVector2]

        return ndvi2 - ndvi1