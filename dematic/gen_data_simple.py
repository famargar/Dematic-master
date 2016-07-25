import datetime as dt
import numpy as np

def makedata():

    """Generates artificial data points for fictitious quantities regarding the MultiShuttle,
       each time it is called. It includes two types of dummy data.
       First type needs to be monitored for outliers and/or trends
       Second type it suffices to not exceed "safety" values.
       args:
            no arguments
       returns:
            n1: data of the first type
            n2: data of the second type
            n3: data of the second type
            index: the temporal index shown as date/time
    """

    n1 = 10 + np.random.randn()
    n2 = np.random.randn()
    n3 = np.random.randn()
    index = dt.datetime.now()

    return n1, n2, n3, index


