
import pandas as pd
import numpy as np
from scipy import interpolate

def add_windows(timeseries:np.array, window_size:int):
    '''
    This function adds window in the front and back of a given timeseries.
    The amount of window size is added.
    '''
    
    # first fill the added points with Na values 
    timeseries_list = timeseries.tolist()
    added_windows = np.repeat(np.nan, window_size).tolist()
    inserted_timeseries = np.array(added_windows + timeseries_list + added_windows)

    # now we interpolate the Na values
    xs = [x for x in range(len(inserted_timeseries))]
    f = interpolate.interp1d(xs[window_size:-window_size], timeseries_list, fill_value='extrapolate')
    interpolated_timeseries = f(xs)
    
    return interpolated_timeseries