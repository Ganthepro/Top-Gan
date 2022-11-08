from PIL import Image
import numpy as np
img = Image.open("test.png")

print(img.mode) #RGB
print(img.size)

width = img.size[0]
height = img.size[1]
for i in range(0,width):# process all pixels
    for j in range(0,height):
            img.putpixel((i,j),(255, 0, 0))
img.show()