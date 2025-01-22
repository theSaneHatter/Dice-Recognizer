import numpy as np
import math
from PIL import Image
import time
from lib import *
import timeit
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


#takes list 
#returns list with each true value uneque number
#currently isnt the most optimized 
def trues_uneque_int_faster_but_worse(arr_arg=np.random.randint(0,2,(10,10))):
    if arr_arg.dtype != int and arr_arg.dtype != float:
        print(f'''\033[31mPossable Error in trues_uneque_int():\n  
    array given not of type float or int, type:>{arr_arg.dtype}<\033[0m''')
    arr = arr_arg.copy()
    guys_to_multiply_by = np.arange(np.prod(arr_arg.shape)).reshape(arr_arg.shape)
    arr = np.multiply(arr,guys_to_multiply_by)
    max_ = np.max(arr)
    range_ = max_ - np.min(arr[arr>np.min(arr)]) 
    arr = np.subtract(arr,range_-2)
    arr = np.where((arr < 0),0,arr)
    return arr


def trues_uneque_int(arr_arg=np.random.randint(0,2,(10,10))):
    arr = arr_arg.copy()
    n = 1
    for colomn in range(arr.shape[0]):
        for element in range(arr.shape[1]):
            if arr[colomn,element] != 0:
                arr[colomn,element] = n
                n+=1
    return arr

print('c:',c)
# print('trues_uneque_int',trues_uneque_int(c))

total_time = time.time() - start
print(f'\033[32mProcess finished.\nElapsed time: {round(total_time,5)} secends.\033[0m')