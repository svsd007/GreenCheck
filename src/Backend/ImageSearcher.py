import Backend.ImageGenerator as ImageGenerator
import Backend.Comparator as Comparator
import rasterio

from rasterio.mask import mask
from shapely.geometry import box, mapping


# Represents the Image searcher to get images with averaed pixel values and overlapping bounds in the area of interest
class ImageSearcher:
    def __init__(self, oldYear : str, newYear : str, season : str, minLongitude : float, minLatitude : float, maxLongitude : float, maxLatitude : float):

        self.aoi = mapping(box(minLongitude, minLatitude, maxLongitude, maxLatitude))

        generator1 = ImageGenerator.ImageGenerator(oldYear, season)
        generator2 = ImageGenerator.ImageGenerator(newYear, season)

        generator1.searchImg(minLongitude, minLatitude, maxLongitude, maxLatitude)
        generator2.searchImg(minLongitude, minLatitude, maxLongitude, maxLatitude)

        imageSet1 = generator1.getImg()
        imageSet2 = generator2.getImg()

        oldMedianImage, newMedianImage = self.mergeImages(imageSet1, imageSet2)


    def mergeImages(self, oldImageSet, newImageSet):
        redSet1 = self.getImageSet(oldImageSet)
        niro8Set1 = self.getImageSet(oldImageSet)

        redSet2 = self.getImageSet(newImageSet)
        niro8Set2 = self.getImageSet(newImageSet)

        

    def getImageSet(self, images):
        redImages = []
        nir08Images = []

        for image in images:
            with rasterio.open(image.assets["red"].href) as src:
                red, transform = mask(src, [self.aoi], crop=True)
                redImages.append(red[0])

            # Crop NIR band
            with rasterio.open(image.assets["nir08"].href) as src:
                nir, transform = mask(src, [self.aoi], crop=True)
                nir08Images.append(nir[0])

        return redImages, nir08Images

    def compositeImage(self, images):



        


