import os
from dotenv import load_dotenv
import pymysql
import pandas as pd
import numpy as np

TIME_WINDOW = 24


class Database:
    def __init__(self, host, port, user, password):
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=password,
            database="mimiciv_processed",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor,
        )
        self.cur = conn.cursor()

    def execute_sql(self, sql: str):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def extract_subject_id(self, death: bool = True) -> pd.DataFrame:
        if death:
            sql = f"""SELECT H.subject_id, 
                        H.stay_id, 
                        {TIME_WINDOW - 1}-ROUND(TIMESTAMPDIFF(MINUTE, H.charttime, D. outtime_hr) / 60) AS hour,
                        H.heart_rate, 
                        COALESCE(H.sbp, H.sbp_ni) as sbp,
                        COALESCE(H.dbp, H.dbp_ni) as dbp,
                        COALESCE(H.mbp, H.mbp_ni) as mbp,
                        H.resp_rate, 
                        H.spo2
                    FROM mimiciv_processed.vital_sign H
                    INNER JOIN (SELECT P.subject_id, I.stay_id, P.dod, I.intime_hr, I.outtime_hr
                        FROM mimiciv.patients P
                        INNER JOIN mimiciv_processed.icustay_times I
                        ON P.subject_id = I.subject_id
                        AND P.dod IS NOT NULL
                        AND I.stay_id IS NOT NULL
                        AND P.dod <= I.outtime_hr
                        AND P.dod >= I.intime_hr
                        ) D
                    ON D.stay_id = H.stay_id
                    AND H.charttime >= DATE_SUB(outtime_hr, INTERVAL {TIME_WINDOW - 1} HOUR)
                    AND H.charttime <= DATE_ADD(outtime_hr, INTERVAL 1 HOUR)"""
        elif not death:
            sql = f"""SELECT H.subject_id, 
                        H.stay_id, 
                        {TIME_WINDOW - 1}-ROUND(TIMESTAMPDIFF(MINUTE, H.charttime, D.outtime_hr) / 60) AS hour,
                        H.heart_rate, 
                        COALESCE(H.sbp, H.sbp_ni) as sbp,
                        COALESCE(H.dbp, H.dbp_ni) as dbp,
                        COALESCE(H.mbp, H.mbp_ni) as mbp,
                        H.resp_rate, 
                        H.spo2
                    FROM mimiciv_processed.vital_sign H
                    INNER JOIN (SELECT P.subject_id, I.stay_id, P.dod, I.intime_hr, I.outtime_hr
                        FROM mimiciv.patients P
                        INNER JOIN mimiciv_processed.icustay_times I
                        ON P.subject_id = I.subject_id
                        AND P.dod IS NULL
                        AND I.stay_id IS NOT NULL
                        ) D
                    ON D.stay_id = H.stay_id
                    AND H.charttime >= DATE_SUB(outtime_hr, INTERVAL {TIME_WINDOW - 1} HOUR)
                    AND H.charttime <= DATE_ADD(outtime_hr, INTERVAL 1 HOUR)"""
        return pd.DataFrame(self.execute_sql(sql))


def hourly_aggregate(series: pd.Series) -> float:
    series.dropna(inplace=True)
    if len(series) == 0:
        return np.nan
    elif len(series) == 1:
        return series.item()
    elif len(series) > 2:
        return series.median()


def aggregate_by_hourly_row(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(["subject_id", "stay_id", "hour"]).agg(
        {
            "heart_rate": hourly_aggregate,
            "sbp": hourly_aggregate,
            "dbp": hourly_aggregate,
            "mbp": hourly_aggregate,
            "resp_rate": hourly_aggregate,
            "spo2": hourly_aggregate,
        }
    )


def save_to_csv(df: pd.DataFrame, filename: str):
    df.to_csv(f"data/processed/{filename}")


def main():
    load_dotenv(verbose=True)

    database = Database(
        os.getenv("HOST"),
        int(os.getenv("PORT")),
        os.getenv("USER"),
        os.getenv("PASSWORD"),
    )

    death_result = database.extract_subject_id(death=True)
    live_result = database.extract_subject_id(death=False)
    death_result = aggregate_by_hourly_row(death_result)
    live_result = aggregate_by_hourly_row(live_result)
    save_to_csv(death_result, "death_df.csv")
    save_to_csv(death_result, "live_df.csv")


if __name__ == "__main__":
    main()
