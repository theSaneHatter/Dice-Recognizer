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

#so bools dont look wierd
np.set_printoptions(formatter={'float': '{:0.2f}'.format})


Dice = Image.open('./assets/Dice4.jpg') 



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
d = 5
h,w = round(h/d),round(w/d)
print('new size', h,w)
time.sleep(2)
size = (h,w)
Dice = Dice.resize(size)


pixels = edge_detect(Dice,buckets=2)


pixels = trim_all_blanks(pixels)


pixels = lines_unique_int(~pixels)
 
pixels = remove_small_lines(pixels,50,blank_id=1)


ranked = rank_shapes_as_circles(pixels)
ranked = ranked[ranked[:,1] < 1]
pixels[~np.isin(pixels,ranked[:,0])] = 0

print(f'\033[32mAnd the number on the dice is: {np.size(np.unique(pixels)) -1}\033[0m')


# pixels = np.multiply(pixels, 255)
# Dice = Image.fromarray(pixels)
# Dice = Dice.resize()
# Dice.show()


total_time = time.time() - start
print(f'\033[32mProcess finished.\nElapsed time: {round(total_time,5)} secends.\033[0m')



