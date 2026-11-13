import backend.ImageGenerator as ImageGenerator
import numpy as np
import rasterio

from rasterio.mask import mask
from rasterio.vrt import WarpedVRT
from rasterio.enums import Resampling
from rasterio.warp import transform_geom, transform_bounds
from rasterio.transform import from_origin
from math import floor, ceil
from shapely.geometry import box, mapping

# Represents the Image searcher to get images with averaed pixel values and overlapping bounds in the area of interest
class ImageSearcher:
    def __init__(self, oldYear : str, newYear : str, season : str, minLongitude : float, minLatitude : float, maxLongitude : float, maxLatitude : float):

        self.aoi = mapping(box(minLongitude, minLatitude, maxLongitude, maxLatitude))
        self.bounds = (minLongitude, minLatitude, maxLongitude, maxLatitude)

        self.oldYear = oldYear
        self.newYear = newYear
        self.season = season

        generator1 = ImageGenerator.ImageGenerator(oldYear, season)
        generator2 = ImageGenerator.ImageGenerator(newYear, season)

        generator1.searchImg(minLongitude, minLatitude, maxLongitude, maxLatitude)
        generator2.searchImg(minLongitude, minLatitude, maxLongitude, maxLatitude)

        imageSet1 = generator1.getImg()
        imageSet2 = generator2.getImg()

        self.oldMedianImage, self.newMedianImage = self.mergeImages(imageSet1, imageSet2)

    # REQUIRES: oldImageSet date < newImageSet date
    # EFFECTS: creates an image composite with ocean filtered out 
    def mergeImages(self, oldImageSet, newImageSet):
        with rasterio.open(oldImageSet[0].assets["red"].href) as src:

            target_crs = src.crs

            xres = abs(src.res[0])
            yres = abs(src.res[1])

        left, bottom, right, top = transform_bounds("EPSG:4326", target_crs, *self.bounds)

        left = floor(left / xres) * xres
        right = ceil(right / xres) * xres
        bottom = floor(bottom / yres) * yres
        top = ceil(top / yres) * yres

        target_width = ceil((right - left) / xres)
        target_height = ceil((top - bottom) / yres)

        target_transform = from_origin(left, top, xres, yres)

        redSet1, nirSet1, qaSet1 = self.getImageSet(oldImageSet, target_crs, target_transform, target_width, target_height)
        redSet2, nirSet2, qaSet2 = self.getImageSet(newImageSet, target_crs, target_transform, target_width, target_height)

        redSet1, nirSet1 = self.filterQA(redSet1, nirSet1, qaSet1)
        redSet2, nirSet2 = self.filterQA(redSet2, nirSet2, qaSet2)

        oldRed = self.compositeImage(redSet1)
        oldNir = self.compositeImage(nirSet1)

        newRed = self.compositeImage(redSet2)
        newNir = self.compositeImage(nirSet2)

        return (oldRed, oldNir), (newRed, newNir)

    # EFFECTS: returns the redImages, nir08Images, and qaImages based on Image set and target area of interest
    def getImageSet(self, images, target_crs, target_transform, target_width, target_height):
        redImages = []
        nir08Images = []
        qaImages = []

        aoi = transform_geom(
            "EPSG:4326",
            target_crs,
            self.aoi
        )
        for image in images:
            with rasterio.open(image.assets["red"].href) as src:
                with WarpedVRT(
                    src,
                    crs=target_crs,
                    transform=target_transform,
                    width=target_width,
                    height=target_height,
                    dtype="float32",
                    nodata=np.nan
                ) as vrt:

                    red, _ = mask(vrt, [aoi], crop=False, filled=False)
                    redData = red[0].astype(np.float32).filled(np.nan)
                    redData = redData * 0.0000275 - 0.2
                    redImages.append(redData)

            with rasterio.open(image.assets["nir08"].href) as src:
                with WarpedVRT(
                    src,
                    crs=target_crs,
                    transform=target_transform,
                    width=target_width,
                    height=target_height,
                    dtype="float32",
                    nodata=np.nan
                ) as vrt:
                    nir, _ = mask(vrt,[aoi], crop=False, filled=False)
                    nirData = nir[0].astype(np.float32).filled(np.nan)
                    nirData = nirData * 0.0000275 - 0.2
                    nir08Images.append(nirData)

            with rasterio.open(image.assets["qa_pixel"].href) as src:
                with WarpedVRT(
                    src,
                    crs=target_crs,
                    transform=target_transform,
                    width=target_width,
                    height=target_height,
                    resampling=Resampling.nearest
                ) as vrt:

                    qa, _ = mask(vrt, [aoi], crop=False, filled=False)
                    qaImages.append(qa[0])

        return redImages, nir08Images, qaImages
    
    # REQUIRES: len(redimgs) == len(nirimgs) == len(qaimgs)
    # EFFECTS: returns redImages and nirImages after being filtered for cloud, snow, and all qaimg filter options
    def filterQA(self, redimgs, nirimgs, qaimgs):
        redOutput = []
        nirOutput = []

        for redImg, nirImg, qaImg in zip(redimgs, nirimgs, qaimgs):
            waterMask = (qaImg.data.astype(np.uint16) & (1 << 7)) != 0
            waterMask |= np.ma.getmaskarray(qaImg)

            redImg[waterMask] = np.nan
            nirImg[waterMask] = np.nan

            redOutput.append(redImg)
            nirOutput.append(nirImg)

        return redOutput, nirOutput

    # EFFECTS: returns the median pixel values across the image set based on the same pixel location
    def compositeImage(self, images):
        return np.nanmedian(np.stack(images), axis=0)

    # EFFECTS: returns the composite images
    def getProcessedImgs(self):
        return self.oldMedianImage, self.newMedianImage

    # EFFECTS: returns years and season of the composite images
    def getDate(self):
        return self.oldYear, self.newYear, self.season




        


