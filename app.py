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

# CSS 스타일 (링크 아이콘 제거 및 리포트 디자인)
st.markdown("""
    <style>
    .st-emotion-cache-15zrgzn { display: none !important; }
    a { pointer-events: none; cursor: default; color: inherit; text-decoration: none; }
    [data-testid="stHeader"] { display: none !important; }
    .block-container { padding-top: 2rem !important; max-width: 100% !important; }
    
    /* 버튼 스타일 */
    div[data-testid="column"] button {
        width: 100% !important; height: 250px !important;
        font-size: 60px !important; font-weight: 900 !important;
        background-color: #ffffff !important; color: #000000 !important;
        border: 6px solid #000000 !important; border-radius: 20px !important;
    }
    div[data-testid="column"] button:active { background-color: #ffff00 !important; }
    
    .word-display {
        background-color: #000000; border-radius: 20px; text-align: center;
        font-size: 70px; font-weight: 900; padding: 30px; color: #ffffff; margin-bottom: 20px;
    }
    .result-box {
        padding: 40px; background-color: #ffffff !important;
        border: 8px solid #000000; border-radius: 25px; color: #000000 !important;
    }
    .result-header { color: #004085; font-size: 42px; font-weight: 900; margin-bottom: 20px; border-bottom: 3px solid #004085; padding-bottom: 10px; }
    .analysis-text { font-size: 21px; line-height: 1.8; margin-bottom: 15px; }
    .highlight { color: #d63384; font-weight: bold; }
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

# --- 1. 인트로: 안내 및 유의사항 ---
if st.session_state.step == 'intro':
    st.title("🧠 잠재적 인지 연합 검사 (IAT)")
    st.markdown("""
    ### 📋 검사 전 필독 안내사항
    이 검사는 당신의 의식적인 생각 너머에 있는 '무의식적 인지 편향'을 측정합니다.
    
    1. 반응 속도가 핵심!: 단어를 보고 판단하는 데 걸리는 '밀리초(ms)' 단위의 시간을 측정합니다.
    2. 직관을 믿기: 너무 오래 고민하면 무의식이 아닌 '생각'이 개입됩니다. 틀려도 좋으니 빠르게 누르는 것이 중요합니다.
    3. 환경 조성: 주변의 방해를 최소화하고, 화면 중앙의 단어에만 집중해 주세요.
    
    ---
    """)
    u_self = st.selectbox("Step 0. 현재 본인이 스스로 느끼는 성향은 어느 쪽에 가깝나요?", ["과학 선호", "인문학 선호", "중립/융합"])
    if st.button("내 무의식 확인하러 가기", use_container_width=True):
        st.session_state.self_choice = u_self
        st.session_state.current_words = random.sample(words_pool, len(words_pool))
        st.session_state.step = 'block_1_instr'; st.rerun()

# --- 2. Phase 1 안내 (버튼 작음 주의 문구) ---
elif st.session_state.step == 'block_1_instr':
    st.subheader("Phase 1: 첫 번째 연합")
    st.info("💡 기준: [과학] 관련 단어나 [긍정] 단어는 왼쪽(L) / 그 외는 오른쪽(R)")
    st.warning("🚨 주의: 버튼 작음! (하지만 최대한 빨리 눌러야 함!)")
    if st.button("이해함! 바로 시작", use_container_width=True):
        st.session_state.step = 'block_1'; st.session_state.idx = 0
        st.session_state.start_time = time.time(); st.rerun()

elif st.session_state.step == 'block_1':
    word, _ = st.session_state.current_words[st.session_state.idx]
    st.markdown(f"<div class='word-display'>{word}</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("L", key=f"b1l_{st.session_state.idx}"):
            st.session_state.results_1.append(time.time() - st.session_state.start_time)
            st.session_state.idx += 1
            if st.session_state.idx < 30: st.session_state.start_time = time.time(); st.rerun()
            else: st.session_state.step = 'block_2_instr'; st.rerun()
    with c2:
        if st.button("R", key=f"b1r_{st.session_state.idx}"):
            st.session_state.results_1.append(time.time() - st.session_state.start_time)
            st.session_state.idx += 1
            if st.session_state.idx < 30: st.session_state.start_time = time.time(); st.rerun()
            else: st.session_state.step = 'block_2_instr'; st.rerun()

# --- 3. Phase 2 안내 ---
elif st.session_state.step == 'block_2_instr':
    st.subheader("Phase 2: 기준 전환 (뇌를 깨우세요!)")
    st.error("💡 기준 변경: [인문학] 관련 단어나 [긍정] 단어는 왼쪽(L) / 그 외는 오른쪽(R)")
    st.warning("🚨 **다시 주의: 버튼 작음! 헷갈리지 말고 클릭하기!")
    if st.button("뇌 준비 완료! 시작", use_container_width=True):
        st.session_state.current_words = random.sample(words_pool, len(words_pool))
        st.session_state.step = 'block_2'; st.session_state.idx = 0
        st.session_state.start_time = time.time(); st.rerun()

elif st.session_state.step == 'block_2':
    word, _ = st.session_state.current_words[st.session_state.idx]
    st.markdown(f"<div class='word-display'>{word}</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("L", key=f"b2l_{st.session_state.idx}"):
            st.session_state.results_2.append(time.time() - st.session_state.start_time)
            st.session_state.idx += 1
            if st.session_state.idx < 30: st.session_state.start_time = time.time(); st.rerun()
            else: st.session_state.step = 'result'; st.rerun()
    with c2:
        if st.button("R", key=f"b2r_{st.session_state.idx}"):
            st.session_state.results_2.append(time.time() - st.session_state.start_time)
            st.session_state.idx += 1
            if st.session_state.idx < 30: st.session_state.start_time = time.time(); st.rerun()
            else: st.session_state.step = 'result'; st.rerun()

# --- 4. 결과 리포트 ---
elif st.session_state.step == 'result':
    diff = round(np.mean(st.session_state.results_2) - np.mean(st.session_state.results_1), 4)
    
    if diff > 0.1:
        res = "분석적 과학 중심 기질"
        long_desc = """
        당신의 무의식은 <span class='highlight'>논리적 질서와 데이터</span>에 반응할 때 가장 빠른 인지적 흐름을 보입니다. 
        현상을 객관적인 구성 요소로 나누어 분석하거나, 인과관계를 파악할 때 뇌의 뉴런이 가장 효율적으로 활성화됩니다. 
        모호한 서사보다는 증명 가능한 사실과 체계적인 구조 속에서 심리적 안정감과 즐거움을 느끼는 경향이 있습니다.
        """
        extra = "이러한 기질은 복잡한 시스템을 설계하거나 데이터 뒤에 숨겨진 법칙을 찾아내는 데 큰 강점이 됩니다."
    elif diff < -0.1:
        res = "통찰적 인문 중심 기질"
        long_desc = """
        당신의 무의식은 <span class='highlight'>인간적 가치와 맥락적 서사</span>에 반응할 때 가장 높은 연결성을 보입니다. 
        단편적인 사실 그 자체보다 사실들이 엮여 만들어내는 '의미'와 '맥락'을 포착하는 데 탁월한 본능을 가졌습니다. 
        인간의 감정, 역사적 흐름, 혹은 텍스트 이면의 숨겨진 상징을 해석할 때 당신의 사고는 가장 빛을 발합니다.
        """
        extra = "이러한 기질은 타인과의 깊은 공감을 이끌어내거나, 파편화된 정보들 속에서 하나의 거대한 이야기를 구성하는 데 탁월합니다."
    else:
        res = "균형 잡힌 창의적 융합 기질"
        long_desc = """
        당신의 무의식은 <span class='highlight'>이성과 감성, 논리와 맥락</span> 사이에서 매우 유연한 균형을 유지하고 있습니다. 
        특정 인지적 틀에 갇히지 않고 사안에 따라 다각도로 사고를 전환하는 능력이 뛰어납니다. 
        과학의 체계성과 인문학의 통찰력을 동시에 활용할 수 있는 잠재력을 가졌으며, 이는 현대 사회가 요구하는 융합적 사고의 핵심입니다.
        """
        extra = "서로 다른 두 영역을 연결하여 새로운 아이디어를 창출하는 '브릿지' 역할에 최적화된 타입입니다."

    st.markdown(f"""
    <div class='result-box'>
        <div class='result-header'>📊 심층 분석 결과: {res}</div>
        <p class='analysis-text'>{long_desc}</p>
        <p class='analysis-text'><b>[추가 분석]</b> {extra}</p>
        <hr style='border: 1px solid #eee; margin: 30px 0;'>
        <p style='color:gray; font-size:16px;'>D-Score (반응 속도 편차): {diff}초<br>
        이 수치는 두 가지 인지 연합 간의 뇌 처리 속도 차이를 의미하며, 귀하의 기질적 선호도를 나타내는 지표입니다.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("final"):
        st.write("### 🎁 데이터 제출 및 참여 확인(선택 사항, 경품 추첨용)")
        u_name = st.text_input("이름")
        u_phone = st.text_input("연락처")
        if st.form_submit_button("연구 데이터 제출"):
            requests.post(FORM_URL, data={ENTRY_NAME: u_name, ENTRY_PHONE: u_phone, ENTRY_RES: res, ENTRY_SCORE: str(diff), ENTRY_SELF: st.session_state.self_choice})
            st.balloons(); st.success("제출 완료! 당신의 무의식을 탐구해주셔서 감사합니다."); st.stop()
