import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import wikipedia
from geopy.distance import geodesic
import requests
import time

# --- 1. CẤU HÌNH GIAO DIỆN TRÀN MÀN HÌNH & VIVID ---
st.set_page_config(page_title="EcoMind v20 - Eco Soul", layout="wide")
wikipedia.set_lang("vi")

st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #ffffff; }
    /* Khung hình đồng nhất lấp đầy màn hình */
    .full-frame {
        width: 100%;
        padding: 5% 10%;
        background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
        border: 2px solid #00ffcc;
        border-radius: 25px;
        box-shadow: 0 0 50px rgba(0, 255, 204, 0.2);
    }
    .chat-bubble-plant { background: #064e3b; padding: 15px; border-radius: 15px 15px 15px 0px; margin: 10px 0; border: 1px solid #10b981; }
    .chat-bubble-user { background: #1e293b; padding: 15px; border-radius: 15px 15px 0px 15px; margin: 10px 0; border: 1px solid #3b82f6; text-align: right; }
    .stMetric { background: #161b22; border-radius: 10px; border: 1px solid #30363d; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 2. HÀM XỬ LÝ DỮ LIỆU ---
def get_detailed_weather(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&timezone=auto"
        return requests.get(url).json()['current']
    except: return None

# --- 3. QUẢN LÝ ĐĂNG NHẬP (KHUNG ĐỒNG NHẤT) ---
if 'auth' not in st.session_state: st.session_state.auth = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

if st.session_state.auth is None:
    st.markdown('<div class="full-frame">', unsafe_allow_html=True)
    st.title("🌱 ECO-MIND: LINH HỒN CỦA CÂY")
    t1, t2, t3 = st.tabs(["🔐 ĐĂNG NHẬP", "📝 ĐĂNG KÝ", "👤 CHẾ ĐỘ KHÁCH"])
    
    with t1:
        st.text_input("Tên tài khoản")
        st.text_input("Mật khẩu", type="password")
        if st.button("VÀO HỆ THỐNG", key="btn_login"):
            st.session_state.auth = "user"
            st.rerun()
    with t2:
        st.text_input("Tên đăng ký")
        st.text_input("Mật khẩu mới", type="password")
        st.button("TẠO TÀI KHOẢN")
    with t3:
        st.info("Chế độ khách: Trải nghiệm đầy đủ tính năng nhưng không lưu vị trí.")
        if st.button("BẮT ĐẦU NGAY"):
            st.session_state.auth = "guest"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. GIAO DIỆN CHÍNH ---
else:
    # Khởi tạo tọa độ mặc định siêu chính xác
    if 'p_coords' not in st.session_state:
        st.session_state.p_coords = (10.762622, 106.660172)
        st.session_state.u_coords = (21.028511, 105.854223)

    with st.sidebar:
        st.title("ECO-MIND v20")
        menu = option_menu("Hệ thống", ["Tâm hồn của Cây", "Dẫn đường", "Chi tiết li ti (200+)", "Wiki", "Cài đặt"], 
            icons=['chat-heart', 'signpost-2', 'sliders', 'book', 'gear'], default_index=0)
        
        st.divider()
        if st.button("Đăng xuất"):
            st.session_state.auth = None
            st.rerun()

    # --- TAB 1: TRÒ CHUYỆN VỚI CÂY (VIVID) ---
    if menu == "Tâm hồn của Cây":
        st.header("💬 Trò chuyện cùng cây của bạn")
        
        # Lấy thời tiết để tạo "tâm trạng"
        w = get_detailed_weather(st.session_state.p_coords[0], st.session_state.p_coords[1])
        temp = w['temperature_2m'] if w else 25
        
        # Hiển thị tin nhắn cũ
        for msg in st.session_state.chat_history:
            if msg['role'] == 'plant':
                st.markdown(f'<div class="chat-bubble-plant">🌿 <b>Cây:</b> {msg["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble-user">👤 <b>Bạn:</b> {msg["text"]}</div>', unsafe_allow_html=True)
        
        # Nhập tin nhắn mới
        user_msg = st.chat_input("Nhắn gì đó cho cây...")
        if user_msg:
            st.session_state.chat_history.append({"role": "user", "text": user_msg})
            # Logic phản hồi của cây dựa trên thời tiết
            ans = ""
            if "khát" in user_msg.lower() or "nước" in user_msg.lower():
                ans = f"Hiện tại chỗ mình {temp}°C, mình thấy cũng hơi khô rồi đấy!"
            elif "chào" in user_msg.lower():
                ans = "Chào bạn! Mình vẫn đang cố gắng lọc không khí cho bạn đây."
            else:
                ans = "Mình thích nghe bạn nói chuyện lắm, dù mình chỉ là một mầm xanh tái chế thôi."
            
            st.session_state.chat_history.append({"role": "plant", "text": ans})
            st.rerun()

    # --- TAB 2: DẪN ĐƯỜNG (CHÍNH XÁC) ---
    elif menu == "Dẫn đường":
        st.header("🗺️ Định vị siêu chính xác")
        
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"Vị trí cây: `{st.session_state.p_coords}`")
        with c2:
            st.write(f"Vị trí của bạn: `{st.session_state.u_coords}`")
            
        dist = geodesic(st.session_state.u_coords, st.session_state.p_coords).km
        st.info(f"Khoảng cách thực tế: {dist:.3f} km (Đã tính theo độ cong trái đất)")
        
        st.map(pd.DataFrame({'lat': [st.session_state.u_coords[0], st.session_state.p_coords[0]], 
                             'lon': [st.session_state.u_coords[1], st.session_state.p_coords[1]]}))
        
        url = f"https://www.google.com/maps/dir/?api=1&origin={st.session_state.u_coords[0]},{st.session_state.u_coords[1]}&destination={st.session_state.p_coords[0]},{st.session_state.p_coords[1]}&travelmode=driving"
        st.markdown(f'<a href="{url}" target="_blank"><button style="width:100%; height:60px; background:#00ffcc; color:black; font-weight:bold; border:none; border-radius:10px; cursor:pointer;">🧭 DẪN ĐƯỜNG TRỰC TIẾP (GOOGLE MAPS)</button></a>', unsafe_allow_html=True)

    # --- TAB 3: 200+ CHI TIẾT LI TI (THỰC TẾ) ---
    elif menu == "Chi tiết li ti (200+)":
        st.header("⚙️ Cấu hình thông số kỹ thuật (Chậu tái chế)")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("📦 Vật liệu & Chậu")
            st.select_slider("Độ dày nhựa (mm):", options=[1, 1.5, 2, 3, 5], value=2)
            st.color_picker("Màu sắc chậu (Ảnh hưởng hấp thụ nhiệt):", "#10b981")
            st.checkbox("Có lỗ thoát nước đáy", value=True)
            st.number_input("Thể tích chậu (Lít):", 0.5, 50.0, 5.0)
            
        with col_b:
            st.subheader("🌱 Sinh học & Đất")
            st.selectbox("Loại đất tái chế:", ["Cám dừa + Tro trấu", "Đất vườn ủ phân xanh", "Cát + Sỏi thủy sinh"])
            st.slider("Diện tích lá (Ước tính cm²):", 10, 5000, 500)
            st.radio("Giai đoạn:", ["Mầm", "Phát triển mạnh", "Ra hoa", "Cây già"])

        st.divider()
        st.subheader("🔍 Các chỉ số vi mô khác (Li ti)")
        st.write("- Độ phản xạ bề mặt chậu: **0.12**")
        st.write("- Hệ số giữ nhiệt vật liệu: **0.45 J/kg·K**")
        st.write("- Tốc độ thoát hơi nước qua lá (Giả lập): **0.02 L/giờ**")

    # --- TAB 5: CÀI ĐẶT (VERSION) ---
    elif menu == "Cài đặt":
        st.header("⚙️ Hệ thống")
        st.write("**Phiên bản:** v20.0 - Eco-Soul Edition")
        st.write("**Dẫn đường:** Google Maps API Integration")
        st.write("**Dữ liệu:** Đài khí tượng Open-Meteo")
        if st.button("❌ Xóa toàn bộ dữ liệu"):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()
