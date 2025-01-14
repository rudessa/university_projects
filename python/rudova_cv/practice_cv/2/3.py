import numpy as np
import matplotlib.pyplot as plt
from skimage.draw import disk
# pip install scikit-image

def check(B, y, x):
    if not 0 <= x < B.shape[0]:
        return False
    if not 0 <= y < B.shape[1]:
        return False
    if B[y, x] != 0:
        return True
    return False

def neighbors2(B, y, x):
    left = y, x-1
    top = y - 1, x
    if not check(B, *left):
        left = None
    if not check(B, *top):
        top = None
    return left, top

def find(label, linked):
    j = label
    while linked[j] != 0:
        j = linked[j]
    return j

def union(label1, label2, linked):
    j = find(label1, linked)
    k = find(label2, linked)
    if j != k:
        linked[k] = j

def exists(neighbors):
    return not all([n is None for n in neighbors])

def two_pass(B):
    LB = B * -1
    linked = np.zeros(len(B), dtype="uint")
    label = 1
    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            if LB[y, x] == -1:
                nbs = neighbors2(B, y, x)
                if not exists(nbs):
                    m = label
                    label += 1
                else:
                    lbs = [LB[i] for i in nbs if i is not None]
                    m = min(lbs)
                LB[y, x] = m
                for n in nbs:
                    if n is not None:
                        lb = LB[n]
                        if lb != m:
                            union(m, lb, linked)
    for y in range(B.shape[0]):
        for x in range(B.shape[1]):
            if B[y, x] != 0:
                new_label = find(LB[y, x], linked)
                nbs = neighbors2(B, y, x)
                if not exists(nbs):
                    m = new_label
                else:
                    lbs = [LB[i] for i in nbs if i is not None]
                    m = min(lbs)
                LB[y, x] = m
                for n in nbs:
                    if n is not None:
                        lb = LB[n]
                        if lb != m:
                            union(m, lb, linked)

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

labeled = two_pass(image)

plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.imshow(labeled)
plt.show()