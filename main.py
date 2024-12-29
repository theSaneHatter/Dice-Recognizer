from PIL import Image, ImageDraw, ImageEnhance
from lib import *
import numpy as np
import math
from scipy import stats
start = time.time()
#purple is ~90,0,70
#green ~90,115,0

Dice1 = Image.open('./assets/Dice1.jpg') 


# resize 
print(Dice1.size)
h,w = Dice1.size
h,w = round(h/30),round(w/30)
print('new size' , h,w)
size = (h,w)
Dice1 = Dice1.resize(size)

# contrast 
contrast = ImageEnhance.Contrast(Dice1)
Dice1 = contrast.enhance(1)

#brightness
brightness = ImageEnhance.Brightness(Dice1)
Dice1 = brightness.enhance(1)

#sharpness 
sharpness = ImageEnhance.Sharpness(Dice1)
Dice1 = sharpness.enhance(3)



Dice1.show()

# Convert the image to a numpy array
pixels = np.array(Dice1)
print(pixels.shape)
# Print the pixel values
# print(pixel_values)




pixels_with_location = give_pixels_location(pixels)


sorted_by_color = give_pixels_location(sort_by_color(pixels_with_location), remove=True)

Dice1 = Image.fromarray(sorted_by_color)
Dice1.show()

total_time = time.time() - start
print(f'\033[32mProcess finished.\nElapsed time: {round(total_time,5)} secends.\033[0m')



