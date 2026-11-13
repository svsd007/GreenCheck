import backend.ImageGenerator as ImageGenerator
import backend.Comparator as Comparator
import backend.ImageSearcher as ImageSearcher

import numpy as np

import matplotlib.pyplot as plt

imgsearcher = ImageSearcher.ImageSearcher("1990", "2024", "summer", -123.3, 49.1, -122.8, 49.4)
oldImgs, newImgs = imgsearcher.getProcessedImgs()
comparator = Comparator.Comparator(oldImgs, newImgs)

ndvi, ndvi1, ndvi2, percentChange = comparator.getNDVI()
print(f"{percentChange}")

# display and save the NDVI image
plt.close("all")

oldYear, newYear, season = imgsearcher.getDate()

valid = np.isfinite(ndvi)

limit = np.nanpercentile(np.abs(ndvi[valid]), 98)

plt.figure(figsize=(10, 8))

img = plt.imshow(
    np.ma.masked_invalid(ndvi),
    cmap="RdYlGn",
    vmin=-limit,
    vmax=limit
)

plt.colorbar(img, label="NDVI Change (2023 - 1984)")

plt.title(f"Vancouver NDVI Change - {oldYear} to {newYear}")
plt.axis("off")
plt.tight_layout()
plt.savefig("vancouver_ndvi.png", dpi=150)
plt.show()
