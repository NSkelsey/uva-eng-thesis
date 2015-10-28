import numpy as np
import pylab
import math
#from pylab import plot as plt
import matplotlib.pyplot as plt

FEE = 50000
DUST_AMNT = 547

def cost(size, rate):
    return (DUST_AMNT*math.ceil(size/20.0) + FEE)*(rate*(1e-6))

def close(size):
    return lambda rate: (DUST_AMNT*math.ceil(size/20.0) + FEE)*(rate*(1e-6))

def dust(factor, size):
    return lambda rate: (factor*DUST_AMNT*math.ceil(size/20.0) + FEE)*(rate*(1e-6))

def make_plot():
    current_price = 234.85

    x_c = current_price
    y_c = cost(140, x_c)

    x = np.linspace(0, 1000, 100)
    y = map(close(140), x)
    pylab.plot(x,y, 'b-', label="Tweet Sized Bulletin Cost")

    # Current cost for a tweet
    pylab.plot(x_c, y_c, 'ro')
    pylab.plot((0, x_c), (y_c, y_c), 'r--')
    pylab.plot((x_c, x_c), (0, y_c), 'r--')
    
    # Annontate the current cost of a tweet size bulletin.
    plt.annotate("Current Cost = %2.2f cents" % y_c, xy=(x_c, y_c), xytext=(50,85),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

    # Cost for tweet with high dust val
    pylab.plot(x, map(dust(10, 140), x), 'y-', label="10x Dust 140B Bulletin Cost")

    # Cost for 1k of storage
    pylab.plot(x, map(close(1000), x), 'g-', label="1KB Bulletin Cost")

    # Add graph features
    pylab.title("Various Bulletin Costs")
    pylab.ylabel("Cost in Cents")
    pylab.xlabel("BTC/USD Conversion Rate")
 
    ax = pylab.gca()
    ax.grid(True, color='0.75', linestyle='-')
    ax.legend(loc="upper left")

    plt.show()

if __name__ == '__main__':
    make_plot()
