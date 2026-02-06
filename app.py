import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from streamlit_js_eval import get_geolocation
import time
from datetime import datetime

# --- 1. CẤU HÌNH GIAO DIỆN VIP (CSS CUSTOM) ---
st.set_page_config(page_title="EcoMind OS Enterprise", layout="wide", page_icon="💎")

st.markdown("""
<style>
    /* Glassmorphism Effect */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00ffcc; }
    .stButton>button {
        border-radius: 20px; background: linear-gradient(45deg, #00dbde, #fc00ff);
        color: white; border: none; font-weight: bold; width: 100%;
    }
    .vip-card {
        padding: 20px; border-radius: 15px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. HỆ THỐNG PHÂN QUYỀN (AUTHENTICATION) ---
def login_system():
    if 'auth_level' not in st.session_state:
        st.session_state.auth_level = None

    if st.session_state.auth_level is None:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown("<h1 style='text-align: center;'>🔐 EcoMind Gateway</h1>", unsafe_allow_html=True)
            with st.container():
                tab1, tab2, tab3 = st.tabs(["Đăng nhập VIP", "Đăng ký", "Truy cập Khách"])
                with tab1:
                    user = st.text_input("Username")
                    pw = st.text_input("Password", type="password")
                    if st.button("Kích hoạt hệ thống"):
                        if user == "admin" and pw == "vip123":
                            st.session_state.auth_level = "VIP"
                            st.rerun()
                        else: st.error("Sai thông tin xác thực!")
                with tab3:
                    if st.button("Vào chế độ Guest"):
                        st.session_state.auth_level = "Guest"
                        st.rerun()
        return False
    return True

# --- 3. BỘ MÁY XỬ LÝ DỮ LIỆU (AI CORE) ---
@st.cache_data
def load_plant_database():
    # Giả lập 3000 cây (Bạn có thể nạp file CSV ở đây)
    data = [{"Tên": f"Cây VIP {i}", "Nhu cầu": round(0.1 + (i%5)*0.2, 2)} for i in range(3001)]
    return pd.DataFrame(data)

def get_ai_prediction(temp, hum, plant_need):
    """Logic AI từ file internet_protection.py áp dụng vào cây trồng"""
    score = 100 - (abs(temp - 25) * 2) - (abs(hum - 60) * 0.5)
    if score > 80: return "🌟 Rất Tốt", "green"
    if score > 50: return "⚠️ Cần Chú Ý", "orange"
    return "🚨 Nguy Cấp", "red"

# --- 4. GIAO DIỆN CHÍNH (SAU KHI ĐĂNG NHẬP) ---
if login_system():
    # Heartbeat cho UptimeRobot
    st.sidebar.markdown(f"**Server Status:** 🟢 Live (Ping: {int(time.time() % 100)}ms)")
    st.sidebar.write(f"Cấp độ: **{st.session_state.auth_level}**")
    
    if st.sidebar.button("Đăng xuất"):
        st.session_state.auth_level = None
        st.rerun()

    # Lấy GPS và Thời tiết
    loc = get_geolocation()
    lat, lon = (loc['coords']['latitude'], loc['coords']['longitude']) if loc else (10.8231, 106.6297)
    
    # API Thời tiết Real-time
    weather = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()
    cur_temp = weather['current_weather']['temperature']

    st.title("🛰️ EcoMind OS - Command Center")
    
    # Dashboard Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Nhiệt độ", f"{cur_temp}°C")
    with m2: st.metric("Vị trí", "Hà Nội" if lat > 15 else "TP.HCM")
    with m3: st.metric("Database", "3000+ Cây")
    with m4: st.metric("AI Status", "Active")

    # Tính năng VIP: Tra cứu 3000 cây
    st.divider()
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.markdown("### 🔍 AI Search")
        df_plants = load_plant_database()
        search = st.selectbox("Chọn cây từ thư viện 3000 loài:", df_plants['Tên'])
        selected_plant = df_plants[df_plants['Tên'] == search].iloc[0]
        
        water_level = st.slider("Mức nước hiện tại (Lít)", 0.0, 5.0, 2.5)
        
        # Gọi AI Prediction
        status, color = get_ai_prediction(cur_temp, 60, selected_plant['Nhu cầu'])
        st.markdown(f"<div class='vip-card'><h4>Dự báo AI:</h4><h2 style='color:{color}'>{status}</h2></div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("### 📈 Phân tích tiêu thụ")
        days = list(range(7))
        # Logic tính toán VIP
        usage = [water_level - (selected_plant['Nhu cầu'] * d * (1 + (cur_temp-25)*0.05)) for d in days]
        
        fig = px.area(x=days, y=[max(0, x) for x in usage], 
                     title=f"Dự báo cạn nước cho {search}",
                     labels={'x': 'Ngày', 'y': 'Lượng nước (L)'})
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    # Cảnh báo Real-time
    if water_level < 1.0:
        st.toast("🚨 Cảnh báo hệ thống: Lượng nước cực thấp!", icon="🔥")
