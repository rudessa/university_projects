from scipy.datasets import face
import numpy as np
import matplotlib.pyplot as plt

def translate(image, vector):
    translated = np.zeros_like(image)

    for i in range(translated.shape[0]):
        for j in range(translated.shape[1]):
            ni = i - vector[0]
            nj = j-vector[1]
            if ni < 0 or nj < 0:
                continue
            if ni >= image.shape[0] or nj >= image.shape[1]:
                continue
            translated[ni, nj] = image[i, j]

    return translated


image = face(True)

result = translate(image, (-500,40))

plt.imshow(result)
plt.show()