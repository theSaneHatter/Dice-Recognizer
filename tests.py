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




array = np.random.randint(0,10,size=(50,3,6))
array = array.reshape(-1,6)

#takes [[r,g,b,h,w,occurances]] 
#sorts by r,g,b
def sort_by_color(pixel):
    # calculate similarity btwn each pixel and the first pixel
    similarities = [mean_dif(pixel[:3], array[0, :3]) for pixel in array]

    #sort pixels based on similarity
    sorted_indices = np.argsort(similarities)
    sorted_array = array[sorted_indices]
    sorted_array = sorted_array.reshape(50,3,6)
    print(sorted_array)

print(sort_by_color(array))