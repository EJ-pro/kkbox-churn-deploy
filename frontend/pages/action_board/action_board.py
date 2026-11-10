from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from pages.action_board.config import (
    SCALE_FACTOR, TWD_TO_KRW, REASON_GROUPS, 
    HIGH_RISK_THRESHOLD, EXPIRY_WINDOW_DAYS
)
from pages.action_board.data_layer import inject_churn_probability, get_shifted_raw_data
from pages.action_board.metrics import build_kpi_report, build_trend_data
from pages.simulator.data_layer import get_simulator_default_date

# ── 페이지 설정 ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="📊 통합 대시보드 | KKBOX",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 벚꽃 + 초록 봄 테마 CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');

:root {
    --sakura-50:  #FFF0F5;
    --sakura-100: #FFD6E7;
    --sakura-200: #FFB3D1;
    --sakura-400: #F472A8;
    --sakura-600: #C94E80;
    --sakura-800: #8B2255;
    --green-50:   #F0FAF0;
    --green-100:  #C8EDC0;
    --green-200:  #97D47F;
    --green-400:  #55A83A;
    --green-600:  #2E7D1A;
    --green-800:  #16500A;
}

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif !important;
}

/* 전체 배경 */
.stApp {
    background: linear-gradient(135deg, #FFF8FB 0%, #F6FBF4 100%) !important;
}

/* 사이드바 */
[data-testid="stSidebar"] {
    background: var(--sakura-50) !important;
    border-right: 1px solid var(--sakura-200) !important;
}
[data-testid="stSidebar"] * {
    color: var(--sakura-800) !important;
}
[data-testid="stSidebar"] .stDateInput > div > div {
    border-color: var(--sakura-200) !important;
}

/* 타이틀 */
h1 {
    font-size: 2rem !important;
    color: var(--sakura-800) !important;
    border-bottom: 3px solid;
    border-image: linear-gradient(90deg, #FFB3D1, #F472A8, #55A83A, #97D47F) 1;
    padding-bottom: 0.4rem;
}

/* 서브헤더 */
h2 {
    color: var(--green-800) !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
}

/* h3 섹션 타이틀 */
h3 {
    color: var(--green-800) !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
}

/* 구분선 */
hr, [data-testid="stDivider"] {
    border: none !important;
    height: 2px !important;
    background: linear-gradient(90deg, var(--sakura-200), var(--sakura-400), var(--green-400), var(--green-200)) !important;
    margin: 0.75rem 0 1.25rem !important;
    opacity: 1 !important;
}

/* KPI 메트릭 카드 */
[data-testid="stMetric"] {
    background: white !important;
    border: 0.5px solid var(--sakura-100) !important;
    border-radius: 14px !important;
    padding: 1.1rem 1.25rem !important;
    box-shadow: 0 2px 12px rgba(244, 114, 168, 0.07) !important;
    transition: box-shadow 0.15s;
}
[data-testid="stMetric"]:hover {
    box-shadow: 0 4px 18px rgba(244, 114, 168, 0.14) !important;
}
[data-testid="stMetric"] label {
    color: var(--sakura-600) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--sakura-800) !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
}
[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
}

/* info 박스 */
[data-testid="stAlert"][data-type="info"] {
    background: var(--sakura-50) !important;
    border-left: 4px solid var(--sakura-400) !important;
    border-radius: 12px !important;
    color: var(--sakura-800) !important;
}
[data-testid="stAlert"][data-type="info"] p,
[data-testid="stAlert"][data-type="info"] li {
    color: var(--sakura-800) !important;
}

/* success 박스 */
[data-testid="stAlert"][data-type="success"] {
    background: var(--green-50) !important;
    border-left: 4px solid var(--green-400) !important;
    border-radius: 12px !important;
}
[data-testid="stAlert"][data-type="success"] p {
    color: var(--green-800) !important;
}

/* warning 박스 */
[data-testid="stAlert"][data-type="warning"] {
    border-radius: 12px !important;
}

/* Plotly 차트 컨테이너 */
[data-testid="stPlotlyChart"] {
    background: white !important;
    border: 0.5px solid var(--sakura-100) !important;
    border-radius: 14px !important;
    padding: 0.5rem !important;
    box-shadow: 0 2px 12px rgba(244, 114, 168, 0.05) !important;
}

/* 스피너 */
[data-testid="stSpinner"] {
    color: var(--sakura-400) !important;
}

/* date_input */
[data-testid="stDateInput"] input {
    border-color: var(--sakura-200) !important;
    border-radius: 9px !important;
    background: white !important;
}
[data-testid="stDateInput"] input:focus {
    border-color: var(--sakura-400) !important;
    box-shadow: 0 0 0 3px rgba(244,114,168,0.15) !important;
}

/* 상단 헤더 및 메뉴 숨기기 (배경과 일체화) */
header[data-testid="stHeader"] {
    background: transparent !important;
}
[data-testid="stDeploymentButton"], 
[data-testid="stMainMenu"] {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ── 데이터 로드 (캐싱) ────────────────────────────────────────────────────────
@st.cache_resource
def get_model():
    """
    ML 모델 로더. 현재는 None 반환(더미 모드).
    팀원에게 pkl 받으면:
      import joblib
      return joblib.load("models/champion_model.pkl")
    """
    return None


@st.cache_data
def get_transactions() -> "pd.DataFrame":
    raw = get_shifted_raw_data()
    model = get_model()
    return inject_churn_probability(raw["transactions"], model=model)


transactions = get_transactions()


# ── 사이드바 ──────────────────────────────────────────────────────────────────
if "virtual_today" not in st.session_state:
    st.session_state.virtual_today = get_simulator_default_date()

with st.sidebar:
    st.markdown("### 📅 시뮬레이션 설정")
    st.date_input(
        "분석 기준일 (Virtual Today)",
        key="virtual_today",
        min_value=datetime(2010, 1, 1).date(),
        max_value=datetime(2030, 12, 31).date(),
    )
    
    virtual_today = datetime.combine(st.session_state.virtual_today, datetime.min.time())

    st.markdown("---")


# ── KPI 계산 ──────────────────────────────────────────────────────────────────
report   = build_kpi_report(transactions, virtual_today)
trend_df = build_trend_data(transactions, virtual_today)


# ── 헤더 ──────────────────────────────────────────────────────────────────────
st.title("🌸 이탈 방어 시스템")
st.subheader("이탈 방어 모니터링")
st.markdown("<hr>", unsafe_allow_html=True)


# ── KPI 카드 ──────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🚨 고위험 유저",
        f"{report.today.high_risk_users:,}명",
        f"{report.user_delta:+,}명",
        delta_color="inverse",
        help=f"구독 만료일이 {EXPIRY_WINDOW_DAYS}일 이내로 남았으며, 이탈 확률이 {int(HIGH_RISK_THRESHOLD*100)}% 이상으로 예측된 유저입니다."
    )

with col2:
    st.metric(
        "💸 매출 위기 총액",
        f"{report.today.revenue_at_risk:,.0f}원",
        f"{report.revenue_delta:+,.0f}원",
        delta_color="inverse",
        help="방어 성공 유저의 매출을 제외한 실질적 매출 위기 금액입니다."
    )

with col3:
    # 방어 성공 금액을 퍼센트 옆에 병기하거나 델타 영역에 표시
    st.metric(
        "🛡️ 이탈 방어 성공률",
        f"{report.today.defense_rate:.1f}%",
        f"+{report.today.defended_revenue:,.0f}원 방어 (전일대비 {report.defense_rate_delta:+.1f}%p)",
        delta_color="normal",
    )

st.markdown("<hr>", unsafe_allow_html=True)


# ── 차트 ──────────────────────────────────────────────────────────────────────
chart_col, pie_col = st.columns(2)

with chart_col:
    st.write("### 📈 최근 7일간 이탈 위험 추이")
    fig_line = px.line(
        trend_df,
        x="날짜",
        y=["고위험 유저", "방어 성공 유저"],
        color_discrete_map={
            "고위험 유저":   "#F472A8",   # 벚꽃 핑크
            "방어 성공 유저": "#55A83A",  # 새싹 그린
        },
        markers=True,
        template="plotly_white",
    )
    fig_line.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Noto Sans KR", color="#8B2255"),
    )
    fig_line.update_traces(line=dict(width=2.5), marker=dict(size=7))
    st.plotly_chart(fig_line, use_container_width=True)

with pie_col:
    st.write("### 🔍 이탈 주원인 분석")

    if "main_reason_code" in transactions.columns:
        # 세부 사유를 5대 카테고리로 매핑하여 그룹화 (차트 터짐 방지)
        def map_to_group(reason):
            for group, members in REASON_GROUPS.items():
                if reason in members:
                    return group
            return "❓ 기타"

        reason_series = transactions["main_reason_code"].fillna("기타/복합").astype(str)
        grouped_counts = reason_series.apply(map_to_group).value_counts().reset_index()
        grouped_counts.columns = ["이탈 카테고리", "유저 수"]

        fig_donut = px.pie(
            grouped_counts,
            values="유저 수",
            names="이탈 카테고리",
            hole=0.4,
            # 벚꽃 핑크 ~ 초록 봄 컬러 팔레트
            color_discrete_sequence=px.colors.qualitative.Pastel,
            template="plotly_white",
        )
        fig_donut.update_layout(
            height=400,
            margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor="white",
            font=dict(family="Noto Sans KR", color="#8B2255"),
        )
        st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ── 운영 요약 ─────────────────────────────────────────────────────────────────
st.write("### 🔔 모니터링 요약")

if "main_reason_code" in transactions.columns and transactions["main_reason_code"].notna().any():
    top_reason = transactions["main_reason_code"].fillna("기타").mode().iloc[0]
else:
    top_reason = "원인 데이터 없음"

st.info(f"""
⚖️ **{virtual_today.strftime('%Y-%m-%d')} 기준 운영 리포트**

- **모니터링 대상**: 감지된 고위험 유저 **{report.today.high_risk_users:,}명** (전일 대비 {report.user_delta:+,}명)
- **방어 성과**: 머신러닝 기반 이탈 방어 성공률 **{report.today.defense_rate:.1f}%** 기록 (전일 대비 {report.defense_rate_delta:+.1f}%p)
- **핵심 인사이트**: 현재 고위험군 내에서 **『{top_reason}』** 비중이 가장 두드러집니다. 해당 유저층을 타겟으로 한 정밀 리텐션 액션(쿠폰/프로모션) 수행을 권장합니다.
""")
