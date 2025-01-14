from skimage.measure import label
from skimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion
import matplotlib.pyplot as plt
import numpy as np

image = np.load('wires5npy.txt')

labeled_image = label(image)
arr = []
for i in range(1, labeled_image.max()+1):
    img = labeled_image == i
    img1 = binary_erosion(img)
    final = label(img1)

    arr.append(final.max())


for i in range(len(arr)):
    if arr[i] == 1:
        print(f'Провод {i+1} ЦЕЛ!')
    elif arr[i] == 0:
        print(f'Провод {i+1} АНИГИЛЛИРОВАН')
    else:
        print(f'Провод {i+1} порван на {arr[i]} частей')


plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.imshow(labeled_image)
plt.show()