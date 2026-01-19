import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 17: O Toki", page_icon="⏰", layout="centered")

# --- CSS 美化 ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #FFF9C4 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #FBC02D;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #F57F17; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #FFFDE7;
        border-left: 5px solid #FFEE58;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #FFF59D; color: #F57F17; border: 2px solid #FBC02D; padding: 12px;
    }
    .stButton>button:hover { background-color: #FFF176; border-color: #F9A825; }
    .stProgress > div > div > div > div { background-color: #FBC02D; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 17 修正版) ---
vocab_data = [
    {"amis": "Dafak", "chi": "早上", "icon": "🌅", "source": "Dict: Morning"},
    {"amis": "Malahok", "chi": "中午", "icon": "☀️", "source": "Row 5542"},
    {"amis": "Lafii", "chi": "深夜", "icon": "🌙", "source": "User Fix"}, # 修正定義
    {"amis": "Anini", "chi": "今天", "icon": "👇", "source": "Row 6500"},
    {"amis": "Anocila", "chi": "明天", "icon": "👉", "source": "Row 486"},
    {"amis": "Nacila", "chi": "昨天", "icon": "👈", "source": "Row 6500"},
    {"amis": "Toki", "chi": "時間 / 鐘", "icon": "⏰", "source": "Unit 11"},
    {"amis": "Mafoti'", "chi": "睡覺", "icon": "💤", "source": "Row 4"},
    {"amis": "Lomowad", "chi": "起床", "icon": "🥱", "source": "Row 22"},
    {"amis": "Komaen", "chi": "吃飯", "icon": "🍚", "source": "Row 2"},
]

sentences = [
    {"amis": "Lomowad to kako.", "chi": "我起床了。", "icon": "🥱", "source": "Row 22"},
    {"amis": "Malahok to.", "chi": "中午了(吃午餐了)。", "icon": "🍱", "source": "Row 363"},
    {"amis": "Mafoti' ci mama i lafii.", "chi": "爸爸在深夜睡覺。", "icon": "💤", "source": "User Fix (Lafii)"}, # 修正翻譯
    {"amis": "Anocila a tayra i pitilidan.", "chi": "明天要去學校。", "icon": "🏫", "source": "Row 486"},
    {"amis": "Safaw tosa ko toki anini.", "chi": "現在是十二點。", "icon": "🕛", "source": "Unit 11"},
]

# --- 3. 隨機題庫 (定義) ---
raw_quiz_pool = [
    {
        "q": "Lomowad to kako.",
        "audio": "Lomowad to kako",
        "options": ["我起床了", "我睡覺了", "我吃飯了"],
        "ans": "我起床了",
        "hint": "Lomowad 是起床"
    },
    {
        "q": "Mafoti' ci mama i lafii.",
        "audio": "Mafoti' ci mama i lafii",
        "options": ["爸爸在深夜睡覺", "爸爸早上起床", "爸爸中午吃飯"],
        "ans": "爸爸在深夜睡覺",
        "hint": "Lafii 是深夜"
    },
    {
        "q": "Malahok to.",
        "audio": "Malahok to",
        "options": ["中午了/吃午餐了", "早上了", "晚上了"],
        "ans": "中午了/吃午餐了",
        "hint": "Malahok 是中午"
    },
    {
        "q": "單字測驗：Anocila",
        "audio": "Anocila",
        "options": ["明天", "昨天", "今天"],
        "ans": "明天",
        "hint": "未來的時間 (Ano-)"
    },
    {
        "q": "單字測驗：Dafak",
        "audio": "Dafak",
        "options": ["早上", "深夜", "中午"],
        "ans": "早上",
        "hint": "太陽剛出來的時候"
    },
    {
        "q": "單字測驗：Lafii",
        "audio": "Lafii",
        "options": ["深夜", "中午", "早上"],
        "ans": "深夜",
        "hint": "很晚很晚的時候"
    },
    {
        "q": "「睡覺」的阿美語怎麼說？",
        "audio": None,
        "options": ["Mafoti'", "Lomowad", "Komaen"],
        "ans": "Mafoti'",
        "hint": "Ma-foti' (Row 4)"
    },
    {
        "q": "Anocila a tayra i pitilidan.",
        "audio": "Anocila a tayra i pitilidan",
        "options": ["明天要去學校", "昨天去過學校", "今天在學校"],
        "ans": "明天要去學校",
        "hint": "Anocila 是明天"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌
    selected_questions = random.sample(raw_quiz_pool, 3)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #F57F17;'>Unit 17: O Toki</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>時間與日常 (Lafii Fixed)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #F57F17;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 3)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 3**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #FFF59D; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #F57F17;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會時間與日常用語了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            # 重置時重新洗牌
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 3)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()
