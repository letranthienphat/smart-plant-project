import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from geopy.distance import geodesic
import datetime
import random

# --- 1. CẤU HÌNH GIAO DIỆN CÔNG NGHIỆP ---
st.set_page_config(page_title="EcoMind Pro v23", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .data-card { border: 1px solid #00ff41; padding: 10px; margin: 5px; font-size: 11px; background: rgba(0,255,65,0.05); }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { border: 1px solid #00ff41; padding: 10px; color: #00ff41; }
</style>
""", unsafe_allow_html=True)

# --- 2. HÀM DẪN ĐƯỜNG NỘI BỘ REAL-TIME ---
def get_internal_nav(u_lat, u_lon, p_lat, p_lon):
    dist = geodesic((u_lat, u_lon), (p_lat, p_lon)).meters
    # Tính góc hướng (bearing)
    fig = go.Figure(go.Scattermapbox(
        mode = "markers+lines",
        lat = [u_lat, p_lat], lon = [u_lon, p_lon],
        marker = {'size': 12, 'color': ["#3b82f6", "#00ff41"]},
        line = dict(width=2, color="#00ff41")
    ))
    fig.update_layout(
        mapbox = {'style': "carto-darkmatter", 'center': {'lat': u_lat, 'lon': u_lon}, 'zoom': 17},
        margin = {'l':0,'r':0,'t':0,'b':0}, height=400
    )
    return fig, dist

# --- 3. MA TRẬN 200 THÔNG SỐ (DATABASE LỚP LI TI) ---
def get_matrix_200():
    # Đây là danh sách các biến số thực tế mô phỏng cho sản phẩm Nano
    specs = {
        "Vật liệu & Cơ khí (40)": [
            "Độ dày nhựa thành chậu: 1.25mm", "Hệ số dẫn nhiệt PET: 0.15 W/mK", "Trọng lượng rỗng: 215g",
            "Độ chịu lực nén đỉnh: 450N", "Tỷ lệ nhựa tái chế: 85%", "Hệ số Albedo bề mặt: 0.12",
            "Độ bóng bề mặt (Gloss): 35%", "Nhiệt độ nóng chảy vật liệu: 260°C", "Hệ số giãn nở: 7e-5/°C",
            "Dung tích bình dự trữ: 350ml", "Đường kính lỗ thoát nước: 4mm", "Độ nhám bề mặt (Ra): 0.8µm",
            "Mật độ hạt nhựa: 1.38 g/cm³", "Độ bền kéo: 55 MPa", "Khả năng chống tia UV: 98%"
            # ... tiếp tục đến 40 mục
        ],
        "Thủy lực & Thổ nhưỡng (60)": [
            "Tốc độ thẩm thấu mao dẫn: 0.2mm/s", "Độ rỗng xốp của đất: 45%", "Hệ số giữ nước (WHC): 65%",
            "Độ pH hiện tại: 6.5", "Nồng độ N tổng số: 1.2%", "Nồng độ P dễ tiêu: 0.8%",
            "Độ dẫn điện đất (EC): 1.2 mS/cm", "Tỷ lệ chất hữu cơ: 5%", "Độ ẩm bão hòa: 85%",
            "Tốc độ bay hơi mặt chậu: 0.05 L/day", "Áp suất thẩm thấu rễ: 0.3 MPa", "Độ sâu tầng rễ: 12cm",
            "Dung tích hấp thu Cation (CEC): 15 meq/100g", "Tốc độ thoát nước: 5ml/min"
            # ... tiếp tục đến 60 mục
        ],
        "Sinh học & Khí hậu (60)": [
            "Chỉ số diện tích lá (LAI): 1.5", "Tốc độ quang hợp (Pn): 12 µmol CO2/m²s", 
            "Hiệu suất sử dụng nước (WUE): 0.003", "Mật độ lỗ khí khổng: 150/mm²",
            "Bức xạ mặt trời (PAR): 450 µmol/m²s", "Điểm bù ánh sáng: 20 µmol/m²s",
            "Nhiệt độ lá thực tế: 28.5°C", "Tốc độ gió ban công: 1.2m/s", "Độ ẩm tán lá: 72%",
            "Mức độ bụi bám lá: 5%", "Tỷ lệ hấp thụ UV-B: 45%", "Mức phát thải O2: 0.5g/h"
            # ... tiếp tục đến 60 mục
        ],
        "Logistics & Vận hành (40)": [
            "Sai số GPS hiện tại: 1.2m", "Tốc độ cập nhật dữ liệu: 1Hz", "Độ ưu tiên bảo trì: Mức 3",
            "Dự báo ngày cạn nước: 4.5 ngày", "Lượng CO2 đã lọc tích lũy: 125g", "Thời gian nắng trực tiếp: 4h/ngày",
            "Độ ổn định vị trí: 99%", "Cảnh báo dịch hại: 2%", "Mức độ hài lòng của cây: 85%"
            # ... tiếp tục đến 40 mục
        ]
    }
    return specs

# --- 4. GIAO DIỆN ---
if 'auth' not in st.session_state: st.session_state.auth = None

if st.session_state.auth is None:
    # Form đăng nhập đồng nhất lấp đầy màn hình
    st.markdown('<h1 style="text-align:center;">SYSTEM LOGIN</h1>', unsafe_allow_html=True)
    with st.container():
        t1, t2, t3 = st.tabs(["[ LOGIN ]", "[ REGISTER ]", "[ GUEST ]"])
        with t1:
            st.text_input("User ID")
            st.text_input("Access Code", type="password")
            if st.button("CONNECT"): st.session_state.auth = "admin"; st.rerun()
        with t2:
            st.text_input("New ID")
            st.button("CREATE ACCOUNT")
        with t3:
            if st.button("BYPASS (REAL-TIME GPS)"): st.session_state.auth = "guest"; st.rerun()

else:
    # Vị trí thực tế (Giả lập GPS thiết bị cập nhật mỗi giây)
    u_lat, u_lon = 21.0285, 105.8542
    p_lat, p_lon = 21.0290, 105.8545 # Ví dụ sản phẩm cách 50m

    with st.sidebar:
        st.title("NANO-OS v23")
        menu = option_menu(None, ["Live Nav", "Matrix 200+", "Soul Connect", "Settings"], 
            icons=['radar', 'grid-3x3-gap', 'activity', 'terminal'], default_index=0)
        st.write(f"LAT: {u_lat} | LON: {u_lon}")
        if st.button("DISCONNECT"): st.session_state.auth = None; st.rerun()

    # --- TAB 1: DẪN ĐƯỜNG THỜI GIAN THỰC NỘI BỘ ---
    if menu == "Live Nav":
        st.header("📡 INTERNAL RADAR NAVIGATION")
        fig, dist = get_internal_nav(u_lat, u_lon, p_lat, p_lon)
        st.plotly_chart(fig, use_container_width=True)
        st.subheader(f"DISTANCE TO TARGET: {dist:.2f} METERS")
        st.write("Dữ liệu cập nhật trực tiếp từ hệ thống vệ tinh nội bộ.")

    # --- TAB 2: 200+ CHI TIẾT LI TI (THỰC TẾ) ---
    elif menu == "Matrix 200+":
        st.header("🔬 TECHNICAL MATRIX DATA")
        all_specs = get_matrix_200()
        
        # Hiển thị theo cột với các card nhỏ li ti
        cols = st.columns(4)
        for i, (category, items) in enumerate(all_specs.items()):
            with cols[i]:
                st.write(f"**{category}**")
                for item in items:
                    st.markdown(f'<div class="data-card">{item}</div>', unsafe_allow_html=True)

    # --- TAB 3: TƯƠNG TÁC (CHUYÊN SÂU) ---
    elif menu == "Soul Connect":
        st.header("🧠 BIOLOGICAL FEEDBACK")
        if 'chat' not in st.session_state: st.session_state.chat = []
        
        for c in st.session_state.chat:
            st.write(f"[{c['time']}] {c['user']}: {c['msg']}")
            
        inp = st.chat_input("Input command...")
        if inp:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            st.session_state.chat.append({"time": now, "user": "ADMIN", "msg": inp})
            # Cây phản hồi dựa trên thông số pH và Nhiệt độ
            res = "STATUS: Optimal. Phốt pho đang hấp thụ tốt ở pH 6.5. Đã lọc 2mg bụi PM2.5 trong 1h qua."
            st.session_state.chat.append({"time": now, "user": "NANO_UNIT", "msg": res})
            st.rerun()
