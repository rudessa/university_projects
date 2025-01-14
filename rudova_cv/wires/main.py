from skimage.measure import label
from skimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion
import matplotlib.pyplot as plt
import numpy as np

image = np.load("wires5npy.txt")
labeled = label(image)#Маркированное изображение
for i in range(1, labeled.max()+1):
    wire = labeled == i
    erosion_wire = binary_erosion(wire)
    labeled_erosion_wire = label(erosion_wire)
    number_wire = labeled_erosion_wire.max()

    if (number_wire) == 1:
        print(("Провод целый"))
    elif (number_wire) == 0:
        print(("Провод анигиллирован"))
    else:
        print(f"Провод порван на {number_wire}")