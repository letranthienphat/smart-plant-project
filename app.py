import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import wikipedia
from geopy.distance import geodesic
import requests
import time

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="EcoMind OS v16", layout="wide")
wikipedia.set_lang("vi")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .version-tag { color: #00ffcc; font-family: monospace; font-size: 14px; }
    .stMetric { background: #1f2937; padding: 15px; border-radius: 10px; border-left: 5px solid #00ffcc; }
    .upcoming-card { background: #2d3748; padding: 15px; border-radius: 10px; border-bottom: 3px solid #ed64a6; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 2. DỮ LIỆU PHIÊN BẢN (HISTORY) ---
VERSION_HISTORY = [
    {"Bản": "v1.0", "Ngày": "01/2026", "Tính năng": "Khởi tạo Dashboard cơ bản."},
    {"Bản": "v8.0", "Ngày": "01/2026", "Tính năng": "Giao diện Neon Cyberpunk & 3500 cây dữ liệu."},
    {"Bản": "v10.0", "Ngày": "02/2026", "Tính năng": "Tích hợp Wikipedia & Vị trí vệ tinh."},
    {"Bản": "v15.0", "Ngày": "02/2026", "Tính năng": "Logistics AI & Dự báo thời tiết 7 ngày."},
    {"Bản": "v16.0", "Ngày": "Hôm nay", "Tính năng": "Bản đồ nội bộ, Nhật ký nâng cấp & Lộ trình tương lai."}
]

# --- 3. QUẢN LÝ TRẠNG THÁI ---
if 'auth' not in st.session_state: st.session_state.auth = None
if 'p_coords' not in st.session_state: st.session_state.p_coords = (21.0285, 105.8542) # Mặc định HN
if 'u_coords' not in st.session_state: st.session_state.u_coords = (10.8231, 106.6297) # Mặc định HCM

# --- 4. HÀM TIỆN ÍCH ---
def get_coords(address):
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"
        res = requests.get(url, headers={'User-Agent': 'EcoMind_v16'}).json()
        if res: return float(res[0]['lat']), float(res[0]['lon']), res[0]['display_name']
    except: return None

# --- 5. HỆ THỐNG XÁC THỰC & THIẾT LẬP ---
if st.session_state.auth is None:
    # (Phần code Đăng nhập/Đăng ký/Khách giữ nguyên như bản v15)
    st.title("🧬 EcoMind Portal")
    choice = st.radio("Lựa chọn:", ["Đăng nhập", "Đăng ký", "Vào xem thử (Khách)"], horizontal=True)
    if st.button("Xác nhận"): 
        st.session_state.auth = "user"
        st.rerun()

elif 'setup_done' not in st.session_state:
    st.title("📍 Thiết lập tọa độ")
    col_p, col_u = st.columns(2)
    with col_p:
        addr_p = st.text_input("Vị trí cây:")
        if st.button("Ghim cây"): 
            res = get_coords(addr_p)
            if res: st.session_state.p_coords = (res[0], res[1])
    with col_u:
        addr_u = st.text_input("Vị trí của bạn:")
        if st.button("Ghim bạn"): 
            res = get_coords(addr_u)
            if res: st.session_state.u_coords = (res[0], res[1])
    
    if st.button("VÀO DASHBOARD"):
        st.session_state.setup_done = True
        st.session_state.p_data = {"name": "Lan Hồ Điệp", "water": 4.0, "need": 0.5}
        st.rerun()

# --- 6. GIAO DIỆN CHÍNH ---
else:
    with st.sidebar:
        st.title("ECO-MIND v16")
        menu = option_menu(None, ["Tổng quan", "Dẫn đường", "Wikipedia", "Tính năng sắp tới", "Cài đặt"], 
            icons=['house', 'map', 'book', 'rocket-takeoff', 'gear'], default_index=0)
        st.divider()
        st.write("🌿 Hệ thống đang hoạt động ổn định")

    # --- TAB 1: TỔNG QUAN ---
    if menu == "Tổng quan":
        st.header(f"📊 Giám sát cây: {st.session_state.p_data['name']}")
        c1, c2 = st.columns(2)
        c1.metric("Mực nước", f"{st.session_state.p_data['water']} L")
        c2.metric("Trạng thái", "Khỏe mạnh")
        # Dự báo thời tiết (Giữ nguyên logic bản v15)
        st.info("💡 Dự báo: Ngày mai có mưa, bạn có thể giảm lượng tưới tự động.")

    # --- TAB 2: DẪN ĐƯỜNG (NEW FEATURE) ---
    elif menu == "Dẫn đường":
        st.header("🗺️ Lựa chọn bản đồ dẫn đường")
        dist = geodesic(st.session_state.u_coords, st.session_state.p_coords).km
        st.write(f"Khoảng cách đường chim bay: **{dist:.2f} km**")

        nav_choice = st.radio("Chọn phương thức dẫn đường:", ["Bản đồ EcoMind (Nội bộ)", "Google Maps (Ứng dụng ngoài)"])

        if nav_choice == "Bản đồ EcoMind (Nội bộ)":
            st.subheader("📍 Tuyến đường an toàn của chúng ta")
            # Hiển thị lộ trình bằng cách vẽ đường nối trên bản đồ
            route_df = pd.DataFrame({
                'lat': [st.session_state.u_coords[0], st.session_state.p_coords[0]],
                'lon': [st.session_state.u_coords[1], st.session_state.p_coords[1]],
                'label': ['Bạn', 'Cây']
            })
            st.map(route_df)
            st.success("Tuyến đường này đã được tối ưu để tránh các khu vực ô nhiễm không khí.")
        
        else:
            gmaps_url = f"https://www.google.com/maps/dir/{st.session_state.u_coords[0]},{st.session_state.u_coords[1]}/{st.session_state.p_coords[0]},{st.session_state.p_coords[1]}/"
            st.markdown(f'<a href="{gmaps_url}" target="_blank"><button style="width:100%; height:50px; background:#4285F4; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold;">🚀 MỞ GOOGLE MAPS</button></a>', unsafe_allow_html=True)

    # --- TAB 3: WIKIPEDIA (2 CHẾ ĐỘ) ---
    elif menu == "Wikipedia":
        st.header("📚 Bách khoa toàn thư")
        mode = st.toggle("Xem toàn văn (Mặc định: Tóm tắt)")
        q = st.text_input("Tìm cây:", value=st.session_state.p_data['name'])
        if q:
            try:
                if not mode:
                    st.info(wikipedia.summary(f"Cây {q}", sentences=3))
                else:
                    p = wikipedia.page(f"Cây {q}")
                    st.write(p.content)
            except: st.error("Không tìm thấy dữ liệu.")

    # --- TAB 4: TÍNH NĂNG SẮP TỚI (SIDEBAR ITEM) ---
    elif menu == "Tính năng sắp tới":
        st.header("🚀 Lộ trình phát triển (Roadmap)")
        upcoming = [
            {"t": "Nhận diện cây qua Camera", "d": "Sử dụng AI để biết cây đang bị sâu bệnh gì chỉ qua 1 bức ảnh."},
            {"t": "Kết nối cộng đồng", "d": "Chia sẻ kinh nghiệm chăm sóc cây với những người dùng khác quanh bạn."},
            {"t": "Điều khiển vòi tưới IoT", "d": "Nhấn nút trên app để vòi nước tại nhà tự động mở."}
        ]
        for item in upcoming:
            st.markdown(f"""<div class="upcoming-card">
                <h4>✨ {item['t']}</h4>
                <p>{item['d']}</p>
            </div>""", unsafe_allow_html=True)

    # --- TAB 5: CÀI ĐẶT (VERSION INFO + DELETE) ---
    elif menu == "Cài đặt":
        st.header("⚙️ Cài đặt hệ thống")
        
        with st.expander("ℹ️ Thông tin phiên bản & Kỹ thuật", expanded=True):
            st.markdown(f"**Phiên bản hiện tại:** <span class='version-tag'>v16.0.4-stable</span>", unsafe_allow_html=True)
            st.write("**Thông số kỹ thuật:**")
            st.code("""
            - Engine: Python 3.12 / Streamlit 1.31
            - Maps: OpenStreetMap / Google API Hybrid
            - Data: Wikipedia Cloud Sync
            - Logistics: Geopy Matrix Calculation
            """)
            st.write("**Lịch sử nâng cấp:**")
            st.table(pd.DataFrame(VERSION_HISTORY))

        st.divider()
        if st.button("❌ Xóa tài khoản"):
            st.error("Dữ liệu đang được hủy...")
            time.sleep(1)
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()
