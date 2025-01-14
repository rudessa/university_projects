import numpy as np
import matplotlib.pyplot as plt
from scipy.datasets import face

# def discritize(image, nvals):
#     mn = np.min(image)
#     mx = np.max(image)
#     levels = np.linspace(mn,mx,nvals)
#     for i in range(0, len(levels)-1):
#         min_level = levels[i]
#         max_level = levels[i+1]
#         image[np.logical_and(image > min_level, image <= max_level)] = i

# image = face(gray=True)
# discritize(image, 5)
# plt.imshow(image)
# plt.show()




# def bloak_mean(image, nx, ny):
#     y_size = image.shape[0] // ny
#     x_size = image.shape[1] // nx
#     for y in range(0, image.shape[0], y_size):
#         for x in range(0, image.shape[1], x_size):
#             sub = image[y:y+y_size, x:x+x_size]
#             image[y:y+y_size, x:x+x_size] = sub.mean()

# image = face(gray=True)
# bloak_mean(image, 40, 40)
# plt.imshow(image)
# plt.show()




# def mse(img1, img2):
#     return ((img1 - img2) ** 2).sum() / img1.size

# def psnr(img1, img2):
#     m = mse(img1, img2) ** 0.5
#     return 20 * np.log10(img1.max() / m)

# original = face(gray=True)

# n = 10 ** 6

# noised = original.copy()
# y = np.random.randint(0, original.shape[0], n)
# x =  np.random.randint(0, original.shape[1], n)
# noised[y,x] = np.random.randint(0, 255, n)

# ss = psnr(original, noised)

# plt.subplot(121)
# plt.imshow(original)
# plt.subplot(122)
# plt.imshow(noised)
# plt.show()




# def convolvue(image, mask):
#     result = np.zeros_like(image).astype("f4")
#     for y in range(1,image.shape[0]-1):
#         for x in range(1, image.shape[1]-1):
#             sub = image[y-1:y+2, x-1:x+2]
#             value = (sub * mask).sum()
#             result[y,x] = value

#     return result[1:-1, 1:-1]

# image = face(gray=True)
# mask = np.array([[-1,-1,-1],
#                  [-2,-2,-2],
#                  [-1,-1,-1]])
# convolved = convolvue(image, mask)

# plt.subplot(121)
# plt.imshow(image)

# plt.subplot(122)
# plt.imshow(convolved)
# plt.show()




exter_mask = np.array([[[0,0],[0,1]],
                       [[0,0], [1,0]],
                       [[0,1], [0,0]],
                       [[1,0], [0,0]]])
inter_mask = np.logical_not(exter_mask)

cross_mask = np.array([[[0,1], [1,0]],
                      [[1,0], [0,1]]])
def match(sub, masks):
    for mask in masks:
        if np.all(sub == mask):
            return True
    return False
        
def count_obj(B):
    e = 0
    i = 0
    for y in range(0, B.shape[0]-1):
        for x in range(0, B.shape[1]-1):
            sub = B[y:y+2, x:x+2]
            if match(sub, exter_mask):
                e += 1
            if match(sub, inter_mask):
                i += 1
            if match(sub, cross_mask):
                e += 2
    return (e-i) / 4

image = np.load("cex2.npy.txt")
print(sum([count_obj(image[:, :, i]) 
                    for i in range(image.shape[2])]))

plt.subplot(131)
plt.imshow(image[:,:,0])
plt.show()