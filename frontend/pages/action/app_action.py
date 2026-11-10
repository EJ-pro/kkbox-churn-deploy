import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from pandas.io.formats.style import Styler
from datetime import datetime, timedelta
import base64
import os

# ── 페이지 설정 ──
st.set_page_config(page_title="고위험군 액션 보드", layout="wide")

# ── 봄 테마 CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=JetBrains+Mono:wght@400&display=swap');

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
    --row-odd:    #FFFFFF;
    --row-even:   #FFF8FC;
    --row-high:   #FFF0F3;
    --row-mid:    #FFFBF0;
    --row-low:    #F4FBF4;
}

html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif !important; }

.stApp { background: linear-gradient(135deg, #FFF8FB 0%, #F6FBF4 100%) !important; }

header[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stDeploymentButton"], [data-testid="stMainMenu"] { visibility: hidden; }

/* 사이드바 */
[data-testid="stSidebar"] {
    background: var(--sakura-50) !important;
    border-right: 1.5px solid var(--sakura-200) !important;
}
[data-testid="stSidebar"] * { color: var(--sakura-800) !important; }
[data-testid="stSidebar"] .stDateInput > div > div { border-color: var(--sakura-200) !important; }
[data-testid="stSidebar"] [data-testid="stNumberInput"] input {
    border-color: var(--sakura-200) !important; border-radius: 9px !important; background: white !important;
}

/* 타이틀 */
h1 {
    font-size: 2rem !important; color: var(--sakura-800) !important;
    border-bottom: 3px solid;
    border-image: linear-gradient(90deg, #FFB3D1, #F472A8, #55A83A, #97D47F) 1;
    padding-bottom: 0.4rem; margin-bottom: 0.2rem !important;
}
.stApp [data-testid="stCaptionContainer"] p {
    color: var(--sakura-600) !important; font-size: 0.82rem; margin-bottom: 0 !important;
}
h3 { color: var(--green-800) !important; font-size: 1rem !important; font-weight: 600 !important; margin-top: 0 !important; margin-bottom: 0.5rem !important; }
h4, h5 { color: var(--sakura-800) !important; font-size: 0.9rem !important; font-weight: 600 !important; margin-bottom: 0.4rem !important; }

/* 구분선 */
hr, [data-testid="stDivider"] {
    border: none !important; height: 2px !important;
    background: linear-gradient(90deg, var(--sakura-200), var(--sakura-400), var(--green-400), var(--green-200)) !important;
    margin: 1rem 0 !important; opacity: 1 !important;
}

/* expander */
[data-testid="stExpander"] {
    background: #FDFAFC !important;
    border: 1px solid var(--sakura-100) !important;
    border-left: 3px solid var(--sakura-200) !important;
    border-radius: 10px !important;
    margin-bottom: 6px !important;
    box-shadow: 0 2px 8px rgba(244,114,168,0.04) !important;
}
[data-testid="stExpander"] summary {
    font-size: 0.85rem !important; font-weight: 600 !important;
    color: var(--sakura-800) !important; padding: 0.5rem 0.75rem !important;
}
[data-testid="stExpander"] [data-testid="stVerticalBlock"] {
    gap: 0.35rem !important; padding: 0 0.5rem 0.5rem !important;
}

/* 멀티셀렉트 */
[data-testid="stMultiSelect"] > div { border-color: var(--sakura-200) !important; border-radius: 10px !important; background: white !important; }
[data-testid="stMultiSelect"] [data-baseweb="tag"] { background-color: var(--sakura-400) !important; border-radius: 20px !important; }
[data-testid="stMultiSelect"] [data-baseweb="tag"] span { color: white !important; }

/* Pills */
[data-testid="stPills"] button { border-radius: 20px !important; border: 1px solid var(--sakura-100) !important; background-color: white !important; transition: all 0.2s !important; font-size: 0.8rem !important; }
[data-testid="stPills"] button[aria-checked="true"] { background-color: var(--sakura-400) !important; color: white !important; border-color: var(--sakura-400) !important; box-shadow: 0 2px 8px rgba(244,114,168,0.3) !important; }

/* 토글 */
[data-testid="stCheckbox"] label p { font-size: 0.8rem !important; font-weight: 500 !important; color: var(--sakura-800) !important; padding-left: 0.4rem !important; }

/* 탭 */
[data-testid="stTabs"] [data-baseweb="tab-list"] { background: transparent !important; gap: 4px; border-bottom: 2px solid var(--sakura-100); }
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 10px 10px 0 0 !important; font-weight: 500 !important; font-size: 0.88rem !important;
    padding: 0.55rem 1.4rem !important; color: var(--sakura-600) !important;
    border: 1px solid var(--sakura-200) !important; border-bottom: none !important;
    background: white !important; transition: all 0.15s;
}
[data-testid="stTabs"] [aria-selected="true"] { background: var(--sakura-400) !important; color: white !important; border-color: var(--sakura-400) !important; }
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { background: var(--sakura-400) !important; height: 0 !important; }
[data-testid="stTabs"] [data-baseweb="tab-panel"] {
    background: #FDFBFC; border: 1px solid var(--sakura-200);
    border-top: none; border-radius: 0 0 14px 14px;
    padding: 1.25rem 1.5rem !important;
    box-shadow: inset 0 2px 8px rgba(244,114,168,0.03);
}

/* 버튼 */
.stButton > button {
    border-radius: 9px !important; font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 500 !important; font-size: 0.82rem !important; transition: all 0.15s !important;
    border: 1px solid var(--sakura-200) !important; background: white !important;
    color: var(--sakura-800) !important; padding: 0.35rem 0.85rem !important;
}
.stButton > button:hover { background: var(--sakura-50) !important; border-color: var(--sakura-400) !important; }
.stButton > button[kind="primary"] {
    background: var(--sakura-400) !important; border-color: var(--sakura-400) !important;
    color: white !important; font-size: 0.88rem !important; padding: 0.45rem 1.2rem !important;
}
.stButton > button[kind="primary"]:hover { background: var(--sakura-600) !important; border-color: var(--sakura-600) !important; }

/* ══════════════════════════════════════════
   데이터 에디터 — 풀 디자인
   ══════════════════════════════════════════ */
[data-testid="stDataEditor"] {
    border: 1px solid var(--sakura-200) !important;
    border-top: 3px solid var(--sakura-400) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 20px rgba(244,114,168,0.10) !important;
    /* 가로 스크롤 방지: 컨테이너가 탭 패널 너비를 꽉 채우도록 */
    width: 100% !important;
    max-width: 100% !important;
}
/* 헤더 배경 */
[data-testid="stDataEditor"] [data-testid="glideDataEditorContainer"] .dvn-scroller .ch {
    background: var(--sakura-50) !important;
    font-weight: 600 !important;
    color: var(--sakura-800) !important;
    font-size: 12px !important;
    border-bottom: 2px solid var(--sakura-200) !important;
}
/* 짝수 행 줄무늬 */
[data-testid="stDataEditor"] tr:nth-child(even) td { background: var(--row-even) !important; }
/* 호버 */
[data-testid="stDataEditor"] tr:hover td { background: var(--sakura-100) !important; transition: background 0.1s; }

/* 알림 박스 */
[data-testid="stAlert"][data-type="success"] { background: var(--green-50) !important; border-left: 4px solid var(--green-400) !important; border-radius: 10px !important; }
[data-testid="stAlert"][data-type="success"] p { color: var(--green-800) !important; }
[data-testid="stAlert"][data-type="info"] { background: var(--sakura-50) !important; border-left: 4px solid var(--sakura-400) !important; border-radius: 10px !important; }
[data-testid="stAlert"][data-type="info"] p { color: var(--sakura-800) !important; }
[data-testid="stAlert"][data-type="warning"] { border-radius: 10px !important; }

/* date_input */
[data-testid="stDateInput"] input { border-color: var(--sakura-200) !important; border-radius: 9px !important; background: white !important; }
[data-testid="stDateInput"] input:focus { border-color: var(--sakura-400) !important; box-shadow: 0 0 0 3px rgba(244,114,168,0.15) !important; }

/* 선택 뱃지 */
.sel-badge-pink {
    display: inline-block; background: var(--sakura-100); color: var(--sakura-800);
    border: 1px solid var(--sakura-200); border-radius: 20px;
    font-size: 0.78rem; font-weight: 600; padding: 3px 14px; margin-bottom: 8px;
}
.sel-badge-green {
    display: inline-block; background: var(--green-100); color: var(--green-800);
    border: 1px solid var(--green-200); border-radius: 20px;
    font-size: 0.78rem; font-weight: 600; padding: 3px 14px; margin-bottom: 8px;
}

[data-testid="stSpinner"] { color: var(--sakura-400) !important; }

@keyframes sakura-fall {
    0%   { transform: translateY(0) rotate(0deg) translateX(0); opacity: 0.8; }
    100% { transform: translateY(110vh) rotate(720deg) translateX(100px); opacity: 0; }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 임포트
# ==========================================
from pages.action_board.data_layer import get_shifted_raw_data, inject_churn_probability
from pages.simulator.data_layer import get_simulator_default_date
from pages.action_board.config import HIGH_RISK_THRESHOLD, EXPIRY_WINDOW_DAYS, REASON_GROUPS

CATEGORY_ACTIONS = {
    "💳 결제 및 구독": {"vvip": "💳 프리미엄 구독 할인권 발송",    "general": "💳 멤버십 결제 수단 혜택 전송",   "msg": "💳 {len_sel}명에게 결제 혜택 쿠폰이 발송되었습니다!"},
    "🔥 활동 및 참여": {"vvip": "🔥 VVIP 전용 럭키박스(7일권) 발송","general": "🚀 리텐션 유도 무료 감상권 발송",   "msg": "🔥 {len_sel}명에게 리텐션 이용권이 발송되었습니다!"},
    "🎧 이용 습관":   {"vvip": "🎶 맞춤형 최애곡 앨범 제작 알림",  "general": "🎧 당신을 위한 신규 추천 곡 발송", "msg": "🎧 {len_sel}명에게 음악 큐레이션 알림을 발송했습니다!"},
    "👤 유저 프로필": {"vvip": "👤 충성 고객 우대 멤버십 상향 안내","general": "👤 지역별 특별 프로모션 가입 안내", "msg": "👤 {len_sel}명에게 멤버십 혜택을 안내했습니다!"},
    "❓ 기타":        {"vvip": "📩 1:1 VIP 전담 상담 매칭 안내",   "general": "💬 고객 만족도 조사 및 건의 접수","msg": "❓ {len_sel}명에게 맞춤 케어 설문을 요청했습니다!"},
    "default":        {"vvip": "💎 프리미엄 리텐션 쿠폰 발송",      "general": "🌱 재참여 유도 메시지 발송",      "msg": "🌸 {len_sel}명에게 마케팅 메시지가 발송되었습니다!"},
}

TWD_TO_KRW = 42
RISK_GRADES = ["높음", "보통", "낮음"]


# ── 데이터 함수 ──
@st.cache_data
def get_real_action_data(virtual_today: pd.Timestamp) -> pd.DataFrame:
    raw = get_shifted_raw_data()
    df  = inject_churn_probability(raw["transactions"]).copy()
    virtual_today = pd.Timestamp(virtual_today).normalize()
    df["membership_expire_date"] = pd.to_datetime(df["membership_expire_date"]).dt.normalize()
    window_end = virtual_today + timedelta(days=EXPIRY_WINDOW_DAYS)
    mask = (
        (df["membership_expire_date"] >= virtual_today) &
        (df["membership_expire_date"] <= window_end) &
        (df["churn_prob"] >= 0.5)
    )
    target = df[mask].copy()
    target = target.drop(columns=["churn_probability"], errors="ignore").rename(
        columns={"msno": "user_id", "churn_prob": "churn_probability"}
    )
    target["plus_price"] = target["plan_list_price"] * TWD_TO_KRW if "plan_list_price" in target.columns else 0
    return target


def apply_filters(df, grades, reasons):
    return df[df["risk_grade"].isin(grades) & df["main_reason_code"].isin(reasons)]

def segment_by_plus_price(df, threshold):
    return df[df["plus_price"] >= threshold].copy(), df[df["plus_price"] < threshold].copy()


def trigger_cherry_blossoms():
    import time
    timestamp = time.time()
    components.html(f"""
    <div id="sk-{timestamp}"></div>
    <script>
    (function() {{
        const pd = window.parent.document;
        const old = pd.getElementById('sakura-container');
        if (old) old.remove();
        const sk = pd.createElement('div');
        sk.id = 'sakura-container';
        Object.assign(sk.style, {{position:'fixed',top:'0',left:'0',width:'100vw',height:'100vh',pointerEvents:'none',zIndex:'99999'}});
        pd.body.appendChild(sk);
        function petal() {{
            const p = pd.createElement('div');
            const sz = Math.random()*15+10;
            Object.assign(p.style, {{position:'absolute',top:'-20px',left:Math.random()*100+'vw',width:sz+'px',height:sz+'px',backgroundColor:['#FFB3D1','#FFD6E7','#F472A8'][Math.floor(Math.random()*3)],borderRadius:'150% 0 150% 0',opacity:'0.85'}});
            const dur = Math.random()*2+3;
            p.animate([{{transform:'translateY(0) rotate(0deg)',opacity:0.85}},{{transform:`translateY(110vh) rotate(${{Math.random()*720}}deg) translateX(${{Math.random()*200}}px)`,opacity:0}}],{{duration:dur*1000,easing:'linear',fill:'forwards'}});
            sk.appendChild(p);
            setTimeout(()=>p.remove(), dur*1000);
        }}
        const iv = setInterval(petal, 70);
        setTimeout(()=>{{ clearInterval(iv); sk.style.transition='opacity 2s'; sk.style.opacity='0'; setTimeout(()=>sk.remove(),2500); }}, 8000);
    }})();
    </script>
    """, height=0)


# ── 세션 상태 ──
for key, val in [("vvip_selected", False), ("gen_selected", False)]:
    if key not in st.session_state:
        st.session_state[key] = val


# ==========================================
# 타이틀
# ==========================================
st.title("고위험군 액션 보드")
st.caption("고객 가치에 따라 그룹을 나누어 맞춤형 마케팅 액션을 시뮬레이션합니다.")
st.markdown("<hr>", unsafe_allow_html=True)


# ==========================================
# 사이드바
# ==========================================
if "virtual_today" not in st.session_state:
    st.session_state.virtual_today = datetime.now().date()

with st.sidebar:
    st.markdown("### 📅 시뮬레이션 설정")
    st.date_input("분석 기준일", key="virtual_today")
    virtual_today = pd.to_datetime(st.session_state.virtual_today)
    st.markdown("---", unsafe_allow_html=True)


# ==========================================
# 데이터 로드
# ==========================================
with st.spinner("🌸 데이터 분석 중..."):
    target_df = get_real_action_data(virtual_today)

if target_df.empty:
    st.warning("분석일 기준 만료 예정인 고위험 유저가 없습니다.")
    st.stop()


# ==========================================
# 공통 필터
# ==========================================
st.markdown("### ⚙️ 공통 필터")

all_reasons_in_data = sorted(target_df["main_reason_code"].unique().tolist())
selected_reasons    = []

c1, c2 = st.columns(2, gap="medium")
with c1:
    selected_grades = st.multiselect("위험 등급", options=RISK_GRADES, default=RISK_GRADES, key="selected_grades_filter")
with c2:
    vvip_threshold = st.number_input("기대 추가수익 기준 (원)", min_value=0, value=20000, step=5000,
        help="기대 추가 수익이 이 금액 이상인 고객을 우량 고객(VVIP)으로 분류합니다.")

st.markdown("##### 🔎 이탈 원인 필터")
f_col1, f_col2 = st.columns(2, gap="large")

active_groups = [(g, [r for r in rs if r in all_reasons_in_data]) for g, rs in REASON_GROUPS.items()]
active_groups = [(g, rs) for g, rs in active_groups if rs]

for i, (g_name, available) in enumerate(active_groups):
    with (f_col1 if i % 2 == 0 else f_col2):
        with st.expander(f"{g_name}  ({len(available)}종)", expanded=True):
            sub_cols = st.columns(2)
            for j, r in enumerate(available):
                with sub_cols[j % 2]:
                    if st.toggle(r, value=True, key=f"tg_{i}_{g_name}_{r}"):
                        selected_reasons.append(r)

if not selected_reasons:
    st.caption("⚠️ 선택된 사유가 없습니다.")

filtered_df = apply_filters(target_df, selected_grades, selected_reasons)

active_cat = "default"
if selected_reasons:
    counts = {}
    for r in selected_reasons:
        for cat, r_list in REASON_GROUPS.items():
            if r in r_list:
                counts[cat] = counts.get(cat, 0) + 1
    if counts:
        active_cat = max(counts, key=counts.get)
cur_actions = CATEGORY_ACTIONS.get(active_cat, CATEGORY_ACTIONS["default"])

st.markdown("<hr>", unsafe_allow_html=True)


# ==========================================
# 그룹 분리
# ==========================================
vvip_df, general_df = segment_by_plus_price(filtered_df, vvip_threshold)

tab_vvip, tab_general = st.tabs([
    f"💎 우량 고객 ({len(vvip_df)}명)",
    f"🌱 일반/신규 고객 ({len(general_df)}명)",
])

# ── 컬럼 설정: 컬럼 너비를 명시해 가로 overflow 방지 ──
COLUMN_CONFIG_BASE = {
    "[☑️ 타겟 선택]":    st.column_config.CheckboxColumn("선택",       width="small"),
    "위험":              st.column_config.TextColumn("⚠️",             width="small"),
    "user_id":           st.column_config.TextColumn("사용자 ID",       width="small"),
    "churn_probability": st.column_config.ProgressColumn(
                             "이탈 확률", format="%.2f", min_value=0, max_value=1, width="medium"),
    "risk_grade":        st.column_config.TextColumn("등급",            width="small"),
    "main_reason_code":  st.column_config.TextColumn("주요 이탈 원인",  width="medium"),
    "plus_price":        st.column_config.NumberColumn("기대 추가 수익", format="%,d원", width="medium"),
}

# ── 위험등급별 행 배경색 매핑 ──
GRADE_BG = {"높음": "#FFF0F3", "보통": "#FFFBF0", "낮음": "#F4FBF4"}
GRADE_COLOR = {"높음": "#991B1B", "보통": "#92400E", "낮음": "#166534"}

def prep_display(df: pd.DataFrame, selected: bool) -> pd.DataFrame:
    out = df.copy()
    out["[☑️ 타겟 선택]"] = selected
    for col in ["user_id","risk_grade","main_reason_code","payment_method_id","registered_via","city"]:
        if col in out.columns: out[col] = out[col].astype(str)
    for col in ["is_auto_renew","is_cancel","[☑️ 타겟 선택]"]:
        if col in out.columns: out[col] = out[col].astype(bool)
    out["user_id"] = out["user_id"].apply(lambda x: x[:10] + ".." if len(str(x)) > 10 else x)
    out["위험"] = out["churn_probability"].apply(
        lambda p: "🔴" if float(p) >= 0.9 else ("🟠" if float(p) >= 0.7 else "🟡")
        if str(p).replace(".","",1).isdigit() else ""
    )
    cols = ["[☑️ 타겟 선택]","위험","user_id","churn_probability","risk_grade","main_reason_code","plus_price"]
    return out[[c for c in cols if c in out.columns]]


def style_table(df: pd.DataFrame, theme: str = "pink") -> Styler:
    """
    theme: 'pink' (우량) | 'green' (일반)
    디자인 요소:
      1. 줄무늬 (짝수행 연핑크/연초록)
      2. 위험등급별 행 배경색 차별화
      3. 이탈확률 셀 색상 강조
      4. 헤더 스타일 (진한 배경)
      5. plus_price 초록 볼드
      6. user_id 모노스페이스 회색
    """
    accent     = "#F472A8" if theme == "pink" else "#55A83A"
    even_bg    = "#FFF8FC" if theme == "pink" else "#F6FBF4"
    reason_col = "#8B2255" if theme == "pink" else "#2E7D1A"

    def row_style(row):
        grade  = str(row.get("risk_grade", ""))
        idx    = row.name
        base   = GRADE_BG.get(grade, "#FFFFFF")
        # 짝수 행이면 약간 다른 tint
        if idx % 2 == 0:
            base = even_bg if grade not in GRADE_BG else base
        styles = [f"background-color: {base}"] * len(row)
        return styles

    def prob_style(val):
        try:
            p = float(val)
            if p >= 0.9: return "background-color:#FECACA; color:#7F1D1D; font-weight:700; border-radius:4px;"
            if p >= 0.8: return "background-color:#FED7AA; color:#7C2D12; font-weight:600;"
            return f"background-color:#DCFCE7; color:#14532D; font-weight:500;"
        except: return ""

    styler = (
        df.style
        .apply(row_style, axis=1)
        .applymap(prob_style, subset=["churn_probability"])
        .format({"churn_probability": "{:.1%}", "plus_price": "{:,.0f}원"})
        .set_properties(subset=["user_id"],
            **{"font-family": "'JetBrains Mono', monospace", "font-size": "11px", "color": "#666"})
        .set_properties(subset=["main_reason_code"],
            **{"color": reason_col, "font-size": "12px"})
        .set_properties(subset=["plus_price"],
            **{"color": "#16500A", "font-weight": "700", "font-size": "12px"})
        .set_properties(subset=["위험"],
            **{"text-align": "center", "font-size": "14px"})
        .set_table_styles([
            # 헤더 강조
            {"selector": "thead th",
             "props": [("background-color", "#FFF0F5" if theme=="pink" else "#F0FAF0"),
                       ("color", "#8B2255" if theme=="pink" else "#16500A"),
                       ("font-weight", "700"), ("font-size", "12px"),
                       ("border-bottom", f"2px solid {accent}"),
                       ("padding", "8px 10px")]},
            # 셀 공통
            {"selector": "td",
             "props": [("padding", "6px 10px"), ("font-size", "12px"),
                       ("border-bottom", "0.5px solid #F5E8F0" if theme=="pink" else "0.5px solid #E8F5E8")]},
            # 테이블 전체
            {"selector": "",
             "props": [("border-collapse", "collapse"), ("width", "100%")]},
        ])
    )
    return styler


def render_tab(df, selected_key, btn_all_key, btn_none_key,
               editor_key, action_key, action_text, success_msg,
               badge_class, theme):
    c1, c2, _ = st.columns([1, 1, 6])
    if c1.button("✅ 전체 선택", key=btn_all_key):
        st.session_state[selected_key] = True; st.rerun()
    if c2.button("⭕ 선택 해제", key=btn_none_key):
        st.session_state[selected_key] = False; st.rerun()

    display = prep_display(df, st.session_state[selected_key])
    styled  = style_table(display, theme=theme)

    # ── 핵심: use_container_width=True + 행 높이 고정으로 페이지 fit ──
    row_h    = 35
    header_h = 42
    max_h    = 520   # 탭 패널 내 최대 높이 (px), 이 이상이면 스크롤
    calc_h   = min(len(df) * row_h + header_h, max_h)

    edited = st.data_editor(
        styled,
        hide_index=True,
        key=editor_key,
        use_container_width=True,   # ← 탭 너비에 맞게 가로 fit
        height=calc_h,              # ← 행 수에 비례한 세로 fit
        column_config=COLUMN_CONFIG_BASE,
    )

    sel = edited[edited["[☑️ 타겟 선택]"] == True]
    if len(sel) > 0:
        st.markdown(f"<span class='{badge_class}'>✔ {len(sel)}명 선택됨</span>", unsafe_allow_html=True)
        if st.button(action_text, type="primary", key=action_key):
            trigger_cherry_blossoms()
            st.success(success_msg.format(len_sel=len(sel)))


# ──────────────────────────────────────────
# 탭 1 : 💎 우량 고객
# ──────────────────────────────────────────
with tab_vvip:
    if len(vvip_df) > 0:
        render_tab(
            df=vvip_df,
            selected_key="vvip_selected",
            btn_all_key="btn_vvip_all", btn_none_key="btn_vvip_none",
            editor_key="editor_vvip",
            action_key="act_vvip",
            action_text=cur_actions["vvip"],
            success_msg=cur_actions["msg"],
            badge_class="sel-badge-pink",
            theme="pink",
        )
    else:
        st.info("조건에 맞는 우량 고객이 없습니다.")


# ──────────────────────────────────────────
# 탭 2 : 🌱 일반/신규 고객
# ──────────────────────────────────────────
with tab_general:
    if len(general_df) > 0:
        render_tab(
            df=general_df,
            selected_key="gen_selected",
            btn_all_key="btn_gen_all", btn_none_key="btn_gen_none",
            editor_key="editor_gen",
            action_key="act_gen",
            action_text=cur_actions["general"],
            success_msg=cur_actions["msg"],
            badge_class="sel-badge-green",
            theme="green",
        )
    else:
        st.info("조건에 맞는 일반 고객이 없습니다.")
