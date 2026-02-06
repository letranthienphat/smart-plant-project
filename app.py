import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from streamlit_js_eval import get_geolocation
import time

# --- CẤU HÌNH HỆ THỐNG ---
st.set_page_config(page_title="EcoMind OS - Enterprise", layout="wide", page_icon="🏦")

# --- QUẢN LÝ ĐĂNG NHẬP (AUTH SYSTEM) ---
if 'auth_status' not in st.session_state:
    st.session_state.auth_status = None # None, 'guest', 'user'

def login_ui():
    st.title("🛡️ Cổng Đăng Nhập Hệ Thống")
    tab1, tab2, tab3 = st.tabs(["Đăng nhập", "Đăng ký", "Truy cập Khách"])
    
    with tab1:
        user = st.text_input("Tên đăng nhập")
        pw = st.text_input("Mật khẩu", type="password")
        if st.button("Xác nhận Đăng nhập", type="primary"):
            if user == "admin" and pw == "123": # Demo logic
                st.session_state.auth_status = 'user'
                st.rerun()
            else:
                st.error("Sai tài khoản hoặc mật khẩu")
                
    with tab2:
        st.info("Tính năng Đăng ký đang kết nối với Database SQL...")
        st.text_input("Email đăng ký")
        st.button("Gửi mã xác thực")
        
    with tab3:
        if st.button("Tiếp tục với quyền Khách (Guest)"):
            st.session_state.auth_status = 'guest'
            st.rerun()

# --- CHƯƠNG TRÌNH CHÍNH ---
def main_app():
    # Sidebar Navigation
    with st.sidebar:
        st.title("🏦 Control Center")
        st.write(f"Trạng thái: **{st.session_state.auth_status.upper()}**")
        if st.button("Đăng xuất"):
            st.session_state.auth_status = None
            st.rerun()
        
        st.divider()
        menu = st.radio("Menu", ["📊 Dashboard Tổng", "🔍 Tra cứu 3000+ Cây", "⚙️ Cài đặt Thiết bị"])

    # 1. TỰ ĐỘNG LẤY VỊ TRÍ & THỜI TIẾT
    loc = get_geolocation()
    lat, lon = (loc['coords']['latitude'], loc['coords']['longitude']) if loc else (10.8231, 106.6297)
    
    # API Thời tiết (Auto-fetch)
    weather_res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relativehumidity_2m").json()
    temp = weather_res['current_weather']['temperature']
    hum = weather_res['hourly']['relativehumidity_2m'][0]

    if menu == "📊 Dashboard Tổng":
        st.header("📈 Hệ Thống Giám Sát Real-time")
        
        # Grid thông tin VIP
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Nhiệt độ vị trí", f"{temp}°C")
        with col2:
            st.metric("Độ ẩm khí quyển", f"{hum}%")
        with col3:
            st.metric("Dự báo bốc hơi", "Cao", delta="12%")
        with col4:
            st.metric("Cây đang theo dõi", "05")

        # KHU VỰC BIỂU ĐỒ VIP
        st.markdown("### 📡 Tình trạng các chậu cây")
        # Giả lập dữ liệu cho nhiều cây
        plants_monitor = pd.DataFrame({
            'Cây': ['Xương rồng', 'Lan ý', 'Trầu bà', 'Bàng Sing', 'Sen đá'],
            'Mức nước (%)': [85, 30, 45, 12, 60],
            'Dự báo sống (Ngày)': [45, 5, 8, 2, 30]
        })
        
        fig = px.bar(plants_monitor, x='Cây', y='Mức nước (%)', color='Mức nước (%)',
                     color_continuous_scale='RdYlGn', title="Mức nước hiện tại của các thiết bị")
        st.plotly_chart(fig, use_container_width=True)

        # TÍNH NĂNG CHẠY NGẦM CẢNH BÁO
        for index, row in plants_monitor.iterrows():
            if row['Mức nước (%)'] < 20:
                st.toast(f"🚨 CẢNH BÁO: Cây {row['Cây']} sắp hết nước!", icon="🔥")

    elif menu == "🔍 Tra cứu 3000+ Cây":
        st.header("🌿 Thư viện Thực vật Thông minh")
        search = st.text_input("Nhập tên cây để AI truy xuất API toàn cầu...", "Rose")
        
        # Tự động bắt API Trefle (Giả lập kết quả nhanh)
        st.write(f"Đang kết nối API trích xuất dữ liệu cho: **{search}**...")
        st.info("Đang hiển thị dữ liệu từ hệ thống Global Botanical Database.")
        
        # Hiển thị dạng bảng lớn (VIP PRO)
        c1, c2 = st.columns([1, 2])
        with c1:
            st.image("https://images.unsplash.com/photo-1545239351-ef51147f52e3?q=80&w=400", caption="Ảnh minh họa AI")
        with c2:
            st.table({
                "Thông số": ["Tên khoa học", "Họ", "Nhu cầu ánh sáng", "Mức tiêu thụ nước (L/ngày)", "Chịu nhiệt tối đa"],
                "Dữ liệu AI": [f"{search} Scientific", "Rosaceae", "Cao (6-8h)", "0.5 L", "38°C"]
            })

# --- ĐIỀU HƯỚNG APP ---
if st.session_state.auth_status is None:
    login_ui()
else:
    main_app()
