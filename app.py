import streamlit as st
import google.generativeai as genai
import PIL.Image
import requests
from io import BytesIO

# --- 頁面設定 ---
st.set_page_config(page_title="小小婚禮造型師", page_icon="💒", layout="centered")

# --- 設定 API KEY (請在 Streamlit Cloud 的 Secrets 設定中填入) ---
# 為了教學安全，建議從 Streamlit 的 secrets 讀取，或先暫時直接寫字串測試
API_KEY = st.sidebar.text_input("請輸入 Gemini API Key", type="password")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.warning("請在側邊欄輸入 API Key 以啟動功能。")

# --- 自定義 CSS 讓介面更像婚禮主題 ---
st.markdown("""
    <style>
    .main { background-color: #fff5f5; }
    .stButton>button { width: 100%; border-radius: 20px; border: 2px solid #feb2b2; height: 3em; font-weight: bold; }
    .stButton>button:active { border-color: #3182ce !important; background-color: #ebf8ff !important; }
    .vocab-box { background-color: white; padding: 20px; border-radius: 15px; border: 2px dashed #feb2b2; }
    </style>
    """, unsafe_allow_html=True)

st.title("💒 小小婚禮造型師")
st.subheader("Người Lên Kế Hoạch Đám Cưới")

# --- 字典設定 ---
dict_data = {
    '角色': {'cô dâu': '新娘 (Vietnamese bride)', 'chú rể': '新郎 (Vietnamese groom)'},
    '服裝': {'áo dài': '傳統長衫', 'áo đầm': '洋裝/裙子', 'đồ vét': '西裝'},
    '顏色': {'đỏ': '紅色', 'trắng': '白色', 'đen': '黑色', 'xanh lá': '綠色', 'vàng': '黃色'}
}

# --- 遊戲邏輯 ---
col1, col2, col3 = st.columns(3)

with col1:
    role = st.radio("第一步：幫誰策劃？", list(dict_data['角色'].keys()), 
                    format_func=lambda x: f"{x} ({dict_data['角色'][x]})")

with col2:
    clothing = st.radio("第二步：選擇服裝", list(dict_data['服裝'].keys()), 
                       format_func=lambda x: f"{x} ({dict_data['服裝'][x]})")

with col3:
    color = st.radio("第三步：選擇顏色", list(dict_data['顏色'].keys()), 
                     format_func=lambda x: f"{x} ({dict_data['顏色'][x]})")

st.divider()

# --- 生成邏輯 ---
if st.button("✨ 開始繪製我的婚禮造型"):
    if not API_KEY:
        st.error("請先填寫 API Key！")
    else:
        with st.spinner("AI 正在繪圖中，請稍候 (約 15-20 秒)..."):
            try:
                # 建立提示詞
                prompt = f"Beautiful illustration style of {dict_data['角色'][role]} wearing {color} {clothing}, Vietnamese wedding theme, cute cartoon art."
                
                # 呼叫 Imagen 模型
                model = genai.GenerativeModel('imagen-3.0-generate-001')
                response = model.generate_content(prompt)
                
                # 顯示圖片
                st.image(response.candidates[0].content.parts[0].inline_data.data, 
                         caption="生成的婚禮造型", use_column_width=True)
                
                # 顯示越語句子
                pronoun = "Cô ấy" if role == 'cô dâu' else "Anh ấy"
                vn_sentence = f"Đây là {role}. {pronoun} sẽ mặc {clothing} màu {color}."
                st.success(f"**越語描述：** {vn_sentence}")
                
            except Exception as e:
                st.error(f"生成失敗，請確認您的帳號是否有 Imagen 3 權限。錯誤訊息：{e}")

# --- 詞彙學習區 ---
st.markdown('<div class="vocab-box"><h4>📝 詞彙學習庫 (Từ vựng)</h4>'
            '<b>cô dâu</b> (新娘) | <b>chú rể</b> (新郎) | <b>áo dài</b> (長衫) | <b>màu đỏ</b> (紅色)</div>', 
            unsafe_allow_html=True)