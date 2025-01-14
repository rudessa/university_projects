import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label

cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
image = cv2.imread("10 cube/out.png")
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
_, binary = cv2.threshold(hsv[:, :, 1], 65, 255, cv2.THRESH_BINARY)
binary = cv2.dilate(binary, None, iterations = 2)

labeled = label(binary)
print(labeled.max())
cv2.imshow("Image", binary)
cv2.waitKey(0)
cv2.destroyAllWindows()