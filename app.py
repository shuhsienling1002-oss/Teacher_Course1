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

# --- CSS 極致美化 (Salongan 主題) ---
st.markdown("""
    <style>
    /* 全局背景：溫潤的米白色，像棉麻布料 */
    .stApp {
        background-color: #FFFBF5;
    }
    
    /* 調整頂部間距 */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
    }

    /* 標題樣式：漸層色設計 */
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        background: -webkit-linear-gradient(45deg, #FF6B6B, #FF8E53);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important;
        text-align: center;
        padding-bottom: 10px;
    }

    /* 按鈕美化：黃金果實風格 */
    .stButton>button {
        width: 100%;
        border-radius: 50px; /* 更圓潤 */
        font-size: 18px;
        font-weight: 700;
        background: linear-gradient(135deg, #FFD700 0%, #FDB931 100%); /* 金色漸層 */
        color: #4A4A4A;
        border: none;
        padding: 15px 0px;
        box-shadow: 0px 5px 15px rgba(253, 185, 49, 0.4); /* 柔和發光 */
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0px 8px 20px rgba(253, 185, 49, 0.6);
    }

    /* 卡片設計：懸浮極簡風 */
    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #F0F0F0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); /* 深度陰影 */
        transition: transform 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px); /* 滑鼠懸停上浮 */
        border-color: #FF6B6B;
    }

    /* 字體排版 */
    .big-font {
        font-size: 32px !important;
        font-weight: 800;
        color: #FF6B6B; /* 阿美紅 */
        margin: 10px 0;
        letter-spacing: 1px;
    }
    .med-font {
        font-size: 18px !important;
        color: #888;
        font-weight: 500;
        margin-bottom: 15px;
    }
    .emoji-icon {
        font-size: 55px;
        margin-bottom: 5px;
        filter: drop-shadow(0 3px 5px rgba(0,0,0,0.1));
    }
    
    /* 講師資訊欄 */
    .instructor-box {
        text-align: center;
        color: #999;
        font-size: 14px;
        background: rgba(255,255,255,0.6);
        padding: 8px 20px;
        border-radius: 20px;
        display: inline-block;
        margin: 0 auto 25px auto;
        border: 1px solid #eee;
    }

    /* 隱藏預設元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tab 優化 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #fff;
        border-radius: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF6B6B !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 數據結構 ---
VOCABULARY = {
    "Salongan": {"zh": "漂亮", "emoji": "✨", "action": "雙手比讚", "file": "Salongan"},
    "Fodoy":    {"zh": "衣服", "emoji": "👕", "action": "拉拉衣服", "file": "Fodoy"},
    "Miso":     {"zh": "你的", "emoji": "🫵", "action": "指指對方", "file": "Miso"}
}

SENTENCES = [
    {"amis": "Salongan ko fodoy no miso.", "zh": "你的衣服很漂亮。", "file": "sentence_salongan"}
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
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
    except:
        st.caption("🔇")

# --- 2. 狀態管理 ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0

# --- 3. 介面邏輯 ---

def show_learning_mode():
    # 標題設計：使用深藍綠色 (Teal) 來對比紅色的主標題，顯得優雅
    st.markdown("""
        <div style='text-align: center; margin-bottom: 25px;'>
            <h2 style='color: #2A9D8F; font-size: 28px; margin: 0;'>Unit 1: Salongan a Fodoy</h2>
            <div style='color: #A0A0A0; font-size: 18px; font-weight: 400; letter-spacing: 2px; margin-top: 5px;'>
                — 漂亮的衣服 —
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("💡 點擊播放按鈕，跟著老師一起唸！")
    
    col1, col2 = st.columns(2)
    words = list(VOCABULARY.items())
    
    for idx, (amis, data) in enumerate(words):
        with (col1 if idx % 2 == 0 else col2):
            st.markdown(f"""
            <div class="card">
                <div class="emoji-icon">{data['emoji']}</div>
                <div class="big-font">{amis}</div>
                <div class="med-font">{data['zh']}</div>
                <div style="color: #2A9D8F; font-size: 13px; font-weight:bold; background: #E0F2F1; padding: 4px 10px; border-radius: 10px; display:inline-block;">
                    {data['action']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            play_audio(amis, filename_base=data.get('file'))

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🗣️ 句型練習")
    
    s1 = SENTENCES[0]
    
    # 句型卡片特別設計：淡黃色背景，強調重點
    st.markdown(f"""
    <div class="card" style="background: linear-gradient(135deg, #FFF9C4 0%, #FFFDE7 100%); border: 2px solid #FFF59D;">
        <div style="font-size: 24px; font-weight:900; color:#FBC02D; margin-bottom: 8px; text-shadow: 1px 1px 0px #fff;">
            {s1['amis']}
        </div>
        <div style="color:#7F8C8D; font-size: 18px;">{s1['zh']}</div>
    </div>
    """, unsafe_allow_html=True)
    play_audio(s1['amis'], filename_base=s1.get('file')) 

def show_quiz_mode():
    st.markdown("<h3 style='text-align: center; color: #FF6B6B; margin-bottom: 20px;'>🏆 小勇士挑戰</h3>", unsafe_allow_html=True)
    
    # 進度條顏色會自動跟隨 Streamlit 主題配置，或預設紅色
    st.progress(st.session_state.current_q / 3)
    st.write("") 

    if st.session_state.current_q == 0:
        st.markdown("**第 1 關：聽聽看，這是什麼意思？**")
        target_word = "Fodoy"
        play_audio(target_word, filename_base="Fodoy")
        
        st.write("")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("✨ 漂亮"): st.error("那是 Salongan 喔！")
        with c2:
            if st.button("👕 衣服"):
                st.balloons()
                st.success("答對了！")
                time.sleep(1.0)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
        with c3:
            if st.button("🫵 你的"): st.error("那是 Miso 喔！")

    elif st.session_state.current_q == 1:
        st.markdown("**第 2 關：句子接龍**")
        st.markdown("請完成句子：")
        st.markdown("""
        <div style="background:#fff; padding:15px; border-radius:10px; border-left: 5px solid #FF6B6B; margin: 10px 0;">
            <span style="font-size:20px;">Salongan ko <b>_______</b> no miso.</span>
        </div>
        """, unsafe_allow_html=True)
        
        play_audio("Salongan ko fodoy no miso", filename_base="sentence_salongan")
        
        options = ["Fodoy (衣服)", "Mata (眼睛)", "Fongoh (頭)"]
        choice = st.radio("請選擇正確的單字：", options)
        
        st.write("")
        if st.button("✅ 確定送出"):
            if "Fodoy" in choice:
                st.success("太棒了！")
                time.sleep(1.5)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.error("再試一次！提示：我們在說衣服喔")

    elif st.session_state.current_q == 2:
        st.markdown("**第 3 關：我是翻譯官**")
        st.markdown("阿美語說：")
        st.markdown("<h1 style='color:#FF6B6B;'>Salongan!</h1>", unsafe_allow_html=True)
        play_audio("Salongan", filename_base="Salongan")
        
        st.info("這是在稱讚什麼？")
        
        if st.button("不好看..."): st.error("不對喔！")
        if st.button("很漂亮！"):
            st.snow()
            st.success("完全正確！")
            time.sleep(1.5)
            st.session_state.score += 100
            st.session_state.current_q += 1
            st.rerun()

    else:
        st.markdown(f"""
        <div class="card" style="background: linear-gradient(180deg, #FFFFFF 0%, #FFF3E0 100%); border: 2px solid #FFD700;">
            <h1 style="margin-bottom:0;">🎉 挑戰完成！</h1>
            <h2 style="color: #E67E22; margin-top:0;">得分：{st.session_state.score}</h2>
            <hr style="border-top: 1px dashed #FFD700;">
            <p style="font-size: 20px; color: #555;">Salongan ko fodoy no miso! ✨</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再玩一次"):
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.rerun()

# --- 4. 主程式入口 ---
# 居中顯示主標題
st.title("阿美語小教室 🌞")

# 講師資訊 - 使用優雅的膠囊樣式置中
st.markdown("""
    <div style="text-align: center;">
        <span class="instructor-box">
            講師：彭三妹 &nbsp;|&nbsp; 教材提供者：彭三妹
        </span>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📖 學習單詞", "🎮 練習挑戰"])

with tab1:
    show_learning_mode()

with tab2:
    show_quiz_mode()
