import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import wikipedia
import random
import time

# --- 1. CẤU HÌNH & CSS NEON (GIỮ NGUYÊN STYLE ĐẸP) ---
st.set_page_config(page_title="EcoMind OS - Professional", layout="wide", page_icon="🌿")
wikipedia.set_lang("vi")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    div[data-testid="stMetricValue"] { color: #00ffcc !important; font-weight: bold; }
    .success-text { color: #00ffcc; font-weight: bold; padding: 10px; border: 1px solid #00ffcc; border-radius: 5px; }
    .stButton>button { border-radius: 5px; background-color: #1f2937; color: #00ffcc; border: 1px solid #00ffcc; width: 100%; }
    .stButton>button:hover { background-color: #00ffcc; color: black; }
</style>
""", unsafe_allow_html=True)

# --- 2. HÀM XỬ LÝ DỮ LIỆU ---
@st.cache_data
def get_plant_db():
    loai = ["Hoa Hồng", "Lan Hồ Điệp", "Xương Rồng", "Trầu Bà", "Sen Đá", "Kim Tiền", "Lưỡi Hổ", "Bàng Singapore"]
    return pd.DataFrame([{"ID": i, "Tên Cây": n, "Nhu cầu": round(random.uniform(0.1, 0.9), 2)} for i, n in enumerate(loai)])

# --- 3. HỆ THỐNG QUẢN LÝ TÀI KHOẢN ---
def auth_system():
    if 'auth_status' not in st.session_state:
        st.session_state.auth_status = None # None, 'logged_in', 'guest'
    
    if st.session_state.auth_status is None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.title("🌿 Hệ Thống Quản Lý Cây Trồng")
            tab_login, tab_reg, tab_guest = st.tabs(["Đăng nhập", "Đăng ký", "Khách"])
            
            with tab_login:
                u = st.text_input("Tên đăng nhập")
                p = st.text_input("Mật khẩu", type="password")
                if st.button("Đăng nhập"):
                    if u == "admin" and p == "123":
                        st.session_state.auth_status = 'logged_in'
                        st.rerun()
                    else: st.error("Tên đăng nhập hoặc mật khẩu không đúng.")
            
            with tab_reg:
                new_u = st.text_input("Chọn tên đăng nhập")
                new_p = st.text_input("Chọn mật khẩu", type="password")
                if st.button("Tạo tài khoản"):
                    if new_u and new_p:
                        # Giả lập đăng ký thành công
                        st.markdown("<p class='success-text'>✅ Đăng ký hoàn tất! Bạn có thể chuyển sang tab Đăng nhập.</p>", unsafe_allow_html=True)
                        st.balloons()
                    else: st.warning("Vui lòng điền đầy đủ thông tin.")
            
            with tab_guest:
                st.info("Chế độ khách cho phép trải nghiệm nhanh các tính năng cơ bản.")
                if st.button("Tiếp tục với quyền Khách"):
                    st.session_state.auth_status = 'guest'
                    st.rerun()
        return False
    return True

# --- 4. GIAO DIỆN CHÍNH ---
if auth_system():
    db = get_plant_db()
    
    # Bước Onboarding (Chọn cây lần đầu)
    if 'my_plant' not in st.session_state:
        st.title("⚙️ Thiết lập ban đầu")
        c1, c2 = st.columns(2)
        with c1:
            choice = st.selectbox("Chọn loại cây của bạn:", db["Tên Cây"])
        with c2:
            water = st.number_input("Lượng nước hiện tại trong bình (Lít):", 0.0, 20.0, 5.0)
        
        if st.button("Xác nhận và vào Dashboard"):
            st.session_state.my_plant = db[db["Tên Cây"] == choice].iloc[0].to_dict()
            st.session_state.current_water = water
            st.session_state.history = [] # Lưu lịch sử tưới
            st.rerun()
            
    else:
        # SIDEBAR
        with st.sidebar:
            st.title("ECO-MIND")
            menu = option_menu(None, ["Giám sát", "Lịch sử & VIP", "Tra cứu", "Vị trí"], 
                icons=['activity', 'graph-up-arrow', 'search', 'geo'], default_index=0)
            
            if st.button("🚪 Đăng xuất"):
                st.session_state.auth_status = None
                del st.session_state.my_plant
                st.rerun()

        # === TAB 1: GIÁM SÁT (DASHBOARD) ===
        if menu == "Giám sát":
            st.header(f"📊 Dashboard: {st.session_state.my_plant['Tên Cây']}")
            
            # Tự động hóa lấy thời tiết giả lập
            temp = random.randint(25, 35)
            hum = random.randint(40, 80)
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Nước hiện tại", f"{st.session_state.current_water:.2f} L")
            m2.metric("Nhiệt độ (Auto)", f"{temp} °C")
            m3.metric("Độ ẩm (Auto)", f"{hum} %")
            
            st.divider()
            st.subheader("🛠️ Cập nhật thông số thủ công")
            updated_water = st.number_input("Cập nhật lại mực nước (Lít):", value=float(st.session_state.current_water))
            if st.button("Cập nhật hệ thống"):
                # Lưu vào lịch sử trước khi cập nhật
                st.session_state.history.append({"Thời gian": time.strftime("%H:%M:%S"), "Lượng nước": updated_water})
                st.session_state.current_water = updated_water
                st.success("Dữ liệu đã được đồng bộ.")

        # === TAB 2: LỊCH SỬ & VIP (TÍNH NĂNG NÂNG CAO) ===
        elif menu == "Lịch sử & VIP":
            st.header("💎 Tính năng Quản lý Chuyên sâu")
            
            if not st.session_state.history:
                st.info("Chưa có dữ liệu lịch sử. Hãy cập nhật nước ở Dashboard.")
            else:
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    st.subheader("Biểu đồ tiêu thụ nước")
                    h_df = pd.DataFrame(st.session_state.history)
                    fig = px.line(h_df, x="Thời gian", y="Lượng nước", markers=True, template="plotly_dark")
                    fig.update_traces(line_color='#00ffcc')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col_b:
                    st.subheader("Xuất báo cáo")
                    st.write("Tải dữ liệu chăm sóc về máy (.csv)")
                    csv = h_df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Tải báo cáo", data=csv, file_name="plant_report.csv", mime="text/csv")

        # === TAB 3: TRA CỨU (FIXED WIKI) ===
        elif menu == "Tra cứu":
            st.header("🔍 Tra cứu từ Wikipedia")
            q = st.text_input("Nhập tên loài cây cần tra cứu:")
            if q:
                try:
                    res = wikipedia.page(f"Cây {q}")
                    st.subheader(res.title)
                    if res.images: st.image(res.images[0], width=400)
                    st.write(wikipedia.summary(f"Cây {q}", sentences=4))
                except:
                    st.error("Không tìm thấy thông tin hoặc có quá nhiều kết quả trùng lặp.")

        # === TAB 4: VỊ TRÍ ===
        elif menu == "Vị trí":
            st.header("📍 Vị trí thiết bị")
            st.write("Tự động xác định vị trí qua IP...")
            # Demo vị trí
            st.map(pd.DataFrame({'lat': [10.762622], 'lon': [106.660172]}))
            st.caption("Vị trí: Quận 10, TP. Hồ Chí Minh (Giả lập)")
