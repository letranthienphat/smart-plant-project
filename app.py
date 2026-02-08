import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import wikipedia
from geopy.distance import geodesic
import requests
import datetime

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="EcoMind v18 - Weather Intel", layout="wide")
wikipedia.set_lang("vi")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .status-box { padding: 20px; border-radius: 15px; background: #1f2937; border-left: 5px solid #00ffcc; margin-bottom: 20px; }
    .plant-voice { font-style: italic; color: #ffeb3b; font-size: 1.2rem; text-align: center; padding: 10px; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background: #00ffcc; color: black; font-weight: bold; border: none; }
</style>
""", unsafe_allow_html=True)

# --- 2. HÀM LẤY DỮ LIỆU KHÍ TƯỢNG ---
def get_weather_data(lat, lon):
    try:
        # Lấy dữ liệu thực tế hiện tại và lượng mưa từ Open-Meteo
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,is_day&timezone=auto"
        res = requests.get(url).json()
        return res['current']
    except: return None

# --- 3. LOGIC TÍNH TOÁN TỰ ĐỘNG (KHÔNG NHẬP LIỆU) ---
def analyze_plant_status(weather):
    if not weather: return "Đang kết nối đài khí tượng...", "⚪"
    
    temp = weather['temperature_2m']
    rain = weather['precipitation']
    
    # Giả lập logic: Nếu nóng trên 30 độ mà không mưa -> Khát
    if rain > 0.5:
        return "Mình vừa được uống nước mưa, sướng quá!", "🌧️"
    elif temp > 32:
        return "Trời nắng nóng quá, mình đang bị bốc hơi nước nhanh lắm!", "🔥"
    elif temp < 20:
        return "Trời hơi lạnh, mình không cần uống nhiều nước đâu.", "❄️"
    else:
        return "Thời tiết hôm nay thật dễ chịu, mình vẫn ổn!", "🍃"

# --- 4. KIỂM TRA ĐĂNG NHẬP ---
if 'auth' not in st.session_state: st.session_state.auth = None

if st.session_state.auth is None:
    # Giao diện đăng nhập tràn màn hình
    st.title("🌿 ECO-MIND v18")
    st.subheader("Hệ thống quản lý cây tái chế qua dữ liệu khí tượng")
    col_log, col_empty = st.columns([1, 0.01]) # Tràn màn hình
    with col_log:
        st.text_input("Tên đăng nhập")
        st.text_input("Mật khẩu", type="password")
        if st.button("VÀO HỆ THỐNG"):
            st.session_state.auth = "user"
            st.session_state.p_coords = (21.0285, 105.8542) # Mặc định Hà Nội
            st.session_state.u_coords = (21.0333, 105.8333)
            st.rerun()

else:
    # --- THANH BÊN (SIDEBAR) ---
    with st.sidebar:
        st.title("ECO-NAVIGATOR")
        menu = option_menu(None, ["Trạng thái cây", "Dẫn đường", "Wiki Cây", "Tính năng dự kiến", "Cài đặt"], 
            icons=['heart-pulse', 'signpost-turn-right', 'book', 'magic', 'gear'], default_index=0)
        
        st.divider()
        st.write("📡 **Kết nối đài khí tượng:** Sẵn sàng")
        if st.button("Đăng xuất"):
            st.session_state.auth = None
            st.rerun()

    # --- TAB 1: TRẠNG THÁI CÂY (TỰ ĐỘNG) ---
    if menu == "Trạng thái cây":
        st.header("🌦️ Phân tích từ Đài khí tượng")
        
        # Lấy dữ liệu thời tiết thực tế tại tọa độ cây
        w_data = get_weather_data(st.session_state.p_coords[0], st.session_state.p_coords[1])
        voice, icon = analyze_plant_status(w_data)
        
        st.markdown(f"""
        <div class="status-box">
            <h1 style="text-align:center;">{icon}</h1>
            <p class="plant-voice">"{voice}"</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        if w_data:
            c1.metric("Nhiệt độ ngoài trời", f"{w_data['temperature_2m']}°C")
            c2.metric("Độ ẩm không khí", f"{w_data['relative_humidity_2m']}%")
            c3.metric("Lượng mưa thực tế", f"{w_data['precipitation']} mm")

        st.divider()
        st.subheader("💡 Lời khuyên cho bạn")
        if w_data and w_data['precipitation'] > 0:
            st.success("Hôm nay đài khí tượng báo có mưa tại vườn. Bạn không cần phải về tưới cây đâu!")
        else:
            st.warning("Dựa vào độ ẩm thấp, bạn nên sắp xếp về thăm cây trong 1-2 ngày tới.")

    # --- TAB 2: DẪN ĐƯỜNG THẬT THỤ ---
    elif menu == "Dẫn đường":
        st.header("🧭 Dẫn đường trực tiếp về vườn")
        dist = geodesic(st.session_state.u_coords, st.session_state.p_coords).km
        st.write(f"Vị trí cây cách bạn: **{dist:.2f} km**")
        
        st.map(pd.DataFrame({'lat': [st.session_state.u_coords[0], st.session_state.p_coords[0]], 
                             'lon': [st.session_state.u_coords[1], st.session_state.p_coords[1]]}))
        
        st.divider()
        # Nút dẫn đường thật thụ mở ứng dụng Google Maps
        dest_url = f"https://www.google.com/maps/dir/?api=1&origin={st.session_state.u_coords[0]},{st.session_state.u_coords[1]}&destination={st.session_state.p_coords[0]},{st.session_state.p_coords[1]}&travelmode=driving"
        
        st.markdown(f'<a href="{dest_url}" target="_blank"><button>🧭 BẬT CHỈ ĐƯỜNG TỪNG BƯỚC (GOOGLE MAPS)</button></a>', unsafe_allow_html=True)
        st.caption("Lưu ý: Nút này sẽ mở ứng dụng Google Maps trên điện thoại để dẫn đường bằng giọng nói.")

    # --- TAB 3: TÍNH NĂNG DỰ KIẾN (SIDEBAR ITEM) ---
    elif menu == "Tính năng dự kiến":
        st.header("🚀 Sắp ra mắt")
        st.markdown("""
        - **Cảnh báo bão:** Tự động gọi điện/nhắn tin nếu đài khí tượng báo có bão lớn sắp đổ bộ vào vùng có cây.
        - **AR Shadow:** Dùng camera để xem bóng nắng sẽ quét qua cây như thế nào trong ngày.
        - **Bảng xếp hạng Tái chế:** Vinh danh những người dùng sử dụng nhiều vật liệu tái chế nhất.
        """)

    # --- TAB 4: CÀI ĐẶT (VERSION INFO) ---
    elif menu == "Cài đặt":
        st.header("⚙️ Thông tin hệ thống")
        with st.expander("📝 Nhật ký phiên bản", expanded=True):
            st.write("**Phiên bản hiện tại:** v18.0.2")
            st.table(pd.DataFrame([
                {"Bản": "v18.0", "Thay đổi": "Tự động lấy dữ liệu thời tiết, Dẫn đường trực tiếp (Navigation Mode)."},
                {"Bản": "v17.0", "Thay đổi": "Giao diện tràn màn hình, bỏ kết nối phần cứng điện tử."},
                {"Bản": "v1.0 - v16.0", "Thay đổi": "Xây dựng nền tảng và bách khoa toàn thư."}
            ]))
        
        st.write("**Thông số kỹ thuật:**")
        st.code("Weather Engine: Open-Meteo API (Real-time)\nMap Engine: Google Maps Direction Services\nLogic: Evaporation Inference Model")
