
import streamlit as st
import time
import numpy as np
import requests
import random

# --- [설정] 데이터 전송 설정 (기존 유지) ---
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScA1_wFColNyFHagQVwuFivI79dp0oIKrNpy1gC3224IMY89A/formResponse"

ENTRY_NAME = "entry.1189315095"   
ENTRY_PHONE = "entry.1779035989"  
ENTRY_RES = "entry.1109564202"    
ENTRY_SCORE = "entry.1391463658"  
ENTRY_SELF = "entry.108666966"    

st.set_page_config(page_title="IAT 무의식 인지 검사", layout="wide")

# [UI/UX 혁신] 버튼 크기 및 결과 가독성 개선
st.markdown("""
    <style>
    /* 상단 여백 제거하여 버튼 공간 확보 */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }

    /* [핵심 1] L/R 버튼: 화면 높이의 60%를 강제로 차지 + 글자 크기 120px */
    div[data-testid="column"] button {
        width: 100% !important;
        height: 60vh !important;      /* 화면 높이의 60% */
        min-height: 500px !important; /* 최소 높이 500px 보장 */
        font-size: 120px !important;  /* 글자 크기 */
        font-weight: 900 !important;
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 12px solid #000000 !important;
        border-radius: 40px !important;
        margin-top: 10px !important;
    }
    
    /* 버튼 눌렀을 때 효과 */
    div[data-testid="column"] button:active {
        background-color: #ffff00 !important;
        transform: scale(0.98);
    }

    /* 키워드 박스: 검은 배경에 흰 글씨 (눈에 확 띄게) */
    .word-display {
        background-color: #000000;
        border-radius: 20px;
        text-align: center;
        font-size: 80px;
        font-weight: 900;
        padding: 20px;
        color: #ffffff;
        margin-bottom: 10px;
        border: 4px solid #333;
    }
    
    /* [핵심 2] 결과 리포트: 흰색 배경에 검은 글씨 강제 (가독성 해결) */
    .result-box {
        padding: 30px;
        background-color: #ffffff !important; /* 배경 흰색 고정 */
        border: 5px solid #000000;
        border-radius: 20px;
        margin-top: 20px;
        margin-bottom: 20px;
        color: #000000 !important; /* 글자 검은색 고정 */
    }
    .result-box h2 {
        color: #004085 !important;
        font-size: 35px !important;
        font-weight: bold;
    }
    .result-box p {
        color: #212529 !important;
        font-size: 22px !important;
        line-height: 1.6;
        font-weight: 500;
    }
    .advice-box {
        background-color: #f8f9fa;
        border-left: 10px solid #28a745;
        padding: 20px;
        margin-top: 20px;
        color: #000000 !important;
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

if st.session_state.step == 'intro':
    st.title("🧠 무의식 인지 연합 검사 (IAT)")
    st.markdown("### 당신의 무의식은 어디를 향하고 있을까요?")
    st.info("👇 아래에서 본인의 성향을 선택하고 시작 버튼을 누르세요.")
    
    u_self = st.selectbox("Step 0. 자가진단: 본인의 성향을 선택하세요.", ["과학 선호", "인문학 선호", "중립/융합"])
    
    if st.button("검사 시작하기 (총 30문항)", use_container_width=True):
        st.session_state.self_choice = u_self
        st.session_state.current_words = random.sample(words_pool, len(words_pool))
        st.session_state.step = 'block_1_instr'; st.rerun()

elif st.session_state.step == 'block_1_instr':
    st.subheader("Phase 1: 인지 연합")
    st.success("💡 [과학] 또는 [긍정] 단어는 **왼쪽(L)** 버튼을 누르세요!")
    st.error("💡 그 외 단어는 **오른쪽(R)** 버튼을 누르세요!")
    if st.button("준비 완료! 시작하기", use_container_width=True):
        st.session_state.step = 'block_1'; st.session_state.idx = 0
        st.session_state.start_time = time.time(); st.rerun()

elif st.session_state.step == 'block_1':
    word, _ = st.session_state.current_words[st.session_state.idx]
    st.markdown(f"<div class='word-display'>{word}</div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("LEFT", key=f"b1l_{st.session_state.idx}"):
            st.session_state.results_1.append(time.time() - st.session_state.start_time)
            st.session_state.idx += 1
            if st.session_state.idx < 30: st.session_state.start_time = time.time(); st.rerun()
            else: st.session_state.step = 'block_2_instr'; st.rerun()
    with c2:
        if st.button("RIGHT", key=f"b1r_{st.session_state.idx}"):
            st.session_state.results_1.append(time.time() - st.session_state.start_time)
            st.session_state.idx += 1
            if st.session_state.idx < 30: st.session_state.start_time = time.time(); st.rerun()
            else: st.session_state.step = 'block_2_instr'; st.rerun()

elif st.session_state.step == 'block_2_instr':
    st.subheader("Phase 2: 기준 전환 (주의!)")
    st.warning("⚠️ 기준이 바뀝니다! 헷갈리지 마세요.")
    st.success("💡 [인문학] 또는 [긍정] 단어는 **왼쪽(L)** 버튼을 누르세요!")
    if st.button("이해했습니다. 시작하기", use_container_width=True):
        st.session_state.current_words = random.sample(words_pool, len(words_pool))
        st.session_state.step = 'block_2'; st.session_state.idx = 0
        st.session_state.start_time = time.time(); st.rerun()

elif st.session_state.step == 'block_2':
    word, _ = st.session_state.current_words[st.session_state.idx]
    st.markdown(f"<div class='word-display'>{word}</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("LEFT", key=f"b2l_{st.session_state.idx}"):
            st.session_state.results_2.append(time.time() - st.session_state.start_time)
            st.session_state.idx += 1
            if st.session_state.idx < 30: st.session_state.start_time = time.time(); st.rerun()
            else: st.session_state.step = 'result'; st.rerun()
    with c2:
        if st.button("RIGHT", key=f"b2r_{st.session_state.idx}"):
            st.session_state.results_2.append(time.time() - st.session_state.start_time)
            st.session_state.idx += 1
            if st.session_state.idx < 30: st.session_state.start_time = time.time(); st.rerun()
            else: st.session_state.step = 'result'; st.rerun()

elif st.session_state.step == 'result':
    # 점수 계산
    diff = round(np.mean(st.session_state.results_2) - np.mean(st.session_state.results_1), 4)
    abs_d = abs(diff)
    
    # 결과 해석 로직
    if diff > 0.15:
        res = "과학적 가치 선호 (Scientific Orientation)"
        desc = "당신의 뇌는 **논리적 인과관계, 데이터, 객관적 사실**을 처리할 때 인지적 효율성이 극대화됩니다. 복잡한 현상을 체계적으로 분석하고 구조화하는 데에 강력한 무의식적 강점을 가지고 있습니다."
        advice = "🔬 **추천 활동:** 데이터 분석, 실험 설계, 알고리즘 구현 등 명확한 답을 찾아가는 탐구 활동에서 큰 성취감을 느낄 것입니다."
    elif diff < -0.15:
        res = "인문학적 가치 선호 (Humanistic Orientation)"
        desc = "당신의 뇌는 **맥락, 서사, 인간의 가치**를 연결할 때 뉴런이 가장 활발하게 반응합니다. 텍스트 너머의 의미를 통찰하고 타인과 공감하며 소통하는 능력에 본능적인 강점이 있습니다."
        advice = "📚 **추천 활동:** 비평문 작성, 역사적 사건 재해석, 심리 분석 등 다양한 관점을 통합하고 의미를 부여하는 활동을 추천합니다."
    else:
        res = "인지적 융합 설계형 (Integrative Thinker)"
        desc = "당신은 어느 한쪽에 치우치지 않는 **유연하고 균형 잡힌 사고 회로**를 가졌습니다. 이성과 감성, 논리와 직관을 자유롭게 넘나들며 창의적인 해결책을 제시할 수 있는 융합형 인재의 자질이 보입니다."
        advice = "💡 **추천 활동:** 서로 다른 분야를 연결하는 프로젝트(예: 과학 윤리 토론, 디지털 예술 창작)에서 독보적인 역량을 발휘할 수 있습니다."

    st.title("📊 심층 인지 분석 리포트")
    
    # 1. 메인 결과 카드 (가독성 개선: 흰 배경 검은 글씨)
    st.markdown(f"""
    <div class='result-box'>
        <h2>핵심 진단: {res}</h2>
        <hr style='border: 1px solid #333;'>
        <p>{desc}</p>
    </div>
    """, unsafe_allow_html=True)

    # 2. 데이터 시각화 (게이지 바)
    st.write("### 🧠 무의식적 선호 강도")
    progress_val = min(abs_d / 0.5, 1.0)
    st.progress(progress_val)
    st.caption(f"D-Score: {diff} (반응 속도 차이 절대값)")

    # 3. 상세 지표
    c1, c2, c3 = st.columns(3)
    is_match = "일치" if st.session_state.self_choice[:2] in res else "불일치"
    if st.session_state.self_choice == "중립/융합" and "융합" in res: is_match = "일치"
    
    with c1: st.metric("자아 일치도", is_match)
    with c2: st.metric("반응 속도 편차", f"{abs_d}초")
    with c3: st.metric("신뢰 구간", "높음" if abs_d > 0.1 else "보통")

    # 4. 맞춤형 조언 (가독성 개선)
    st.markdown(f"""
    <div class='advice-box'>
        <h3 style='margin:0; color:#155724;'>✨ 성장을 위한 제언</h3>
        <p style='margin-top:10px; font-size:18px;'>{advice}</p>
    </div>
    """, unsafe_allow_html=True)

    # 5. 최종 제출
    st.divider()
    with st.form("final_form"):
        st.markdown("#### 🎁 연구 데이터 제출 (경품 추첨)")
        u_name = st.text_input("성함 (익명 가능)")
        u_phone = st.text_input("연락처 (선택 사항)")
        if st.form_submit_button("결과 저장 및 제출"):
            payload = {
                ENTRY_NAME: u_name if u_name else "익명",
                ENTRY_PHONE: u_phone if u_phone else "미기입",
                ENTRY_RES: res,
                ENTRY_SCORE: str(diff),
                ENTRY_SELF: st.session_state.self_choice
            }
            try:
                requests.post(FORM_URL, data=payload)
                st.balloons(); st.success("제출 완료! 탐구에 참여해주셔서 감사합니다."); st.stop()
            except:
                st.error("전송 오류 발생")
    