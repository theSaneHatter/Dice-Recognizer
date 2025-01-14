import numpy as np
import math
from PIL import Image
import time
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
print("before\n",c)

bitmask = np.add.reduce(c,1) > 0
bitmask_f = np.logical_or.accumulate(bitmask)

bitmask_b = np.logical_or.accumulate(bitmask[::-1])
bitmask_b = bitmask_b[::-1]
cumulative = np.logical_and(bitmask_f, bitmask_b)



c = np.array(arr,dtype=int)
print("before\n",c)

shift_down  = np.roll(arr,1,0)
print('shift_down\n',shift_down)

shift_up = np.roll(arr,-1,0)
print('shift_up\n',shift_up)

shift_left = np.roll(arr,1,-1)
print('shift_left\n',shift_left)

shift_right = np.roll(arr,1,1)
print('shift_right\n',shift_right)



total_time = time.time() - start
print(f'\033[32mProcess finished.\nElapsed time: {round(total_time,5)} secends.\033[0m')