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

def preprocess_before_pca(data_X, data_Y, choice):
    train_x, test_x, train_y, test_y = train_test_split(data_X, data_Y, test_size=0.3, stratify=data_Y, random_state=0)
    sc = StandardScaler()
    train_x_std = sc.fit_transform(train_x)
    test_x_std = sc.transform(test_x)
    result = {'train_x_std': train_x_std, 'test_x_std': test_x_std,'train_y': train_y, 'test_y': test_y}
    return result[choice]

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



