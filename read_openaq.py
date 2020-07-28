from DAAQS import OpenAQData, gen_radial_coordinates
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import operator

from sklearn import gaussian_process
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel, RBF
from scipy.stats import gaussian_kde
import numpy as np

# day = "2019-01-4"
# span = 3
# locations = ["London Bloomsbury", "官园", "US Diplomatic Post: New Delhi"]

# openaq = OpenAQData(day, span = span)
# openaq.sort_dict()

# x = []
# y = []

# for loc in locations:
#     oaq_pahala = openaq.data_dict[loc] 
#     oaq_pahala.sort(key=operator.attrgetter("time"))

#     for each in oaq_pahala:
#         if each.parameter == "pm25":
#             y.append(each.value)
#             x.append(each.time.hour)

#     X = np.array(x).reshape(-1,1)
#     Y = np.array(y).reshape(-1,1)
#     np.savetxt("data/"+loc+" X.csv", X)
#     np.savetxt("data/"+loc+" Y.csv", Y)

loc = "官园"
# loc = "US Diplomatic Post: New Delhi"
# loc = "London Bloomsbury"

X = np.loadtxt("data/"+loc+" X.csv").reshape(-1,1)
Y = np.loadtxt("data/"+loc+" Y.csv").reshape(-1,1)

mean = np.mean(Y)
std = np.std(Y)
Y = (Y-mean)/std


#kernel = ConstantKernel()+ Matern(length_scale=0.2, nu=3/2.0)+WhiteKernel(noise_level=1)

kernel =RBF(length_scale=0.5)+WhiteKernel(noise_level=1)

gp = gaussian_process.GaussianProcessRegressor(kernel=kernel)
gp.fit(X,Y)

x_pred = np.linspace(0,24, num = 24*60).reshape(-1,1)
y_pred, sigma = gp.predict(x_pred, return_std=True)


Y = Y*std+mean
y_lower = y_pred[:,0]-1.96*sigma
y_upper = y_pred[:,0]+1.96*sigma
y_lower = y_lower*std+mean
y_upper = y_upper*std+mean
y_pred = y_pred*std+mean


fig, ax = plt.subplots(1,1, figsize=(10,4))
ax.scatter(X[:,0],Y[:,0], marker = ".")
ax.fill_between(x_pred[:,0], y_lower, y_upper, alpha = 0.3, color = "r")
ax.plot(x_pred, y_pred, color = "crimson")
ax.set_xlim(left = 0, right = 24)
ax.plot([0,24], [0,0], linestyle = "--", color = "k")
fig.tight_layout()

plt.savefig("plots/scratch.png")


# fig = plt.figure()
# #ax = plt.axes(projection= "3d")
# ax = Axes3D(fig)
# X1, X2 = gen_radial_coordinates(X)
# x1_pred, x2_pred = gen_radial_coordinates(x_pred)

# ax.scatter3D(X1,X2, Y, marker = "*")

# vert = [list(zip(x1_pred[:,0], x2_pred[:,0], y_upper))]

# poly = Poly3DCollection(vertices, alpha = 0.5, color = "r")
# ax.add_collection3d(poly)

# plt.savefig("plots/scratch.png")