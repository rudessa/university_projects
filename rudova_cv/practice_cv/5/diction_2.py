import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from collections import defaultdict # частотный словарик
from pathlib import Path
from collections import defaultdict

#заполняющий_фактор
def filling_factor(arr):
    return np.sum(arr)/arr.size

#счетчик отверстий
def count_holes(region):
    labeled = label(np.logical_not(region.image))
    regions = regionprops(labeled)
    holes = 0
    for region in regions:
        coords = np.where(labeled == region.label)
        bound = True
        for y, x in zip(*coords):
            if y == 0 or x == 0 or y == labeled.shape[0] - 1 or x == labeled.shape[1] - 1:
                bound = False
        holes += bound
    return holes

#наличие линий
def has_vline(arr, width=1):
    return width <= np.sum(arr.mean(0) == 1)


def extractor(region):
    area = region.area / region.image.size
    cy, cx = region.centroid_local
    cy /= region.image.shape[0]
    cx /= region.image.shape[1]
    eccentricity = region.eccentricity
    perimeter = region.perimeter / region.image.size
    euler = region.euler_number
    f_factor = filling_factor(region.image)
    c_holes = count_holes(region.image)
    h_vline = has_vline(region.image)
    return np.array([area, cy, cx, eccentricity, perimeter, euler,f_factor, h_vline ])


def classificator(props, classes):
    klass = None
    min_d = 10 ** 16
    for cls in classes:
        d = distance(props, classes[cls])
        if  d < min_d:
            klass = cls
            min_d = d
    return klass


def distance(p1, p2):
    return ((p1 - p2)**2 ).sum()**0.5


#наличие линий
def has_vline(arr, width=1):
    return width <= np.sum(arr.mean(0) == 1)


# считываем изображение с символами
image = plt.imread("5/alphabet_ext.png").mean(2)
image[image == 1] = 0
image[image > 0] = 1
labeled = label(image)
regions = regionprops(labeled)


classes = {"A": extractor(regions[2]),
           "B": extractor(regions[3]),
           "8": extractor(regions[0]),
           "1": extractor(regions[4]),
           "W": extractor(regions[5]),
           "X": extractor(regions[6]),
           "*": extractor(regions[7]),
           "-": extractor(regions[11]),
           "/": extractor(regions[8]),
           "P": extractor(regions[9]),
           "D": extractor(regions[10]),
           }
print(classes)


alphabet = plt.imread("5/fr_dic.png").mean(2)
alphabet[alphabet > 0] = 1
labeled = label(alphabet)
print(np.max(labeled))
regions = regionprops(labeled)

result = defaultdict(lambda: 0)

for region in regions:
    symbols_props  = extractor(region)
    symbol = classificator(symbols_props, classes)
    result[symbol] += 1
print(result)

# symbols_props = extractor(regions[1])
# print(classificator(symbols_props, classes))

plt.imshow(regions[1].image)
plt.show()
#{'D': 31, 'X': 23, '/': 35, '*': 41, '1': 40, 'A': 35, 'P': 37, '8': 33, '-': 31, 'B': 38, 'W': 26, '0': 30})