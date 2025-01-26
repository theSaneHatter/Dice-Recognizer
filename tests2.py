import numpy as np
import math
from PIL import Image
import time
import timeit
from lib import *
start = time.time()


def remove_small_lines(arr_arg,min_pixels,lines_uneque=False):
    uneque = list_max(arr_arg)
    max_ = np.max(uneque)
    for i in range(max_+1):
        if np.size



a = np.zeros((10,5), dtype=int)
a[:,:] = 1
c = np.random.randint(0,2,(3,3))
arr = [
    [1,0,0,0,0,1,1,0],
    [1,0,0,0,0,1,1,0],
    [1,1,1,0,0,1,1,0],
    [1,0,0,0,0,1,0,0],
    [1,0,1,1,0,0,1,0],
    [1,0,0,0,0,1,1,0],
    [1,0,0,0,0,1,1,0]
]
p = [
[0,0,0,0,0],        
[0,1,1,1,0],
[0,1,0,1,0],
[0,1,1,1,0]
]
p = np.array(p)

a = np.array(arr)
print("before\n",c,'\nPost:\n')
print('std',distance_std(p))





total_time = time.time() - start
print(f'\033[32mProcess finished.\nElapsed time: {round(total_time,5)} secends.\033[0m')
