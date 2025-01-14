from skimage.measure import label
import numpy as np
import matplotlib.pyplot as plt

image = np.load('8/8.1/holes.npy')
labeled_image = label(image)

X = np.array([[0, 0], [0, 1]])
V = np.array([[0, 1], [1, 1]])


def match(a, mask_euler):
    if np.all(a == mask_euler):
        return True
    return False

def count_objects(B):
    e = 0
    i = 0
    for y in range(1, B.shape[0] - 1):
        for x in range(1, B.shape[1] - 1):
            sub = B[y-1:y + 1, x-1:x + 1]
            if match(sub, X):
                e += 1
            if match(sub, V):
                i += 1
    return (e - i)

holes = 0
arr = []
for i in range(1, labeled_image.max()+1):
    n = count_objects(labeled_image == i)
    arr.append(n)
    plt.imshow(labeled_image == i)
print(arr)
numbers_holes = {1: 0, 2: 0, 0: 0}
for index, i in enumerate(arr):
    if i == -1:
        print("2 holes in figure", index+1)
        numbers_holes[2] += 1
    if i == 0:
        print("1 holes in figure", index+1)
        numbers_holes[1] += 1
    if i == 1:
        print("0 holes in figure", index+1)
        numbers_holes[0] += 1

for k, v in numbers_holes.items():
    print(f"Figures with {k} holes: {v}")


plt.imshow(image)
plt.show()