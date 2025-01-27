import numpy as np
import math
from PIL import Image
import time
import timeit
from lib import *
start = time.time()




a = np.zeros((10,5), dtype=int)
a[:,:] = 1
c = np.random.randint(0,2,(5,5))
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

a = np.array(arr,dtype=bool)
print("before\n",c,'\nPost:\n')
print('std',distance_std(c))
# print('remove_small_lines',remove_small_lines(a,10,lines_id=1).astype('int'))

# print('remove_small_lines',remove_small_lines(a,10,lines_id=1).astype('int'))

# print('lines_unique_int',lines_unique_int(c))
# asd = remove_small_lines(c.astype(bool),100)
# print('remove_small_lines',asd)
# print(np.sum(asd),np.sum(c))

print(lines_unique_int(a.astype(int)))
print(remove_small_lines(a,10))

total_time = time.time() - start
print(f'\033[32mProcess finished.\nElapsed time: {round(total_time,5)} secends.\033[0m')
