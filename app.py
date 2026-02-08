import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from geopy.distance import geodesic
import requests
import datetime

# --- 1. CẤU HÌNH & GIAO DIỆN TRÀN MÀN HÌNH ---
st.set_page_config(page_title="EcoMind Urban Core v25", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0a0c10; color: #00ffcc; }
    .main-frame { border: 2px solid #00ffcc; padding: 25px; border-radius: 20px; background: rgba(0, 255, 204, 0.03); box-shadow: 0 0 20px rgba(0,255,204,0.1); }
    .stMetric { background: #161b22 !important; border-radius: 10px !important; border: 1px solid #30363d !important; }
    .chat-bubble { padding: 10px; border-radius: 10px; margin-bottom: 5px; border-left: 4px solid #00ffcc; background: #1c2128; }
    .stButton>button { border-radius: 10px; height: 3em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 2. HỆ THỐNG DẪN ĐƯỜNG NỘI BỘ (REAL-TIME NAV) ---
def build_radar_map(u_lat, u_lon, p_lat, p_lon):
    fig = go.Figure(go.Scattermapbox(
        lat=[u_lat, p_lat], lon=[u_lon, p_lon],
        mode='markers+lines',
        marker=dict(size=[15, 25], color=['#3b82f6', '#00ffcc'], symbol=['circle', 'garden']),
        line=dict(width=4, color='#00ffcc'),
        text=['BẠN', 'SẢN PHẨM ECO'],
    ))
    fig.update_layout(
        mapbox=dict(style="carto-darkmatter", center=dict(lat=u_lat, lon=u_lon), zoom=16),
        margin=dict(l=0, r=0, t=0, b=0), height=450, paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# --- 3. LOGIC ĐĂNG NHẬP (CẤU TRÚC CHUẨN) ---
if 'auth' not in st.session_state: st.session_state.auth = None

if st.session_state.auth is None:
    st.markdown('<div class="main-frame">', unsafe_allow_html=True)
    st.title("🏙️ ECO-MIND: URBAN CORE v25")
    t1, t2, t3 = st.tabs(["🔐 TRUY CẬP", "📝 ĐĂNG KÝ", "🌍 KHÁCH TỰ DO"])
    with t1:
        st.text_input("Tài khoản người dùng")
        st.text_input("Mật khẩu", type="password")
        if st.button("KÍCH HOẠT HỆ THỐNG"): st.session_state.auth = "admin"; st.rerun()
    with t2:
        st.text_input("Họ và tên")
        st.text_input("Email liên kết")
        st.button("TẠO TÀI KHOẢN")
    with t3:
        st.info("Chế độ này sử dụng tọa độ GPS thực tế của trình duyệt.")
        if st.button("VÀO TRỰC TIẾP"): st.session_state.auth = "guest"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # GPS Giả lập thời gian thực (Cần kết nối API GPS thật nếu deploy)
    u_lat, u_lon = 21.0285, 105.8542
    p_lat, p_lon = 21.0295, 105.8555

    with st.sidebar:
        st.title("ECO-MIND OS")
        menu = option_menu(None, ["Radar Dẫn đường", "Sức khỏe Cây", "Chat & Nhật ký", "Chợ Tái chế", "Wiki & Cài đặt"], 
            icons=['compass', 'heart-pulse', 'chat-quote', 'shop', 'gear'], default_index=0)
        st.divider()
        st.metric("Khoảng cách", f"{geodesic((u_lat, u_lon), (p_lat, p_lon)).meters:.1f} m")
        if st.button("Đăng xuất"): st.session_state.auth = None; st.rerun()

    # --- TAB 1: RADAR DẪN ĐƯỜNG (INTERNAL) ---
    if menu == "Radar Dẫn đường":
        st.header("🧭 Radar Định vị Nano")
        st.plotly_chart(build_radar_map(u_lat, u_lon, p_lat, p_lon), use_container_width=True)
        st.success("Hệ thống dẫn đường nội bộ đang hoạt động. Đi theo đường Neon xanh.")

    # --- TAB 2: SỨC KHỎE CÂY (AI WEATHER) ---
    elif menu == "Sức khỏe Cây":
        st.header("📊 Phân tích Sức khỏe (Không cảm biến)")
        col1, col2, col3 = st.columns(3)
        col1.metric("Bức xạ UV (Dự báo)", "Cao (7/10)")
        col2.metric("Nước bốc hơi", "150ml/ngày")
        col3.metric("Dự kiến cạn nước", "3 ngày tới")
        
        st.markdown("""
        **🔍 Phân tích AI:**
        - Vì bạn đặt cây ở hướng Tây, lượng nắng chiều đang làm tăng nhiệt độ chậu nhựa PET.
        - **Khuyến nghị:** Di chuyển chậu vào sâu trong ban công thêm 20cm để giảm 5°C nhiệt độ đất.
        """)
        

    # --- TAB 3: CHAT & NHẬT KÝ ---
    elif menu == "Chat & Nhật ký":
        st.header("💬 Tương tác & Nhật ký Eco")
        c1, c2 = st.columns([2, 1])
        with c1:
            st.subheader("Trò chuyện")
            if 'msgs' not in st.session_state: st.session_state.msgs = []
            for m in st.session_state.msgs:
                st.markdown(f'<div class="chat-bubble"><b>{m["u"]}:</b> {m["t"]}</div>', unsafe_allow_html=True)
            txt = st.chat_input("Nhắn cho cây...")
            if txt:
                st.session_state.msgs.append({"u": "Bạn", "t": txt})
                st.session_state.msgs.append({"u": "Cây", "t": "Mình cảm nhận được nắng đang lên, cảm ơn bạn đã quan tâm!"})
                st.rerun()
        with c2:
            st.subheader("Nhật ký Cây")
            st.write("📅 *Hôm qua:* Nắng gắt, mình đã lọc được 50mg CO2.")
            st.write("📅 *Hôm nay:* Trời dịu, mình đang ra thêm 1 mầm nhỏ.")

    # --- TAB 4: CHỢ TÁI CHẾ (NEW FEATURE) ---
    elif menu == "Chợ Tái chế":
        st.header("♻️ Cộng đồng Tái chế Thành phố")
        st.info("Nơi trao đổi vật liệu nâng cấp cho sản phẩm Nano của bạn.")
        st.table(pd.DataFrame([
            {"Vật liệu": "Can nhựa HDPE 5L", "Khoảng cách": "500m", "Tình trạng": "Sẵn sàng"},
            {"Vật liệu": "Lưới lọc nước cũ", "Khoảng cách": "1.2km", "Tình trạng": "Đã đặt chỗ"},
            {"Vật liệu": "Phân bón hữu cơ ủ tại nhà", "Khoảng cách": "200m", "Tình trạng": "Sẵn sàng"}
        ]))
        st.button("Đăng tin trao đổi vật liệu")

    # --- TAB 5: WIKI & CÀI ĐẶT ---
    elif menu == "Wiki & Cài đặt":
        st.header("⚙️ Cấu hình Hệ thống")
        with st.expander("Bách khoa toàn thư Cây Nano"):
            st.write("Tra cứu cách chăm sóc các loại cây phù hợp với không gian nhỏ.")
        st.write("**Phiên bản:** Ultimate v25.0")
        st.write("**Chủ sở hữu:** Admin")
        if st.button("⚠️ XÓA DỮ LIỆU"): st.rerun()
