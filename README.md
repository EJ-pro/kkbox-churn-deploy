## KKBOX 구독자 이탈 예측 및 방지 시스템 (Churn Prevention System)
- KKBOX 데이터를 활용하여 이탈 위험 고객을 조기에 감지하고, 맞춤형 마케팅 액션을 시뮬레이션하여 비즈니스 손실을 최소화하는 솔루션입니다.

## Live Demo / 배포

이 저장소는 Streamlit Community Cloud에서 바로 실행할 수 있도록 준비되어 있습니다. 배포본은 개인정보가 없는 고정 시드의 익명 데모 데이터를 사용합니다.

### 로컬 실행

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run frontend/app.py
```

DB 없이 데모 모드를 고정하려면 `.env.example`을 `.env`로 복사한 뒤 `DATA_SOURCE=demo`를 사용합니다. 환경변수가 없으면 MySQL 연결을 먼저 시도하고, 연결할 수 없을 때 자동으로 데모 모드로 전환됩니다.

### Streamlit Community Cloud

1. 저장소를 배포할 GitHub 계정에 Fork합니다.
2. [share.streamlit.io](https://share.streamlit.io/)에서 `New app`을 선택합니다.
3. Main file path를 `frontend/app.py`로 설정합니다.
4. Advanced settings의 Secrets에 아래 값을 추가합니다.

```toml
DATA_SOURCE = "demo"
```

MySQL을 연결할 때는 `DATA_SOURCE = "mysql"`로 변경하고 `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`을 환경변수로 설정합니다. 실제 비밀번호나 원본 KKBOX 데이터는 Git에 커밋하지 않습니다.

## 팀원 소개

<table>
<colgroup>
<col style="width: 20%;">
<col style="width: 20%;">
<col style="width: 20%;">
<col style="width: 20%;">
<col style="width: 20%;">
</colgroup>
<tbody>
<!-- 1. 프로필 이미지 -->
<tr>
<td style="text-align: center;"><img src="Image/content1.png" alt="이혜림"style="width: 180px;"></td>
<td style="text-align: center;"><img src="Image/content3.png" alt="오주희"style="width: 180px;"></td>
<td style="text-align: center;"><img src="Image/content2.png" alt="이재희"style="width: 180px;"></td>
<td style="text-align: center;"><img src="Image/content4.png" alt="박송원"style="width: 180px;"></td>
<td style="text-align: center;"><img src="Image/content5.png" alt="신동혁"style="width: 180px;"></td>
</tr>
<!-- 2. 이름 -->
<tr style="font-weight: bold;">
<td style="text-align: center;">이혜림</td>
<td style="text-align: center;">오주희</td>
<td style="text-align: center;">이재희</td>
<td style="text-align: center;">박송원</td>
<td style="text-align: center;">신동혁</td>
</tr>
<!-- 3. GitHub 링크 -->
<tr>
<td style="text-align: center;">
<a href="https://github.com/hi20260204-maker"><img src="https://img.shields.io/badge/hi20260204--maker-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
</td>
<td style="text-align: center;">
<a href="https://github.com/ohjuheecode"><img src="https://img.shields.io/badge/ohjuheecode-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
</td>
<td style="text-align: center;">
<a href="https://github.com/EJ-pro"><img src="https://img.shields.io/badge/EJ--pro-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
</td>
<td style="text-align: center;">
<a href="https://github.com/SongwonPark08"><img src="https://img.shields.io/badge/SongwonPark08-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
</td>
<td style="text-align: center;">
<a href="https://github.com/techshin31"><img src="https://img.shields.io/badge/techshin31-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
</td>
</tr>

<!-- 5. 세부 업무 -->
<tr style="font-size: 0.85em;">
<td style="text-align: center;">이탈률 방어 모델<br>백엔드</td>
<td style="text-align: center;">이탈률 예측 모델<br>데이터 전처리 및 수집<br>백엔드</td>
<td style="text-align: center;">이탈 원인 분석 모델<br>프론트</td>
<td style="text-align: center;">이탈률 예측 모델<br>프론트</td>
<td style="text-align: center;">이탈률 예측 모델<br>데이터 전처리 및 수집<br>문서정리</td>
</tr>
</tbody>
</table>

## 프로젝트 개요   
- 배경

- "구독 경제의 핵심, 리텐션(서비스나 제품을 이용한 사용자가 특정 기간 후에도 재방문하거나 지속적으로 이용하는 비율(잔존율))" 
> 성숙기에 접어든 스트리밍 시장: 디지털 음악 스트리밍 산업은 고도의 성숙 단계에 진입하였으며, 대만 시장 점유율 1위인 KKBOX 역시 Spotify, Apple Music 등 글로벌 거대 플랫폼과의 치열한 경쟁에 직면해 있습니다.

> 신규 유치보다 중요한 유지: 구독 경제 모델에서 신규 고객 유치 비용(CAC,Customer Acquisition Cost)은 기존 고객 유지 비용(CRC, Customer Retention Cost)보다 5~25배 더 높게 발생합니다. 따라서 지속 가능한 성장을 위해서는 고객 이탈율(Churn Rate)을 낮추고 고객 생애 가치(LTV)를 극대화하는 것이 필수적입니다.

> 데이터 기반 의사결정의 필요성: 수백만 명의 사용자 행동 로그와 결제 데이터를 수동으로 분석하여 이탈 징후를 파악하는 것은 불가능합니다. 이에 머신러닝을 활용한 자동화된 이탈 예측 시스템 도입이 절실해졌습니다.

- 목적
- 선제적 대응을 통한 비즈니스 방어
  > 고위험군 조기 식별: 사용자의 활동 패턴 및 결제 이력을 분석하여 이탈 가능성이 높은 사용자를 서비스 종료 전 선제적으로 분류합니다.

  > 이탈 핵심 원인 파악: 어떤 요소(결제 수단, 청취 시간 감소 등)가 고객의 이탈에 가장 큰 영향을 미치는지 데이터로 증명합니다.

  > 데이터 기반 리텐션 전략 수립: 모델이 예측한 이탈 확률을 바탕으로 마케팅 예산을 효율적으로 배분하고, 개인화된 혜택(쿠폰, 푸시 알림 등)을 제공할 수 있는 근거를 마련합니다.

## 데이터 소개
> 데이터 수집 경로(kkbox) : (https://www.kaggle.com/c/kkbox-churn-prediction-challenge)

- Data Dictionary

| 분류 | 파일명 | 컬럼명 | 설명 |
| :--- | :--- | :--- | :--- |
| **Label** | `train.csv` | `msno` | 사용자 고유 ID |
| | | `is_churn` | **Target**: 1 (이탈), 0 (유지) |
| **User Info** | `members.csv` | `city` | 거주 도시 정보 |
| | | `bd` | 나이 (이상치 포함 가능성 높음) |
| | | `gender` | 성별 |
| | | `registered_via` | 등록 경로 |
| | | `registration_init_time` | 최초 등록일 |
| **Finance** | `transactions.csv` | `payment_method_id` | 결제 수단 코드 |
| | | `payment_plan_days` | 구독 계획 기간 (일 단위) |
| | | `plan_list_price` | 정가 |
| | | `actual_amount_paid` | 실제 결제 금액 |
| | | `is_auto_renew` | 자동 갱신 설정 여부 |
| | | `transaction_date` | 결제 발생 일자 |
| | | `membership_expire_date` | 멤버십 만료 예정일 |
| | | `is_cancel` | 사용자의 명시적 구독 취소 여부 |
| **Activity** | `user_logs.csv` | `date` | 로그 기록 일자 |
| | | `num_25/50/75/985/100` | 전체 곡 길이 대비 재생 비율별 횟수 |
| | | `num_unq` | 일일 고유 곡 재생 수 |
| | | `total_secs` | 일일 총 재생 시간(초) |

---
## Raw Dataset
| File Name | Description | Size (Disk) | Est. Rows |
| :--- | :--- | :---: | :---: |
| **`user_logs.csv`** | 사용자의 일별 스트리밍 활동 로그 | **~30.5 GB** | 약 3억 9,000만 행 |
| **`transactions.csv`** | 사용자의 결제 및 구독 갱신 이력 | ~1.7 GB | 약 2,150만 행 |
| **`members_v3.csv`** | 사용자의 인구통계학적 정보 (도시, 나이 등) | ~428 MB | 약 676만 행 |
| **`train_v2.csv`** | 이탈(`is_churn`) 여부가 포함된 학습용 라벨 데이터 | ~45 MB | 약 97만 행 |

 
> 전체 30GB 이상의 데이터를 그대로 학습에 사용하기에는 너무 오랜 시간이 걸리기에, 따라서 본 프로젝트에서는 결측값이 없고 모든 활동 기록이 존재하는 100,000명의 사용자만을 선별하여, 분석 효율성을 극대화한 Balanced 데이터셋을 생성하였습니다.
- Data Balance: 학습 성능 향상을 위해 이탈과 유지 데이터를 1:1 비율로 구성하였습니다.

##  기술 스택   

### Language
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

### Data Analysis
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)

### Visualization
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=plotly&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-4C72B0?style=for-the-badge&logoColor=white)

### Machine Learning
![XGBoost](https://img.shields.io/badge/XGBoost-218EBB?style=for-the-badge&logo=xgboost&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)

### Frontend & Library
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

### Tool
![Google Colab](https://img.shields.io/badge/Google%20Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![PyMySQL](https://img.shields.io/badge/PyMySQL-4479A1?style=for-the-badge&logo=python&logoColor=white)<!-- Git -->
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white)
![Figma](https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white)

### DevOps & Infrastructure
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
   
## WBS (Work Breakdown Structure)
| 작업                           | 3/26 | 3/27 | 3/28 | 3/29 | 3/30 | 3/31 | 4/1 | 4/2 |
| ----------------------------| ---- | ---- | ---- | ---- | ---- | ---- | --- | --- |
| 요구사항 정의서 작성           | ███  | ███  | ███  |      |      |      |     |     |
| 화면설계서 작성                | ███  | ███  | ███  |      |      |      |     |     |
| ERD 설계                       | ███  | ███  | ███  |      |      |      |     |     |
| 데이터 수집                    | ███  | ███  |      |      |      |      |     |     |
| 데이터 전처리                  |      | ███  | ███  | ███  | ███  | ███  | ███ |     |
| 모델링 & 실험                  |      |      |      | ███  | ███  | ███  | ███ |     |
| 백엔드 개발                    |      |      |      |       | ███  |     |      |     |
| 프론트 개발                    |      |      |███   | ███  |       |     |      |     |
| 프론트&백엔드 연결 및 통합 테스트|      |      |      |      |      |       | ███ |  ███ |
| 발표 준비                      |      |      |      |      |      |      | ███ | ███ |
   

<br>   

# 요구사항정의서
<p align="center">
  <img src="Image/ERD.png" width="80%" alt="ERD">
</p>

# ERD
<p align="center">
  <img src="Image/ERD1.png" width="80%" alt="ERD">
</p>

## 프로젝트 구조
```
SKN27-2nd-3Team/ 
│
frontend/
└─pages/ (📚 멀티 페이지 앱의 메뉴 구성)
    │   Streamlit은 이 pages 폴더 안에 있는 파이썬 파일들을 파일명에 맞춰
    │   웹 페이지 좌측 사이드바(Sidebar)의 '메뉴(페이지)'로 자동 인식합니다.
    │
    ├─action/ (✨ 개별 페이지 또는 기능 모듈 1)
    │  │   '액션(행동/작업)'과 관련된 UI 화면이나 동작을 렌더링하는 코드가 있는 폴더입니다.
    │  └─pycache/
    │
    ├─action_board/ (📊 개별 페이지 또는 기능 모듈 2)
    │  │   진행 중인 액션들의 현황을 보여주는 '대시보드(게시판)' 역할의 화면을 구현한 파이썬 코드가 위치합니다.
    │  └─pycache/
    │
    ├─simulator/ (🕹️ 개별 페이지 또는 기능 모듈 3)
    │  │   어떠한 조건이나 데이터를 입력하여 결과를 예측해보는 '시뮬레이터' 기능의 화면 로직이 위치합니다.
    │  └─pycache/
    │
    └─pycache/ (무시해도 되는 파이썬 캐시 파일)
    backend/
    ├─app/ (🌟 핵심 애플리케이션 코드)
    │  │   실제 비즈니스 로직, API 라우터, 모델 등이 작성되는 메인 작업 공간입니다.
    │  │
    │  ├─config/
    │  │   데이터베이스 URL, 비밀키, 환경 변수 등 애플리케이션의 설정(Settings)을 관리하는 코드가 들어갑니다.
    │  │
    │  ├─database/
    │  │   데이터베이스 연결(Connection), 세션 관리, ORM 모델(SQLAlchemy 등) 설정 코드가 위치합니다.
    │  │   └─pycache/ (Python 실행 파일 캐시 - 무시해도 됨)
    │  │
    │  └─pycache/ (Python 실행 파일 캐시 - 무시해도 됨)
    │
    ├─data/ (📁 정적 데이터 로컬 저장소)
    │  │   앱에서 사용하거나 외부에서 가져온 데이터를 임시로 보관하는 곳입니다.
    │  │
    │  └─raw/
    │      웹 스크래핑 결과, 엑셀/CSV 파일 등 아직 가공되지 않은 '원본 데이터'를 저장해두는 용도로 사용됩니다.
    │
    ├─docker/ (🐳 도커 컨테이너 설정)
    │  │   프로젝트를 쉽게 배포하고 실행하기 위한 Docker 관련 설정 파일들이 모여있는 곳입니다.
    │  │
    │  └─mysql/
    │      MySQL 데이터베이스 컨테이너를 위한 폴더입니다.
    │      └─init/
    │          데이터베이스가 처음 생성될 때 자동으로 실행될 초기화 스크립트(.sql 파일 등)를 넣는 곳입니다. 테이블을 생성하거나 기초 데이터를 넣는 코드가 들어갑니다.
    │
    ├─scripts/ (🛠️ 유틸리티 및 보조 스크립트)
    │  │   백엔드 서버를 직접 띄우는 코드는 아니지만, 개발/운영에 필요한 잡다한 파이썬 스크립트 파일들이 위치합니다.
    │  │   (예: 메일 발송 테스트, DB 마이그레이션 실행, 초기 더미 데이터 삽입 스크립트 등)
    │  └─pycache/
    │
    └─sql/ (💾 순수 SQL 쿼리 파일)
       파이썬 코드 내부가 아닌, 분리해서 관리하고 싶은 복잡한 SQL 쿼리문 파일이나 뷰(View), 프로시저 생성 스크립트 등을 저장해두는 폴더입니다.
```
## PAGE
<p align="center">
  <img src="Image/page2.png" width="80%" alt="ERD">
</p>

<p align="center">
  <img src="Image/page1.png" width="80%" alt="ERD">
</p>

<p align="center">
  <img src="Image/page3.png" width="80%" alt="ERD">
</p>

---
## 데이터 전처리 결과서 (EDA)

### 1. 원본 및 기본 변수 (Raw Features)
사용자 마스터 데이터(`members.csv`)를 기반으로 한 기초 변수

| 변수명 | 설명 | 전처리 및 특징 |
| :--- | :--- | :--- |
| `city` | 거주 도시 | 사용자 지역 특성 반영 |
| `bd` | 나이 | 비정상값(0 이하, 100 이상) 중앙값 대체 |
| `gender` | 성별 | female(0), male(1) 변환 |
| `registered_via` | 가입 채널 | 가입 경로별 잔존율 차이 반영 |
| `registration_init_time` | 최초 가입일 | `tenure` 변수 생성의 기준점 |
| `tenure` | 서비스 이용 기간 | 기준일 직전까지의 총 누적 일수 |

### 2. 거래 기반 파생 변수 (Transaction Derived)
결제 이력(`transactions.csv`)을 가공하여 사용자의 결제 패턴과 가격 민감도를 추출

#### 할인 및 가격 관련
- `discount_amount`: 정가 대비 실결제 금액의 차이 (할인 절대 크기)
- `discount_rate`: 할인율 (가격 민감도 및 할인 의존도 파악)
- `has_discount`: 할인 적용 여부 (0/1)
- `discount_rate_mean / last`: 전체 평균 할인율 및 최근 거래 할인율
- `has_discount_rate`: 전체 거래 중 할인 거래가 차지하는 비중

#### 거래 상태 및 주기
- `payment_method_id_last / nunique`: 최근 결제 수단 및 수단 변경의 다양성
- `payment_plan_days_last / mean / std`: 최근 및 평균 구독 기간과 그 변동성
- `is_auto_renew_last / rate`: 최근 자동갱신 여부 및 전체 기간 자동갱신 비율
- `is_cancel_last / rate`: 최근 구독 취소 여부 및 전체 기간 취소 비율
- `days_since_last_txn`: 마지막 결제 후 경과 일수
- `days_until_expire`: 기준일 기준 멤버십 만료까지 남은 잔여 일수
- `last_payment_gap`: 마지막 결제일과 마지막 만료일 사이의 간격

#### 최근 2회 거래 변화량
- `actual_paid_change_last2`: 최근 2회 결제 금액의 변화량
- `plan_days_change_last2`: 최근 2회 구독 기간의 변화량
- `txn_gap_last2`: 최근 2회 결제 발생 사이의 시간 간격

### 3. 로그 기반 파생 변수 (Log Derived)
사용자 활동 로그(`user_logs.csv`)를 집계하여 서비스 충성도를 정량화

| 카테고리 | 주요 변수 | 설명 |
| :--- | :--- | :--- |
| **활동성** | `active_days_all / 7 / 30` | 전체/최근 7일/최근 30일 실제 활동 일수 |
| **청취량** | `total_secs_all / 7 / 30` | 기간별 총 청취 시간 및 평균 시간 |
| **패턴** | `num_100_all`, `completion_ratio` | 완청(100% 재생) 횟수 및 전체 재생 대비 완청 비율 |
| **다양성** | `num_unq_all`, `unique_ratio` | 고유 곡 재생 수 및 전체 재생 대비 고유 곡 비율 |
| **결제 후 행동** | `days_to_first_listen` | 결제 발생 후 첫 청취까지 걸린 시간 (평균/최근) |

---

## Model Performance & Evaluation

- 모델의 예측 성능을 측정하기 위해 여러가지 모델을 사용했으며 이와 같은 결과값에 대한 설명입니다.

### 1. 성능 지표 요약 (Summary Table)

| Evaluation Metric | Result (Mean) | Description |
| :--- | :---: | :--- |
| **XGBoost** | `0.9045` | features 변수 생성 |
| **Stacking(XGB,LGBM,CAT)** | `0.9054` | Stacking 활용 |

---

### 성능 시각화 (Visualizations)

### XGBoost

#### Confusion Matrix & Loss Curve

1. Confusion Matrix (혼동 행렬)

<p align="center">
  <img src="Image/confusion_matrix1.png" width="90%" alt="Confusion Matrix" />
</p>

2. Loss Curve (학습 손실 곡선)

<p align="center">
<img src="Image/roc_auc_curve1.png" width="90%" alt="ROC-AUC Curve" />
</p>

- Feature Importance 

<p align="center">
  <img src="Image/feature_importance1.png" width="90%" alt="Feature Importance" />
</p>

### Stacking

#### Confusion Matrix & Loss Curve
1. Confusion Matrix (혼동 행렬)

<p align="center">
  <img src="Image/confusion_matrix.png" width="90%" alt="Confusion Matrix" />
</p>

2. Loss Curve (학습 손실 곡선)

<p align="center">
<img src="Image/roc_auc_curve.png" width="90%" alt="ROC-AUC Curve" />
</p>

- Feature Importance

<p align="center">
  <img src="Image/feature_importance.png" width="90%" alt="Feature Importance" />
</p>

---

## 최종 결론 및 프로젝트 인사이트

## 1. 주요 이탈 요인 분석 (Feature Importance)
- **is_auto_renew_last (자동 갱신 여부)**  
  마지막 결제 시 자동 갱신을 선택하지 않은 사용자는 이탈 가능성이 매우 높다. 이 시점에 즉각적인 리텐션 프로모션 제공이 필수적이다.
- **is_cancel_last (최근 결제 취소 여부)**  
  최근 결제를 직접 취소한 사용자는 강력한 이탈 선행 지표로 확인되었다.
- **last_payment_gap, days_since_last_txn (결제 공백 및 거래 간격)**  
  결제 공백 기간이 길어지거나 결제 간격이 벌어질수록 이탈 위험이 증가한다.
- **활동성 변수의 중요성**  
  unique_ratio_7(최근 7일간 고유 곡 비율)과 active_days_30(30일 내 활동일수)은 예측에 중요한 역할을 해, 사용 패턴 변화 역시 이탈 신호임을 보여준다.

## 2. 모델 성능 및 안정성 평가 (Confusion Matrix & Loss Curve)
- **XGBoost CV Ensemble (baseline) 모델 성능**  
  - True Negative (유지 맞춤): 6,612건  
  - False Positive (유지→이탈 오분류): 1,379건  
  - False Negative (이탈→유지 오분류): 1,236건  
  - True Positive (이탈 맞춤): 6,754건  
- **Stacking 모델 성능**  
  - True Negative: 6,802건  
  - False Positive: 1,189건  
  - False Negative: 1,369건  
  - True Positive: 6,621건  
- Stacking 모델이 유지(0) 클래스에서 더 높은 정확도를 보이며, 이탈(1) 클래스도 균형 있게 예측하여 전체적인 성능 안정성을 개선하였다.
- XGBoost, LightGBM, CatBoost 세 모델 모두 Loss Curve가 안정적으로 감소하며 과적합 없이 신뢰성 있는 학습을 달성하였다.

## 3. 비즈니스 제안 및 추가 제안
- **타겟 마케팅 집중**  
  이탈 확률(pred_prob_is_churn)이 높고, 자동 갱신이 꺼진 사용자에게 할인 쿠폰 등 맞춤 혜택 제공으로 자동 갱신 전환을 유도해야 한다.
- **이탈 징후 모니터링 자동화**  
  결제 공백이 늘어나는 사용자를 위험군으로 분류해 푸시 알림과 개인 맞춤 콘텐츠로 재방문을 유도해야 한다.
- **실시간 리텐션 전략 수립**  
  Stacking 모델을 마케팅 자동화 시스템과 연동하여 다이내믹한 고객 관리 및 즉각 대응이 가능하도록 해야 한다.
- **추가 제안 - 고객 세분화 및 행동 분석 심화**  
  고객 생애가치(LTV), 가입 기간, 음악 장르 선호도 등 추가 변수를 결합해 세분화 마케팅 전략을 강화할 수 있다.
- **지속적 모델 업데이트 및 재학습 강조**  
  사용자 행동 및 시장 변화를 반영해 정기적인 데이터 갱신과 모델 재학습을 통해 모델 성능을 유지·개선해야 한다.

## 결론

이번 프로젝트에서는 XGBoost와 Stacking(XGBoost, LightGBM, CatBoost) 모델을 활용해 고객 이탈 예측을 수행하였다. 모델 성능 비교 결과, XGBoost의 평균 성능은 0.9045, Stacking 모델의 평균 성능은 0.9054로 나타나 Stacking이 단일 모델 대비 소폭 우수한 예측력을 보였다. 수치 차이는 크지 않지만, 이는 서로 다른 부스팅 계열 모델의 장점을 결합함으로써 예측의 안정성과 일반화 성능을 높인 결과로 해석할 수 있다.

혼동행렬 결과를 보면, XGBoost는 유지 고객 6,612건과 이탈 고객 6,754건을 정확히 예측한 반면, Stacking 모델은 유지 고객 6,802건을 정확히 분류하여 유지 고객 판별 측면에서 더 나은 성능을 보였다. 특히 유지 고객을 이탈로 잘못 분류한 False Positive가 1,379건에서 1,189건으로 감소해, 실제 서비스 운영 시 불필요한 마케팅 비용이나 과도한 리텐션 개입을 줄일 수 있다는 장점이 있다. 반면 이탈 고객 탐지 수는 다소 감소했지만, 전체적으로는 두 클래스를 보다 균형 있게 예측하며 안정적인 분류 성능을 보였다.

학습 곡선 측면에서도 XGBoost, LightGBM, CatBoost 모두 loss가 안정적으로 감소하는 모습을 보여 과적합 없이 신뢰할 수 있는 학습이 이루어졌음을 확인하였다. 이는 본 프로젝트에서 생성한 행동·결제 기반 파생변수들이 실제 이탈 패턴을 잘 반영하고 있으며, 모델이 이를 효과적으로 학습했다는 점을 뒷받침한다.

주요 이탈 요인으로는 자동 갱신 여부(is_auto_renew_last), 최근 결제 취소 여부(is_cancel_last), 결제 공백 기간(last_payment_gap), 최근 거래 이후 경과일(days_since_last_txn) 등이 확인되었다. 특히 자동 갱신이 해제된 고객과 결제 공백이 길어진 고객은 이탈 가능성이 높은 핵심 위험군으로 볼 수 있다. 또한 최근 7일 고유곡 비율(unique_ratio_7), 최근 30일 활동일수(active_days_30)와 같은 활동성 변수도 중요하게 작용하여, 결제 정보뿐 아니라 사용 패턴 변화 역시 이탈을 설명하는 주요 신호임을 확인하였다.

종합하면, 본 프로젝트는 단순히 고객 이탈을 예측하는 데 그치지 않고, 실제 비즈니스 현장에서 활용 가능한 리텐션 전략 수립의 근거를 제공했다는 점에서 의미가 있다. 향후에는 자동 갱신 해지 고객을 대상으로 한 맞춤형 프로모션, 결제 공백 증가 고객에 대한 실시간 모니터링, 고객 세분화 기반의 차등 마케팅 전략을 적용함으로써 보다 정교한 churn prevention system으로 확장할 수 있을 것이다. 또한 지속적인 데이터 업데이트와 주기적인 모델 재학습을 통해 예측 성능과 리텐션 효과를 함께 높여 나갈 수 있을 것으로 기대된다.

## 한줄 회고

- 이혜림 : 머신러닝을 배우는 좋은 기회였습니다. 도메인의 조사에 대한 중요성을 느낄 수 있었어요!

- 이재희 : 이번 프로젝트를 경험으로 처음으로 데이터와 프론트엔드의 안정적인 연결을 구현해 낸거같다. 경험을 늘리는데 많이 도움이 되었다. 

- 박송원 : 데이터와 머신러닝을 우리만의 데이터로 다룰 수 있는 기회가 주어져서 지식도 많이 늘고 도움이 많이 되었습니다.

- 오주희 : 데이터 기반 변수 설계와 모델 비교를 통해 고객 이탈 예측의 실효성을 확인했으며, 앞으로는 성능 향상뿐 아니라 실제 리텐션 전략에 바로 연결되는 분석으로 확장해야 함을 배웠다.

- 신동혁 : 그동안의 데이터 셋보다 큰 데이터셋일 경우 어떻게 처리해야 될지, 그리고 여러 모델들을 직접 활용 해보면서 많은 점을 배운 것 같습니다.
