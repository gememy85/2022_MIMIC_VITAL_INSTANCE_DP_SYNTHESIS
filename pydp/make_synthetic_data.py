'''
**discription**
this code is for processing the original data into a synthetic data using the
LDP method. 

this code does not have the validation codes. 

'''

from multiprocessing import Pool
from tqdm import tqdm
import config
from utils import write_pkl_file
from differential_privacy import DiffPrivacy
from data import Original, Label, Data


def main():
    # config
    filename = config.DP_CONFIG["filename"]
    filedir = config.DP_CONFIG["filedir"]
    outputdir = config.DP_CONFIG["output_file_directory"]
    categorical_columns = config.DP_CONFIG["categorical_columns"]
    epsilon_list = config.DP_CONFIG["epsilon_list"]

    original = Original(filedir, filename, categorical_columns)

    write_pkl_file(original, outputdir, "original.pkl")

    # DP class
    diffprivacy = DiffPrivacy(
        original,
        outputdir,
    )

    # multiprocessing DP
    print("Get DP data")
    
    # print("finished..!")
    pool = Pool(5)
    pool.map(diffprivacy.dp, epsilon_list)
    # epsilon = 10
    # diffprivacy.dp(epsilon)


if __name__=='__main__':
    import os
    print(os.getcwd())
    main()
