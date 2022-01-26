#%%
import pandas as pd
import numpy as np
import pickle
from sdv.tabular import GaussianCopula, CTGAN, CopulaGAN, TVAE
from sdv.constraints import Positive, GreaterThan
from utils import *

from multiprocessing import Pool


# 1.0 data loading
sample_df = pd.read_csv('../data/processed/sample_df.csv')
y = pd.read_csv('../data/processed/Y.csv')

original_data = pd.concat([sample_df, y], axis=1)


def f(x):
    global original_data
    x.fit(original_data)
    return x


def main():

    # 1.1 constraints
    RACE1V_constraint = Positive(
        high='RACE1V',
        strict=False,
        handling_strategy='reject_sampling'
    )

    SEX_constraint = GreaterThan(
        low=0,
        high='SEX',
        handling_strategy='reject_sampling'
    )

    Lateral_constraint = Positive(
        high='LATERAL',
        strict=False,
        handling_strategy='reject_sampling'
    )

    Maligcount_constraint = Positive(
        high='MALIGCOUNT',
        strict=False,
        handling_strategy='reject_sampling'
    )

    
    constraints = [RACE1V_constraint,
                SEX_constraint,
                Lateral_constraint,
                Maligcount_constraint
                ]

    # 1.2 build models

    GCo = GaussianCopula(constraints=constraints)
    CG = CTGAN(constraints=constraints)
    CoG = CopulaGAN(constraints=constraints)
    TV = TVAE(constraints=constraints)
    models_list = [GCo, CG, CoG, TV]

    # 1.3 multiprocessing 

    with Pool(16) as p:
        result_models = p.map(f, models_list)

    # 1.4 save models
    names = ["GCo","CG","CoG","TV"]
    
    for name, model in zip(names,result_models):
        model.save(f'../models/{name}_model.pkl')

if __name__=='__main__':
    main()



