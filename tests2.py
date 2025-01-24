import numpy as np
import math
from PIL import Image
import time
import timeit
from lib import *
start = time.time()




def shift_9(arr_arg):
    arr = arr_arg.copy()
    shift_d = np.roll(arr_arg, 1,0)
    shift_u = np.roll(arr_arg, -1,0)
    shift_l = np.roll(arr_arg, -1,1)
    shift_r = np.roll(arr_arg, 1,1)

    shift_lu = np.roll(shift_l, -1,1)
    shift_ru = np.roll(shift_r,1,1)  
    shift_ld = np.roll(shift_l,-1,0) 
    shift_rd = np.roll(shift_r,1,0) 
    
    out = np.array([arr,
                    shift_d,
                    shift_u,
                    shift_l,
                    shift_r,
                    shift_lu,
                    shift_ru,
                    shift_ld,
                    shift_rd
                    ])
    return out    


def list_max(arr_arg):
    arr = arr_arg.copy()
    go = True
    while go:
        save = arr
        arr = np.multiply(np.maximum.reduce(shift_9(trues_unique_int(arr))), arr_arg)     
        print('np.array_equal(save, arr)',np.array_equal(save, arr))
        if np.array_equal(save, arr):
            go = False
    return arr
            
            



a = np.zeros((10,5), dtype=int)
a[:,:] = 1
c = np.random.randint(0,2,(8,8))
arr = [
    [0,0,0,0,0,1,1,0],
    [0,0,0,0,0,1,1,0],
    [0,1,1,0,0,1,1,0],
    [0,0,0,0,0,1,0,0],
    [0,0,1,1,0,0,1,0],
    [0,0,0,0,0,1,1,0],
    [0,0,0,0,0,1,1,0],
]

a = np.array(arr)
print("before\n",c,'\nPost:\n')
print(list_max(a))



total_time = time.time() - start
print(f'\033[32mProcess finished.\nElapsed time: {round(total_time,5)} secends.\033[0m')
