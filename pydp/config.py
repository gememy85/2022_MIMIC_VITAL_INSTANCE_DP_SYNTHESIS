#%% 
DP_CONFIG = {
    "filename": "max_val.csv",  # input file name
    "filedir": "/home/wonseok/work/synthetic_data/data/processed/",      # input file directory
    # output file directory
    "output_file_directory": "/home/wonseok/work/synthetic_data/dp_output/",
    "categorical_columns": [],  # categorical column names
    "epsilon_list": [0.1, 1, 10, 100, 1000, 10000],
    "label_filename": "for_survival_stage_notnull_y.csv",
    "train_size": 0.8,
    "epoch": 10,
}


