import matplotlib.pyplot as plt
import numpy as np

def easy_plot(x, y, scat_fmt='kx3', trend_fmt='k-', y_error=None, return_r2=True, show=True):
    '''Plot scatter of `x` and `y` with best fit line.
    Returns coefficients of linear rgeression line [and r squared value].
    
    Args:
        x (tuple/list/numpy.ndarray): values of data points for the horizontal axis
        y (tuple/list/numpy.ndarray): values of data points for the vertical axis
    Kwargs:
        scat_fmt (str): format for scatter plot, two characters as follows:
            scat_fmt[0] = one character colour (sets `c` in matplotlib.pyplot.scatter)
            scat_fmt[1] = marker type (sets `marker` in matplotlib.pyplot.scatter)
            scat_fmt[2] = error bar capsize in points (only used if y_error is not None)
        trend_fmt (str): format for trendline, passed directly to matplotlib.pyplot.plot
        y_error (scalar/array-like): if none, no error bars are plotted (default)
            otherwise, plots error bars on graph according to values given
            if array-like, must be of equal length to `x` and `y`
            colour used is the same as that from `scat_fmt`
        return_r2 (bool): whether to return the r squared value for the linear regression
        show (bool): whether to show the graph (plt.show(block=False))
    Returns:
        tuple: Information about the linear regression:
            return_r2==False: (gradient, intercept)
            return_r2==True: ((gradient, intercept), r squared)
    '''
    if y_error is None:
        plt.scatter(x, y, c=scat_fmt[0], marker=scat_fmt[1])
    else:
        plt.errorbar(x, y, yerr=y_error, color=scat_fmt[0], marker=scat_fmt[1], capsize=int(scat_fmt[2]), elinewidth=1, ls='none')
        # plt.errorbar(x, y, yerr=y_error, ls='none', color=scat_fmt[0], marker=scat_fmt[1]) 
    # Get coefficients of linear regression
    m_c = np.polyfit(x, y, 1)
    trend_func = np.poly1d(m_c)
    # calculate r squared for the linear regression
    if return_r2:
        if not isinstance(y, np.ndarray):
            x = np.array(x)
            y = np.array(y)
        r2 = 1 - np.sum((y - trend_func(x))**2) / np.sum((y-np.mean(y))**2)
    # plot trend line
    min_max_x = np.array((np.min(x), np.max(x)))
    plt.plot(min_max_x, trend_func(min_max_x), trend_fmt)
    if show:
        plt.show(block=False)
    if return_r2:
        return tuple(m_c), r2
    return tuple(m_c)

def formal_plot(x, y, y_error=None, title='', x_title='', y_title='', x_units=[], y_units=[], show=True):
    '''Plots a `x` and `y` for a formal looking graph.
    
    Args:
        x (tuple/list/numpy.ndarray): values of data points for the horizontal axis
        y (tuple/list/numpy.ndarray): values of data points for the vertical axis
    Kwargs:
        y_error (scalar/array-like): if none, no error bars are plotted (default)
            otherwise, plots error bars on graph according to values given
            if array-like, must be of equal length to `x` and `y`
        title (str): title of the graph
        x_title (str): label for horizontal axis (excluding units)
        y_title (str): label for vertical axis (excluding units)
        x_units (tuple[tuple]): of (unit (str), exponent (int/str)) pairs for units of the horizontal axis
        y_units (tuple[tuple]): of (unit (str), exponent (int/str)) pairs for units of the vertical axis
        show (bool): whether to show the graph (plt.show(block=False))
    Returns:
        tuple: Information about the linear regression: ((gradient, intercept), r squared)
    '''
    def make_latex(units):
        '''Convert list of units and their exponents to latex (using superscripts).
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
        
    trend_info = easy_plot(x, y, y_error=y_error, show=False)
    
    plt.title(title)
    if x_units:
        plt.xlabel(' / '.join((x_title, make_latex(x_units))))
    else:
        plt.xlabel(x_title)
    if y_units:
        plt.ylabel(' / '.join((y_title, make_latex(y_units))))
    else:
        plt.ylabel(y_title)
    
    if show:
        plt.show(block=False)
    return trend_info

def chi_r_2(observed, observed_error, expected, ddof=0):
    '''Performs reduced chi squared statistic.
    <1 implies overfitting (errors too large)
    >1 implies poor fit (line of fit is bad description, or errors to small)
    1 implies a good fit. Values closer to 1 are better.
    
    Calculated as:
        sum( ((observed - expected) / observed_error)**2 ) / dof
        where the degrees of freedom (dof) are:
            len(observed) - 1 - ddof
    Args:
        observed (iterable): observed data points
        observed_error(iterable/numeric): standard error in observed data points
            if a numeric (eg. float) is given, error is taken as constant for all data points
        expected (iterable): expected values for each data point
    Kwargs:
        ddof (int): number of variables in fitting function
            degrees of freedom = len(observed) - 1 - ddof
    Returns:
        float: reduced chi squared statistic
    '''
    length = len(observed)
    if isinstance(observed_error, (float, int)):
        observed_error = np.array((observed_error,) * length)
    # ensure all inputs are an np.ndarray
    observed, observed_error, expected = np.array((observed, observed_error, expected))
    # calculate degrees of freedom
    dof = length - 1 - ddof
    if dof < 1:
        raise RuntimeError(f'Degrees of freedom must be at least 1, not {dof}.')
    return np.sum(((observed - expected) / observed_error)**2) / dof
