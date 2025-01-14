import cv2
import numpy as np
# import matplotlib.pyplot as plt


rose = cv2.imread("6/rose.jpg")

hsv = cv2.cvtColor(rose, cv2.COLOR_BGR2HSV)

lower = np.array([0, 150, 50])
upper = np.array([0, 255, 255])

mask = cv2.inRange(hsv, lower, upper)

result = cv2.bitwise_and(rose, rose, mask = mask)


cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL| cv2.WINDOW_KEEPRATIO)
cv2.imshow("Image", result)
cv2.waitKey()

# plt.subplot(131)
# plt.title("Hue")#тон
# plt.imshow(hsv[:, :, 0])
# plt.subplot(132)
# plt.title("Saturation")#насыщенность
# plt.imshow(hsv[:, :, 1])
# plt.subplot(133)
# plt.title("Value")#яркость
# plt.imshow(hsv[:, :, 2])
# plt.show()