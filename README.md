# Create vital sign instances

- Author: MinDong Sung
- Date: 2022/1/25

---

## Objective

- Create two vital sign instances for 24hours.
- One is for death patient.
- The Other is for live patient.

## Reference Dataset

- [MIMICIV](https://physionet.org/content/mimiciv/1.0/)

## Summary

- sql로 죽기 전 24시간 동안 vital sign 추출
- 살아 있는 환자는 ICU 나가기 전 24시간 동안 vital sign 추출
- numpy array(VITAL SIGN, STAY_ID, HOUR)로 추출
