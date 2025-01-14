import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("balls_and_rects.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
colors_rect = {}
colors_circle = {}
out = cv2.connectedComponentsWithStats(gray, 4, cv2.CV_32S)
(volume_labels, labels, data, centroids) = out

for i in range(1, volume_labels):
        x, y, w, h = data[i, cv2.CC_STAT_LEFT], data[i, cv2.CC_STAT_TOP], data[i, cv2.CC_STAT_WIDTH], data[i, cv2.CC_STAT_HEIGHT]
        area = data[i, cv2.CC_STAT_AREA]
        (cX, cY) = centroids[i]
        low = image_hsv[y:y+h, x:x+w]          
        key = low[h//2, w//2, 0]
        if(area == w*h):
            if key not in colors_rect.keys():
                    colors_rect[key] = 1
            else:
                    colors_rect[key] += 1     
        else:
            if key not in colors_circle.keys():
                    colors_circle [key] = 1
            else:
                    colors_circle [key] += 1
print(f"Number of circles:{colors_circle}, Number of rectangles:{colors_rect}")    
plt.imshow(image_hsv)
plt.show()
