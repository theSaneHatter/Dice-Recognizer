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
d = 1
h,w = round(h/d),round(w/d)
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





def GOL_clock2(GOL_arr):
    if np.sum(GOL_arr) <= 0:
        print('\033[32mWorning from GOL_clock(): Entered array are all zeros\033[0m')
        return None
    rows, colms = GOL_arr.shape
    board_save = np.zeros((rows+2,colms+2),dtype=int)
    board_save[1:rows+1,1:colms+1] = GOL_arr[:,:]
    

    shift_up = np.roll(board_save,1,0)
    shift_down = np.roll(board_save,-1,0)
    shift_right = np.roll(board_save,1,1)
    shift_left = np.roll(board_save,-1,1)

    shift_RU = np.roll(shift_right,1,0)
    shift_RD = np.roll(shift_right,-1,0)
    shift_LU = np.roll(shift_left,1,0)
    shift_LD = np.roll(shift_left,-1,0)
    
    neighbers = shift_up+shift_down+shift_right+shift_left+shift_RU+shift_RD+shift_LU+shift_LD

    rectified_board = np.where((board_save == 1) & ((neighbers < 2) | (neighbers > 3)), 0, board_save)
    rectified_board = np.where((board_save == 0) & (neighbers == 3), 1, rectified_board)
    
    return rectified_board


pixels = edge_detect(Dice,buckets=2)
pixels = trim_all_blanks(pixels)
# pixels = np.multiply(pixels, 255)
Dice = Image.fromarray(pixels)

Dice.show()


pixels_up = np.roll(pixels, )



total_time = time.time() - start
print(f'\033[32mProcess finished.\nElapsed time: {round(total_time,5)} secends.\033[0m')



