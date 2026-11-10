import streamlit as st

# ==========================================
# 1. 페이지 설정 (공통 레이아웃)
# ==========================================
st.set_page_config(
    page_title="🌸 KKBOX 이탈 방어 시스템",
    page_icon="🌸",
    layout="wide"
)

# ==========================================
# 2. 페이지 정의 및 내비게이션 설정
# ==========================================
# 각 기능별 페이지를 정의합니다. (st.Page API 사용)
action_board_page = st.Page(
    "pages/action_board/action_board.py", 
    title="통합 대시보드", 
    icon="📊", 
    default=True
)

action_manager_page = st.Page(
    "pages/action/app_action.py",
    title="고위험군 액션 보드",
    icon="🎯"
)

app_simulator_page = st.Page(
    "pages/simulator/app_simulator.py",
    title="마케팅 성과 시뮬레이터",
    icon="📈"
)

# 사이드바 내비게이션 그룹화
pg = st.navigation({
    "대시보드": [action_board_page, action_manager_page],
    "시뮬레이터": [app_simulator_page],
})

# 페이지 실행
pg.run()
