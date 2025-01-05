import time
from PIL import Image, ImageDraw
import PIL
import os
import numpy as np
import math


def outline(point, image, width=50, thickness="1 (its an int tho)", color="red"):
    if thickness == "1 (its an int tho)":
        thickness=round((image.size[0] + image.size[1])/200)

    draw = ImageDraw.Draw(image)
    if point[0]-width/2 < 0 or point[1]-width/2 < 0:

        print('\033[31mWorning from function >outline()<: some of your box might be outta the frame\033[0m')
    shape = [
        (point[0]-width/2,point[1]-width/2),
        (point[0]+width/2, point[1]+width/2)
    ]
    draw.rectangle(shape,outline=color,width=thickness)


def compare(a,b,dif):
    if len(a) != len(b):
        return IndexError
    c = 0
    for n in range(len(a) -1):
        if type(c) == int:
            c = abs(a[n] - b[n])
            if c > dif:
                return False
    return True


#returns avg rgb of image
def find_avg(image):
    #note: could be acheved by image.resize(1,1)
    image = image.convert("RGB")
    pixels = np.array(image)
    r = np.mean(pixels[:,:,0])
    g = np.mean(pixels[:,:,1])
    b = np.mean(pixels[:,:,2])
    r = round(r)
    g = round(g)
    b = round(b)
    e = (r,g,b)
    return e


def sort_by_brightness(image):
    pixels = np.array(image)
    pixels_1d = pixels.reshape(-1, 3)
    brightness = np.sum(pixels_1d, axis=1)
    indices = np.argsort(brightness)
    sorted_pixels = pixels_1d[indices]
    sorted_image_array = sorted_pixels.reshape(pixels.shape)
    sorted_image = Image.fromarray(sorted_image_array)
    print(sorted_pixels)
    return sorted_image


#r,g,b,h,w,0 
#takes np list of pixels, r,g,b, and manipulates their list so that 
#the 6th value in the rgb list is the frequency of the r,g,b
def pixel_list_mode_old(list_arg, dimen=1):
    l = list_arg.copy()

    biggests = []
    #clear frequency index
    l[:,:,5] = 0

    for i in range(dimen):
        biggest = [[0,0,0],0]
        biggests.append(biggest)

        for y in l:
            for x in y:
                for y1 in l:
                    for x1 in y1:
                        if np.array_equal(x[:2],x1[0:2]) and (x[5] != x1[5] or x[5] == x1[5] == 0):
                            x[5] += 1
                            
        biggest = [[0,0,0],0]
        biggests.append(biggest)
        for y in l:
            for x in y:
                if  x[5] > biggests[i][1]:
                    biggest[0][:3] = x[:3]
                    biggest[1] = x[5]
        biggests.append(biggest)
        #clear every freq except highest unless on last run
        if i != dimen -1:
            for j in l[0]:
                if biggests[i][1] != j[5]:
                    j[i]
    return biggests


#takes pixels_with_location, r,g,b,h,w,0
#takes np list of pixels, r,g,b, and returns a list of the frequency of the
# r,g,b so that the 6th index (arr[5]) is the frequency, with the pixels sorted, and 
#all duplacates removed.
def pixel_list_mode(pixels_with_location,dimen=None):
    array = pixels_with_location.copy()
    array = array.reshape(-1,6)
    array[:,5] = 0
    array = array[np.argsort(array[:,5])]
    array = array[::-1]

    for j in array:
        for k in array:
            if np.array_equal(j[:3], k[:3]):
                j[5] += 1

    # cleaned_array = cleaned_array.reshape(array.shape)    
    array = np.unique(array, axis=0)


    array = array[np.argsort(array[:, 5])]
    array = array[::-1]

    if dimen != None:
        return array[:dimen, :]
    else:
        return array



#takes pixels_with_location, r,g,b,h,w,0
#takes np list of pixels, r,g,b, and manipulates their list so that 
#the 6th value in the rgb list is the frequency of the r,g,b
def give_pixels_mode(pixels_with_location,dimen=None):
    array = pixels_with_location.copy()
    array = array.reshape(-1,6)
    array[:,5] = 0
    for j in array:
        for k in array:
            if np.array_equal(j[:3], k[:3]): 
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


#r,g,b,h,w,occurance
def blackout_white(pixles_w_loc,dif=10, mode=None):
    print('pixles_w_locs.shape',pixles_w_loc.shape)
    print('pixel_list_mode(pixles_w_loc, dimen=3): ', pixel_list_mode(pixles_w_loc, dimen=1))
    if mode==None:
        mode = pixel_list_mode(pixles_w_loc, dimen=1)[0]
    print('mode: ', mode)
    l = pixles_w_loc.copy()
    print('l.shape:',l.shape)
    for j in l:
        for k in j:
            if compare(k[:3], mode, dif):
                k[:3] = [0]*3
    return l
   
        
def benchmark(fn,arguements=None):
    if arguements==None:
        start_time = time.time()
        fn()
        elapsed = time.time() - start_time
        return elapsed
    else:
        start_time = time.time()
        fn(*arguements)
        elapsed = time.time() - start_time
        return elapsed


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


#takes [[r,g,b,h,w,occurances]] 
#sorts by r,g,b
def sort_by_color(pixels_with_loc):
    # calculate similarity btwn each pixel and the first pixel
    array = pixels_with_loc.reshape(-1,6).copy()
    similarities = [mean_dif(pixel[:3], array[0, :3]) for pixel in array]

    #sort pixels based on similarity
    sorted_indices = np.argsort(similarities)
    sorted_array = array[sorted_indices]
    sorted_array = sorted_array.reshape(pixels_with_loc.shape)
    print(sorted_array)
    return sorted_array


def ack():
    print(f'yo {__name__} been imported!')