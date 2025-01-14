import cv2
import numpy as np

pencils = 0
for i in range(1, 13):
    current_pencils = 0
    image = cv2.imread(f"images/img ({i}).jpg",  cv2.IMREAD_GRAYSCALE) 
    thresh = cv2.bitwise_not(cv2.erode(cv2.threshold(image, 120, 255,cv2.THRESH_BINARY)[1], None, iterations = 40))
    mask = np.zeros(thresh.shape, dtype="uint8")
    out = cv2.connectedComponentsWithStats(thresh, 4, cv2.CV_32S)
    (numLabels, labels, stats, centroids) = out

    for i in range(1, numLabels):   
        x, y, w, h = stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP], stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        (cy, cy) = centroids[i]
        if (area > 500000 and area < 700000):
            current_pencils += 1
            pencils += 1
    print(f"На изображении {current_pencils} карандашей")  
print(f"На изображениях {pencils} карандашей")   