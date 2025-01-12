from PIL import Image, ImageDraw, ImageEnhance
import PIL.Image
from lib import *
import numpy as np
import math
from scipy import stats
start = time.time()
#purple is ~90,0,70
#green ~90,115,0

Dice = Image.open('./assets/Dice1.jpg') 



#sharpness 
sharpness = ImageEnhance.Sharpness(Dice)
Dice = sharpness.enhance(-10)

#contrast 
contrast = ImageEnhance.Contrast(Dice)
Dice = contrast.enhance(1)

Dice.show()
#brightness
brightness = ImageEnhance.Brightness(Dice)
Dice = brightness.enhance(0.03)


# resize 
print(Dice.size)
h,w = Dice.size
h,w = round(h/5),round(w/5)
print('new size' , h,w)
size = (h,w)
Dice = Dice.resize(size)




# We have edge detection!

# If the die non-pip and the background, edge detection can find only the pips if we use just two buckets.
# This is great!
# But if there are more than one die, and they are close, how do we differentate the dice?
# We can do edge detection with like 30 buckets to get edges where the dice are
# and then find what columns and rows we need to split on.
# Then use those to split the two bucket bitmap.




pixels2 = edge_detect(Dice)
pixels2 = np.multiply(pixels2, 255)
Dice = Image.fromarray(pixels2)



Dice.show()

total_time = time.time() - start
print(f'\033[32mProcess finished.\nElapsed time: {round(total_time,5)} secends.\033[0m')



