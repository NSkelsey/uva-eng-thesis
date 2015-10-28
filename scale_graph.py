from datetime import datetime, timedelta
import json

import numpy as np
import matplotlib.dates as mdates
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pylab
from IPython import embed;

x = "blah"
y = "yah"

def load_blkchain_info_data(f):
    '''
    Returns a list of elements that look like 
    {u'y': 27302.0, u'x': 1421518505}, 
    {u'y': 27351.0, u'x': 1421604905}, 
    {u'y': 27404.0, u'x': 1421691305}
    '''
    f = open(f, 'r')
    d = f.read()
    lst = json.loads(d)['values']
    # Slice the first 700 elems out
    lst = lst[700:]
    return lst

def load_quandl_data(f):
    '''
    Returns a list of elements as (x, y) tuples e.g:
    ("datetime<2015-02-18>", 28941.0),
    ("datetime<2015-02-19>", 28991.0),
    ("datetime<2015-02-20>",28881.0),
    '''
    f = open(f, 'r')
    d = f.read()
    raw = json.loads(d)
    lst = raw['dataset']['data']
    
    # reverse the list
    lst = lst[::-1]
    # slice them bones off
    lst = lst[1200:]

    conv_date = lambda s: datetime.strptime(s, "%Y-%m-%d")
    tups = [(conv_date(e[0]), e[1]) for e in lst]
    return tups


def exp_func(x, a, c, d):
        return a*np.exp(c*x)+d

def make_plot(lst):
    # Blockchain info handles
    # Convert to python datetime
    #utc_x = [int(e['x']) for e in lst]
    #dates = [datetime.fromtimestamp(x) for x in utc_x]
    # Convert to GB
    #y = [int(e['y'])/1024.0 for e in lst]

    # Quandl data
    dates = [x for x, _ in lst]
    y = [y/1024.0 for _, y in lst]


    day_x = range(0, len(dates))
    proj_day_x = range(0, int(2.15*len(dates)))


    p2 = np.poly1d(np.polyfit(day_x, y, 2))
    p3 = np.poly1d(np.polyfit(day_x, y, 3))

    # exponential fit
    popt, pcov = curve_fit(exp_func, np.array(day_x), np.array(y), p0=(1, 1e-6, 0))


    # f - mb block size projection forward
    def lin_mb(f):
        def proj(d):
            x = d - len(y)
            p = (f*144.0/1024)*x + y[-1]
            return p
        return proj
    
    # Only use forward dates
    future_days = proj_day_x[len(dates):]


    fig, ax = plt.subplots(1)

    # 2mb ceil projected 
    plt.plot(future_days, map(lin_mb(2), future_days), '-c', label="2MB block ceiling")
    # 1mb ceil projected 
    plt.plot(future_days, map(lin_mb(1), future_days), '-m', label="1MB block ceiling")

    # Exponential projection
    plt.plot(proj_day_x, map(lambda x: exp_func(x, *popt), proj_day_x), '--g', label="Exponential fit")

    # 3rd order poly
    plt.plot(proj_day_x, p3(proj_day_x), '--r', label="Cubic fit")

    # 2nd order poly
    plt.plot(proj_day_x, p2(proj_day_x), '--y', label="Quadratic fit")

    # Actual data
    plt.plot(day_x, y, '-b', label="Historic size")

    # Annontate the current size of the block chain.
    plt.annotate("Current Size is %d GB" % y[-1], xy=(day_x[-1], y[-1]), xytext=(30,85),
                textcoords = 'offset points', ha = 'right', va = 'bottom',
                bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5), 
                arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))


    plt.title("Block Chain Growth Projections")
    plt.ylabel("Size in GB")

    ax = pylab.gca()
    ax.grid(True, color='0.75', linestyle='-')
    ax.legend(loc="upper left")
    ax.set_ylim([0, 500])
 
    start = dates[0]
    utc_x_now = map(lambda x: start+timedelta(days=x), day_x)
    utc_x_fut = map(lambda x: start+timedelta(days=x), proj_day_x)

    # fit the year labels to the bottom
    x_lbls = []
    for day in utc_x_fut[::367]:
        i = utc_x_fut.index(day)
        x_lbls.append((proj_day_x[i], day))

    plt.xticks([x for x, _ in x_lbls], [l.year for _, l in x_lbls])
    plt.show()
    
    return x, y



if __name__ == '__main__':
    #lst = load_blkchain_info_data('blkinfo.json')
    lst = load_quandl_data('quandl.json')
    x, y = make_plot(lst)
     
