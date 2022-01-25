import os
from dotenv import load_dotenv
import pymysql
import pandas as pd
import numpy as np

TIME_WINDOW = 24

load_dotenv(verbose=True)

conn = pymysql.connect(
    host=os.getenv("HOST"),
    port=int(os.getenv("PORT")),
    user=os.getenv("USER"),
    passwd=os.getenv("PASSWORD"),
    database="mimiciv_processed",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor,
)

cur = conn.cursor()


def execute_sql(sql: str):
    cur.execute(sql)
    return cur.fetchall()


# Death instance 개수 확인 - 4796
#    - patients table의 dob 확인
#    - dob 있는 사람 추출 as group #1 : group1_subject_id; group2_subject_id
# Death 시간으로부터 24시간 전 vital array 전체 추출


def extract_death_subject_id():
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
            AND H.charttime <= DATE_ADD(outtime_hr, INTERVAL 1 HOUR)"""  # 4796
    return pd.DataFrame(execute_sql(sql))


result = extract_death_subject_id()

## Hourly aggreate


def hourly_aggregate(series: pd.Series) -> float:
    series.dropna(inplace=True)
    if len(series) == 0:
        return np.nan
    elif len(series) == 1:
        return series.item()
    elif len(series) > 2:
        return series.median()


death_hourly_aggregated = result.groupby(["subject_id", "stay_id", "hour"]).agg(
    {
        "heart_rate": hourly_aggregate,
        "sbp": hourly_aggregate,
        "dbp": hourly_aggregate,
        "mbp": hourly_aggregate,
        "resp_rate": hourly_aggregate,
        "spo2": hourly_aggregate,
    }
)

## 저장
death_hourly_aggregated.to_csv("data/processed/result_death.csv")

# feature selection - groupby stay_id, Variable별 null 갯수 확인

death_hourly_aggregated.isnull().groupby("stay_id").aggregate(
    lambda x: round(sum(x) / len(x) * 100, 2)
).to_csv("data/processed/null_sum.csv")

# imputation 후 array 생성


# Survive instance 개수를 1:1로 만들어서 random 추출
# vital sign 5개(SBP, DBP, MBP, PR, BT, SpO2) arr 생성
# Array shape 2 * (6 * N * 24) N은 사망 환자 수
