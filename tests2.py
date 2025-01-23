import numpy as np
import math
from PIL import Image
import time
import timeit
from lib import *
start = time.time()






a = np.zeros((10,5), dtype=int)
a[:,:] = 1


c = np.random.randint(0,2,(2,3))
arr = [
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,1,1,0,0],
    [0,0,0,0,0],
    [0,0,1,1,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
]
c = np.array(arr)
print("before\n",c,'\nPost:\n')

def roll_8(arr_arg):
    arr = arr_arg.copy()
    shift_d = np.roll(arr_arg, 1,0)
    shift_u = np.roll(arr_arg, -1,0)
    shift_l = np.roll(arr_arg, -1,1)
    shift_r = np.roll(arr_arg, 1,1)

    shift_lu = np.roll(shift_l, -1,1)
    shift_ru = np.roll(shift_r,1,1)  
    shift_ld = np.roll(shift_l,-1,0) 
    shift_ld = np.roll(shift_r,1,0) 
    

roll_8(c)



total_time = time.time() - start
print(f'\033[32mProcess finished.\nElapsed time: {round(total_time,5)} secends.\033[0m')
