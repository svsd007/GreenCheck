import planetary_computer as pc
from pystac_client import Client
import rasterio
import numpy as np
import matplotlib.pyplot as plt

# 1. Connect to the satellite imagery catalog
catalog = Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=pc.sign_inplace,
)

# 2. Search a small area around Vancouver
search = catalog.search(
    collections=["landsat-c2-l2"],
    bbox=[-123.3, 49.1, -122.8, 49.4],
    datetime="2026-01-01/2026-09-30",
    query={"eo:cloud_cover": {"lt": 20}},
    max_items=10,
)

items = list(search.items())

if not items:
    raise RuntimeError("No suitable images found. Try a wider date range.")

# Choose the least cloudy image
item = min(
    items,
    key=lambda x: x.properties.get("eo:cloud_cover", 100),
)

print("Image:", item.id)
print("Date:", item.datetime)
print("Cloud cover:", item.properties.get("eo:cloud_cover"), "%")

# 3. Read the red and near-infrared bands
with rasterio.open(item.assets["red"].href) as src:
    red = src.read(1).astype(np.float32)
    profile = src.profile.copy()

with rasterio.open(item.assets["nir08"].href) as src:
    nir = src.read(1).astype(np.float32)

# 4. Calculate NDVI
# Mask invalid pixels and avoid division by zero
denominator = nir + red
ndvi = np.full(red.shape, np.nan, dtype=np.float32)

valid = denominator != 0
ndvi[valid] = (nir[valid] - red[valid]) / denominator[valid]

# 5. Display and save the NDVI image
plt.figure(figsize=(8, 6))
plt.imshow(ndvi, cmap="RdYlGn", vmin=-1, vmax=1)
plt.colorbar(label="NDVI")
plt.title(f"Vancouver NDVI — {item.datetime.date()}")
plt.axis("off")
plt.tight_layout()
plt.savefig("vancouver_ndvi.png", dpi=150)
plt.show()

print("Saved vancouver_ndvi.png")
