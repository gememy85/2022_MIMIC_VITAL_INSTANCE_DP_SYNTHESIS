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
- 시간축(dim = 3)에서 0번째가 24시간 전, 23번째가 퇴원할(죽을) 당시 vital
- null값은 -1로 표현

## Load npz data

```
import numpy as np
death = np.load('data/processed/death_numpy.npz')['result']
live = np.load('data/processed/live_numpy.npz')['result']

```
