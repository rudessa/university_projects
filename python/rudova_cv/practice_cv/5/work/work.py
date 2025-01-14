import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from collections import defaultdict

answer_dict =  {'/': 21, 'B': 25, '-': 20, '8': 23, 'A': 21, '1': 31, 'W': 12, '*': 22, '0': 10, 'X': 15}


def has_line(region, horizontal=True):
    return 1. in np.mean(region.image, int(horizontal))


def count_holes(region):
    inv = np.logical_not(region.image)
    labeled = label(inv)
    holes = np.max(labeled)
    return holes


def extractor(region):
    area = region.area / region.image.size
    cy, cx = region.centroid_local
    cy /= region.image.shape[0]
    cx /= region.image.shape[1]
    eccentricity = region.eccentricity
    if eccentricity < 0.4:
        eccentricity = 0
    perimeter = region.perimeter / region.image.size
    euler = region.euler_number
    vline = has_line(region, False)
    hline = has_line(region)
    holes = 0 if eccentricity == 0 else count_holes(region)
    return np.array([area, cy, cx,  eccentricity, perimeter,  euler, vline, hline, holes])


def distance(p1, p2):
    return ((p1 - p2) ** 2).sum() ** 0.5


def classificator(props, classes):
    klass = None
    min_d = 10 ** 16
    for cls in classes:
        d = distance(props, classes[cls])
        if d < min_d:
            klass = cls
            min_d = d
    return klass

image = plt.imread('alphabet_ext.png').mean(2)
image [ image == 1] = 0
image [ image > 0] = 1
labeled = label(image)
regions = regionprops(labeled)

classes = {
    "A": extractor(regions[2]),
    "B": extractor(regions[3]),
    "8": extractor(regions[0]),
    "0": extractor(regions[1]),
    "1": extractor(regions[4]),
    "W": extractor(regions[5]),
    "X": extractor(regions[6]),
    "*": extractor(regions[7]),
    "-": extractor(regions[11]),
    "/": extractor(regions[8]),
    }

alphabet = plt.imread('fr_dic.png').mean(2)
alphabet[alphabet > 0] = 1
labeled = label(alphabet)
regions = regionprops(labeled)

dict_ = defaultdict(lambda: 0)

for sym in regions:
    extracted = extractor(sym)
    symb = classificator(extracted, classes)
    dict_[symb] += 1

print(dict_)
if dict_ == answer_dict:
    print("Верно")