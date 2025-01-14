import numpy as np
import matplotlib.pyplot as plt


arr = np.array([[0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,1,1,1,1,1,1,1,0,0],
                [0,0,0,0,1,1,1,1,0,0],
                [0,0,0,0,1,1,1,1,0,0],
                [0,0,0,1,1,1,1,1,0,0],
                [0,0,0,0,1,1,1,1,0,0],
                [0,0,0,1,1,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0]])



struct = np.ones((3,3))


def dilation(arr):
    result = np.zeros_like(arr)
    for y in range(1, arr.shape[0]-1):
        for x in range(1, arr.shape[1]-1):
            if arr[y, x] == 1:
                result[y-1:y+2, x-1:x+2] = struct

    return result

def erosion(arr):
    result = np.zeros_like(arr)
    for y in range(1, arr.shape[0]-1):
        for x in range(1, arr.shape[1]-1):
            if np.all(arr[y-1:y+2, x-1:x+2] == struct):
                result[y,x] = 1

    return result

def closing(arr):
    return erosion(dilation(arr))

def opening(arr):
    return dilation(erosion(arr))

result = opening(arr)
plt.imshow(result)
plt.show()
