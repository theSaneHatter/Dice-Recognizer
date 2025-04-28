from PIL import Image
from lib import *
import numpy as np

start = time.time()


#so bools dont look wierd
np.set_printoptions(formatter={'float': '{:0.2f}'.format})

path = './assets/Dice1.jpg'


# UNCOMMENT FOR SUBMISSION
#print(print(PR()))
print(count_pips(path, buckets=4, removal_size=50, std_bar=1, time_myself=True, show_processing=True, resizement=5))

total_time = time.time() - start
print(f'\033[32mProcess finished.\nElapsed time: {round(total_time,5)} secends.\033[0m')





