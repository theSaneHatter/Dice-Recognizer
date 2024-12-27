# Dice Recognizer 

## This is a Dice Recognizer program, which began to be initially developed around 12/14/24.
## It uses PIL and numpy to recognize what is on the face of dices.
## As of 12/26, it does not yet work. 

## What i have done so far:
###    Made a system for indexing the pixels in a easier way to analise:
###        After turning the image to a numpy array, give_pixels_location() adds 3 more indexes
###        to each pixel: y,x and frequency. frequency is 0 for now.
###        After running the big ass list through give_pixels_location(), each pixel looks like:
####            [r,g,b,y,x,0].
###        Most functions take the list created by give_pixels_location() as an arg.
###    Made a function for benchmarking function speeds, finding the frequency for each pixel,
###    finding the mean dif of 2 lists, compairing 2 lists, finding the mean avg rgb of an image,
###    making the 6th index of each pixel equl to its frequency (pixel_list_mode()), and sorting
###    the pixel list with created by give_pixels_location() by color. 

## What meeds to be done:
###    The dice actually need to be recognized. 
###    Go through pixels with simolar colors and find circles based on their x,y. 

## How i think it should be done:
###   After sorting the list based on color, you can try and look for simolar colors that have
###    simolar locations in their y,x. 

##There need be little more work done on this project to get it to work. I just dont have the
##time rn, cuz im going to mex for break. I might have time tmmr. 
