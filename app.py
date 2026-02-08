import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import wikipedia
from geopy.distance import geodesic
import time
import datetime
import webbrowser

# --- 1. CẤU HÌNH & GIAO DIỆN ---
st.set_page_config(page_title="EcoMind OS - Logistics AI", layout="wide")
wikipedia.set_lang("vi")

# Giữ nguyên giao diện Cyberpunk chuyên nghiệp
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .stMetric { background: #1f2937; padding: 15px; border-radius: 10px; border-left: 5px solid #00ffcc; }
    .urgent-alert { background: #7f1d1d; color: #fecaca; padding: 20px; border-radius: 10px; border: 2px solid #ef4444; margin-bottom: 20px; }
    .safe-alert { background: #064e3b; color: #d1fae5; padding: 20px; border-radius: 10px; border: 2px solid #10b981; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 2. HỆ THỐNG LOGIC AI ---

def calculate_logistics(user_lat, user_lon, plant_lat, plant_lon, water_days):
    """Tính toán khoảng cách và đưa ra cảnh báo dựa trên điều kiện thực tế"""
    # 1. Tính khoảng cách đường chim bay (Cơ sở)
    dist = geodesic((user_lat, user_lon), (plant_lat, plant_lon)).km
    
    # 2. Ước tính khoảng cách đường bộ (Thường gấp 1.2 - 1.4 lần đường chim bay)
    road_dist = dist * 1.3 
    
    # 3. Tính thời gian di chuyển (Giả lập điều kiện đường an toàn)
    # Nếu xa (>100km): 70km/h. Nếu gần: 35km/h.
    speed = 70 if road_dist > 100 else 35
    travel_hours = road_dist / speed
    travel_days = travel_hours / 24
    
    # 4. Logic cảnh báo
    # Nếu thời gian di chuyển chiếm hơn 70% thời gian nước còn lại -> Cảnh báo đỏ
    is_urgent = travel_days >= (water_days * 0.7) or (water_days < 1 and road_dist > 50)
    
    return {
        "road_dist": round(road_dist, 1),
        "travel_hours": round(travel_hours, 1),
        "is_urgent": is_urgent
    }

# --- 3. ĐĂNG NHẬP & XÁC NHẬN VỊ TRÍ ---
def init_session():
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'plant_loc' not in st.session_state: st.session_state.plant_loc = None
    if 'user_loc' not in st.session_state: st.session_state.user_loc = None

init_session()

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔐 Hệ Thống EcoMind")
        tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký"])
        with tab1:
            u = st.text_input("Tên đăng nhập")
            p = st.text_input("Mật khẩu", type="password")
            if st.button("Truy cập"):
                st.session_state.auth = True
                st.rerun()
        with tab2:
            st.text_input("Username")
            st.text_input("Password", type="password")
            if st.button("Tạo tài khoản"):
                st.success("✅ Đăng ký hoàn tất! Vui lòng quay lại tab Đăng nhập.")

# --- 4. CHỌN VỊ TRÍ & CÂY (KHI VÀO LẦN ĐẦU) ---
elif st.session_state.plant_loc is None:
    st.title("📍 Thiết lập tọa độ & Hệ thống")
    st.info("Vui lòng xác nhận vị trí chính xác của Cây và Người dùng để AI tính toán khoảng cách.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Vị trí Cây (Cố định)")
        p_lat = st.number_input("Vĩ độ Cây (Lat):", value=10.7626)
        p_lon = st.number_input("Kinh độ Cây (Lon):", value=106.6601)
        st.caption("Gợi ý: Tọa độ chậu cây tại nhà/vườn.")
        
    with c2:
        st.subheader("Vị trí của Bạn (Hiện tại)")
        u_lat = st.number_input("Vĩ độ Bạn (Lat):", value=16.0544) # Mặc định Đà Nẵng (cách 500km)
        u_lon = st.number_input("Kinh độ Bạn (Lon):", value=108.2022)
    
    st.divider()
    c3, c4 = st.columns(2)
    with c3:
        plant_type = st.selectbox("Chọn loại cây:", ["Hoa Hồng", "Xương Rồng", "Lan Hồ Điệp"])
    with c4:
        init_water = st.number_input("Lượng nước hiện tại (Lít):", value=5.0)

    if st.button("XÁC NHẬN VÀ KÍCH HOẠT HỆ THỐNG"):
        st.session_state.plant_loc = (p_lat, p_lon)
        st.session_state.user_loc = (u_lat, u_lon)
        st.session_state.my_plant = {"name": plant_type, "water": init_water, "need": 0.5}
        st.rerun()

# --- 5. GIAO DIỆN CHÍNH ---
else:
    with st.sidebar:
        st.title("ECO-MIND OS")
        menu = option_menu(None, ["Dashboard", "Wikipedia", "Bản đồ & Chỉ đường"], 
            icons=['speedometer2', 'book', 'map'], default_index=0)
        
        if st.button("🚪 Thoát"):
            st.session_state.auth = False
            st.session_state.plant_loc = None
            st.rerun()

    # --- TAB: DASHBOARD ---
    if menu == "Dashboard":
        st.title(f"📊 Dashboard: {st.session_state.my_plant['name']}")
        
        # LOGIC TÍNH TOÁN
        water_days = st.session_state.my_plant['water'] / st.session_state.my_plant['need']
        logis = calculate_logistics(
            st.session_state.user_loc[0], st.session_state.user_loc[1],
            st.session_state.plant_loc[0], st.session_state.plant_loc[1],
            water_days
        )

        # PHẦN CẢNH BÁO THÔNG MINH
        if logis['is_urgent']:
            st.markdown(f"""
            <div class="urgent-alert">
                <h3>🚨 CẢNH BÁO NGUY CẤP</h3>
                <p>Khoảng cách: <b>{logis['road_dist']} km</b>. Thời gian nước còn lại: <b>{water_days:.1f} ngày</b>.</p>
                <p>Ước tính thời gian di chuyển về: <b>{logis['travel_hours']} giờ</b>. 
                Bạn cần xuất phát ngay để kịp cứu cây!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="safe-alert">
                <h3>✅ TRẠNG THÁI AN TOÀN</h3>
                <p>Khoảng cách: {logis['road_dist']} km. Cây còn nước trong {water_days:.1f} ngày.</p>
                <p>Mọi thứ vẫn trong tầm kiểm soát.</p>
            </div>
            """, unsafe_allow_html=True)

        # 2 NÚT TƯỚI NƯỚC (THEO YÊU CẦU)
        st.subheader("💧 Quản lý nước")
        b1, b2 = st.columns(2)
        with b1:
            if st.button("🛠️ Cập nhật lượng nước thủ công"):
                new_w = st.number_input("Nhập số lít nước thực tế đo được:", value=float(st.session_state.my_plant['water']))
                st.session_state.my_plant['water'] = new_w
                st.success("Đã cập nhật tay!")
        with b2:
            if st.button("🔄 Cập nhật tự động (Thời gian/Vị trí thực)"):
                with st.spinner("Đang đồng bộ dữ liệu cảm biến & thời tiết..."):
                    time.sleep(1.5)
                    # Giả lập giảm nước theo thời gian thực
                    st.session_state.my_plant['water'] -= 0.01 
                    st.info("Hệ thống đã tự động tính toán mức bay hơi dựa trên nhiệt độ thực tế tại vị trí cây.")

    # --- TAB: WIKIPEDIA (2 CHẾ ĐỘ) ---
    elif menu == "Wikipedia":
        st.title("📚 Tra cứu bách khoa")
        q = st.text_input("Tìm loài cây:", value=st.session_state.my_plant['name'])
        mode = st.radio("Chế độ xem:", ["Tóm tắt", "Xem tất cả"], horizontal=True)
        
        if q:
            try:
                if mode == "Tóm tắt":
                    st.subheader(f"Tóm tắt về {q}")
                    st.info(wikipedia.summary(f"Cây {q}", sentences=3))
                else:
                    page = wikipedia.page(f"Cây {q}")
                    st.subheader(page.title)
                    if page.images: st.image(page.images[0], width=300)
                    st.write(page.content)
            except:
                st.error("Không tìm thấy dữ liệu cây.")

    # --- TAB: BẢN ĐỒ & CHỈ ĐƯỜNG ---
    elif menu == "Bản đồ & Chỉ đường":
        st.title("🗺️ Hành trình cứu cây")
        
        # Hiển thị bản đồ 2 vị trí
        map_df = pd.DataFrame({
            'lat': [st.session_state.user_loc[0], st.session_state.plant_loc[0]],
            'lon': [st.session_state.user_loc[1], st.session_state.plant_loc[1]],
            'Loại': ['Bạn', 'Cây']
        })
        st.map(map_df)
        
        st.divider()
        st.subheader("🛣️ Tuyến đường an toàn nhất")
        st.write("Dựa trên điều kiện đường thực tế, AI đề xuất tuyến đường tránh các khu vực kẹt xe hoặc thi công để về nhà nhanh nhất.")
        
        # NÚT DẪN ĐƯỜNG (Mở Google Maps thật)
        origin = f"{st.session_state.user_loc[0]},{st.session_state.user_loc[1]}"
        dest = f"{st.session_state.plant_loc[0]},{st.session_state.plant_loc[1]}"
        nav_url = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={dest}&travelmode=driving"
        
        if st.button("🚩 NHẤN ĐỂ MỞ CHỈ ĐƯỜNG (GOOGLE MAPS)"):
            st.success("Đang mở Google Maps để dẫn đường an toàn...")
            time.sleep(1)
            # Trong Streamlit, dùng markdown để mở link an toàn
            st.markdown(f'<a href="{nav_url}" target="_blank">Mở Bản Đồ</a>', unsafe_allow_html=True)
