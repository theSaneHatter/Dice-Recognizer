import numpy as np
import math
from PIL import Image
import time
start = time.time()

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



def pixel_list_mode(pixels_with_location,dimen=None, mode_given=False):
    if not mode_given:
        array = give_pixels_mode(pixels_with_location)

    # cleaned_array = cleaned_array.reshape(array.shape)    
    # array = np.unique(array, axis=0)
    trash, index = np.unique(array[:, :3], axis=0, return_index=True)
    array = array[index]

    array = array[np.argsort(array[:, 5])]
    array = array[::-1]

    if dimen != None:
        return array[:dimen, :]
    else:
        return array


def give_pixels_mode(pixels_with_location,dimen=None):
    array = pixels_with_location.copy()
    array = array.reshape(-1,6)
    array[:,5] = 0
    array = array[np.argsort(array[:,5])]
    array = array[::-1]
    for j in array:
        for k in array:
            if np.array_equal(j[:3], k[:3]):  # changed from j[:2] to j[:3]
                j[5] += 1

    array = array[np.argsort(array[:, 5])]
    array = array[::-1]

    if dimen != None:
        return array[:dimen, :]
    else:
        return array

def give_pixels_location(pixels, remove=False):
    if remove == False:
        shape = [0]*(pixels.shape[0] * pixels.shape[1] * (pixels.shape[2]+3))
        pixels_with_location = np.array(shape)
        
        shape = pixels.shape[0],pixels.shape[1],(pixels.shape[2] + 3 )
        pixels_with_location = pixels_with_location.reshape(shape[0],shape[1],shape[2])

        for a,y in enumerate(pixels_with_location):
            for b,x in enumerate(y):
                pixels_with_location[a,b,0] = pixels[a,b,0]
                pixels_with_location[a,b,1] = pixels[a,b,1]
                pixels_with_location[a,b,2] = pixels[a,b,2]
                pixels_with_location[a,b,3] = a
                pixels_with_location[a,b,4] = b

        return pixels_with_location
    
    if remove:
        shape = pixels.shape[0], pixels.shape[1], 3
        print('shape var: ', shape)
        pixels_w_o_location = np.zeros(math.prod(shape), dtype=np.uint8)
        pixels_w_o_location = pixels_w_o_location.reshape(pixels.shape[0], pixels.shape[1], 3)
        print('shape: ', pixels_w_o_location.shape)
        pixels_w_o_location[:,:,:] = pixels[:,:,:3]
        return pixels_w_o_location

array = np.random.randint(0,10,size=(30,1,6))
array[:,:,:3] *= math.floor(255/10)
array[:,:,:3] = array[:,:,0][:,:,np.newaxis]
#array = array.reshape(-1,6)


#takes r,g,b,h,w,0 list genorated by give_pixels_location() and pixel_list_mode
#returns pixels sorted based on their mode index
def sort_pixels_by_mode(pixels_with_loc, modes_given=False):
    # sorted_array = pixels_with_loc.copy()
    # if not modes_given:
    #     sorted_array = give_pixels_mode(sorted_array)
    
    # sorted_array = sorted_array.reshape(-1,6)
    # sorted_array = sorted_array[np.argsort(sorted_array[:,5])]
    # sorted_array = sorted_array[::-1]
    # sorted_array = sorted_array.reshape(pixels_with_loc.shape)
    array = pixels_with_loc.copy()
    mode = pixel_list_mode(array.copy())
    print('mode:',mode)
    array =  array.reshape(-1,6)
    sorted_array = array.copy()
    sorted_array[:,:] = 0
    count = 0

    total_pixels = sum(mode[:,5])
    print("total_pixels:", total_pixels)
    sorted_array = np.zeros((total_pixels,6), dtype=int)
    sorted_array = sorted_array.reshape(total_pixels,6)

    for j in mode:
        sorted_array[count:count+j[5],:] = j
        count += j[5]
    
    print('pixels_with_loc.shape: ',pixels_with_loc.shape)
    print('sorted_array.shape: ',sorted_array.shape)
    print()
    sorted_array = sorted_array.reshape(pixels_with_loc.shape)
    return sorted_array
    

    
sorted_array = sort_pixels_by_mode(array)
sorted_array = give_pixels_location(sorted_array, remove=True)
print(sorted_array)

img = Image.fromarray(sorted_array)
img.show()









total_time = time.time() - start
print(f'\033[32mProcess finished.\nElapsed time: {round(total_time,5)} secends.\033[0m')
