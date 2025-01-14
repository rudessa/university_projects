import cv2
import numpy as np

cat = cv2.imread("7/cat.png")
cat1 = cv2.cvtColor(cat, cv2.COLOR_BGR2GRAY)
cat2 = cv2.imread("7/cat2.png", cv2.IMREAD_GRAYSCALE)

diff = cv2.absdiff(cat1, cat2)
thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.dilate(thresh, None, iterations=2)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    cat[y: y+h, x:x+w, :] = np.random.randint(0, 255, size = (h, w, 3))
    cv2.rectangle(cat, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.putText(cat, f"Differences = {len(contours)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0))
cv2.namedWindow("Original", cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Difference", cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_KEEPRATIO)
cv2.imshow("Original", cat)
cv2.imshow("Difference", thresh)
cv2.waitKey()
cv2.destroyAllWindows()