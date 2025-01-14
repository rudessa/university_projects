from skimage.measure import label
from skimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion
import matplotlib.pyplot as plt
import numpy as np 
from skimage.measure import regionprops
from skimage import draw
from skimage.filters import threshold_otsu


image = np.zeros((1000,1000), dtype="uint8")
image[:] = np.random.randint(20, 75, size=image.shape)

rr, cc = draw.disk((250, 250), 100)
image[rr, cc] = np.random.randint(60, 120, size=len(rr))
rr, cc = draw.disk((750, 750), 200)
image[rr, cc] = np.random.randint(80, 140, size=len(rr))

thresh = threshold_otsu(image)

# hist = np.zeros(256)

# for y in range(image.shape[0]):
#     for x in range(image.shape[1]):
#         v = image[y, x]
#         hist[v] += 1

# image[image < 75] = 0
# image[image > 0] = 1
# plt.imshow(image)


print(thresh)

image[image < thresh] = 0
image[image > 0] = 1
plt.imshow(image)
plt.show()