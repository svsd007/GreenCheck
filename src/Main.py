import Backend.ImageGenerator as ImageGenerator
import Backend.Comparator as Comparator
import Backend.ImageSearcher as ImageSearcher

import numpy as np

import matplotlib.pyplot as plt

imgsearcher = ImageSearcher.ImageSearcher("1990", "2024", "summer", -123.3, 49.1, -122.8, 49.4)
oldImgs, newImgs = imgsearcher.getProcessedImgs()
comparator = Comparator.Comparator(oldImgs, newImgs)

# get img

# ImgGenerator1 = ImageGenerator.ImageGenerator("1980", "summer")
# ImgGenerator1.searchImg(-123.3, 49.1, -122.8, 49.4)
# item = ImgGenerator1.getImg()

# ImgGenerator2 = ImageGenerator.ImageGenerator("2024", "summer")
# ImgGenerator2.searchImg(-123.3, 49.1, -122.8, 49.4)
# item2 = ImgGenerator2.getImg()

# print("Image:", item.id)
# print("Date:", item.datetime)
# print("Cloud cover:", item.properties.get("eo:cloud_cover"), "%")

# print("Image:", item2.id)
# print("Date:", item2.datetime)
# print("Cloud cover:", item2.properties.get("eo:cloud_cover"), "%")

# comparison = Comparator.Comparator(item, item2)

ndvi = comparator.getNDVI()

# display and save the NDVI image
plt.close("all")

oldYear, newYear, season = imgsearcher.getDate()

plt.figure(figsize=(8, 6))
plt.colorbar(label="NDVI")

limit = np.nanpercentile(np.abs(ndvi), 98)

plt.imshow(
    ndvi,
    cmap="RdYlGn",
    vmin=-limit,
    vmax=limit
)

plt.title(f"Vancouver NDVI — {season} - {oldYear} -> {newYear}")
plt.axis("off")
plt.tight_layout()
plt.savefig("vancouver_ndvi.png", dpi=150)
plt.show()

print("Saved vancouver_ndvi.png")
