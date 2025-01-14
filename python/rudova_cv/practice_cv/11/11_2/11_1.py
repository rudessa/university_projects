from skimage.draw import disk
import numpy as np
import matplotlib.pyplot as plt
import time
from itertools import chain


def euclidean(x1, y1, x2, y2):
    return ((x1 - x2)** 2 + (y1 - y2)** 2) ** 0.5


image = np.zeros((100, 100))
#КВАДРАТ
# image[30:50, 30:50] = 1


#КРУГИ ###################################################################
# rr, cc = disk((35, 35), 20)
# image[rr, cc] = 1

# rr, cc = disk((65, 65), 25)
# image[rr, cc] = 1
###########################################################################


t = time.perf_counter()
pos = np.where(image == 1)
distance_map = np.zeros_like(image)

for y, x in zip(*pos): 
    step = 1
    while True:
#ГРАНИЦЫ квадрата##########################################################
        # size = 2 * step +1
        # top = [y  - step] * size, list(range(x - step, x + step + 1))
        # bottom = [y  + step] * size, list(range(x - step, x + step + 1)) 
        # left = list(range(y - step, y + step + 1)), [x  - step] * size 
        # right = list(range(y - step, y + step + 1)), [x  + step] * size

        # image[top[0], top[1]] = 2
        # image[bottom[0], bottom[1]] = 2
        # image[left[0], left[1]] = 2
        # image[right[0], right[1]] = 2
###########################################################################


#ПИРАМИДКА################################################################
        min_d = 10 ** 19
        size = 2 * step +1
        top = [y  - step] * size, list(range(x - step, x + step + 1))
        bottom = [y  + step] * size, list(range(x - step, x + step + 1)) 
        left = list(range(y - step + 1, y + step)), [x  - step] * size # Убрали дубл точки +1
        right = list(range(y - step + 1, y + step)), [x  + step] * size # Убрали дубл точки +1
        for ny, nx in zip(chain(top[0], bottom[0], left[0], right[0]), chain(top[1], bottom[1], left[1], right[1])):
            #расстояние до 0
            if image[ny, nx] == 0:
                d = euclidean(y, x, ny, nx)
                #мин расстояние до 0
                if d < min_d:
                    min_d = d
        if min_d != 10 ** 19:
            distance_map[y, x] = min_d
            break
        step += 1
###########################################################################

print(f"Elpased{time.perf_counter() - t}")
plt.imshow(distance_map)
plt.show()