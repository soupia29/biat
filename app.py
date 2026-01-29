import streamlit as st
import time
import numpy as np
import requests
import random

# --- [설정] 구글 폼 데이터 전송 설정 ---
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScA1_wFColNyFHagQVwuFivI79dp0oIKrNpy1gC3224IMY89A/formResponse"
ENTRY_NAME = "entry.1189315095"   
ENTRY_PHONE = "entry.1779035989"  
ENTRY_RES = "entry.1109564202"    
ENTRY_SCORE = "entry.1391463658"  
ENTRY_SELF = "entry.108666966"    

st.set_page_config(page_title="IAT 무의식 인지 검사", layout="wide")

# CSS 스타일: 버튼을 좌우로 배치하고 디자인 최적화
st.markdown("""
    <style>
    /* 1. 상단 여백 및 가로 여백 완전 제거 */
    .st-emotion-cache-15zrgzn { display: none !important; }
    [data-testid="stHeader"] { display: none !important; }
    .block-container { 
        padding-top: 1rem !important; 
        padding-left: 0.5rem !important; 
        padding-right: 0.5rem !important; 
        max-width: 100% !important; 
    }

    /* 2. 키워드 표시창 (가로 꽉 차게) */
    .word-display {
        background-color: #000000; 
        border-radius: 15px; 
        text-align: center;
        font-size: 60px !important; /* 모바일 폭을 고려해 살짝 조정 */
        font-weight: 900; 
        padding: 30px 10px; 
        color: #ffffff; 
        margin-bottom: 15px;
        width: 100%;
    }

    /* 3. 버튼 좌우 배치 강제 및 간격 0 */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 0px !important; /* 버튼 사이 간격 0 */
        width: 100% !important;
    }

    /* 4. 각 컬럼 설정 (가로 절반씩) */
    [data-testid="column"] {
        flex: 1 1 50% !important;
        min-width: 50% !important;
        padding: 0 !important; /* 컬럼 사이 여백 제거 */
    }

    /* 5. 버튼 디자인 (화면 폭에 꽉 차게) */
    div[data-testid="column"] button {
        width: 100% !important; 
        height: 280px !important; 
        font-size: 80px !important; 
        font-weight: 900 !important;
        background-color: #ffffff !important; 
        color: #000000 !important;
        border: 6px solid #000000 !important; /* 테두리 살짝 얇게 해서 공간 확보 */
        border-radius: 10px !important;
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* 클릭 시 피드백 */
    div[data-testid="column"] button:active { 
        background-color: #ffff00 !important; 
    }

    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state:
    st.session_state.update({
        'step': 'intro', 'results_1': [], 'results_2': [], 
        'idx': 0, 'self_choice': "과학 선호", 'current_words': []
    })

words_pool = [
    ("미분적분", "sci"), ("철학사조", "hum"), ("환희", "pos"), ("절망", "neg"),
    ("양자역학", "sci"), ("서양사학", "hum"), ("영광", "pos"), ("혐오", "neg"),
    ("화학식", "sci"), ("고전소설", "hum"), ("승리", "pos"), ("파멸", "neg"),
    ("인공지능", "sci"), ("시나리오", "hum"), ("평화", "pos"), ("공포", "neg"),
    ("유전자", "sci"), ("언어학", "hum"), ("감동", "pos"), ("분노", "neg"),
    ("알고리즘", "sci"), ("고고학", "hum"), ("축복", "pos"), ("고립", "neg"),
    ("열역학", "sci"), ("문학비평", "hum"), ("열정", "pos"), ("타락", "neg"),
    ("천체물리", "sci"), ("비교문학", "hum")
]

# --- 1. 인트로 ---
if st.session_state.step == 'intro':
    st.title("🧠 암묵적 연합 검사 (IAT)")
    st.markdown("""
    ### ⭐️검사 방법
    : 암묵적 연합 검사는 당신이 특정 키워드를 다른 키워드와 얼마나 빨리 연결 시키는지 그 반응속도를 측정해 무의식적 편향을 알아보는 테스트입니다.
    다음 화면에 나오는 기준을 꼼꼼히 확인하고, 빠르고 정확하게 눌러주세요!
    
    ### 🚨!필독!🚨
    1. 반응 속도가 핵심!: 직관적으로 최대한 빠르게 눌러 주세요(오래 생각X).
    2. 방해가 없는 곳에서 화면 중앙 단어에 집중해 주세요.
    ---
    """)
    u_self = st.selectbox("현재 본인이 느끼는 본인의 성향은?", ["과학 선호", "인문학 선호", "중립/융합"])
    if st.button("내 무의식 확인하러 가기", use_container_width=True):
        st.session_state.self_choice = u_self
        st.session_state.current_words = random.sample(words_pool, len(words_pool))
        st.session_state.step = 'block_1_instr'; st.rerun()

# --- 2. Phase 1 안내 ---
elif st.session_state.step == 'block_1_instr':
    st.subheader("Phase 1: 첫 번째 연합")
    st.info("💡 기준: [과학] 또는 [긍정] 단어는 왼쪽(L) / 그 외는 오른쪽(R)")
    st.warning("🚨 주의: 버튼 작음!")
    if st.button("바로 시작", use_container_width=True):
        st.session_state.step = 'block_1'; st.session_state.idx = 0
        st.session_state.start_time = time.time(); st.rerun()

elif st.session_state.step == 'block_1':
    word, _ = st.session_state.current_words[st.session_state.idx]
    st.markdown(f"<div class='word-display'>{word}</div>", unsafe_allow_html=True)
    
    # 좌우 배치 핵심 로직
    col1, col2 = st.columns(2)
    with col1:
        if st.button("L", key=f"b1l_{st.session_state.idx}"):
            st.session_state.results_1.append(time.time() - st.session_state.start_time)
            st.session_state.idx += 1
            if st.session_state.idx < 30: 
                st.session_state.start_time = time.time()
                st.rerun()
            else: st.session_state.step = 'block_2_instr'; st.rerun()
    with col2:
        if st.button("R", key=f"b1r_{st.session_state.idx}"):
            st.session_state.results_1.append(time.time() - st.session_state.start_time)
            st.session_state.idx += 1
            if st.session_state.idx < 30: 
                st.session_state.start_time = time.time()
                st.rerun()
            else: st.session_state.step = 'block_2_instr'; st.rerun()

# --- 3. Phase 2 안내 ---
elif st.session_state.step == 'block_2_instr':
    st.subheader("Phase 2: 기준 전환")
    st.error("💡 기준 변경: [인문학] 또는 [긍정] 단어는 왼쪽(L) / 그 외는 오른쪽(R)")
    st.warning("🚨 다시 주의: 버튼 작음! 헷갈리지 말고 클릭하기!")
    if st.button("준비 완료! 시작", use_container_width=True):
        st.session_state.current_words = random.sample(words_pool, len(words_pool))
        st.session_state.step = 'block_2'; st.session_state.idx = 0
        st.session_state.start_time = time.time(); st.rerun()

elif st.session_state.step == 'block_2':
    word, _ = st.session_state.current_words[st.session_state.idx]
    st.markdown(f"<div class='word-display'>{word}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("L", key=f"b2l_{st.session_state.idx}"):
            st.session_state.results_2.append(time.time() - st.session_state.start_time)
            st.session_state.idx += 1
            if st.session_state.idx < 30: 
                st.session_state.start_time = time.time()
                st.rerun()
            else: st.session_state.step = 'result'; st.rerun()
    with col2:
        if st.button("R", key=f"b2r_{st.session_state.idx}"):
            st.session_state.results_2.append(time.time() - st.session_state.start_time)
            st.session_state.idx += 1
            if st.session_state.idx < 30: 
                st.session_state.start_time = time.time()
                st.rerun()
            else: st.session_state.step = 'result'; st.rerun()

# --- 4. 결과 리포트 (풍부한 분석 유지) ---
elif st.session_state.step == 'result':
    diff = round(np.mean(st.session_state.results_2) - np.mean(st.session_state.results_1), 4)
    if diff > 0.1:
        res = "분석적 과학 중심 기질"
        long_desc = "당신의 무의식은 논리적 질서와 데이터에 반응할 때 가장 효율적으로 활성화됩니다. 체계적인 구조 속에서 심리적 안정감을 느끼는 분석가 타입입니다."
    elif diff < -0.1:
        res = "통찰적 인문 중심 기질"
        long_desc = "당신의 무의식은 인간적 가치와 맥락적 서사에 반응할 때 가장 높은 연결성을 보입니다. 의미와 통찰을 포착하는 데 탁월한 해석가 타입입니다."
    else:
        res = "균형 잡힌 창의적 융합 기질"
        long_desc = "당신의 무의식은 이성과 감성, 논리와 맥락 사이에서 매우 유연한 균형을 유지하고 있습니다. 다각도로 사고를 전환하는 통합가 타입입니다."

    st.markdown(f"""
    <div class='result-box'>
        <div class='result-header'>📊 심층 분석 결과: {res}</div>
        <p class='analysis-text'>{long_desc}</p>
        <hr style='border: 1px solid #eee; margin: 30px 0;'>
        <p style='color:gray;'>D-Score: {diff}초</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("final"):
        st.write("데이터 제출 및 참여 확인(선택사항, 경품 추첨용)")
        u_name = st.text_input("이름"); u_phone = st.text_input("연락처")
        if st.form_submit_button("연구 데이터 제출"):
            requests.post(FORM_URL, data={ENTRY_NAME: u_name, ENTRY_PHONE: u_phone, ENTRY_RES: res, ENTRY_SCORE: str(diff), ENTRY_SELF: st.session_state.self_choice})
            st.balloons(); st.success("제출 완료!"); st.stop()
