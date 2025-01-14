import numpy as np
import matplotlib.pyplot as plt
from skimage.draw import disk

def neighbours4(y, x):
    return (y, x-1), (y-1, x), (y, x+1), (y+1,x)

def neighboursX(y, x):
    return (y-1, x-1), (y-1, x+1), (y+1, x+1), (y+1, x-1)

def neighbours8(y, x):
    return neighbours4(y, x) + neighboursX(y, x)

def search(LB, label, y, x):
    LB[y,x] = label
    for ny, nx in neighbours4(y, x):
        if LB[ny, nx] == -1:
            search(LB, label, ny, nx)

def recursive_label(B):
    LB = B * -1
    label = 0
    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            if LB[y, x] == -1:
                label += 1
                search(LB, label, y, x)
    return LB

image = np.zeros((20, 20), dtype='int32')

image[1:-1, -2] = 1

image[1, 1:5] = 1
image[1, 7:12] = 1
image[2, 1:3] = 1
image[2, 6:8] = 1
image[3:4, 1:7] = 1

image[7:11, 11] = 1
image[7:11, 14] = 1
image[10:15, 10:15] = 1

image[5:10, 5] = 1
image[5:10, 6] = 1

image = np.zeros((500, 500))
rr, cc = disk((250, 250), 150)
image[rr, cc] = 1

import sys
sys.setrecursionlimit(71000)

image1 = recursive_label(image)

plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.imshow(image1)
plt.show()