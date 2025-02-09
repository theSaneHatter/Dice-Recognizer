import numpy as np
import math
from PIL import Image
import time
import timeit
from lib import *
start = time.time()


#takes bitmap and gives all lines uneque int
#currently could do with some optomization: it reappilies some fns sometimes
def lines_unique_int(arr_arg):
    arr = arr_arg.copy().astype(int)
    
    top_sum = np.sum(arr[(0,-1),:])
    bottom_sum = np.sum(arr[:,(0,-1)])

    if top_sum + bottom_sum != 0:
        arr = np.pad(arr,1)

    # arr = trues_unique_int(arr)

    arg = arr.copy()
    arr = trues_unique_int(arr)
    itter = 0
    go = True
    while go:
        itter += 1
        save = arr
        arr = np.multiply(np.maximum.reduce(shift_9(arr)), arg)      
        if np.array_equal(save.astype(int), arr.astype(int)):
            go = False
        # print('itter in lines_uneque_int',itter)
    

    if top_sum + bottom_sum != 0:
        arr = arr[1:-1,1:-1]

    return arr


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

print('lines_unique_int',lines_unique_int(a))
print('remove_small_lines2',remove_small_lines2(a,3,lines_unique=False))

total_time = time.time() - start
print(f'\033[32mProcess finished.\nElapsed time: {round(total_time,5)} secends.\033[0m')




'''
!!!!!!!!!!!!!
lines_uneque_int doesnt make each value smallest possable! do that!

'''