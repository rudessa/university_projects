from skimage.measure import label
from skimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion
import matplotlib.pyplot as plt
import numpy as np 


def area(LB, label=1):
    return np.sum(LB==label)

def coin(LB, label=1):
    area_ = area(LB, label)

    return area_

LB = np.load('coins.npy.txt')
LB = label(LB)


sum_of_coins = 0

cnt_coins = LB.max()

coins_dict = {}
for i in range(1, cnt_coins+1):
    curr_coin = LB == i
    area_ = area(curr_coin)

    if area_ not in coins_dict.keys():
        coins_dict[area_] = 1
    else:
        coins_dict[area_] += 1


arr = [1, 2, 5, 10]
coins_dict = sorted(coins_dict.items())
for l in range(len(coins_dict)):
    sum_of_coins += coins_dict[l][1] * arr[l]


print(sum_of_coins)
plt.imshow(LB)
plt.show()