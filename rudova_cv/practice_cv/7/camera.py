import cv2
import numpy as np
import matplotlib.pyplot as plt

bg = cv2.imread("7/news.jpg")
# fg = cv2.imread("7/cheb.jpg")
camera = cv2.VideoCapture(0) 
if not camera.isOpened():
    raise RuntimeError("Camera not working!")

_, fg = camera.read()
rows, cols, _ = fg.shape

pts_bg = np.float32([[19, 25], [433, 56], [41, 296], [435, 269]])
pts_fg = np.float32([[0, 0], [cols, 0], [0, rows], [cols, rows]])

M = cv2.getPerspectiveTransform(pts_fg, pts_bg)
# print(M)
while True:
    _, fg = camera.read()
    fg = fg[:, ::-1, :]
    aff_fg = cv2.warpPerspective(fg, M, (bg.shape[1], bg.shape[0]))

    pos = np.where(aff_fg >0)
    bg[pos] = aff_fg[pos]
    cv2.imshow("Image", bg)
    key = cv2.waitKey(10)
    if key == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()