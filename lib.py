import time
from PIL import Image
import numpy as np

#trims blank lines from array
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

    return bitmap

#takes bitmap shape: (n,n)
#returns list with each true value uneque number shape: (n,n)
    #each true value uneque number
def trues_unique_int(arr_arg):
    arr = arr_arg.copy()
    arr[arr==1] = np.arange(1,np.sum(arr[arr==1].shape) +1 )
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
def lines_unique_int(arr_arg):
    arr = arr_arg.copy().astype(int)
    
    top_sum = np.sum(arr[(0,-1),:])
    bottom_sum = np.sum(arr[:,(0,-1)])

    if top_sum + bottom_sum != 0:
        arr = np.pad(arr,1)

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
    ranks = ranks[np.argsort(ranks[:,1])]
    
    return ranks

# takes image path and returns the number of pips it sees
def count_pips(image_path, buckets=4,removal_size=50,std_bar=1,time_myself=False, show_processing=True, resizement=5):
    start = time.time()

    Dice = Image.open(image_path)
    Dice.show()
    
    h,w = Dice.size
    h,w = round(h/resizement),round(w/resizement)
    size = (h,w)
    Dice = Dice.resize(size)

    pixels = edge_detect(Dice, buckets=buckets)
    pixels = lines_unique_int(~pixels)
    pixels = remove_small_lines(pixels, removal_size, blank_id=1)
    if show_processing:
        Dice = Image.fromarray(pixels)
        Dice.show()
    ranked = rank_shapes_as_circles(pixels)
    ranked = ranked[ranked[:,1] < std_bar]
    pixels[~np.isin(pixels,ranked[:,0])] = 0
    pips_count = np.size(np.unique(pixels)) -1
    if time_myself:
        print(f'It took {time.time()-start} secs to process image')
    if show_processing:
        Dice = Image.fromarray(pixels)
        Dice.show()
    return pips_count

#communacates with the user to process dice image. 
def PR():
    print(f'\033[4mDice Recognizer\033[0m')
    dice_picture_path = input("Enter Picture of dice path:")
    buckets = int(input('Enter number of buckets to use (default 4):') or 4) 
    std = int(input('Enter standerd devation for dice pipes (default 1):') or 1)
    time_myself = input("Time image processing time (y/n)?:") == 'y'
    removal_size = int(input('Enter small lines size (default 50):') or 50)
    show_processing = input("show processing (y/n)?:") == "y"
    resizment = int(input('Resizment (default 5):') or 5)
    print('processing image...') 
    out = count_pips(dice_picture_path, buckets=buckets, removal_size=removal_size, std_bar=std, time_myself=time_myself, show_processing=show_processing, resizement=resizment)
    return f'\033[33mnumber of pips on dice: {out}\033[0m'

def ack():
    print(f'yo {__name__} been imported!')
