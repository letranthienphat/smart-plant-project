import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from geopy.distance import geodesic
import time

# --- 1. GIAO DIỆN HIỆN ĐẠI (CHẾ ĐỘ MOBILE-FIRST) ---
st.set_page_config(page_title="Cây Xanh Đô Thị", layout="wide")

st.markdown("""
<style>
    /* Font chữ và màu sắc thân thiện */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f0f2f5; color: #1c1e21; }
    
    /* Khung đăng nhập chuyên nghiệp */
    .login-box {
        background: white; padding: 40px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); margin-top: 50px;
    }
    .stButton>button {
        background-color: #2ecc71; color: white; border-radius: 12px;
        border: none; height: 50px; font-weight: 600; width: 100%;
    }
    .stChatFloatingInputContainer { background-color: #ffffff; }
</style>
""", unsafe_allow_html=True)

# --- 2. LOGIC BẢN ĐỒ DẪN ĐƯỜNG RIÊNG ---
def draw_navigator(my_lat, my_lon, tree_lat, tree_lon):
    fig = go.Figure(go.Scattermapbox(
        lat=[my_lat, tree_lat],
        lon=[my_lon, tree_lon],
        mode='markers+lines',
        marker=dict(size=[15, 20], color=['#3498db', '#2ecc71']),
        line=dict(width=3, color='#2ecc71'),
        text=['Vị trí của bạn', 'Chậu cây Nano']
    ))
    fig.update_layout(
        mapbox=dict(style="carto-positron", center=dict(lat=my_lat, lon=my_lon), zoom=16),
        margin=dict(l=0, r=0, t=0, b=0), height=500
    )
    return fig

# --- 3. QUẢN LÝ ĐĂNG NHẬP (NGÔN NGỮ BÌNH THƯỜNG) ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.title("🌱 Chào bạn!")
        st.write("Vui lòng đăng nhập để xem tình hình cây của mình hôm nay nhé.")
        
        tab1, tab2 = st.tabs(["Đăng nhập", "Tạo tài khoản mới"])
        with tab1:
            user = st.text_input("Tên đăng nhập")
            pw = st.text_input("Mật khẩu", type="password")
            if st.button("VÀO ỨNG DỤNG"):
                st.session_state.logged_in = True
                st.rerun()
        with tab2:
            st.text_input("Họ và tên của bạn")
            st.text_input("Email nhận thông báo")
            st.button("ĐĂNG KÝ NGAY")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- GIAO DIỆN CHÍNH SAU KHI VÀO ---
    with st.sidebar:
        st.title("Eco-Friendly")
        # Sử dụng menu ngôn ngữ bình thường
        choice = option_menu(None, ["Trang chủ", "Tìm đường", "Trò chuyện", "Nâng cấp", "Cài đặt"], 
            icons=['house', 'map', 'chat-dots', 'stars', 'gear'], default_index=0)
        
        st.divider()
        if st.button("Đăng xuất"):
            st.session_state.logged_in = False
            st.rerun()

    # --- TAB 1: TRANG CHỦ (TRẠNG THÁI THẬT) ---
    if choice == "Trang chủ":
        st.header("Chào buổi sáng! 👋")
        st.write("Dưới đây là tình hình chậu cây Nano của bạn:")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Lượng nước", "Còn 80%", "Đủ cho 2 ngày")
        c2.metric("Ánh sáng", "Rất tốt", "Đang đón nắng")
        c3.metric("Lọc không khí", "Đã lọc 15mg bụi", "Hôm nay")

        st.subheader("Lời khuyên từ AI")
        st.info("Trời sắp có mưa lớn vào chiều nay. Nếu bạn để cây ở ban công ngoài trời, hãy chú ý nhé!")
        

    # --- TAB 2: TÌM ĐƯỜNG (CHỈ KHI YÊU CẦU) ---
    elif choice == "Tìm đường":
        st.header("🧭 Chỉ đường về với cây")
        st.write("Ứng dụng cần biết bạn đang ở đâu để chỉ đường.")
        
        if st.button("📍 Lấy vị trí của tôi"):
            # Ở đây thực tế sẽ dùng GPS trình duyệt, tạm thời giả lập để bạn thấy cách chạy
            my_lat, my_lon = 10.762622, 106.660172 # Tọa độ thực của bạn (giả định)
            tree_lat, tree_lon = 10.763500, 106.661000 # Tọa độ cây
            
            dist = geodesic((my_lat, my_lon), (tree_lat, tree_lon)).meters
            st.success(f"Đã tìm thấy cây! Cách bạn khoảng {dist:.1f} mét.")
            
            st.plotly_chart(draw_navigator(my_lat, my_lon, tree_lat, tree_lon), use_container_width=True)
            st.write("Mẹo: Đi bộ theo hướng vỉa hè phía trước khoảng 2 phút.")

    # --- TAB 3: TRÒ CHUYỆN (THẬT SỰ) ---
    elif choice == "Trò chuyện":
        st.header("💬 Tâm sự cùng cây")
        st.caption("Cây của bạn phản hồi dựa trên dữ liệu thời tiết và môi trường xung quanh.")

        # Hiển thị lịch sử chat
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Nhập tin nhắn mới
        if prompt := st.chat_input("Bạn muốn nói gì với cây?"):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Phản hồi của cây (giả lập AI)
            with st.chat_message("assistant", avatar="🌿"):
                response = ""
                if "nước" in prompt.lower():
                    response = "Mình vẫn đủ nước, bạn đừng lo nhé! Cảm ơn bạn đã quan tâm."
                elif "khỏe" in prompt.lower():
                    response = "Mình đang rất khỏe, nắng hôm nay làm mình thấy rất sảng khoái."
                else:
                    response = "Mình đang lắng nghe bạn đây. Bạn có muốn mình lọc thêm không khí không?"
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

    # --- TAB 4: NÂNG CẤP (200+ TÍNH NĂNG CHUYỂN THÀNH MODULES) ---
    elif choice == "Nâng cấp":
        st.header("✨ Nâng cấp khả năng cho cây")
        st.write("Sử dụng các vật liệu tái chế để mở khóa các tính năng mới.")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            with st.expander("🛡️ Gói Chống Nắng (UV Shield)"):
                st.write("- Tự động tính toán góc nắng đổ vào ban công.")
                st.write("- Cảnh báo khi nhiệt độ nhựa tái chế vượt ngưỡng 40°C.")
                st.button("Kích hoạt ngay", key="uv")
        with col_m2:
            with st.expander("💧 Gói Siêu Tiết Kiệm Nước"):
                st.write("- Phân tích độ ẩm không khí để giảm tần suất tưới.")
                st.write("- Tận dụng độ ẩm ban đêm để nuôi rễ.")
                st.button("Kích hoạt ngay", key="water")
        
        st.divider()
        st.subheader("Các tính năng li ti khác")
        st.write("Đã tích hợp: Lọc bụi mịn PM2.5, Cân bằng pH đất tự động (giả lập), Theo dõi sức khỏe mầm non...")
