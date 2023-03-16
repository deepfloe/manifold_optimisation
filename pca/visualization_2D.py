import matplotlib.pyplot as plt
import numpy as np
from pca import pca

data = np.random.rand(2,100)
x,y = data
plt.scatter(x,y)
centre = np.mean(data,axis=1)

gradient = pca(data,1)[0]

x = [centre[0]-gradient[0], centre[0]+gradient[0]]
y = [centre[1]-gradient[1], centre[1]+gradient[1]]

plt.plot(x,y)
plt.show()


