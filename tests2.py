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

a = np.array(arr)
print("before\n",c,'\nPost:\n')



#takes array with each circle a uneque value (whitespace = 0)
#returns sorted list (n,(value, std))
#might not work 
def rank_shapes_as_circles(arr_arg, depth=None):
    ranks = []
    ittr = 0
    for i in np.unique(arr_arg[arr_arg!=0]):
        bitmask = np.where(arr_arg==i,1,0)
        to_append = [i, rate_as_circle(bitmask, count=False)]
        ranks += [to_append]
        if depth != None:
            if ittr >= depth:
                break    
        ittr+=1
    
    ranks = np.array(ranks)
    ranks = ranks[np.argsort(ranks[:,0])]
    return ranks

print(rank_shapes_as_circles(a))


total_time = time.time() - start
print(f'\033[32mProcess finished.\nElapsed time: {round(total_time,5)} secends.\033[0m')



