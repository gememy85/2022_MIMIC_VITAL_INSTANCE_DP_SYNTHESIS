from pathlib import Path
import pandas as pd
import numpy as np

try:
    PROJECT_PATH = Path(__file__).parents[1]
except NameError:
    PROJECT_PATH = Path(".").absolute().parents[0]

TIME_WINDOW = 24

df = pd.read_csv(Path(PROJECT_PATH, "data/processed/result_death.csv"))
id_list = df.stay_id.unique()

hour = pd.DataFrame({"hour": range(24)})
stay_id = pd.DataFrame({"stay_id": id_list})
stay_id_hour_df = pd.merge(stay_id, hour, how="cross")
filled_df = (
    pd.merge(df, stay_id_hour_df, on=["stay_id", "hour"], how="right")
    .sort_values(["stay_id", "hour"])
    .fillna(-1)
)

target_variables = ['heart_rate', 'sbp', 'dbp', 'mbp', 'resp_rate', 'spo2']

result = np.empty((len(target_variables), len(id_list), TIME_WINDOW), dtype=np.float32)

for t, target_variable in enumerate(target_variables):
    for i, stay_id in enumerate(id_list):
        result[t, i] = (
            filled_df.loc[filled_df.stay_id == stay_id, target_variable]
            .to_numpy()
            .reshape(-1, TIME_WINDOW)
        )

np.savez_compressed(f"data/processed/death.npz", result)

