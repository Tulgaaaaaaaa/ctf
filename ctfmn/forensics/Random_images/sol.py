from PIL import Image

from PIL import Image, ImageChops
im1 = Image.open('image1.png')
im2 = Image.open('image2.png')

im3 = ImageChops.add(ImageChops.subtract(im2, im1), ImageChops.subtract(im1, im2))

image = im3.convert('RGB')
pixels = image.load()

for i in range(image.width):
    for j in range(image.height):
        r, g, b = pixels[i, j]
        pixels[i, j] = (0, g, 0)

image.show()
