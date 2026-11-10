import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling


from rasterio.transform import array_bounds

# creates an image of the specified place and compares the change in vegetation between these two images
class Comparator:
    img1 = None # older img
    img2 = None # newer img

    def __init__(self, img1, img2):
        self.img1 = img1
        self.img2 = img2        


    # REQUIRES: band be one of red, blue, green, nir08
    # EFFECTS: returns a 2d array of the specified band pixel values from the given image
    def getBand(self, image, band):
        src = rasterio.open(image.assets[band].href)
        arr = src.read(1).astype(np.float32)
        profile = src.profile
        src.close()
        return arr, profile

    # EFFECTS: returns the change in 2d matrix of NDVI values between the old and new image
    def getNDVI(self):
        image1Red, profile1 = self.getBand(self.img1, "red")
        image1NIR, _ = self.getBand(self.img1, "nir08")

        image2Red, profile2 = self.getBand(self.img2, "red")
        image2NIR, _ = self.getBand(self.img2, "nir08")

        ndvi1 = np.full(image1Red.shape, np.nan, dtype=np.float32)
        ndvi2 = np.full(image2Red.shape, np.nan, dtype=np.float32)

        denominator1 = image1NIR + image1Red
        validVector1 = denominator1 != 0
        ndvi1[validVector1] = (image1NIR[validVector1] - image1Red[validVector1]) / denominator1[validVector1]

        denominator2 = image2NIR + image2Red
        validVector2 = denominator2 != 0
        ndvi2[validVector2] = (image2NIR[validVector2] - image2Red[validVector2]) / denominator2[validVector2]

        ndvi2Aligned = np.full(ndvi1.shape, np.nan, dtype=np.float32)


        # reproject because dimension of images don't match
        reproject(
            source=ndvi2,
            destination=ndvi2Aligned,
            src_transform=profile2["transform"],
            src_crs=profile2["crs"],
            dst_transform=profile1["transform"],
            dst_crs=profile1["crs"],
            src_nodata=np.nan,
            dst_nodata=np.nan,
            resampling=Resampling.bilinear
        )

        return ndvi2Aligned - ndvi1