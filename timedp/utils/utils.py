import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import re

from lifelines import CoxPHFitter
from lifelines import KaplanMeierFitter


def read_csv_file(filename):
    return pd.read_csv(filename)

def read_pkl_file(fullfilepath):
    with open(fullfilepath, "rb") as f:
        return pickle.load(f)

def write_pkl_file(data, filepath, filename):
    with open(os.path.join(filepath, filename), "wb") as f:
        pickle.dump(data, f)

def check_folder(folder):
    return os.path.isdir(folder)

def mkdir_folder(folder):
    os.mkdir(folder)
    pass 

def transform_to_original_data_format(fake_X, data_Y, cols_list):
    data = pd.concat([fake_X,data_Y], axis=1)
    data.columns = cols_list
    return data

def do_survival_analysis(T, E, data=None ,Kaplan=False):
    if Kaplan : model = KaplanMeierFitter().fit(T,E)
    else : model = CoxPHFitter(penalizer=0.1).fit(data, T, E, show_progress=True, step_size=0.5)

    return model

def give_wanted_list(lst, regular_expression):
    r = re.compile(regular_expression)
    return list(filter(r.match, lst))

def read_output_to_pd(path_to_pkl_output):
    return pd.DataFrame(pd.read_pickle(path_to_pkl_output))
    

def get_categorical_levels_from_data(data:np.ndarray, col: str) -> int:
    sr = data.loc[:, col]
    return int(sr.max() - sr.min() + 1)


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
