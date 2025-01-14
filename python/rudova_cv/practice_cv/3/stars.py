from skimage.measure import label
from skimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion
import matplotlib.pyplot as plt
import numpy as np


cross_struct = np.array([[1,0,0,0,1],
                         [0,1,0,1,0],
                         [0,0,1,0,0],
                         [0,1,0,1,0],
                         [1,0,0,0,1]])

plus_struct = np.array([[0,0,1,0,0],
                        [0,0,1,0,0],
                        [1,1,1,1,1],
                        [0,0,1,0,0],
                        [0,0,1,0,0]])

image = np.load('stars.npy.txt')

labeled_image = label(image)

number_of_stars = labeled_image.max()
print(number_of_stars)

stars_1 = label(binary_erosion(image, cross_struct)).max()
stars2 = label(binary_erosion(image, plus_struct)).max()
print(f'Number of stars: {stars_1+stars2}')

plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.imshow(binary_erosion(image, cross_struct))
plt.show()