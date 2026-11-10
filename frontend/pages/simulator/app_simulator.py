import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from pages.simulator.config import (
    COLOR_GROUP_A, COLOR_GROUP_B, COLOR_GRAY,
    DEFAULT_A_TARGET_COUNT, FILTER_OPTIONS_B,
    A_PRICE_SENSITIVITY_K, A_MAX_RETENTION_CAP,
    B_BASE_RETENTION, B_LOYALTY_SCALE, B_MAX_RETENTION_CAP,
    MONTHLY_CHURN_DECAY, B_FREE_EXTENSION_MONTHS,
)
from pages.simulator.data_layer import (
    get_real_sim_data,
    calculate_retention_rates,
    calculate_roi_data,
    calc_individual_retention_a,
    calc_individual_retention_b,
    get_simulator_default_date,
)
from pages.action_board.config import TWD_TO_KRW

# ── 페이지 설정 ──
st.set_page_config(page_title="마케팅 성과 시뮬레이터 🌸", layout="wide")

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');

:root {
    --sk-50:  #FFF0F5;
    --sk-100: #FFD6E7;
    --sk-200: #FFB3D1;
    --sk-400: #F472A8;
    --sk-600: #C94E80;
    --sk-800: #8B2255;
    --gn-50:  #F0FAF0;
    --gn-100: #C8EDC0;
    --gn-200: #97D47F;
    --gn-400: #55A83A;
    --gn-600: #2E7D1A;
    --gn-800: #16500A;
    --radius: 14px;
    --shadow-pink:  0 4px 18px rgba(244,114,168,0.10);
    --shadow-green: 0 4px 18px rgba(85,168,58,0.10);
}

html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif !important; }
.stApp { background: linear-gradient(150deg, #FFF8FB 0%, #F6FBF4 100%) !important; }
header[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stDeploymentButton"],
[data-testid="stMainMenu"] { visibility: hidden; }
h1, h2, h3, h4 { margin-top: 0 !important; }

[data-testid="stSidebar"] {
    background: var(--sk-50) !important;
    border-right: 1.5px solid var(--sk-200) !important;
}
[data-testid="stSidebar"] * { color: var(--sk-800) !important; }

.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: white;
    border: 1px solid var(--sk-100);
    border-left: 5px solid var(--sk-400);
    border-radius: var(--radius);
    padding: 1rem 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow-pink);
}
.page-header-title { font-size: 1.45rem; font-weight: 700; color: var(--sk-800); margin: 0; }
.page-header-sub   { font-size: 0.78rem; color: var(--sk-600); margin-top: 0.2rem; }
.page-header-badge {
    font-size: 0.75rem; font-weight: 600;
    background: var(--sk-100); color: var(--sk-800);
    border: 1px solid var(--sk-200); border-radius: 20px;
    padding: 5px 14px; white-space: nowrap;
}

.section-title {
    font-size: 0.85rem; font-weight: 700;
    letter-spacing: 0.07em; text-transform: uppercase;
    color: var(--sk-600);
    border-left: 3px solid var(--sk-400);
    padding-left: 0.6rem; margin: 0 0 1rem 0;
}

.divider {
    height: 2px;
    background: linear-gradient(90deg, var(--sk-200), var(--sk-400), var(--gn-400), var(--gn-200));
    border: none; border-radius: 2px;
    margin: 1.75rem 0; opacity: 1;
}

/* 수식 설명 박스 */
.formula-box {
    background: #FAFAFA;
    border: 1px solid #EEE;
    border-left: 4px solid var(--sk-400);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin: 0.75rem 0 1rem 0;
    font-size: 0.82rem;
    color: #444;
    line-height: 1.7;
}
.formula-box.green { border-left-color: var(--gn-400); }
.formula-box code {
    background: var(--sk-50);
    border-radius: 4px;
    padding: 1px 5px;
    font-family: 'Courier New', monospace;
    font-size: 0.83rem;
    color: var(--sk-800);
}
.formula-box.green code { background: var(--gn-50); color: var(--gn-800); }

div[data-testid="stVerticalBlock"]:has(> div.card-pink) {
    background: white;
    border: 1px solid var(--sk-100);
    border-top: 4px solid var(--sk-400);
    border-radius: var(--radius);
    padding: 1rem 1.5rem 1.5rem;
    box-shadow: var(--shadow-pink);
}
div[data-testid="stVerticalBlock"]:has(> div.card-green) {
    background: white;
    border: 1px solid var(--gn-100);
    border-top: 4px solid var(--gn-400);
    border-radius: var(--radius);
    padding: 1rem 1.5rem 1.5rem;
    box-shadow: var(--shadow-green);
}

.card-chip {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.05em; padding: 4px 12px; border-radius: 20px;
    margin-bottom: 1rem;
}
.card-chip.pink  { background: var(--sk-100); color: var(--sk-800); border: 1px solid var(--sk-200); }
.card-chip.green { background: var(--gn-100); color: var(--gn-800); border: 1px solid var(--gn-200); }

.target-auto-badge {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.55rem 1rem; border-radius: 10px;
    font-size: 0.83rem; margin-bottom: 0.9rem;
}
.target-auto-badge.pink  { background: var(--sk-50);  border: 1px solid var(--sk-200); color: var(--sk-800); }
.target-auto-badge.green { background: var(--gn-50); border: 1px solid var(--gn-200); color: var(--gn-800); }
.target-auto-badge span.label { font-weight: 500; }
.target-auto-badge span.value { font-weight: 700; font-size: 1rem; }

.rate-badge {
    display: flex; align-items: center; gap: 8px;
    padding: 0.65rem 1rem; border-radius: 10px;
    font-size: 0.83rem; font-weight: 600;
    margin-top: 0.9rem; margin-bottom: 0;
}
.rate-badge.pink  { background: var(--sk-50);  border: 1px solid var(--sk-200); color: var(--sk-800); }
.rate-badge.green { background: var(--gn-50); border: 1px solid var(--gn-200); color: var(--gn-800); }

.expander-spacer { margin-top: 1.5rem; }

[data-testid="stExpander"] {
    background: white !important;
    border: 1px solid var(--sk-100) !important;
    border-left: 3px solid var(--sk-200) !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary { font-size: 0.85rem !important; font-weight: 500 !important; color: var(--sk-800) !important; }

[data-testid="stSlider"] > div > div > div { background: transparent !important; }
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: var(--sk-400) !important;
    border-color: var(--sk-400) !important;
}
div[data-testid="stSliderValue"] {
    color: var(--sk-800) !important;
    font-size: 0.85rem !important; font-weight: 700 !important;
    background: var(--sk-100) !important;
    border: 1px solid var(--sk-200) !important;
    border-radius: 8px !important;
    padding: 2px 10px !important; margin-bottom: 6px !important;
    visibility: visible !important; opacity: 1 !important; display: inline-block !important;
}
[data-testid="stSlider"] label p { color: var(--sk-800) !important; font-weight: 600 !important; font-size: 0.88rem !important; }

[data-testid="stSelectbox"] > div > div { border-color: var(--gn-200) !important; border-radius: 9px !important; }
[data-testid="stRadio"] label { color: var(--sk-800) !important; font-size: 0.85rem !important; }

[data-testid="stMetric"] {
    background: white !important;
    border: 1px solid var(--sk-100) !important;
    border-top: 3px solid var(--sk-400) !important;
    border-radius: var(--radius) !important;
    padding: 1.1rem 1rem !important;
    box-shadow: var(--shadow-pink) !important;
    text-align: center !important;
    transition: transform 0.15s, box-shadow 0.15s;
}
[data-testid="stMetric"]:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(244,114,168,0.15) !important; }
[data-testid="stMetricLabel"] { font-size: 0.8rem !important; color: var(--sk-600) !important; font-weight: 500 !important; justify-content: center !important; }
[data-testid="stMetricValue"] { font-size: 1.65rem !important; color: var(--sk-800) !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"] { justify-content: center !important; }

[data-testid="stDataFrame"] { border: 1px solid var(--sk-100) !important; border-radius: 10px !important; overflow: hidden; box-shadow: 0 2px 8px rgba(244,114,168,0.04) !important; }
[data-testid="stDataFrame"] th { background: var(--sk-50) !important; color: var(--sk-800) !important; font-size: 12px !important; }

[data-testid="stPlotlyChart"] {
    background: white !important;
    border: 1px solid var(--sk-100) !important;
    border-radius: var(--radius) !important;
    padding: 0.75rem !important;
    box-shadow: var(--shadow-pink) !important;
}

[data-testid="stAlert"] { border-radius: 12px !important; }
[data-testid="stAlert"][data-type="info"]    { background: var(--sk-50) !important; border-left: 4px solid var(--sk-400) !important; }
[data-testid="stAlert"][data-type="info"] p  { color: var(--sk-800) !important; }
[data-testid="stAlert"][data-type="success"] { background: var(--gn-50) !important; border-left: 4px solid var(--gn-400) !important; }
[data-testid="stAlert"][data-type="success"] p { color: var(--gn-800) !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════
# 0. 사이드바 & 데이터 로드
# ══════════════════════════════════════════
if "virtual_today" not in st.session_state:
    st.session_state.virtual_today = get_simulator_default_date()

with st.sidebar:
    st.markdown("### 📅 시뮬레이션 설정")
    st.date_input("분석 기준일", key="virtual_today")
    virtual_today = datetime.combine(st.session_state.virtual_today, datetime.min.time())
    st.markdown("---")

with st.spinner("🌸 실제 고객 데이터 분석 중..."):
    sim_df = get_real_sim_data(virtual_today)
    if sim_df.empty:
        st.error("데이터 분석 실패: 조건에 맞는 고객을 찾을 수 없습니다.")
        st.stop()

total_pool_size = len(sim_df)


# ══════════════════════════════════════════
# 헤더 배너
# ══════════════════════════════════════════
st.markdown(f"""
<div class="page-header">
  <div>
    <div class="page-header-title">📈 마케팅 성과 시뮬레이터</div>
    <div class="page-header-sub">실제 고객 데이터 기반 · 캠페인 전략별 이탈 방어율 비교 분석</div>
  </div>
  <div class="page-header-badge">👥 총 분석 대상 {total_pool_size:,}명</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════
# 1. 캠페인 그룹 설정
# ══════════════════════════════════════════
st.markdown('<p class="section-title">① 캠페인 그룹 설정</p>', unsafe_allow_html=True)

col_a, col_b = st.columns(2, gap="large")

_filter_default_idx = 2
_filter_default     = FILTER_OPTIONS_B[_filter_default_idx]

if "filter_b" not in st.session_state:
    st.session_state.filter_b = _filter_default

_months_limit  = int(st.session_state.filter_b.split("개월")[0])
target_b_df    = sim_df[sim_df["membership_duration_months"] >= _months_limit]
target_b_count = len(target_b_df)
target_a_count = max(total_pool_size - target_b_count, 0)

# ── Group A 카드 ──
with col_a:
    with st.container():
        st.markdown('<div class="card-pink"></div>', unsafe_allow_html=True)
        st.markdown('<span class="card-chip pink">🅰️ GROUP A &nbsp;·&nbsp; 할인 쿠폰</span>', unsafe_allow_html=True)

        st.markdown(
            f'<div class="target-auto-badge pink">'
            f'<span class="label">🎯 타겟 유저 수 (자동)</span>'
            f'<span class="value">{target_a_count:,}명</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        discount_rate = st.slider(
            "할인율 (%)", 0, 100, 50, step=5, key="d_a", format="%d%%",
            help=f"가격 탄력성 모델(k={A_PRICE_SENSITIVITY_K})에 따라 할인율이 높을수록 이탈 억제 효과가 지수적으로 증가합니다."
        )
        ret_a, ret_b  = calculate_retention_rates(discount_rate, sim_df, target_b_df)

        st.markdown(
            f'<div class="rate-badge pink">💡 예상 방어 성공률 &nbsp;<strong>{ret_a*100:.1f}%</strong></div>',
            unsafe_allow_html=True,
        )

# ── Group B 카드 ──
with col_b:
    with st.container():
        st.markdown('<div class="card-green"></div>', unsafe_allow_html=True)
        st.markdown('<span class="card-chip green">🅱️ GROUP B &nbsp;·&nbsp; 무료 연장</span>', unsafe_allow_html=True)

        filter_option = st.selectbox(
            "타겟 필터링 조건",
            options=FILTER_OPTIONS_B,
            index=_filter_default_idx,
            key="filter_b",
        )
        months_limit   = int(filter_option.split("개월")[0])
        target_b_df    = sim_df[sim_df["membership_duration_months"] >= months_limit]
        target_b_count = len(target_b_df)
        target_a_count = max(total_pool_size - target_b_count, 0)

        # ret_b 재계산 (B 필터 변경 반영)
        _, ret_b = calculate_retention_rates(discount_rate, sim_df, target_b_df)

        st.markdown(
            f'<div class="target-auto-badge green">'
            f'<span class="label">🎯 필터링된 타겟</span>'
            f'<span class="value">{target_b_count:,}명</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="rate-badge green">💡 예상 방어 성공률 &nbsp;<strong>{ret_b*100:.1f}%</strong></div>',
            unsafe_allow_html=True,
        )


# ── 방어율 분포 시각화 ──
st.markdown('<div class="expander-spacer"></div>', unsafe_allow_html=True)

with st.expander("📊 개인별 방어율 분포 보기", expanded=False):
    dist_col_a, dist_col_b = st.columns(2)

    with dist_col_a:
        st.markdown("**Group A — 할인율별 방어율 커브**")
        # 할인율 0~100 커브
        x_disc = np.linspace(0, 100, 200)
        avg_churn = sim_df["churn_probability"].mean() if not sim_df.empty else 0.72
        y_curve  = [calc_individual_retention_a(avg_churn, d) * 100 for d in x_disc]
        current_ret = calc_individual_retention_a(avg_churn, discount_rate) * 100

        fig_a = go.Figure()
        fig_a.add_trace(go.Scatter(
            x=x_disc, y=y_curve,
            mode="lines", line=dict(color="#F472A8", width=2.5),
            name="방어율 커브"
        ))
        fig_a.add_trace(go.Scatter(
            x=[discount_rate], y=[current_ret],
            mode="markers", marker=dict(color="#8B2255", size=10),
            name=f"현재 ({discount_rate}%→{current_ret:.1f}%)"
        ))
        fig_a.update_layout(
            height=240, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Noto Sans KR", size=11, color="#8B2255"),
            xaxis=dict(title="할인율 (%)", showgrid=True, gridcolor="#F5F0F3"),
            yaxis=dict(title="방어율 (%)", range=[0, 100], showgrid=True, gridcolor="#F5F0F3"),
            legend=dict(font=dict(size=10)), margin=dict(t=10, b=10, l=10, r=10),
        )
        st.plotly_chart(fig_a, use_container_width=True)

    with dist_col_b:
        st.markdown("**Group B — 가입 기간별 방어율 커브**")
        x_months = np.linspace(1, 12, 200)
        y_b_curve = [calc_individual_retention_b(m) * 100 for m in x_months]

        fig_b = go.Figure()
        fig_b.add_trace(go.Scatter(
            x=x_months, y=y_b_curve,
            mode="lines", line=dict(color="#55A83A", width=2.5),
            name="방어율 커브"
        ))
        if not target_b_df.empty:
            avg_dur = target_b_df["membership_duration_months"].mean()
            avg_ret = calc_individual_retention_b(avg_dur) * 100
            fig_b.add_trace(go.Scatter(
                x=[avg_dur], y=[avg_ret],
                mode="markers", marker=dict(color="#16500A", size=10),
                name=f"그룹 평균 ({avg_dur:.1f}개월→{avg_ret:.1f}%)"
            ))
        fig_b.update_layout(
            height=240, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Noto Sans KR", size=11, color="#2E7D1A"),
            xaxis=dict(title="가입 기간 (개월)", showgrid=True, gridcolor="#F0FAF0"),
            yaxis=dict(title="방어율 (%)", range=[0, 80], showgrid=True, gridcolor="#F0FAF0"),
            legend=dict(font=dict(size=10)), margin=dict(t=10, b=10, l=10, r=10),
        )
        st.plotly_chart(fig_b, use_container_width=True)

with st.expander("🔍 시뮬레이션 대상 데이터 미리보기", expanded=False):
    group_view = st.radio("그룹 선택", ["할인 쿠폰군 (A)", "무료 연장군 (B)"], horizontal=True)
    view_df = (
        sim_df.sort_values("churn_probability", ascending=False).head(target_a_count)
        if group_view == "할인 쿠폰군 (A)" else target_b_df
    )
    display_df = view_df[["user_id", "churn_probability", "membership_duration_months"]].copy()
    display_df["user_id"] = display_df["user_id"].apply(
        lambda x: x[:10] + ".." if isinstance(x, str) else x
    )
    # 개인별 방어율 컬럼 추가
    if group_view == "할인 쿠폰군 (A)":
        display_df["예상 방어율"] = display_df["churn_probability"].apply(
            lambda p: f"{calc_individual_retention_a(p, discount_rate)*100:.1f}%"
        )
    else:
        display_df["예상 방어율"] = display_df["membership_duration_months"].apply(
            lambda m: f"{calc_individual_retention_b(m)*100:.1f}%"
        )
    st.dataframe(display_df.head(100), height=230, use_container_width=True)


# ══════════════════════════════════════════
# 2. KPI 요약
# ══════════════════════════════════════════
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<p class="section-title">② 성과 예측 요약</p>', unsafe_allow_html=True)

avg_price = sim_df["plan_list_price"].mean() if not sim_df.empty else 149
roi_df, total_rev_a, total_rev_b, dist_a, dist_b = calculate_roi_data(
    target_a_count, target_b_count, ret_a, ret_b, discount_rate, avg_price, sim_df, target_b_df
)
# 데이터 안정성 확보 (NaN 방지)
roi_df = roi_df.fillna(0)
total_rev_a = 0 if np.isnan(total_rev_a) else total_rev_a
total_rev_b = 0 if np.isnan(total_rev_b) else total_rev_b
better_group = "A" if total_rev_a > total_rev_b else "B"
diff_rev     = abs(total_rev_a - total_rev_b)

# 방어 성공 인원수
success_a = int(target_a_count * ret_a)
success_b = int(target_b_count * ret_b)

# 금융 지표 계산
total_profit = total_rev_a + total_rev_b
cost_a = (target_a_count * ret_a) * (avg_price * (discount_rate/100)) * TWD_TO_KRW
cost_b = (target_b_count * ret_b) * (avg_price * B_FREE_EXTENSION_MONTHS) * TWD_TO_KRW
total_cost = cost_a + cost_b

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric(
        "🌸 Group A 방어 성공률", 
        f"{ret_a*100:.1f}%", 
        f"≈ {success_a:,}명 방어",
        help=f"가격 탄력성 모델: 1 - churn_prob * exp(-{A_PRICE_SENSITIVITY_K} * d). 상한 {A_MAX_RETENTION_CAP*100:.0f}%"
    )
with kpi2:
    st.metric(
        "🌿 Group B 방어 성공률", 
        f"{ret_b*100:.1f}%", 
        f"≈ {success_b:,}명 방어",
        help=f"로열티 가중 모델: {B_BASE_RETENTION} * (1 + ln(1+m) / {B_LOYALTY_SCALE}). 상한 {B_MAX_RETENTION_CAP*100:.0f}%"
    )
with kpi3:
    st.metric("💰 수익 우위 그룹", f"Group {better_group}", f"{diff_rev:+,.0f}원")
with kpi4:
    st.metric("🌈 총 예상 수익 (3Mo)", f"{total_profit:,.0f}원", help="A그룹과 B그룹의 3개월 누적 예상 매출 합계입니다.")

# 수익 및 비용 상세 열
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("💎 A그룹 예상 수익", f"{total_rev_a:,.0f}원")
with c2:
    st.metric("💎 B그룹 예상 수익", f"{total_rev_b:,.0f}원")
with c3:
    st.metric("🎟️ A 쿠폰 할인액", f"-{cost_a:,.0f}원", delta_color="inverse")
with c4:
    st.metric("🎫 B 무료연장 비용", f"-{cost_b:,.0f}원", delta_color="inverse")


# ══════════════════════════════════════════
# 3. 수익 차트 + 월별 잔존 유저 추이
# ══════════════════════════════════════════
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    f'<p class="section-title">③ 3개월 누적 수익 추이 &nbsp;'
    f'<span style="font-weight:400;font-size:0.75rem;color:#C94E80">'
    f'{virtual_today.strftime("%Y-%m-%d")} 기준</span></p>',
    unsafe_allow_html=True,
)

chart_col1, chart_col2 = st.columns([3, 2])

with chart_col1:
    fig_rev = px.bar(
        roi_df,
        x="경과 월", y="예상 매출액", color="그룹",
        barmode="group",
        text="예상 매출액",
        color_discrete_map={"할인 쿠폰군 (A)": "#F472A8", "무료 연장군 (B)": "#55A83A"},
    )
    # 막대 위 숫자가 잘리지 않도록 Y축 상단 마진 확보
    max_val = roi_df["예상 매출액"].max() if not roi_df.empty else 100
    
    fig_rev.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="auto", # 막대 크기에 따라 내부/외부 자동 결정
        marker_line_width=0,
        textfont=dict(size=10, color="#8B2255"),
        cliponaxis=False # 축 밖으로 나가도 숫자 표시
    )
    fig_rev.update_layout(
        height=380,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Noto Sans KR", size=11, color="#8B2255"),
        title_text="", # 'undefined' 방지
        legend=dict(
            orientation="h", 
            yanchor="bottom", y=1.05, 
            xanchor="right", x=1, 
            title_text="", # 범례 타이틀 제거하여 공간 확보
            font=dict(size=11)
        ),
        margin=dict(t=70, b=60, l=20, r=20), # 하단 마진 확대하여 '개월 후' 표시 보장
        xaxis=dict(title=None, showgrid=False, tickangle=0),
        yaxis=dict(
            title=None, showgrid=True, gridcolor="#F5F0F3", 
            showticklabels=False,
            range=[0, max_val * 1.3] # 상단 여백 추가 확보
        ),
        bargap=0.28, bargroupgap=0.08,
    )
    st.plotly_chart(fig_rev, use_container_width=True)

with chart_col2:
    # 월별 잔존 유저 추이 (감가 시각화)
    months = [1, 2, 3]
    decay = 1 - MONTHLY_CHURN_DECAY
    surv_a = [int(success_a * (decay ** (m-1))) for m in months]
    surv_b = [int(success_b * (decay ** (m-1))) for m in months]

    fig_surv = go.Figure()
    fig_surv.add_trace(go.Scatter(
        x=["1개월", "2개월", "3개월"], y=surv_a,
        mode="lines+markers+text",
        name="Group A",
        line=dict(color="#F472A8", width=2),
        marker=dict(size=8),
        text=[f"{v:,}" for v in surv_a],
        textposition="top center",
        textfont=dict(size=10, color="#8B2255"),
    ))
    fig_surv.add_trace(go.Scatter(
        x=["1개월", "2개월", "3개월"], y=surv_b,
        mode="lines+markers+text",
        name="Group B",
        line=dict(color="#55A83A", width=2),
        marker=dict(size=8),
        text=[f"{v:,}" for v in surv_b],
        textposition="bottom center",
        textfont=dict(size=10, color="#2E7D1A"),
    ))
    fig_surv.update_layout(
        height=380,
        title=dict(
            text="월별 잔존 유저 추이", 
            font=dict(size=13, color="#8B2255"),
            x=0, y=0.95
        ),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Noto Sans KR", size=11),
        legend=dict(
            orientation="h", 
            yanchor="bottom", y=1.02, 
            xanchor="right", x=1,
            title_text=""
        ),
        margin=dict(t=70, b=60, l=50, r=20), # 좌측 마진 확대하여 '잔존 유저수' 레이블 공간 확보
        xaxis=dict(showgrid=False, tickfont=dict(size=11)),
        yaxis=dict(title="잔존 유저 수", showgrid=True, gridcolor="#F5F0F3", tickfont=dict(size=11)),
    )
    st.plotly_chart(fig_surv, use_container_width=True)


# ══════════════════════════════════════════
# 4. 종합 결론
# ══════════════════════════════════════════
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<p class="section-title">④ 종합 결론</p>', unsafe_allow_html=True)

if better_group == "A":
    st.success(
        f"🟢 **최종 분석**: **할인 쿠폰군(A)** 이 캠페인 초기 매출 회수가 빠르며, "
        f"3개월 누적 수익이 무료 연장군(B) 대비 약 **{diff_rev:,.0f}원** 더 높게 예측됩니다.\n\n"
        "👉 **단기 수익 최적화 전략**으로 본 캠페인을 추천합니다."
    )
else:
    st.info(
        f"🔵 **최종 분석**: **무료 연장군(B)** 이 첫 달 매출 공백이 있으나, "
        f"고객 유지 효과로 3개월 누적 수익이 할인 쿠폰군(A)보다 약 **{diff_rev:,.0f}원** 더 유리합니다.\n\n"
        "👉 **장기 LTV(고객 생애 가치) 극대화 전략**으로 본 캠페인을 추천합니다."
    )

st.caption(
    f"※ 본 시뮬레이션은 실제 고객 {total_pool_size:,}명을 기반으로 계산되었으며, "
    f"환율 1 TWD = {TWD_TO_KRW}원이 적용되었습니다. "
    f"월별 감가율 {MONTHLY_CHURN_DECAY*100:.0f}% 적용."
)
