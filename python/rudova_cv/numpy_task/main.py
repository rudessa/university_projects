import numpy as np

a = np.array([3, 2, 1], dtype="uint8")

assert a.dtype == "uint8"

b = np.zeros((5, 5))

assert b.shape == (5, 5) and b.sum() == 0

c = np.ones((3, 3, 3))

assert c.ndim == 3 and c.sum() / c.size == 1

d = np.arange(-5, 5)

assert np.all(d == np.array([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4]))

e = np.linspace(0, 1, 5)

assert np.all(e == np.array([0., 0.25, 0.5, 0.75, 1.0]))

f = np.arange(5 * 5).reshape(5, 5)
fc = f[::2,1::2]

assert np.all(fc == np.array([[1, 3], [11, 13], [21, 23]]))

g = np.ones((5, 3))
gc = np.sum(g, axis = 1)

assert np.all(gc == np.array([3., 3., 3., 3., 3.]))

h = np.arange(5) + 1
hc = h * 2

assert np.all(hc == np.array([2., 4., 6., 8., 10.]))

j = np.array([1, 2, 3, 4, 9, 7, 11, 12, 15, 14, 33])
mask = j % 3 == 0
jc = j[mask]

assert np.all(jc == np.array([3, 9, 12, 15, 33]))

k = np.array([1, 2, 3, 4, 5])
l = np.array([2, 2, 3, 3, 4])
kl = k ** l

assert np.all(kl == np.array([1, 4, 27, 64, 625]))

m = np.array([2, 2, 2, 3, 3, 3])
mc = np.std(m)

assert mc == 0.5

n = np.array([1, 2, 3, 4, 5, 6])
nc = np.median(n)

assert nc == 3.5

o = np.array([2, 2, 2, 2])
oc = o.reshape(2, 2)

assert oc.ndim == 2 and oc.shape == (2, 2)

p = np.array([1, 2, 3, 4])
pc = p[::-1]

assert np.all(pc == np.array([4, 3, 2, 1]))

r = np.array([3, 3, 5, 5])
rc = r.copy()
rc[1:3] = -1

assert np.all(r[1:3] == np.array([3, 5])) and np.all(rc[1:3] == np.array([-1, -1]))
