# check Pillow version number
import PIL
print('Pillow Version:', PIL.__version__)

# load and show an image with Pillow
from PIL import Image
import numpy as np
from numpy import asarray
# Open the image form working directory
image = Image.open('../data/1mb.jpg')
# summarize some details about the image
print(image.format)
print(image.size)
print(image.mode)
# show the image
# image.show()


data = asarray(image)
print(type(data))
# summarize shape
print(data.shape)

# create Pillow image
image2 = Image.fromarray(data)
print(type(image2))

# summarize image details
print(image2.mode)
print(image2.size)
print(data)


np.save("../data/np_array.npy", data)