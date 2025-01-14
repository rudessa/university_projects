import cv2
import numpy as np

# arr = np.random.random_sample((1000, 1000))

# cv2.namedWindow("Image")
# cv2.imshow("Image", arr)

# while True:
#     key = cv2.waitKey(5)
#     if key == ord("w"):
#         break

# cv2.destroyAllWindows()

mushroom = cv2.imread("6/mushroom.jpg")
logo = cv2.imread("6/cvlogo.png")
logo = cv2.resize(logo, (logo.shape[0] // 2, logo.shape[1] // 2))
## mushroom[:logo.shape[0], :logo.shape[1]] = logo
rows, cols, channels, = logo.shape

logo_gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(logo_gray, 10, 255, cv2.THRESH_BINARY)
roi = mushroom[:rows, :cols]
bg = cv2.bitwise_and(roi, roi, mask = cv2.bitwise_not(mask))
fg = cv2.bitwise_and(logo, logo, mask = mask)

combined = cv2.add(bg, fg)

mushroom[:rows, :cols] = combined

# print(mushroom.shape)
# print(logo.shape)
cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL| cv2.WINDOW_KEEPRATIO)
cv2.imshow("Image", mushroom)
cv2.waitKey()