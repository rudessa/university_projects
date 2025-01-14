from skimage.measure import label
from skimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion
import matplotlib.pyplot as plt
import numpy as np 
from skimage.measure import regionprops

LB = np.zeros((16, 16), dtype='uint8')
LB[4:, :4] = 2

LB[3:10, 8:] = 1
LB[[3, 4, 3],[8, 8, 9]] = 0
LB[[8, 9, 9],[8, 8, 9]] = 0
LB[[3, 4, 3],[-2, -1, -1]] = 0
LB[[9, 8, 9],[-2, -1, -1]] = 0

LB[12:-1, 6:9] = 3

props = regionprops(LB)
for prop in props:
    plt.figure()
    plt.imshow(prop.image)
plt.show()