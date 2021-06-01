from PIL import Image

n_number = 72
for no in range(0, 20):
    img = Image.open(f"test_a/img-{str(n_number).zfill(4)}.png")
    cropped_img = img.crop((388, 388, 612, 612))
    cropped_img.save(f"test_a/0/img-{str(n_number).zfill(4)}.png")
    n_number += 3


# 500-(224/2)