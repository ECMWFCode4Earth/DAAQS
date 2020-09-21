from DAAQS import OpenAQData, gen_radial_coordinates
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import operator

from sklearn import gaussian_process
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel, RBF
from scipy.stats import gaussian_kde
import numpy as np

# day = "2020-04-15"
# year = " 2020"
# span = 7
# locations = ["London Bloomsbury", "官园", "US Diplomatic Post: New Delhi"]

# openaq = OpenAQData(day, span = span)
# openaq.sort_dict()

# x = []
# y = []

# for loc in locations:
#     oaq = openaq.data_dict[loc] 
#     oaq.sort(key=operator.attrgetter("time"))

#     for each in oaq:
#         if each.parameter == "pm25":
#             y.append(each.value)
#             x.append(each.time.hour)

#     X = np.array(x).reshape(-1,1)
#     Y = np.array(y).reshape(-1,1)
#     np.savetxt("data/"+loc+year+" X.csv", X)
#     np.savetxt("data/"+loc+year+" Y.csv", Y)



def scratch_year(year):
    # loc = "官园"
    loc = "US Diplomatic Post: New Delhi"
    # loc = "London Bloomsbury"

    X = np.loadtxt("data/"+loc+year+" X.csv").reshape(-1,1)
    Y = np.loadtxt("data/"+loc+year+" Y.csv").reshape(-1,1)

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
    y_lower = y_pred[:,0]-3*sigma
    y_upper = y_pred[:,0]+3*sigma
    y_lower = y_lower*std+mean
    y_upper = y_upper*std+mean
    y_pred = y_pred*std+mean

    return X, Y, x_pred, y_pred, y_lower, y_upper

X1, Y1, x1_pred, y1_pred, y1_lower, y1_upper = scratch_year(" 2019")
X2, Y2, x2_pred, y2_pred, y2_lower, y2_upper = scratch_year(" 2020")

fig, ax = plt.subplots(1,1, figsize=(10,4))
ax.scatter(X1[:,0],Y1[:,0], marker = ".",  color = "crimson", label = "OpenAQ Data 2019")
ax.scatter(X2[:,0],Y2[:,0], marker = ".", color = "navy", label = "OpenAQ Data 2020")

ax.fill_between(x1_pred[:,0], y1_lower, y1_upper, alpha = 0.2, color = "crimson",label = "3 SD (99.7%) 2019")
ax.fill_between(x2_pred[:,0], y2_lower, y2_upper, alpha = 0.2, color = "navy",label = "3 SD (99.7%) 2020")

ax.plot(x1_pred, y1_pred, color = "crimson")
ax.plot(x2_pred, y2_pred, color = "navy")

ax.set_xlim(left = 0, right = 24)
ax.plot([0,24], [0,0], linestyle = "--", color = "k")
ax.legend()

ax.set_xlabel("Hour of the day")
ax.set_ylabel("PM2.5 concentration [$\mu g/m^3$]")
ax.set_title(f"15 days in mid-April 2019 and 2020 near Delhi")
fig.tight_layout()

plt.savefig("plots/delhi_comp.png")



# fig, ax = plt.subplots(1,1, figsize=(10,4))
# ax.scatter(X[:,0],Y[:,0], marker = ".", label = "OpenAQ Data")
# ax.fill_between(x_pred[:,0], y_lower, y_upper, alpha = 0.3, color = "r",label = "3 SD (99.7%)")
# ax.plot(x_pred, y_pred, color = "crimson")
# ax.set_xlim(left = 0, right = 24)
# ax.plot([0,24], [0,0], linestyle = "--", color = "k")
# ax.legend()
# ax.set_xlabel("Hour of the day")
# ax.set_ylabel("PM2.5 concentration [$\mu g/m^3$]")
# ax.set_title(f"15 days in mid-April 2020 near Delhi")
# fig.tight_layout()

# plt.savefig("plots/delhi_2020.png")

