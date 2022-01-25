from pathlib import Path
import pandas as pd
import numpy as np

try:
    PROJECT_PATH = Path(__file__).parents[1]
except NameError:
    PROJECT_PATH = Path(".").absolute().parents[0]

TIME_WINDOW = 24


def load_from_csv(death: bool) -> pd.DataFrame:
    if death:
        filename = "result_death.csv"
    elif not death:
        filename = "result_live.csv"

    return pd.read_csv(Path(PROJECT_PATH, f"data/processed/{filename}"))


def change_to_numpy(df: pd.DataFrame) -> np.ndarray:
    id_list = df.stay_id.unique()

    hour = pd.DataFrame({"hour": range(24)})
    stay_id = pd.DataFrame({"stay_id": id_list})
    stay_id_hour_df = pd.merge(stay_id, hour, how="cross")
    filled_df = (
        pd.merge(df, stay_id_hour_df, on=["stay_id", "hour"], how="right")
        .sort_values(["stay_id", "hour"])
        .fillna(-1)
    )

    target_variables = ["heart_rate", "sbp", "dbp", "mbp", "resp_rate", "spo2"]

    result = np.empty(
        (len(target_variables), len(id_list), TIME_WINDOW), dtype=np.float32
    )

    for t, target_variable in enumerate(target_variables):
        for i, stay_id in enumerate(id_list):
            result[t, i] = (
                filled_df.loc[filled_df.stay_id == stay_id, target_variable]
                .to_numpy()
                .reshape(-1, TIME_WINDOW)
            )
    return result


def save_numpy(arr, filename):
    np.savez_compressed(f"data/processed/{filename}", arr)


def main():
    death_df = load_from_csv(death = True)
    live_df = load_from_csv(death = False)
    
    death_arr = change_to_numpy(death_df)
    live_arr = change_to_numpy(live_df)

    save_numpy(death_arr, "death_numpy.npz")
    save_numpy(live_arr, "live_numpy.npz")

if __name__ == "__main__":
    main()
