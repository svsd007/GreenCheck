from Backend.ImageGenerator import ImageGenerator
from Backend.Comparator import Comparator
import rasterio
import numpy as np
import matplotlib.pyplot as plt

# get img

ImgGenerator1 = ImageGenerator("2000-01-01/2010-01-01")
ImgGenerator1.searchImg(-123.3, 49.1, -122.8, 49.4)
item = ImgGenerator1.getImg()

ImgGenerator2 = ImageGenerator("2016-01-01/2026-01-01")
ImgGenerator2.searchImg(-123.3, 49.1, -122.8, 49.4)
item2 = ImgGenerator1.getImg()

print("Image:", item.id)
print("Date:", item.datetime)
print("Cloud cover:", item.properties.get("eo:cloud_cover"), "%")

NDVICompare = Comparator(item, item2)

# 2. Read the red and near-infrared bands
with rasterio.open(item.assets["red"].href) as src:
    red = src.read(1).astype(np.float32)
    profile = src.profile.copy()

with rasterio.open(item.assets["nir08"].href) as src:
    nir = src.read(1).astype(np.float32)



# 3 Calculate NDVI
# Mask invalid pixels and avoid division by zero
denominator = nir + red
ndvi = np.full(red.shape, np.nan, dtype=np.float32)

valid = denominator != 0
ndvi[valid] = (nir[valid] - red[valid]) / denominator[valid]

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
