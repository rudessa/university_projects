import cv2
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.color import rgb2hsv
import numpy as np
print(cv2.getBuildInformation())
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if cam.isOpened():
    ret, frame = cam.read()
    print(frame.shape)
cam.release()

image = plt.imread("balls.png")

hsv_image = rgb2hsv(image)
colors = hsv_image[:, :, 0]

unique_colors = np.unique(colors)
dict = {}
for i in unique_colors:
    if round(i, 1) not in dict.keys():
        dict[round(i, 1)] = [i]
    else:
        dict[round(i, 1)].append(i)

lenghts = []
for item in dict.values():
    length = np.mean(item)
    lenghts.append(length)

print(lenghts)

plt.plot(unique_colors, "o")
plt.show()