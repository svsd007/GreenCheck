from Backend.ImageGenerator import ImageGenerator
from Backend.Comparator import Comparator
import rasterio
import numpy as np
import matplotlib.pyplot as plt

import planetary_computer as pc


# get img



ImgGenerator1 = ImageGenerator("2000-01-01/2000-06-01")
ImgGenerator1.searchImg(-123.3, 49.1, -122.8, 49.4)
item = ImgGenerator1.getImg()

ImgGenerator2 = ImageGenerator("2025-01-01/2025-12-31")
ImgGenerator2.searchImg(-123.3, 49.1, -122.8, 49.4)
item2 = ImgGenerator2.getImg()




print("Image:", item.id, flush = True)
print("Date:", item.datetime)
print("Cloud cover:", item.properties.get("eo:cloud_cover"), "%")


print("Image:", item2.id, flush = True)
print("Date:", item2.datetime)
print("Cloud cover:", item2.properties.get("eo:cloud_cover"), "%")

NDVICompare = Comparator(item, item2)

# 2. Read the red and near-infrared bands
red_url = pc.sign(item.assets["red"].href)
print("done siging")
with rasterio.open(red_url) as src:
    red = src.read(1).astype(np.float32)
    profile = src.profile.copy()

print("done opning")

nir_url = pc.sign(item.assets["nir08"].href)
print("done signing again")

with rasterio.open(nir_url) as src:
    nir = src.read(1).astype(np.float32)

print("done opening again")




red_url2 = pc.sign(item2.assets["red"].href)
print("done siging")
with rasterio.open(red_url2) as src:
    red2 = src.read(1).astype(np.float32)
    profile2 = src.profile.copy()

print("done opning")

nir_url2 = pc.sign(item2.assets["nir08"].href)
print("done signing again")

with rasterio.open(nir_url2) as src:
    nir2 = src.read(1).astype(np.float32)

print("done opening again")


# 3 Calculate NDVI
# Mask invalid pixels and avoid division by zero
denominator = nir + red
ndvi = np.full(red.shape, np.nan, dtype=np.float32)

valid = denominator != 0
ndvi[valid] = (nir[valid] - red[valid]) / denominator[valid]




denominator2 = nir2 + red2
ndvi2 = np.full(red2.shape, np.nan, dtype=np.float32)

valid2 = denominator2 != 0
ndvi2[valid2] = (nir2[valid2] - red2[valid2]) / denominator2[valid2]



# 4. Display and save the NDVI image
plt.figure(figsize=(8, 6))
plt.imshow(ndvi, cmap="RdYlGn", vmin=-1, vmax=1)
plt.colorbar(label="NDVI")
plt.title(f"Vancouver NDVI — {item.datetime.date()}")
plt.axis("off")
plt.tight_layout()
plt.savefig("vancouver_ndvi.png", dpi=150)
plt.show()

print("Saved vancouver_ndvi.png")
