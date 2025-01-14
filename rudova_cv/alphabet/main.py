import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from collections import defaultdict # частотный словарик
from pathlib import Path

# дерево решений

# процент заполнения массива 1, ищем "-"
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

#распознавание
def recognize(region):
    if filling_factor(region.image) == 1.0:
        return "-"
    else:
        holes = count_holes(region)
        if holes == 2: # 8 or B
            if has_vline(region.image, 3):
                return "B"
            else:
                return "8"
        elif holes == 1: # A, 0, D или P
            ny, nx = (region.centroid_local[0] / region.image.shape[0], 
            region.centroid_local[1] / region.image.shape[1])
            if np.isclose(ny, nx, 0.05):
                if has_vline(region.image) and (ny < 0.4 or nx < 0.4):
                        return "P"
                return "0"           
            elif has_vline(region.image):
                if filling_factor(region.image) > 0.53:
                    return "D"
                return "P"
            else:
                if ny < 0.5 or nx < 0.5:
                    if filling_factor(region.image) > 0.5:
                        return "0"
                return "A"
        else:
            
            if has_vline(region.image): 
                if filling_factor(region.image) > 0.5:
                    return "*"
                return "1"
            else: #W, X, *, /
                eccentricity = (region.eccentricity)
                framed = region.image
                framed[0, :] = 1
                framed[-1, :] = 1
                framed[:, 0] = 1
                framed[:, -1] = 1
                holes = count_holes(region)
                if eccentricity < 0.4:
                    return "*"
                else: 
                    match holes:
                        case 2: return '/'
                        case 4: return "X"
                    if eccentricity > 0.5:
                        return "W"
                    else:
                        return "*"

image = plt.imread("5/symbols.png").mean(2)
image[image > 0] = 1

regions = regionprops(label(image))
symbols = len(regions)

result = defaultdict(lambda: 0)

path = Path(".") / "5/result"
path.mkdir (exist_ok = True)

plt.figure()

for i, region in enumerate(regions):
    symbol = recognize(region)
    plt.clf()
    plt.title(f"{symbol = }")
    plt.imshow(region.image)
    plt.tight_layout()
    plt.savefig(path / f"{i}.png")
    result[symbol] += 1
print(result)
