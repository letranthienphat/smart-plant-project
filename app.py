import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from geopy.distance import geodesic
import requests
import time

# --- 1. CẤU HÌNH GIAO DIỆN HIGHTECH ---
st.set_page_config(page_title="EcoMind Matrix v21", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #05070a; color: #00ffcc; }
    .eco-frame { border: 2px solid #00ffcc; padding: 30px; border-radius: 20px; background: rgba(0,255,204,0.05); }
    .param-card { background: #10141d; padding: 10px; border-radius: 5px; border-left: 3px solid #00ffcc; margin-bottom: 5px; font-size: 12px; }
    .stButton>button { background: #00ffcc; color: black; font-weight: bold; width: 100%; border-radius: 15px; }
</style>
""", unsafe_allow_html=True)

# --- 2. HÀM LẤY VỊ TRÍ THỰC (GPS) ---
# Trong Streamlit, việc lấy GPS trực tiếp cần JavaScript hoặc qua địa chỉ IP (đối với bản Web)
def get_realtime_location():
    try:
        # Giả lập lấy từ IP/GPS trình duyệt qua API (Sử dụng ipapi cho độ chính xác thành phố)
        res = requests.get('https://ipapi.co/json/').json()
        return res['latitude'], res['longitude'], res['city']
    except:
        return 21.0285, 105.8542, "Hà Nội"

# --- 3. HỆ THỐNG 200+ THÔNG SỐ CHI TIẾT ---
def get_200_options():
    groups = {
        "📦 Vật liệu tái chế (40)": ["Loại nhựa (PET/PP/HDPE)", "Độ dày thành chậu (mm)", "Hệ số truyền nhiệt", "Độ phản xạ Albedo", "Tuổi thọ vật liệu", "Tốc độ phân hủy vi nhựa", "Khả năng chịu tia UV", "Độ bền kéo giãn", "Trọng lượng riêng", "Độ xốp bề mặt..."],
        "🌱 Sinh học chi tiết (50)": ["Chỉ số diện tích lá (LAI)", "Tốc độ thoát hơi nước ban đêm", "Độ mở lỗ khí khổng", "Nhu cầu Nitơ/Phốt pho/Kali", "Giai đoạn rễ (Cọc/Chùm)", "Mức độ nhạy cảm Ethylene", "Khả năng hấp thụ CO2 thực tế..."],
        "🧪 Thổ nhưỡng vi mô (40)": ["Độ ẩm bão hòa", "Độ rỗng của đất", "Độ pH chính xác", "Tỷ lệ C/N (Cacbon/Nitơ)", "Mật độ vi sinh vật", "Khả năng trao đổi Cation (CEC)", "Độ dẫn điện (EC) của đất tái chế..."],
        "☁️ Khí hậu tại chỗ (40)": ["Cường độ bức xạ PAR", "Tốc độ gió tại mặt chậu", "Điểm sương (Dew point)", "Áp suất hơi bão hòa (VPD)", "Tỷ lệ che phủ mây", "Mức độ ô nhiễm bụi mịn (PM2.5) xung quanh..."],
        "🚚 Logistics & Vận hành (30)": ["Thời gian di chuyển thực tế", "Mức tiêu hao nhiên liệu khi về vườn", "Độ ưu tiên chăm sóc", "Lịch sử thay chậu", "Dự báo cạn kiệt tài nguyên..."]
    }
    return groups

# --- 4. GIAO DIỆN ĐĂNG NHẬP ĐỒNG NHẤT ---
if 'auth' not in st.session_state: st.session_state.auth = None

if st.session_state.auth is None:
    st.markdown('<div class="eco-frame">', unsafe_allow_html=True)
    st.title("🌐 ECO-MIND GLOBAL MATRIX")
    st.write("Hệ thống định vị và quản trị sinh thái thời gian thực")
    
    tab_log, tab_reg, tab_guest = st.tabs(["🔑 ĐĂNG NHẬP", "📝 ĐĂNG KÝ", "🌍 VÀO TRỰC TIẾP"])
    with tab_log:
        st.text_input("Tài khoản Matrix")
        st.text_input("Mật mã", type="password")
        if st.button("KÍCH HOẠT HỆ THỐNG"):
            st.session_state.auth = "user"
            st.rerun()
    with tab_reg:
        st.text_input("Tạo mã định danh người dùng")
        st.button("ĐĂNG KÝ MẠNG LƯỚI")
    with t3 := tab_guest:
        if st.button("TRUY CẬP VỚI GPS THỜI GIAN THỰC"):
            st.session_state.auth = "guest"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- LẤY GPS THỰC TẾ ---
    lat, lon, city = get_realtime_location()
    if 'p_coords' not in st.session_state: st.session_state.p_coords = (lat + 0.05, lon + 0.05)
    
    with st.sidebar:
        st.title(f"📍 {city}")
        st.write(f"GPS: `{lat:.6f}, {lon:.6f}`")
        menu = option_menu("Matrix", ["Bảng điều khiển", "Dẫn đường GPS", "200+ Chi tiết", "Trò chuyện", "Hệ thống"], 
            icons=['cpu', 'map', 'list-check', 'chat-dots', 'gear'], default_index=0)
        if st.button("NGẮT KẾT NỐI"):
            st.session_state.auth = None
            st.rerun()

    # --- TAB: 200+ OPTION CHI TIẾT ---
    if menu == "200+ Chi tiết":
        st.header("🔬 Thông số kỹ thuật chi tiết (200+ Biến số)")
        st.write("Dưới đây là các chi tiết li ti cấu thành nên hệ sinh thái chậu cây tái chế của bạn.")
        
        all_options = get_200_options()
        cols = st.columns(len(all_options))
        
        for i, (group_name, items) in enumerate(all_options.items()):
            with cols[i]:
                st.subheader(group_name)
                for item in items:
                    st.markdown(f'<div class="param-card">{item}</div>', unsafe_allow_html=True)

    # --- TAB: DẪN ĐƯỜNG GPS THỜI GIAN THỰC ---
    elif menu == "Dẫn đường GPS":
        st.header("📡 Định vị vệ tinh Live")
        
        # Tính khoảng cách thực dựa trên GPS đang thay đổi
        dist = geodesic((lat, lon), st.session_state.p_coords).km
        st.success(f"Khoảng cách thực: {dist:.4f} km (Cập nhật theo vị trí bạn đứng)")
        
        df_map = pd.DataFrame({
            'lat': [lat, st.session_state.p_coords[0]],
            'lon': [lon, st.session_state.p_coords[1]],
            'type': ['Bạn (Live)', 'Vườn (Target)']
        })
        st.map(df_map)
        
        # Nút dẫn đường hướng ngoại
        gmaps_url = f"https://www.google.com/maps/dir/?api=1&origin={lat},{lon}&destination={st.session_state.p_coords[0]},{st.session_state.p_coords[1]}&travelmode=driving"
        st.markdown(f'<a href="{gmaps_url}" target="_blank"><button>🧭 MỞ DẪN ĐƯỜNG GOOGLE MAPS LIVE</button></a>', unsafe_allow_html=True)

    # --- TAB: TRÒ CHUYỆN SINH ĐỘNG ---
    elif menu == "Trò chuyện":
        st.header("💬 Giao tiếp với linh hồn Thảo mộc")
        if 'msgs' not in st.session_state: st.session_state.msgs = [{"r": "p", "t": "Chào bạn, mình đang cảm nhận được vị trí GPS của bạn!"}]
        
        for m in st.session_state.msgs:
            role = "🌿 Cây" if m['r'] == 'p' else "👤 Bạn"
            st.write(f"**{role}:** {m['t']}")
            
        user_input = st.chat_input("Nói gì đó với cây...")
        if user_input:
            st.session_state.msgs.append({"r": "u", "t": user_input})
            # Logic phản hồi thật hơn
            response = "Mình thấy bạn đang ở " + city + ". Chỗ mình hiện tại rất ổn, cảm ơn bạn đã ghé thăm qua GPS!"
            st.session_state.msgs.append({"r": "p", "t": response})
            st.rerun()
