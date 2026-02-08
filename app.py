import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import wikipedia
import requests
import random
import time

# --- 1. CẤU HÌNH & GIAO DIỆN ---
st.set_page_config(page_title="EcoMind OS - Enterprise", layout="wide", page_icon="🔐")
wikipedia.set_lang("vi")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    div[data-testid="stMetricValue"] { color: #00ffcc !important; font-weight: bold; }
    h1, h2, h3 { color: #00ffcc !important; }
    .stButton>button { border-radius: 5px; background-color: #1f2937; color: #00ffcc; border: 1px solid #00ffcc; width: 100%; }
    .stButton>button:hover { background-color: #00ffcc; color: black; }
</style>
""", unsafe_allow_html=True)

# --- 2. DỮ LIỆU & LOGIC ---
@st.cache_data
def get_plant_db():
    loai = ["Hoa Hồng", "Lan Hồ Điệp", "Xương Rồng", "Trầu Bà", "Sen Đá", "Kim Tiền", "Lưỡi Hổ"]
    data = []
    for i, name in enumerate(loai):
        data.append({"ID": i, "Tên Cây": name, "Nhu cầu": round(random.uniform(0.1, 0.8), 2)})
    return pd.DataFrame(data)

def strict_wiki_search(query):
    try:
        results = wikipedia.search(f"Cây {query}")
        if results:
            page = wikipedia.page(results[0])
            # FIX LỖI IMAGE TYPEERROR: Kiểm tra xem có ảnh không
            img_url = page.images[0] if (hasattr(page, 'images') and len(page.images) > 0) else None
            return {
                "found": True, "title": page.title,
                "summary": wikipedia.summary(results[0], sentences=3),
                "url": page.url, "img": img_url
            }
    except: pass
    return {"found": False}

# --- 3. HỆ THỐNG ĐĂNG NHẬP / ĐĂNG KÝ ---
def auth_system():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            st.title("🔐 EcoMind Portal")
            tab_login, tab_reg = st.tabs(["Đăng nhập", "Đăng ký mới"])
            
            with tab_login:
                user = st.text_input("Tên đăng nhập")
                pw = st.text_input("Mật khẩu", type="password")
                if st.button("Truy cập hệ thống"):
                    if user == "admin" and pw == "123": # Demo
                        st.session_state.logged_in = True
                        st.rerun()
                    else: st.error("Sai thông tin!")
            
            with tab_reg:
                st.text_input("Email")
                st.text_input("Tạo Username")
                st.text_input("Tạo Password", type="password")
                st.button("Tạo tài khoản VIP")
        return False
    return True

# --- 4. GIAO DIỆN CHÍNH ---
if auth_system():
    db = get_plant_db()
    
    # --- TÍNH NĂNG CHỌN CÂY LẦN ĐẦU (ONBOARDING) ---
    if 'my_plant' not in st.session_state:
        st.balloons()
        st.title("🌱 Chào mừng VIP User!")
        st.subheader("Hãy thiết lập chậu cây đầu tiên của bạn")
        
        c1, c2 = st.columns(2)
        with c1:
            choice = st.selectbox("Chọn loài cây bạn đang trồng:", db["Tên Cây"])
        with c2:
            water = st.number_input("Lượng nước hiện có trong bình (Lít):", min_value=0.1, max_value=10.0, value=2.0)
        
        if st.button("Bắt đầu giám sát ngay"):
            st.session_state.my_plant = db[db["Tên Cây"] == choice].iloc[0].to_dict()
            st.session_state.current_water = water
            st.rerun()
            
    else:
        # SIDEBAR MENU
        with st.sidebar:
            st.title("ECO-MIND OS")
            selected = option_menu(None, ["Dashboard", "Tra cứu Wiki", "Vị trí", "Cài đặt"], 
                icons=['cpu', 'search', 'map', 'gear'], default_index=0)
            if st.button("Đăng xuất"):
                st.session_state.logged_in = False
                del st.session_state.my_plant
                st.rerun()

        # === TAB DASHBOARD ===
        if selected == "Dashboard":
            st.title(f"📊 Giám sát: {st.session_state.my_plant['Tên Cây']}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Nước còn lại", f"{st.session_state.current_water:.2f} L")
            col2.metric("Nhu cầu", f"{st.session_state.my_plant['Nhu cầu']} L/ngày")
            
            # Tính toán tự động
            days_left = st.session_state.current_water / st.session_state.my_plant['Nhu cầu']
            col3.metric("Dự kiến hết nước", f"{days_left:.1f} ngày")
            
            # Cập nhật nước thủ công
            new_water = st.slider("Cập nhật lại lượng nước thực tế (nhập tay):", 0.0, 10.0, float(st.session_state.current_water))
            if st.button("Lưu thông số nước"):
                st.session_state.current_water = new_water
                st.toast("Đã cập nhật dữ liệu nước!")

        # === TAB TRA CỨU WIKI (ĐÃ FIX LỖI) ===
        elif selected == "Tra cứu Wiki":
            st.title("🔍 Bách khoa thực vật")
            query = st.text_input("Tìm tên cây:")
            if query:
                res = strict_wiki_search(query)
                if res["found"]:
                    st.subheader(res["title"])
                    # FIX LỖI Ở ĐÂY: Kiểm tra URL ảnh trước khi hiện
                    if res["img"]:
                        st.image(res["img"], width=400)
                    else:
                        st.info("Loài này không có ảnh trên Wiki.")
                    st.write(res["summary"])
                else:
                    st.error("Không tìm thấy thông tin thực vật phù hợp.")

        # === TAB VỊ TRÍ ===
        elif selected == "Vị trí":
            st.title("📍 Định vị vườn")
            city = st.text_input("Nhập thành phố:", "Hanoi")
            # Tự động lấy tọa độ đơn giản
            if city:
                st.map(pd.DataFrame({'lat': [21.0285], 'lon': [105.8542]})) # Demo
                st.info("Vị trí của bạn được đồng bộ tự động với trạm thời tiết gần nhất.")
