import streamlit as st
import time
import os
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語小教室", 
    page_icon="🌞", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS 優化 ---
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
    }
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        font-size: 20px;
        font-weight: bold;
        background-color: #FFD700;
        color: #333;
        border: none;
        padding: 12px 0px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #FFC107;
        transform: translateY(-2px);
        box-shadow: 0px 6px 8px rgba(0,0,0,0.15);
    }
    .card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 15px;
        border: 1px solid #eee;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .big-font {
        font-size: 28px !important;
        font-weight: 800;
        color: #2E86C1;
        margin: 5px 0;
    }
    .med-font {
        font-size: 18px !important;
        color: #666;
        margin-bottom: 10px;
    }
    .emoji-icon {
        font-size: 50px;
        margin-bottom: 5px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 1. 數據結構 (Unit 2: 飲食篇) ---
VOCABULARY = {
    "Komaen": {"zh": "吃", "emoji": "🍽️", "action": "做出吃飯動作", "file": "Komaen"},
    "Hemay":  {"zh": "飯", "emoji": "🍚", "action": "像是捧著碗", "file": "Hemay"},
    "Nanom":  {"zh": "水", "emoji": "💧", "action": "做出喝水動作", "file": "Nanom"}
}

SENTENCES = [
    {"amis": "Komaen kako to hemay.", "zh": "我正在吃飯。", "file": "sentence_komaen"}
]

# --- 1.5 智慧語音核心 ---
def play_audio(text, filename_base=None):
    if filename_base:
        path_m4a = f"audio/{filename_base}.m4a"
        if os.path.exists(path_m4a):
            st.audio(path_m4a, format='audio/mp4')
            return
        path_mp3 = f"audio/{filename_base}.mp3"
        if os.path.exists(path_mp3):
            st.audio(path_mp3, format='audio/mp3')
            return

    try:
        tts = gTTS(text=text, lang='id') # 印尼語發音近似阿美語
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
    except:
        st.caption("🔇 (語音暫無法播放)")

# --- 2. 狀態管理 ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0

# --- 3. 介面邏輯 ---

def show_learning_mode():
    st.markdown("<div style='text-align: center; color: #888; margin-bottom: 10px;'>Unit 2: 飲食與生活</div>", unsafe_allow_html=True)
    st.info("👆 點擊播放按鈕聽發音！")
    
    col1, col2 = st.columns(2)
    words = list(VOCABULARY.items())
    
    for idx, (amis, data) in enumerate(words):
        with (col1 if idx % 2 == 0 else col2):
            st.markdown(f"""
            <div class="card">
                <div class="emoji-icon">{data['emoji']}</div>
                <div class="big-font">{amis}</div>
                <div class="med-font">{data['zh']}</div>
                <div style="color: #999; font-size: 14px; border-top: 1px dashed #ddd; padding-top:5px;">
                    動作：{data['action']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            play_audio(amis, filename_base=data.get('file'))

    st.markdown("---")
    st.markdown("### 🗣️ 句型練習")
    
    s1 = SENTENCES[0]
    
    st.markdown(f"""
    <div class="card" style="background-color: #FEF9E7; border: none;">
        <div style="font-size: 20px; font-weight:bold; color:#D4AC0D; margin-bottom: 5px;">
            {s1['amis']}
        </div>
        <div style="color:#555;">{s1['zh']}</div>
    </div>
    """, unsafe_allow_html=True)
    play_audio(s1['amis'], filename_base=s1.get('file')) 

def show_quiz_mode():
    st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>🏆 小勇士挑戰</h3>", unsafe_allow_html=True)
    
    st.progress(st.session_state.current_q / 3)
    st.write("") 

    if st.session_state.current_q == 0:
        # --- Q1: 聽力測驗 ---
        st.markdown("**第 1 關：聽聽看，這是什麼意思？**")
        target_word = "Nanom"
        play_audio(target_word, filename_base="Nanom")
        
        st.write("")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🍽️ 吃"): st.error("那是 Komaen 喔！")
        with c2:
            if st.button("🍚 飯"): st.error("那是 Hemay 喔！")
        with c3:
            if st.button("💧 水"):
                st.balloons()
                st.success("答對了！Nanom 就是水。")
                time.sleep(1.0)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()

    elif st.session_state.current_q == 1:
        # --- Q2: 填空測驗 ---
        st.markdown("**第 2 關：句子接龍**")
        st.markdown("請完成句子：")
        st.markdown("`Komaen kako to _______.`")
        st.caption("(我正在吃飯)")
        
        play_audio("Komaen kako to hemay", filename_base="sentence_komaen")
        
        options = ["Hemay (飯)", "Nanom (水)", "Fodoy (衣服)"]
        choice = st.radio("請選擇正確的單字：", options)
        
        st.write("")
        if st.button("✅ 確定送出"):
            if "Hemay" in choice:
                st.success("太棒了！")
                time.sleep(1.5)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.error("再試一次！Komaen 是吃，所以要選吃的東西喔。")

    elif st.session_state.current_q == 2:
        # --- Q3: 意義測驗 ---
        st.markdown("**第 3 關：我是翻譯官**")
        st.markdown("阿美語說： **Komaen!**")
        play_audio("Komaen", filename_base="Komaen")
        
        st.info("這個動作是在做什麼？")
        
        if st.button("喝水"): st.error("喝水是 Minom (或喝 Nanom) 喔！")
        if st.button("吃飯"):
            st.snow()
            st.success("完全正確！Komaen 就是吃。")
            time.sleep(1.5)
            st.session_state.score += 100
            st.session_state.current_q += 1
            st.rerun()

    else:
        # 結算畫面
        st.markdown(f"""
        <div class="card" style="background-color: #FFF8DC; border: 2px solid #FFD700;">
            <h1>🎉 挑戰完成！</h1>
            <h2 style="color: #E67E22;">得分：{st.session_state.score}</h2>
            <p>Komaen kako to hemay! 🍚</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再玩一次"):
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.rerun()

# --- 4. 主程式入口 ---
st.title("阿美語小教室 🌞")

# 講師資訊
st.markdown("""
    <div style="text-align: center; color: #555; font-size: 16px; margin-top: -15px; margin-bottom: 25px; font-weight: 500;">
        講師：彭三妹 &nbsp;|&nbsp; 教材提供者：彭三妹
    </div>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📖 學習單詞", "🎮 練習挑戰"])

with tab1:
    show_learning_mode()

with tab2:
    show_quiz_mode()
