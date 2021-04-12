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

def formal_plot(x, y, title, x_title, y_title, x_units, y_units, show=True):
    def make_latex(units):
        ''' Convert list of units and their exponents to latex (using superscripts).
        A unit without an exponent is assumed to be raised to the power of one.
        Exponents can be expressed as int or str.
        
        Args:
            units (iterable): of list/tuple of unit-exponent pairs
        Returns:
            str: string that will be interpretted as latex by matplotlib
        
        Examples:
        >>> make_latex([['kJ',1], 'N', ['m',2], ['s', -2]])
        '$kJ\\ N\\ m^{2}\\ s^{-2}$'
        '''
        # convert str values in units to have a power of 1
        units = ((unit, 1) if isinstance(unit, str) else unit for unit in units)
        latex = r'\ '.join(unit[0] if unit[1] == 1 
                           else f'{unit[0]}^{{{unit[1]}}}'
                           for unit in units)
        return '$' + latex + '$'
        
    trend_info = easy_plot(x, y, show=False)
    plt.title(title)
    plt.xlabel(' / '.join((x_title, make_latex(x_units))))
    plt.ylabel(' / '.join((y_title, make_latex(y_units))))
    if show:
        plt.show(block=False)
    return trend_info