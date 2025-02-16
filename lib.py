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
# r,g,b so that the 6th index (arr[5]) is the frequency, with the pixels sorted 
#all duplacates are removed.
def pixel_list_mode(pixels_with_location,dimen=None, mode_given=False):
    if not mode_given:
        array = give_pixels_mode(pixels_with_location)

    # cleaned_array = cleaned_array.reshape(array.shape)    
    # array = np.unique(array, axis=0)
    _, index = np.unique(array[:, :3], axis=0, return_index=True)
    array = array[index]

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
        #('shape var: ', shapeprint)
        pixels_w_o_location = np.zeros(math.prod(shape), dtype=np.uint8)
        pixels_w_o_location = pixels_w_o_location.reshape(pixels.shape[0], pixels.shape[1], 3)
        #print('shape: ', pixels_w_o_location.shape)
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
    #print(sorted_array)
    return sorted_array


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
    #print('mode:',mode)
    array =  array.reshape(-1,6)
    sorted_array = array.copy()
    sorted_array[:,:] = 0
    count = 0

    total_pixels = sum(mode[:,5])
    #print("total_pixels:", total_pixels)
    sorted_array = np.zeros((total_pixels,6), dtype=int)
    sorted_array = sorted_array.reshape(total_pixels,6)

    for j in mode:
        sorted_array[count:count+j[5],:] = j
        count += j[5]
    
    #print('pixels_with_loc.shape: ',pixels_with_loc.shape)
    #print('sorted_array.shape: ',sorted_array.shape)
    #print()
    sorted_array = sorted_array.reshape(pixels_with_loc.shape)
    return sorted_array

# trims blank lines from array
def trim_blank(arr, r2=0.01):
    bitmask = np.add.reduce(arr,1) < arr.shape[1] - arr.shape[1]*r2
    bitmask_f = np.logical_or.accumulate(bitmask)
    bitmask_b = np.logical_or.accumulate(bitmask[::-1])
    bitmask_b = bitmask_b[::-1]
    usefull_bitmask = np.logical_and(bitmask_f, bitmask_b)
    if sum(usefull_bitmask) <= 1:
         print(f'\033[31mWorning from trim_blank(): The size of the processed image (size=[{usefull_bitmask.shape}]) is [too] small\033[0m')
    return arr[usefull_bitmask]

#trims t,b,l,r
def trim_all_blanks(arr,r2=0.01):
    bitmask = trim_blank(arr, r2)
    bitmask = np.transpose(trim_blank(np.transpose(bitmask), r2))
    return bitmask

#turns image into bitmap of edges, shape (a,b)
def edge_detect(img,buckets=2):
    img = img.convert('HSV')
    pixels = np.array(img)
    pixels = pixels[:,:,0]
    pixels = np.floor(np.divide(pixels,360//buckets))
    pixels_l, pixels_up = np.roll(pixels,1,1), np.roll(pixels,1,0)
    bitmap_l, bitmap_up = np.equal(pixels_l, pixels), np.equal(pixels_up, pixels)
    bitmap = np.logical_and(bitmap_l, bitmap_up)
    # bitmap = trim_blank(bitmap)
    # bitmap = np.transpose(trim_blank(np.transpose(bitmap)))
    # bitmap = np.multiply(bitmap, 255)
    return bitmap


def get_neighbors(bitmap):
    if np.sum(bitmap) <= 0:
        print('\033[32mWorning from GOL_clock(): Entered array are all zeros\033[0m')
        return None
    rows, colms = bitmap.shape
    bitmap_save = np.zeros((rows+2,colms+2),dtype=int)
    bitmap_save[1:rows+1,1:colms+1] = bitmap[:,:]
    

    shift_up = np.roll(bitmap_save,1,0)
    shift_down = np.roll(bitmap_save,-1,0)
    shift_right = np.roll(bitmap_save,1,1)
    shift_left = np.roll(bitmap_save,-1,1)

    shift_RU = np.roll(shift_right,1,0)
    shift_RD = np.roll(shift_right,-1,0)
    shift_LU = np.roll(shift_left,1,0)
    shift_LD = np.roll(shift_left,-1,0)
    
    neighbers = shift_up+shift_down+shift_right+shift_left+shift_RU+shift_RD+shift_LU+shift_LD
    
    neighbers = neighbers[1:rows, 1:colms]
    
    return neighbers

#takes bitmap shape: (n,n)
#returns list with each true value uneque number shape: (n,n)
    #each true value uneque number
def trues_unique_int(arr_arg):
    arr = arr_arg.copy()
    arr[arr==1] = np.arange(1,np.sum(arr[arr==1].shape) +1 )
    return arr

#takes bitmap shape: (n,n)
#returns list with each true value uneque number shape: (n,n)
    #with each true value uneque number
#currently not the fastest, but orders the numbers so they are the smallest possable
def trues_uneque_int_lineor(arr_arg):
    arr = arr_arg.copy()
    n = 1
    for colomn in range(arr.shape[0]):
        for element in range(arr.shape[1]):
            if arr[colomn,element] != 0:
                arr[colomn,element] = n
                n+=1
    return arr

#takes bitmap, returns list of that bitmap shifted in all 9ds (9th being same thingy)
#connects bottom to top because it uses roll 
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

#takes bitmap and gives all lines uneque int
#currently could do with some optomization: it reappilies some fns sometimes
def list_max(arr_arg):
    arr = arr_arg.copy().astype(int)
    
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
            

#gives avg location of 1s in bitmask
#takes bitmask, returns avg (x,y) posistion
def avg_location(arr_arg):
    locs = np.nonzero(arr_arg)
    avg_x = np.average(locs[0])
    avg_y = np.average(locs[1])
    avg = avg_x,avg_y
    return avg


#takes bitmask, returns avg (x,y) posistion
#gives avg location of 1s in bitmask
def center(arr_arg):
    locs = np.nonzero(arr_arg)
    avg_x = np.average(locs[0])
    avg_y = np.average(locs[1])
    avg = avg_x,avg_y
    return avg


#takes bitmask, returns the std of the distance of each True point to the avg point
def distance_std(bitmask):
    Cx, Cy = center(bitmask)
    Xs, Ys = np.nonzero(bitmask)
    Ds = np.sqrt( np.add(np.subtract(Xs,Cx)**2, np.subtract(Ys,Cy)**2))
    std = np.std(Ds)
    return std

#removes small lines from bitmask
#takes bitmask shape (n,n) returns bitmask with all inner lines bigger then arg=min_pixels
def remove_small_lines_old(arr_arg,min_pixels,lines_id=0,lines_unique=False):
    if lines_id == 0:
        arr = ~arr_arg.copy().astype(int)
    else:
        arr = arr_arg.copy().astype(int)

    if lines_unique == False:
        arr = lines_unique_int(arr).astype(int)
    

    max_ = np.max(arr)
    print('max_',max_)
    for i in range(1,max_+1):
        if np.size(arr[arr==i]) < min_pixels:
            arr[arr==i] = 0
            print('number:',i)
            print('occurances:',np.size(arr[arr==i]))
    arr[arr>0] = 1

    if lines_id == 0:
        arr = ~arr
    return arr

#removes small lines from bitmask
#takes bitmask shape (n,n) returns bitmask with all inner lines bigger then arg=min_pixels
def remove_small_lines(arr_arg,min_pixels,blank_id=0,lines_unique=True):
    arr = arr_arg.copy()
    if not lines_unique:
        arr = lines_unique_int(arr)
    for i in np.unique(arr):
        if np.size(arr[arr==i]) < min_pixels:
            arr[arr==i ] = blank_id
    return arr

#takes bitmask, returns its rateing as a circle
#input: bitmask. Output: stdm, pixel count
def rate_as_circle(arr_arg, count=False):
    std = distance_std(arr_arg)
    count = np.size(arr_arg[arr_arg==1])
    if np.size(arr_arg[arr_arg>1]) >0:
        print(f'\033[31mWorning from rate_as_circle(): arr_arg is not a bitmask. \n    There are {np.size(arr_arg[arr_arg>1])} values that are not zero!\033[0m')
    if count == True:
        return std, count
    else:
        return std

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
        print(ranks)
        if depth != None:
            if ittr >= depth:
                break    
        ittr+=1
    
    ranks = np.array(ranks)
    ranks = ranks[np.argsort(ranks[:,1])]
    # ranks = ranks[::-1]
    return ranks



def ack():
    print(f'yo {__name__} been imported!')
