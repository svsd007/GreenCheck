import Backend.ImageGenerator as ImageGenerator
import Backend.Comparator as Comparator
import Backend.ImageSearcher as ImageSearcher

import matplotlib.pyplot as plt

imgsearcger = ImageSearcher.ImageSearcher("1990", "2024", "summer", -123.3, 49.1, -122.8, 49.4)

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

# ndvi = comparison.getNDVI()

# # 4. Display and save the NDVI image
# plt.close("all")


# plt.figure(figsize=(8, 6))
# plt.imshow(ndvi, cmap="RdYlGn", vmin=-1, vmax=1)
# plt.colorbar(label="NDVI")
# plt.title(f"Vancouver NDVI — {item.datetime.date()} -> {item2.datetime.date()}")
# plt.axis("off")
# plt.tight_layout()
# plt.savefig("vancouver_ndvi.png", dpi=150)
# plt.show()

# print("Saved vancouver_ndvi.png")
