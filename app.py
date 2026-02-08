import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import wikipedia
from geopy.distance import geodesic
import requests
import time
import datetime

# --- 1. GIAO DIỆN CYBERPUNK ---
st.set_page_config(page_title="EcoMind Explorer", layout="wide")
wikipedia.set_lang("vi")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .stMetric { background: #1f2937; padding: 15px; border-radius: 10px; border-left: 5px solid #00ffcc; }
    .status-card { padding: 20px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #374151; }
    .stButton>button { border-radius: 8px; border: 1px solid #00ffcc; background: transparent; color: #00ffcc; transition: 0.3s; }
    .stButton>button:hover { background: #00ffcc; color: black; box-shadow: 0 0 15px #00ffcc; }
</style>
""", unsafe_allow_html=True)

# --- 2. BỘ MÁY TÍNH TOÁN & API ---

def get_weather_forecast(lat, lon):
    """Lấy dự báo thời tiết 7 ngày từ Open-Meteo"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
        res = requests.get(url).json()
        return pd.DataFrame({
            "Ngày": res['daily']['time'],
            "Max (°C)": res['daily']['temperature_2m_max'],
            "Min (°C)": res['daily']['temperature_2m_min'],
            "Mưa (mm)": res['daily']['precipitation_sum']
        })
    except: return None

def get_coords(address):
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"
        headers = {'User-Agent': 'EcoMind_Explorer'}
        response = requests.get(url, headers=headers).json()
        if response: return float(response[0]['lat']), float(response[0]['lon']), response[0]['display_name']
    except: pass
    return None

# --- 3. QUẢN LÝ TÀI KHOẢN & XÁC THỰC ---
if 'auth' not in st.session_state: st.session_state.auth = None

if st.session_state.auth is None:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🌿 Chào mừng bạn!")
        tab_log, tab_reg, tab_guest = st.tabs(["Đăng nhập", "Đăng ký", "Vào xem thử"])
        with tab_log:
            st.text_input("Tên đăng nhập")
            st.text_input("Mật khẩu", type="password")
            if st.button("Vào hệ thống"): 
                st.session_state.auth = "user"
                st.rerun()
        with tab_reg:
            st.text_input("Chọn tên đăng nhập")
            st.text_input("Chọn mật khẩu", type="password")
            if st.button("Tạo tài khoản"): st.success("Xong rồi! Giờ bạn qua tab đăng nhập nhé.")
        with tab_guest:
            if st.button("Xem thử ngay (Khách)"):
                st.session_state.auth = "guest"
                st.rerun()

# --- 4. THIẾT LẬP VỊ TRÍ & CHỌN CÂY ---
elif 'setup_done' not in st.session_state:
    st.title("📍 Cài đặt một chút nhé")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Vị trí chậu cây")
        p_addr = st.text_input("Cây của bạn đang ở đâu?", "Hồ Gươm, Hà Nội")
        if st.button("Tìm vị trí cây"):
            res = get_coords(p_addr)
            if res:
                st.session_state.p_coords = (res[0], res[1])
                st.success(f"Đã ghim cây tại: {res[0]}, {res[1]}")
    with c2:
        st.subheader("Vị trí của bạn")
        u_addr = st.text_input("Bạn đang ở đâu thế?", "Sân bay Đà Nẵng")
        if st.button("Tìm chỗ tôi đứng"):
            res = get_coords(u_addr)
            if res:
                st.session_state.u_coords = (res[0], res[1])
                st.success(f"Đã ghim bạn tại: {res[0]}, {res[1]}")
    
    if 'p_coords' in st.session_state and 'u_coords' in st.session_state:
        st.divider()
        pt = st.selectbox("Hôm nay bạn muốn chăm cây gì?", ["Hoa Hồng", "Xương Rồng", "Lan Hồ Điệp", "Trầu Bà"])
        wl = st.number_input("Số lít nước còn trong bình:", value=3.0)
        if st.button("XONG, VÀO THÔI!", use_container_width=True):
            st.session_state.setup_done = True
            st.session_state.p_data = {"name": pt, "water": wl, "need": 0.5}
            st.rerun()

# --- 5. GIAO DIỆN CHÍNH ---
else:
    with st.sidebar:
        st.title("ECO-MIND")
        menu = option_menu(None, ["Theo dõi", "Dẫn đường", "Bách khoa", "Tính năng mới", "Tài khoản"], 
            icons=['cpu', 'signpost-split', 'book', 'stars', 'person'], default_index=0)
        if st.button("🚪 Đăng xuất"):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()

    # --- TAB 1: THEO DÕI (Dashboard) ---
    if menu == "Theo dõi":
        st.header(f"🌿 Cây {st.session_state.p_data['name']} của bạn")
        
        # Lấy thời tiết thật tại vị trí cây
        weather_df = get_weather_forecast(st.session_state.p_coords[0], st.session_state.p_coords[1])
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Nước còn lại", f"{st.session_state.p_data['water']:.1f} L")
        if weather_df is not None:
            c2.metric("Nhiệt độ sắp tới", f"{weather_df.iloc[0]['Max (°C)']}°C")
            c3.metric("Khả năng mưa", f"{weather_df.iloc[0]['Mưa (mm)']}mm")
        
        st.divider()
        st.subheader("📅 Dự báo thời tiết 7 ngày tại vườn")
        if weather_df is not None:
            fig = px.bar(weather_df, x="Ngày", y="Max (°C)", color="Mưa (mm)", template="plotly_dark", title="Thời tiết tuần tới")
            st.plotly_chart(fig, use_container_width=True)

    # --- TAB 2: DẪN ĐƯỜNG (Logistics & Maps) ---
    elif menu == "Dẫn đường":
        st.header("🗺️ Đường về với cây")
        dist = geodesic(st.session_state.u_coords, st.session_state.p_coords).km
        road_dist = dist * 1.3
        travel_time = road_dist / 50 # Giả định đi xe máy/oto 50km/h
        water_days = st.session_state.p_data['water'] / st.session_state.p_data['need']

        if travel_time / 24 > water_days * 0.8:
            st.error(f"🚨 CẢNH BÁO: Bạn cách cây {road_dist:.1f} km. Nước chỉ còn đủ dùng trong {water_days:.1f} ngày. Hãy về ngay!")
        else:
            st.success(f"✅ Yên tâm: Bạn cách cây {road_dist:.1f} km. Vẫn còn đủ thời gian di chuyển.")

        # Bản đồ & Nút dẫn đường
        st.map(pd.DataFrame({'lat': [st.session_state.u_coords[0], st.session_state.p_coords[0]], 
                             'lon': [st.session_state.u_coords[1], st.session_state.p_coords[1]]}))
        
        # Link dẫn đường Google Maps
        gmaps_url = f"https://www.google.com/maps/dir/{st.session_state.u_coords[0]},{st.session_state.u_coords[1]}/{st.session_state.p_coords[0]},{st.session_state.p_coords[1]}/"
        st.markdown(f'<a href="{gmaps_url}" target="_blank"><button style="width:100%; height:50px; background:#00ffcc; color:black; font-weight:bold; border:none; border-radius:10px; cursor:pointer;">🧭 BẮT ĐẦU DẪN ĐƯỜNG (GOOGLE MAPS)</button></a>', unsafe_allow_html=True)

    # --- TAB 3: BÁCH KHOA (Wikipedia) ---
    elif menu == "Bách khoa":
        st.header("📚 Tìm hiểu về loài cây")
        q = st.text_input("Tên cây:", value=st.session_state.p_data['name'])
        m = st.radio("Cách xem:", ["Đọc tóm tắt", "Xem đầy đủ"], horizontal=True)
        if q:
            try:
                if "tóm tắt" in m.lower():
                    st.info(wikipedia.summary(f"Cây {q}", sentences=3))
                else:
                    p = wikipedia.page(f"Cây {q}")
                    if p.images: st.image(p.images[0], width=300)
                    st.write(p.content)
            except: st.error("Không tìm thấy thông tin.")

    # --- TAB 4: TÍNH NĂNG MỚI LẠ (Smart AI) ---
    elif menu == "Tính năng mới lạ":
        st.header("✨ Góc thông minh & Sáng tạo")
        
        col_m, col_e = st.columns(2)
        with col_m:
            st.subheader("😊 Tâm trạng của cây")
            # Tính toán tâm trạng dựa trên lượng nước
            w_ratio = st.session_state.p_data['water'] / 5.0
            if w_ratio > 0.8: mood, icon = "Hạnh phúc", "☀️"
            elif w_ratio > 0.4: mood, icon = "Bình thường", "☁️"
            else: mood, icon = "Đang khát/Buồn", "🥀"
            st.markdown(f"<div style='font-size:40px; text-align:center;'>{icon}<br>{mood}</div>", unsafe_allow_html=True)
            
        with col_e:
            st.subheader("🌍 Đóng góp môi trường")
            co2 = (st.session_state.p_data['need'] * 100) / 2 # Giả lập chỉ số CO2
            st.metric("CO2 đã hấp thụ", f"{co2:.2f} mg/ngày")
            st.caption("Cây của bạn đang giúp Trái Đất xanh hơn mỗi ngày!")

    # --- TAB 5: TÀI KHOẢN & XÓA ---
    elif menu == "Tài khoản":
        st.header("👤 Cài đặt cá nhân")
        st.write(f"Tài khoản: **{st.session_state.auth}**")
        st.divider()
        if st.button("❌ XÓA TÀI KHOẢN VÀ DỮ LIỆU"):
            st.warning("Đang xóa dữ liệu...")
            time.sleep(1)
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()
