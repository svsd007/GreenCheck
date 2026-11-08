import rasterio
import numpy as np

# creates an image of the specified place and compares the change in vegetation between these two images
class Comparator:
    img1 = None
    img2 = None

    def __init__(self, img1, img2):
        self.img1 = img1
        self.img2 = img2        


    # REQUIRES: band be one of red, blue, green, nir08
    # EFFECTS: returns a 2d array of the specified band pixel values from the given image
    def getBand(self, image, band):
        src = rasterio.open(image.assets[band].href)
        arr = src.read(1).astype(np.float32)
        src.close()
        return arr

    # EFFECTS: returns the change in 2d matrix of NDVI values for 2 given images
    def getNDVI(self):
        image1Red = self.getBand(self.img1, "red")
        image1NIR = self.getBand(self.img1, "nir08")

        image2Red = self.getBand(self.img2, "red")
        image2NIR = self.getBand(self.img2, "nir08")

        ndvi1 = np.full(image1Red.shape, np.nan, dtype=np.float32)
        ndvi2 = np.full(image2Red.shape, np.nan, dtype=np.float32)

        denominator1 = image1NIR + image1Red
        validVector1 = denominator1 != 0
        ndvi1[validVector1] = (image1NIR[validVector1] - image1Red[validVector1]) / denominator1[validVector1]

        denominator2 = image2NIR + image2Red
        validVector2 = denominator2 != 0
        ndvi2[validVector2] = (image2NIR[validVector2] - image2Red[validVector2]) / denominator2[validVector2]

        return np.abs(ndvi1 - ndvi2)