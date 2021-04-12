import matplotlib.pyplot as plt
import numpy as np

def easy_plot(x, y, scat_fmt='kx', trend_fmt='k-', return_r2=True, show=True):
    plt.scatter(x, y, c=scat_fmt[0], marker=scat_fmt[1])
    # Get coefficients of linear regression
    m_c = np.polyfit(x, y, 1)
    trend_func = np.poly1d(m_c)
    # calculate r squared for the linear regression
    if return_r2:
        y = np.array(y)
        # r2 = 1 - np.sum((y-f(x))**2) / np.sum((y-np.mean(y))**2)
        r2 = 1 - sum((yi-trend_func(xi))**2 for xi, yi in zip(x, y)) / np.sum((y-np.mean(y))**2)
    # plot trend line
    min_max_x = np.array((np.min(x), np.max(y)))
    plt.plot(min_max_x, trend_func(min_max_x), trend_fmt)
    if show:
        plt.show(block=False)
    if return_r2:
        return m_c, r2
    else:
        return m_c

a=[1,2,3,4,5,6]
b=[0,2,3,5,4,7]
print(easy_plot(a,b))
