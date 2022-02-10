from multiprocessing import Pool

from tqdm import tqdm
import config
from utils import write_pkl_file, read_pkl_file
from differential_privacy import DiffPrivacy
from data import Original, Label, Data
from validation import Validation

filedir = config.DP_CONFIG["filedir"]
filename = config.DP_CONFIG["filename"]
categorical_columns = config.DP_CONFIG["categorical_columns"]
epsilon_list = config.DP_CONFIG["epsilon_list"]
original = Original(filedir, filename, categorical_columns)
label_filename = config.DP_CONFIG["label_filename"]
label = Label(filedir, label_filename, original)
epsilon_list = config.DP_CONFIG["epsilon_list"]
outputdir = config.DP_CONFIG["output_file_directory"]
train_size = config.DP_CONFIG["train_size"]
epoch = config.DP_CONFIG["epoch"]



print("Start Get Metric...")
categorical_results = []
continuous_results = []
model_results = []




for epsilon in tqdm([0, *epsilon_list]): # epsilon에 있는 원소들을 추가한 리스트
    if epsilon == 0:
        validation = Validation(
            epsilon, original, original, label, train_size, epoch
        )
        validation.process()
        model_results.extend(validation.model_result)
        continue
    
    dp = Data(epsilon, outputdir)
    validation = Validation(epsilon, original, dp, label, train_size, epoch)
    validation.process()

    categorical_results.append(validation.category_result)
    continuous_results.append(validation.continuous_result)
    print(validation.model_result)
    model_results.extend(validation.model_result)

write_pkl_file(categorical_results, outputdir, "categorical_results.pkl")
write_pkl_file(continuous_results, outputdir, "continuous_results.pkl")
write_pkl_file(model_results, outputdir, "model_results.pkl")

print("job finished")

if __name__ == "__main__":
    print("do validation executed! \n")
