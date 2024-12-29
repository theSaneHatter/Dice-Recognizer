import numpy as np
import math


#returns mean dif of 2 lists
def mean_dif(a,b):
    if len(a) != len(b):
        print(f"\033[31mError in mean_dif():\n   len({a}) != len({b}).\narg a & arg b must have = length")
    difs = []
    for i in range(len(a)):
        dif = abs(a[i] - b[i])
        difs.append(dif)
    mean = sum(difs)/len(difs)
    return mean



def pixel_list_mode(pixels_with_location,dimen=None):
    array = pixels_with_location.copy()
    array = array.reshape(-1,6)
    array[:,5] = 0
    array = array[np.argsort(array[:,5])]
    array = array[::-1]

    for j in array:
        for k in array:
            if np.array_equal(j[:2], k[:2]):
                j[5] += 1

    # cleaned_array = cleaned_array.reshape(array.shape)    
    array = np.unique(array, axis=0)


    array = array[np.argsort(array[:, 5])]
    array = array[::-1]

    if dimen != None:
        return array[:dimen, :]
    else:
        return array





array = np.random.randint(0,10,size=(10,3,6))
#array = array.reshape(-1,6)


#takes r,g,b,h,w,occ list genorated by give_pixels_location() and pixel_list_mode
def sort_pixels_by_mode(pixels_with_loc, modes_given=False):
    
    mode = pixel_list_mode(pixels_with_loc)
    sorted_array = pixels_with_loc.copy()
    sorted_array = sorted_array.reshape(-1,6)
    sorted_array = sorted_array[np.argsort(sorted_array[:,5])]
    sorted_array = sorted_array[::-1]
    sorted_array = sorted_array.reshape(pixels_with_loc.shape)

    # for j in range(len(mode)):
    #     for k in range(len(pixels_with_loc)):
    #         if np.array_equal(mode[j,:], pixels_with_loc[k,:]):
    #             sorted = np.concatenate((array, pixels_with_loc[k].reshape(1, -1)), axis=0)
    print('sorted_array', sorted_array)
    print('pixels_with_loc.shape:',pixels_with_loc.shape)
    print('sorted.shape',sorted_array.shape)

sort_pixels_by_mode(array)
