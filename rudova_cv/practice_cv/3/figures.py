from skimage.measure import label
from skimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion
import matplotlib.pyplot as plt
import numpy as np

image = np.load('ps.npy.txt')
labeled_image = label(image)
number_of_items = labeled_image.max()
print(f'Total number of elements: {number_of_items}')

unique_items = []
for i in range(1, number_of_items+1):
    curr_item = labeled_image == i
    k = False
    for j in range(len(unique_items)):
        if np.all(curr_item == unique_items[j][0]):
            unique_items[j][1] += 1
            k = True
    if not k:
        unique_items.append((curr_item, 1))
    

print(unique_items)


plt.subplot(121)
plt.imshow(labeled_image)
plt.show()