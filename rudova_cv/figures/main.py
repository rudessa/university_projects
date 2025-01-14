from matplotlib import pyplot as plt
import numpy as np
from scipy.ndimage import label
from skimage.morphology import binary_erosion, binary_dilation


image = np.load("ps.npy.txt")


#структуры
structure_1 = np.array([[1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0]])

structure_2 = np.array([[1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 0, 0],
                        [0, 0, 1, 1, 0, 0],
                        [0, 0, 1, 1, 0, 0],
                        [1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 0, 0]])

structure_3 = np.array([[1, 1, 0, 0, 1, 1],
                        [1, 1, 0, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0]])

structure_4 = np.array([[1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1],
                        [1, 1, 0, 0, 1, 1],
                        [1, 1, 0, 0, 1, 1],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0]])

structure_5 = np.array([[1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 0, 0],
                        [1, 1, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0, 0],
                        [1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 0, 0]])


labeled = label(image)[0]
print(f'Количество фигур: {labeled.max()}')


picture_1 = binary_dilation(binary_erosion(image, structure_1), structure_1)
image -= picture_1
picture_2 = binary_dilation(binary_erosion(image, structure_2), structure_2)
image -= picture_2
picture_3 = binary_dilation(binary_erosion(image, structure_3), structure_3)
image -= picture_3
picture_4 = binary_dilation(binary_erosion(image, structure_4), structure_4)
image -= picture_4
picture_5 = binary_dilation(binary_erosion(image, structure_5), structure_5)
image -= picture_5
print(f'Тип 1: {label(picture_1)[0].max()}')
print(f'Тип 2: {label(picture_2)[0].max()}')
print(f'Тип 3: {label(picture_3)[0].max()}')
print(f'Тип 4: {label(picture_4)[0].max()}')
print(f'Тип 5: {label(picture_5)[0].max()}')

plt.imshow(image)
plt.show()


