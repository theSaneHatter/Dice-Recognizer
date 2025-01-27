from PIL import Image, ImageDraw, ImageEnhance
import PIL.Image
from lib import *
import numpy as np
import math
from scipy import stats
import cv2
start = time.time()
#purple is ~90,0,70
#green ~90,115,0

Dice = Image.open('./assets/Dice_optimal.jpg') 



#sharpness 
sharpness = ImageEnhance.Sharpness(Dice)
Dice = sharpness.enhance(1)

#contrast 
contrast = ImageEnhance.Contrast(Dice)
Dice = contrast.enhance(1)
# Dice.show()

#brightness
brightness = ImageEnhance.Brightness(Dice)
Dice = brightness.enhance(1)

# resize 
print(Dice.size)
h,w = Dice.size
d = 10
h,w = round(h/d),round(w/d)
print('new size', h,w)
time.sleep(2)
size = (h,w)
Dice = Dice.resize(size)




# We have edge detection!

# If the die non-pip and the background, edge detection can find only the pips if we use just two buckets.
# This is great!
# But if there are more than one die, and they are close, how do we differentate the dice?
# We can do edge detection with like 30 buckets to get edges where the dice are
# and then find what columns and rows we need to split on.
# Then use those to split the two bucket bitmap.



pixels = edge_detect(Dice,buckets=2)

# pixels = np.random.randint(0,2,(30,33))

pixels = trim_all_blanks(pixels)
print('unique values:',np.unique(pixels))

# pixels = remove_small_lines(pixels,10)
print('unique values after lines_uneque_int():',np.unique(pixels))

print(trues_unique_int(pixels))


pixels = np.multiply(pixels, 255)
Dice = Image.fromarray(pixels)
#grayscale 
# Dice = Dice.resize()
Dice.show()



total_time = time.time() - start
print(f'\033[32mProcess finished.\nElapsed time: {round(total_time,5)} secends.\033[0m')



