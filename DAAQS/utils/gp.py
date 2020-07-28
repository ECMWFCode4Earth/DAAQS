from sklearn import gaussian_process
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel


def gp_model(X,y):
    kernel = ConstantKernel()+Matern(length_scale=2, nu=3/2.0)+WhiteKernel(noise_level=1)
    gp = gaussian_process.GaussianProcessRegressor(kernel=kernel)
    gp.fit(X,y)
    
    return gp
