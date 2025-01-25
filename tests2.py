import numpy as np
import math
from PIL import Image
import time
import timeit
from lib import *
start = time.time()



def shift_9(arr_arg):
    
    arr = arr_arg.copy()

    shift_d = np.roll(arr, 1,0)
    shift_u = np.roll(arr, -1,0)
    shift_l = np.roll(arr, -1,1)
    shift_r = np.roll(arr, 1,1)

    shift_lu = np.roll(shift_l, 1,0)
    shift_ru = np.roll(shift_r,1,0)  
    shift_ld = np.roll(shift_l,-1,0) 
    shift_rd = np.roll(shift_r,-1,0) 
    
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
    
    top_sum = np.sum(arr[(0,-1),:])
    bottom_sum = np.sum(arr[:,(0,-1)])
    if top_sum + bottom_sum != 0:
        arr = np.pad(arr,1)

    arg = arr.copy()

    go = True
    while go:
        save = arr
        arr = np.multiply(np.maximum.reduce(shift_9(trues_unique_int(arr))), arg)     
        
        if np.array_equal(save, arr):
            go = False
    if top_sum + bottom_sum != 0:
        arr = arr[1:-1,1:-1]

    return arr

#takes bitmask, returns avg (x,y) posistion
#gives avg location of 1s in bitmask
def center(arr_arg):
    locs = np.nonzero(arr_arg)
    avg_x = np.average(locs[0])
    avg_y = np.average(locs[1])
    avg = avg_x,avg_y
    return avg

def distance_std(bitmask):
    Cx, Cy = center(bitmask)
    Xs, Ys = np.nonzero(bitmask)
    Ds = np.sqrt( np.add(np.subtract(Xs,Cx)**2, np.subtract(Ys,Cy)**2))
    std = np.std(Ds)
    return std

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

a = np.array(arr)
print("before\n",c,'\nPost:\n')
print('avg=',distance_std(c))




total_time = time.time() - start
print(f'\033[32mProcess finished.\nElapsed time: {round(total_time,5)} secends.\033[0m')
