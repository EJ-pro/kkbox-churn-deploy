"""
data_layer.py
- Streamlit 프론트에서 MySQL(churn_db)에 직접 연결
- members / transactions / user_logs / churn_predictions 조회
- 화면에서 바로 쓸 수 있게 DataFrame 가공
"""

from __future__ import annotations

import os
import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from pages.action_board.config import HIGH_RISK_THRESHOLD

# ── DATABASE CONNECTION ──────────────────────────────────────────────────
# backend/.env 파일에서 DB 정보를 로드합니다.
env_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend", ".env")
load_dotenv(env_path)

DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASSWORD", "app1234")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3307")
DB_NAME = os.getenv("DB_NAME", "churn_db")

def _build_demo_data(size: int = 1200) -> dict[str, pd.DataFrame]:
    """무료 배포와 포트폴리오 시연을 위한 재현 가능한 익명 데모 데이터."""
    rng = np.random.default_rng(20260402)
    user_ids = np.array([f"demo_{index:05d}" for index in range(1, size + 1)])
    base_date = pd.Timestamp("2026-04-02")

    auto_renew = rng.choice([0, 1], size=size, p=[0.38, 0.62])
    is_cancel = rng.choice([0, 1], size=size, p=[0.86, 0.14])
    activity_drop = rng.beta(2.1, 3.7, size=size)
    churn_probability = np.clip(
        0.18
        + (1 - auto_renew) * 0.34
        + is_cancel * 0.30
        + activity_drop * 0.24
        + rng.normal(0, 0.055, size),
        0.03,
        0.99,
    )

    reasons = np.select(
        [
            is_cancel == 1,
            auto_renew == 0,
            activity_drop >= 0.62,
            activity_drop >= 0.40,
        ],
        [
            "멤버십 직접해지",
            "자동결제 미등록",
            "최근 7일간 활동성 급감",
            "일평균 청취량 및 몰입도 저하",
        ],
        default="복합적 요인(기타 사유)",
    )
    risk_grade = np.select(
        [churn_probability >= 0.90, churn_probability >= 0.80],
        ["높음", "보통"],
        default="낮음",
    )

    members = pd.DataFrame({
        "msno": user_ids,
        "city": rng.integers(1, 23, size=size),
        "registered_via": rng.choice([3, 4, 7, 9, 13], size=size),
        "is_churn": (churn_probability >= 0.68).astype(int),
    })
    transactions = pd.DataFrame({
        "msno": user_ids,
        "payment_method_id": rng.choice([29, 30, 36, 38, 41], size=size),
        "payment_plan_days": rng.choice([30, 60, 90], size=size, p=[0.82, 0.12, 0.06]),
        "plan_list_price": rng.choice([99, 129, 149, 180], size=size, p=[0.14, 0.51, 0.25, 0.10]),
        "actual_amount_paid": rng.choice([99, 129, 149, 180], size=size, p=[0.14, 0.51, 0.25, 0.10]),
        "is_auto_renew": auto_renew,
        "is_cancel": is_cancel,
        "transaction_date": base_date - pd.to_timedelta(rng.integers(1, 45, size=size), unit="D"),
        "membership_expire_date": base_date + pd.to_timedelta(rng.integers(-7, 15, size=size), unit="D"),
        "is_churn": (churn_probability >= 0.68).astype(int),
    })
    user_logs = pd.DataFrame({
        "msno": user_ids,
        "num_25": rng.integers(0, 80, size=size),
        "num_50": rng.integers(0, 60, size=size),
        "num_75": rng.integers(0, 50, size=size),
        "num_985": rng.integers(0, 40, size=size),
        "num_100": rng.integers(0, 160, size=size),
        "num_unq": rng.integers(1, 120, size=size),
        "total_secs": rng.integers(600, 72000, size=size),
    })
    predictions = pd.DataFrame({
        "msno": user_ids,
        "prediction_date": base_date,
        "churn_probability": churn_probability,
        "risk_grade": risk_grade,
        "main_reason_code": reasons,
    })

    return {
        "members": members,
        "transactions": transactions,
        "user_logs": user_logs,
        "predictions": predictions,
    }


# ── 내부 헬퍼 ─────────────────────────────────────────────────────────────
def _parse_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.copy()
    df.columns = df.columns.str.strip()

    date_cols = [c for c in df.columns if ("date" in c.lower()) or ("time" in c.lower())]

    for col in date_cols:
        s = df[col].copy()

        # 1) 문자열로 통일
        s = s.astype(str).str.strip()

        # 2) 자주 나오는 비정상값 제거
        s = s.replace({
            "nan": None,
            "None": None,
            "NaT": None,
            "": None,
            "0": None,
            "00000000": None,
        })

        # 3) 20170131.0 같은 값 처리
        s = s.str.replace(r"\.0$", "", regex=True)

        # 4) YYYYMMDD 우선 파싱
        parsed = pd.to_datetime(s, format="%Y%m%d", errors="coerce")

        # 5) 그래도 실패한 건 일반 파싱 재시도
        fallback = pd.to_datetime(s, errors="coerce")

        # Ensure datetime type and shift by 3320 days to make 2017 data appear as 2026
        dt_series = pd.to_datetime(parsed.fillna(fallback), errors='coerce')
        df[col] = dt_series + pd.Timedelta(days=3320)

    return df

def _read_table(table_name: str) -> pd.DataFrame:
    from sqlalchemy import create_engine, text

    connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(connection_string)
    with engine.connect() as conn:
        df = pd.read_sql(text(f"SELECT * FROM {table_name}"), conn)
    return _parse_date_columns(df)


@st.cache_data(ttl=3600)
def get_shifted_raw_data(force_refresh: bool = False) -> dict[str, pd.DataFrame]:
    """
    모든 테이블을 로드하고 날짜를 3320일 밀어줍니다. (v3: Renamed to clear cache)
    """
    data_source = os.getenv("DATA_SOURCE", "auto").lower()
    if data_source == "demo":
        return _merge_source_data(_build_demo_data())

    try:
        members = _read_table("members")
        transactions = _read_table("transactions")
        user_logs = _read_table("user_logs")
    except Exception as exc:
        if data_source == "mysql":
            raise
        print(f"MySQL unavailable; using demo data: {exc}")
        return _merge_source_data(_build_demo_data())

    # churn_prediction 은 있을 수도 있고 없을 수도 있게 처리
    try:
        predictions = _read_table("churn_prediction")
    except Exception:
        predictions = pd.DataFrame()
    print("members:", members.shape)
    print("transactions:", transactions.shape)
    print("user_logs:", user_logs.shape)
    print("predictions:", predictions.shape)


    return _merge_source_data({
        "members": members,
        "transactions": transactions,
        "user_logs": user_logs,
        "predictions": predictions,
    })


def _merge_source_data(raw: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    members = raw.get("members", pd.DataFrame()).copy()
    transactions = raw.get("transactions", pd.DataFrame()).copy()
    user_logs = raw.get("user_logs", pd.DataFrame()).copy()
    predictions = raw.get("predictions", pd.DataFrame()).copy()

    # 1) members.is_churn 병합
    if not members.empty and not transactions.empty:
        if "msno" in members.columns and "msno" in transactions.columns:
            if "is_churn" in members.columns and "is_churn" not in transactions.columns:
                transactions = pd.merge(
                    transactions,
                    members[["msno", "is_churn"]],
                    on="msno",
                    how="left"
                )
                transactions["is_churn"] = transactions["is_churn"].fillna(0)

    # 2) user_logs 요약 병합
    # 주의: 현재 스키마엔 user_logs 날짜 컬럼이 없음
    if not user_logs.empty and not transactions.empty:
        if "msno" in user_logs.columns and "msno" in transactions.columns:
            agg_dict = {}
            for col in ["num_25", "num_50", "num_75", "num_985", "num_100", "num_unq", "total_secs"]:
                if col in user_logs.columns:
                    agg_dict[col] = "sum"

            if agg_dict:
                log_summary = user_logs.groupby("msno", as_index=False).agg(agg_dict)

                rename_map = {}
                if "num_25" in log_summary.columns:
                    rename_map["num_25"] = "total_25"
                if "num_50" in log_summary.columns:
                    rename_map["num_50"] = "total_50"
                if "num_75" in log_summary.columns:
                    rename_map["num_75"] = "total_75"
                if "num_985" in log_summary.columns:
                    rename_map["num_985"] = "total_985"
                if "num_100" in log_summary.columns:
                    rename_map["num_100"] = "total_100"
                if "num_unq" in log_summary.columns:
                    rename_map["num_unq"] = "total_unq"
                if "total_secs" in log_summary.columns:
                    rename_map["total_secs"] = "sum_total_secs"

                log_summary = log_summary.rename(columns=rename_map)

                transactions = pd.merge(
                    transactions,
                    log_summary,
                    on="msno",
                    how="left"
                )

    return {
        "members": members,
        "transactions": transactions,
        "user_logs": user_logs,
        "predictions": predictions,
    }


def _inject_churn_probability(
    transactions: pd.DataFrame,
    model=None,
) -> pd.DataFrame:
    """
    우선순위
    1. churn_prediction 테이블 값 사용
    2. transactions에 이미 churn_prob 있으면 사용
    3. is_churn 기반 더미
    4. is_auto_renew 기반 더미
    """
    df = transactions.copy()
    if df.empty:
        return df

    raw = get_shifted_raw_data()
    predictions = raw.get("predictions", pd.DataFrame())

    # 1) churn_prediction 우선
    if not predictions.empty and "msno" in predictions.columns:
        pred_df = predictions.copy()

        # prediction_date가 있으면 최신 예측만 사용
        if "prediction_date" in pred_df.columns:
            pred_df = pred_df.sort_values("prediction_date").drop_duplicates("msno", keep="last")

        keep_cols = ["msno"]
        if "churn_probability" in pred_df.columns:
            keep_cols.append("churn_probability")
        if "risk_grade" in pred_df.columns:
            keep_cols.append("risk_grade")
        if "main_reason_code" in pred_df.columns:
            keep_cols.append("main_reason_code")

        pred_df = pred_df[keep_cols]

        df = pd.merge(df, pred_df, on="msno", how="left")

        if "churn_probability" in df.columns:
            df["churn_prob"] = df["churn_probability"]

        if "churn_prob" in df.columns and df["churn_prob"].notna().any():
            # 예측 없는 행만 fallback
            missing_mask = df["churn_prob"].isna()

            if missing_mask.any():
                rng = np.random.default_rng(42)
                if "is_churn" in df.columns:
                    df.loc[missing_mask, "churn_prob"] = df.loc[missing_mask, "is_churn"].apply(
                        lambda x: rng.uniform(0.85, 1.0) if x == 1 else rng.uniform(0.0, 0.4)
                    )
                elif "is_auto_renew" in df.columns:
                    df.loc[missing_mask, "churn_prob"] = np.where(
                        df.loc[missing_mask, "is_auto_renew"].fillna(1).values == 0,
                        rng.uniform(0.7, 1.0, missing_mask.sum()),
                        rng.uniform(0.0, 0.6, missing_mask.sum()),
                    )
                else:
                    df.loc[missing_mask, "churn_prob"] = rng.uniform(0.0, 1.0, missing_mask.sum())

            # risk_grade 없으면 churn_prob로 생성
            if "risk_grade" not in df.columns:
                def determine_grade(x):
                    if x >= 0.9: return "높음"
                    if x >= 0.8: return "보통"
                    return "낮음"
                df["risk_grade"] = df["churn_prob"].apply(determine_grade)

            # main_reason_code 없으면 간단 규칙으로 생성
            if "main_reason_code" not in df.columns:
                def determine_reason(row):
                    if row.get("is_cancel") == 1:
                        return "멤버십 직접해지"
                    if row.get("is_auto_renew") == 0:
                        return "자동결제 미등록"
                    return "활동성 저하(추정)"
                df["main_reason_code"] = df.apply(determine_reason, axis=1)

            return df

    # 2) 이미 churn_prob 있으면 그대로
    if "churn_prob" in df.columns:
        return df

    # 3) fallback
    rng = np.random.default_rng(42)

    if "is_churn" in df.columns:
        df["churn_prob"] = df["is_churn"].apply(
            lambda x: rng.uniform(0.85, 1.0) if x == 1 else rng.uniform(0.0, 0.4)
        )
    elif "is_auto_renew" in df.columns:
        df["churn_prob"] = np.where(
            df["is_auto_renew"].fillna(1).values == 0,
            rng.uniform(0.7, 1.0, len(df)),
            rng.uniform(0.0, 0.6, len(df)),
        )
    else:
        df["churn_prob"] = rng.uniform(0.0, 1.0, len(df))

    if "risk_grade" not in df.columns:
        df["risk_grade"] = df["churn_prob"].apply(
            lambda x: "높음" if x >= 0.9 else ("보통" if x >= 0.8 else "낮음")
        )

    if "main_reason_code" not in df.columns:
        def determine_reason(row):
            if row.get("is_cancel") == 1:
                return "멤버십 직접해지"
            if row.get("is_auto_renew") == 0:
                return "자동결제 미등록"
            return "활동성 저하(추정)"
        df["main_reason_code"] = df.apply(determine_reason, axis=1)

    return df

def inject_churn_probability(
    transactions: pd.DataFrame,
    model=None,
) -> pd.DataFrame:
    """
    우선순위
    1. churn_prediction 테이블 값 사용
    2. transactions에 이미 churn_prob 있으면 사용
    3. is_churn 기반 더미
    4. is_auto_renew 기반 더미

    + main_reason_code가 없거나 비어 있으면 fallback 원인 생성
    """
    df = transactions.copy()
    if df.empty:
        return df

    raw = get_shifted_raw_data()
    predictions = raw.get("predictions", pd.DataFrame())

    def determine_reason(row):
        if row.get("is_cancel") == 1:
            return "멤버십 직접해지"
        if row.get("is_auto_renew") == 0:
            return "자동결제 미등록"
        return "활동성 저하(추정)"

    # 1) churn_prediction 우선 사용
    if not predictions.empty and "msno" in predictions.columns:
        pred_df = predictions.copy()

        if "prediction_date" in pred_df.columns:
            pred_df = pred_df.sort_values("prediction_date").drop_duplicates("msno", keep="last")

        keep_cols = ["msno"]
        if "churn_probability" in pred_df.columns:
            keep_cols.append("churn_probability")
        if "risk_grade" in pred_df.columns:
            keep_cols.append("risk_grade")
        if "main_reason_code" in pred_df.columns:
            keep_cols.append("main_reason_code")

        pred_df = pred_df[keep_cols]
        df = pd.merge(df, pred_df, on="msno", how="left")

        # churn_probability -> churn_prob 통일
        if "churn_probability" in df.columns:
            df["churn_prob"] = df["churn_probability"]

        # churn_prob fallback
        if "churn_prob" not in df.columns:
            df["churn_prob"] = np.nan

        missing_mask = df["churn_prob"].isna()
        if missing_mask.any():
            rng = np.random.default_rng(42)

            if "is_churn" in df.columns:
                df.loc[missing_mask, "churn_prob"] = df.loc[missing_mask, "is_churn"].apply(
                    lambda x: rng.uniform(0.85, 1.0) if x == 1 else rng.uniform(0.0, 0.4)
                )
            elif "is_auto_renew" in df.columns:
                df.loc[missing_mask, "churn_prob"] = np.where(
                    df.loc[missing_mask, "is_auto_renew"].fillna(1).values == 0,
                    rng.uniform(0.7, 1.0, missing_mask.sum()),
                    rng.uniform(0.0, 0.6, missing_mask.sum()),
                )
            else:
                df.loc[missing_mask, "churn_prob"] = rng.uniform(0.0, 1.0, missing_mask.sum())

        # risk_grade fallback
        def determine_grade(x):
            if x >= 0.9: return "높음"
            if x >= 0.8: return "보통"
            return "낮음"

        if "risk_grade" not in df.columns:
            df["risk_grade"] = df["churn_prob"].apply(determine_grade)
        else:
            generated_grade = df["churn_prob"].apply(determine_grade)
            df["risk_grade"] = df["risk_grade"].fillna(generated_grade)

        # main_reason_code fallback
        if "main_reason_code" not in df.columns:
            df["main_reason_code"] = df.apply(determine_reason, axis=1)
        else:
            fallback_reason = df.apply(determine_reason, axis=1)
            df["main_reason_code"] = df["main_reason_code"].fillna(fallback_reason)

        return df

    # 2) churn_prob가 없으면 fallback 생성
    if "churn_prob" not in df.columns:
        rng = np.random.default_rng(42)

        if "is_churn" in df.columns:
            df["churn_prob"] = df["is_churn"].apply(
                lambda x: rng.uniform(0.85, 1.0) if x == 1 else rng.uniform(0.0, 0.4)
            )
        elif "is_auto_renew" in df.columns:
            df["churn_prob"] = np.where(
                df["is_auto_renew"].fillna(1).values == 0,
                rng.uniform(0.7, 1.0, len(df)),
                rng.uniform(0.0, 0.6, len(df)),
            )
        else:
            df["churn_prob"] = rng.uniform(0.0, 1.0, len(df))

    # risk_grade 보강
    def determine_grade(x):
        if x >= 0.9: return "높음"
        if x >= 0.8: return "보통"
        return "낮음"

    if "risk_grade" not in df.columns:
        df["risk_grade"] = df["churn_prob"].apply(determine_grade)
    else:
        generated_grade = df["churn_prob"].apply(determine_grade)
        df["risk_grade"] = df["risk_grade"].fillna(generated_grade)

    # main_reason_code 보강
    if "main_reason_code" not in df.columns:
        df["main_reason_code"] = df.apply(determine_reason, axis=1)
    else:
        fallback_reason = df.apply(determine_reason, axis=1)
        df["main_reason_code"] = df["main_reason_code"].fillna(fallback_reason)

    return df
