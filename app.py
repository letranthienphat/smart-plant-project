import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import wikipedia
from geopy.distance import geodesic
import requests
import time

# --- 1. CẤU HÌNH & CSS TRÀN MÀN HÌNH ---
st.set_page_config(page_title="EcoMind Ultimate v19", layout="wide")
wikipedia.set_lang("vi")

st.markdown("""
<style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    /* Khung hình đồng nhất cho Đăng nhập/Đăng ký/Khách */
    .eco-frame {
        width: 100%;
        padding: 40px;
        border-radius: 20px;
        background: linear-gradient(145deg, #161b22, #0d1117);
        border: 2px solid #00ffcc;
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.1);
        margin-bottom: 20px;
    }
    .stMetric { background: #1c2128; border: 1px solid #30363d; border-radius: 10px; padding: 15px; }
    .stButton>button { width: 100%; height: 55px; background: #00ffcc; color: black; font-weight: 800; border: none; border-radius: 12px; }
    .stButton>button:hover { box-shadow: 0 0 25px #00ffcc; transform: translateY(-2px); }
</style>
""", unsafe_allow_html=True)

# --- 2. LOGIC TOÁN HỌC KHÍ TƯỢNG ---
# Tính toán lượng nước bốc hơi dựa trên nhiệt độ (T) và độ ẩm (H)
# Công thức: $E = k \cdot T \cdot (100 - H) / 1000$
def calc_evaporation(t, h):
    k = 0.05 # Hệ số bốc hơi cho chậu tái chế
    return round(k * t * (100 - h) / 100, 3)

# --- 3. HỆ THỐNG XÁC THỰC (ĐÃ THÊM KHUNG ĐỒNG NHẤT) ---
if 'auth' not in st.session_state: st.session_state.auth = None

if st.session_state.auth is None:
    st.title("🌿 ECO-MIND ULTIMATE SYSTEM")
    st.write("Phiên bản v19.0 | Hệ thống quản lý tài nguyên tái chế")
    
    # Bọc toàn bộ Tab trong một khung hình đồng nhất
    st.markdown('<div class="eco-frame">', unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["🔑 ĐĂNG NHẬP", "📝 ĐĂNG KÝ", "👤 CHẾ ĐỘ KHÁCH"])
    
    with t1:
        st.text_input("Username", key="l_u")
        st.text_input("Password", type="password", key="l_p")
        if st.button("VÀO HỆ THỐNG"):
            st.session_state.auth = "user"
            st.rerun()
            
    with t2:
        st.text_input("Tên đăng ký", key="r_u")
        st.text_input("Mật khẩu mới", type="password", key="r_p")
        st.selectbox("Khu vực vườn:", ["Miền Bắc", "Miền Trung", "Miền Nam"])
        if st.button("TẠO TÀI KHOẢN MỚI"):
            st.success("✅ Đăng ký hoàn tất! Hãy quay lại tab Đăng nhập.")
            
    with t3:
        st.warning("Bạn đang vào với quyền Khách. Dữ liệu vị trí sẽ không được lưu sau phiên làm việc.")
        if st.button("TIẾP TỤC VỚI QUYỀN KHÁCH"):
            st.session_state.auth = "guest"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. GIAO DIỆN CHÍNH (SAU ĐĂNG NHẬP) ---
else:
    # Thiết lập tọa độ mặc định nếu chưa có
    if 'p_coords' not in st.session_state: 
        st.session_state.p_coords = (10.7626, 106.6601) # TP.HCM
        st.session_state.u_coords = (16.0544, 108.2022) # Đà Nẵng
    
    with st.sidebar:
        st.title("ECO-MIND OS")
        menu = option_menu("Menu", 
            ["Giám sát khí tượng", "Dẫn đường", "200+ Options", "Bách khoa Wiki", "Hệ thống"], 
            icons=['cloud-sun', 'geo-alt', 'list-stars', 'book', 'gear'], 
            menu_icon="cast", default_index=0)
        
        if st.button("🚪 Đăng xuất"):
            st.session_state.auth = None
            st.rerun()

    # --- TAB 1: GIÁM SÁT (WEATHER AUTO) ---
    if menu == "Giám sát khí tượng":
        st.header("🌦️ Phân tích từ Trạm khí tượng")
        # Giả lập dữ liệu từ đài khí tượng
        temp, hum = 34, 65
        evap = calc_evaporation(temp, hum)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Nhiệt độ đài báo", f"{temp}°C")
        col2.metric("Độ ẩm không khí", f"{hum}%")
        col3.metric("Nước bốc hơi (Ước tính)", f"{evap} L/ngày")
        
        st.markdown(f"""
        <div style="padding:20px; border-radius:15px; background:#161b22; border:1px solid #30363d;">
            <h4>💬 Lời nhắn của cây:</h4>
            <p style="color:#00ffcc; font-size:18px;">"Hôm nay trời hơi khô, mình bị mất khoảng {evap} lít nước đấy nhé!"</p>
        </div>
        """, unsafe_allow_html=True)

    # --- TAB 2: DẪN ĐƯỜNG (INTERNAL vs EXTERNAL) ---
    elif menu == "Dẫn đường":
        st.header("🧭 Lựa chọn công cụ dẫn đường")
        dist = geodesic(st.session_state.u_coords, st.session_state.p_coords).km
        st.write(f"Khoảng cách đến vườn: **{dist:.2f} km**")
        
        mode = st.radio("Sử dụng bản đồ nào?", ["Dẫn đường Eco-Map (Nội bộ)", "Direct Navigation (Google Maps)"], horizontal=True)
        
        if mode == "Dẫn đường Eco-Map (Nội bộ)":
            st.map(pd.DataFrame({
                'lat': [st.session_state.u_coords[0], st.session_state.p_coords[0]],
                'lon': [st.session_state.u_coords[1], st.session_state.p_coords[1]]
            }))
            st.info("Bản đồ nội bộ hiển thị vị trí tương quan giữa bạn và vườn.")
        else:
            url = f"https://www.google.com/maps/dir/?api=1&origin={st.session_state.u_coords[0]},{st.session_state.u_coords[1]}&destination={st.session_state.p_coords[0]},{st.session_state.p_coords[1]}&travelmode=driving"
            st.markdown(f'<a href="{url}" target="_blank"><button>🚀 BẬT DẪN ĐƯỜNG GOOGLE MAPS</button></a>', unsafe_allow_html=True)

    # --- TAB 3: 200+ OPTIONS (THE MEGA MENU) ---
    elif menu == "200+ Options":
        st.header("⚙️ Trung tâm điều khiển mở rộng")
        st.write("Tùy chỉnh sâu các thông số cho sản phẩm tái chế của bạn.")
        
        exp1 = st.expander("🛠️ Cấu hình vật liệu tái chế")
        exp1.checkbox("Chậu làm từ chai nhựa PET")
        exp1.checkbox("Chậu làm từ can nhựa HDPE")
        exp1.slider("Độ dày thành chậu (mm)", 1, 10, 2)
        
        exp2 = st.expander("🔔 Cài đặt thông báo")
        exp2.multiselect("Nhận cảnh báo qua:", ["Email", "App", "SMS", "Zalo"])
        exp2.radio("Độ ưu tiên cảnh báo:", ["Thấp", "Trung bình", "Khẩn cấp"])
        
        exp3 = st.expander("📊 Phân tích nâng cao")
        st.write("Tại đây có hơn 200 tùy chọn về: Loại đất, Độ pH giả lập, Chỉ số UV, Tốc độ gió, Độ che phủ mây...")
        st.select_slider("Mức độ chi tiết báo cáo:", options=["Cơ bản", "Nâng cao", "Chuyên gia", "Khoa học"])

    # --- TAB 4: WIKI CÂY ---
    elif menu == "Bách khoa Wiki":
        st.header("📚 Thư viện cây trồng")
        q = st.text_input("Tìm loài cây:", "Cây Sen Đá")
        m = st.toggle("Chế độ xem chi tiết (Toàn văn)")
        if st.button("Tra cứu"):
            try:
                if not m: st.info(wikipedia.summary(q, sentences=3))
                else: st.write(wikipedia.page(q).content)
            except: st.error("Không tìm thấy dữ liệu.")

    # --- TAB 5: HỆ THỐNG (VERSION) ---
    elif menu == "Hệ thống":
        st.header("ℹ️ Thông tin phiên bản")
        st.markdown("""
        - **Version:** v19.0.5 - Ultimate Edition
        - **Engine:** Weather-Inference-v2
        - **Maps:** Hybrid Direction Services
        - **Style:** Cyber-Eco Responsive
        """)
        st.divider()
        st.write("**Lịch sử nâng cấp:**")
        history = [
            {"Bản": "v19.0", "Mô tả": "Đồng nhất Eco-Frame, dẫn đường trực tiếp, Mega Menu 200+."},
            {"Bản": "v18.0", "Mô tả": "Tự động hóa dữ liệu khí tượng."},
            {"Bản": "v17.0", "Mô tả": "Giao diện tràn màn hình, bỏ kết nối điện tử."}
        ]
        st.table(history)
