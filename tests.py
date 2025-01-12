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
print(np.add.reduce(c,1) > 0)
bitmask_f = np.logical_or.accumulate(bitmask)
print(bitmask_f)

bitmask_b = np.logical_or.accumulate(bitmask[::-1])
bitmask_b = bitmask_b[::-1]
print('b',bitmask_b)
cumulative = np.logical_and(bitmask_f, bitmask_b)
print(cumulative)

print(c[cumulative])






total_time = time.time() - start
print(f'\033[32mProcess finished.\nElapsed time: {round(total_time,5)} secends.\033[0m')
