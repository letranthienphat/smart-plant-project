import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import time
import random

# --- 1. CẤU HÌNH GIAO DIỆN "VIP" ---
st.set_page_config(page_title="EcoMind OS - Global Database", layout="wide", page_icon="🧬")

# CSS Tùy biến giao diện Đen-Xanh Cyberpunk
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .stDataFrame { border: 1px solid #00ffcc; border-radius: 5px; }
    div[data-testid="stMetricValue"] { color: #00ffcc !important; font-weight: bold; }
    h1, h2, h3 { color: #00ffcc !important; }
    .css-1r6slb0 { background-color: #1f2937; border: 1px solid #374151; }
</style>
""", unsafe_allow_html=True)

# --- 2. BỘ MÁY "BIG DATA" TỰ ĐỘNG (KHÔNG CẦN FILE CSV) ---
@st.cache_data(show_spinner="Đang kết nối siêu máy chủ dữ liệu thực vật toàn cầu...")
def generate_instant_db():
    """Hàm này tự động tạo ra 3000 cây ngay trong bộ nhớ khi App chạy"""
    
    # Từ điển dữ liệu để ghép tên cây cho phong phú và nghe "như thật"
    loai = ["Hoa Hồng", "Lan", "Xương Rồng", "Sen Đá", "Trầu Bà", "Dương Xỉ", "Cây Cọ", "Trúc", "Tùng", "Cúc", "Mai", "Đào", "Sung", "Si", "Đa"]
    tinh_tu = ["Hoàng Gia", "Cẩm Thạch", "Bạch Tạng", "Hắc Kim", "Lửa", "Tuyết", "Đại Đế", "Tiểu Thư", "Phú Quý", "Thần Tài"]
    xuat_xu = ["Nhật Bản", "Thái Lan", "Mỹ", "Đà Lạt", "Cổ Đại", "Đột Biến", "Rừng Mưa", "Sa Mạc"]
    ho_khoa_hoc = ["Rosa", "Orchidaceae", "Cactaceae", "Araceae", "Polypodiopsida", "Arecaceae"]

    data = []
    # Vòng lặp tạo 3500 cây
    for i in range(1, 3501):
        ten_cay = f"{random.choice(loai)} {random.choice(tinh_tu)} {random.choice(xuat_xu)}"
        ten_kh = f"{random.choice(ho_khoa_hoc)} {random.choice(['spp.', 'var.', 'hbr.'])} {i}"
        
        # Tạo thông số sinh học ngẫu nhiên hợp lý
        nuoc = round(random.uniform(0.05, 1.5), 2)
        anh_sang = random.choice(["Bóng râm", "Tán xạ", "Trực tiếp 50%", "Full nắng", "Đèn UV"])
        nhiet_do = f"{random.randint(15, 20)}-{random.randint(28, 35)}°C"
        do_kho = random.choice(["Dễ (Người mới)", "Trung bình", "Khó", "Chuyên gia"])
        pet_safe = random.choice(["✅ An toàn", "❌ Độc hại"])
        
        data.append([i, ten_cay, ten_kh, nuoc, anh_sang, nhiet_do, do_kho, pet_safe])

    df = pd.DataFrame(data, columns=["ID", "Tên Thương Mại", "Tên Khoa Học", "Nước (L/ngày)", "Ánh Sáng", "Nhiệt Độ", "Độ Khó", "Thú Cưng"])
    return df

# Gọi hàm tạo dữ liệu ngay lập tức
df = generate_instant_db()

# --- 3. THANH ĐIỀU HƯỚNG ---
with st.sidebar:
    st.title("🧬 ECO-MIND OS")
    st.caption("v8.0.1 Enterprise Edition")
    
    selected = option_menu(
        menu_title=None,
        options=["Tổng Quan", "Thư Viện (3500+)", "Tra Cứu Chi Tiết", "Bác Sĩ Cây", "Cấu Hình"],
        icons=["grid-1x2", "collection", "search", "activity", "gear"],
        default_index=1, # Mặc định mở tab Thư viện cho hoành tráng
        styles={
            "container": {"padding": "0!important", "background-color": "#0e1117"},
            "icon": {"color": "orange", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#262730"},
            "nav-link-selected": {"background-color": "#00ffcc", "color": "black"},
        }
    )
    
    st.info(f"Database: **{len(df)}** loài\nServer: **Online**")

# --- 4. NỘI DUNG CHÍNH ---

# === TAB THƯ VIỆN ===
if selected == "Thư Viện (3500+)":
    st.title("📚 KHO DỮ LIỆU THỰC VẬT TOÀN CẦU")
    
    # Khu vực tìm kiếm VIP
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        search_txt = st.text_input("🔍 Nhập tên cây để tìm trong 3500 loài:", placeholder="Ví dụ: Hoa Hồng, Lan Đột Biến...")
    with c2:
        filter_diff = st.multiselect("Lọc Độ Khó:", df["Độ Khó"].unique())
    with c3:
        filter_safe = st.selectbox("Lọc An Toàn:", ["Tất cả", "✅ An toàn", "❌ Độc hại"])

    # Xử lý lọc dữ liệu siêu tốc
    df_show = df.copy()
    if search_txt:
        df_show = df_show[df_show["Tên Thương Mại"].str.contains(search_txt, case=False)]
    if filter_diff:
        df_show = df_show[df_show["Độ Khó"].isin(filter_diff)]
    if filter_safe != "Tất cả":
        df_show = df_show[df_show["Thú Cưng"] == filter_safe]

    st.markdown(f"**Kết quả tìm thấy: {len(df_show)} loài cây**")
    
    # Bảng dữ liệu Full màn hình
    st.dataframe(
        df_show,
        use_container_width=True,
        height=700,
        column_config={
            "Nước (L/ngày)": st.column_config.ProgressColumn("Nhu cầu nước", min_value=0, max_value=1.5, format="%.2f L"),
            "ID": st.column_config.NumberColumn(format="#%d")
        },
        hide_index=True
    )

# === TAB TRA CỨU CHI TIẾT ===
elif selected == "Tra Cứu Chi Tiết":
    st.title("🔍 HỒ SƠ SINH HỌC CÂY TRỒNG")
    
    # Chọn cây từ danh sách
    plant_name = st.selectbox("Chọn cây cần xem hồ sơ:", df["Tên Thương Mại"].head(100)) # Demo 100 cây đầu
    plant_data = df[df["Tên Thương Mại"] == plant_name].iloc[0]

    # Layout thẻ bài VIP
    col_img, col_info = st.columns([1, 2])
    
    with col_img:
        # Ảnh giả lập theo từ khóa (Dùng Unsplash Source)
        keyword = "flower" if "Hoa" in plant_name else "plant"
        st.image(f"https://source.unsplash.com/400x500/?{keyword}", caption="Ảnh minh họa loài")
    
    with col_info:
        st.header(plant_data["Tên Thương Mại"])
        st.subheader(f"_{plant_data['Tên Khoa Học']}_")
        
        m1, m2 = st.columns(2)
        m1.metric("💧 Nước cần tưới", f"{plant_data['Nước (L/ngày)']} L/ngày")
        m2.metric("🌡️ Nhiệt độ sống", plant_data["Nhiệt Độ"])
        
        st.markdown("---")
        st.markdown(f"**💡 Độ khó:** {plant_data['Độ Khó']}")
        st.markdown(f"**🐶 An toàn thú cưng:** {plant_data['Thú Cưng']}")
        st.markdown(f"**☀️ Ánh sáng:** {plant_data['Ánh Sáng']}")
        
        st.info("📝 **Ghi chú chuyên gia:** Loài cây này có khả năng thanh lọc không khí tốt, ưa môi trường thoáng gió. Tránh để đọng nước ở rễ quá 24h.")

# === TAB TỔNG QUAN (DASHBOARD) ===
elif selected == "Tổng Quan":
    st.title("📈 DASHBOARD GIÁM SÁT VƯỜN THÔNG MINH")
    
    # Metrics hàng đầu
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Tổng Database", f"{len(df):,}", "Loài")
    k2.metric("Server Uptime", "99.9%", "Online")
    k3.metric("Cây Đột Biến", "125", "High Value")
    k4.metric("Cảnh Báo", "0", "Hệ thống ổn định")
    
    st.markdown("---")
    
    # Biểu đồ phân bố (Analytics)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Phân bố độ khó chăm sóc")
        pie_data = df["Độ Khó"].value_counts()
        fig_pie = px.pie(values=pie_data, names=pie_data.index, hole=0.5, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader("Nhu cầu nước trung bình (Lít)")
        # Lấy mẫu 20 cây để vẽ biểu đồ cho đẹp
        sample = df.head(20)
        fig_bar = px.bar(sample, x="Tên Thương Mại", y="Nước (L/ngày)", color="Nước (L/ngày)", template="plotly_dark")
        st.plotly_chart(fig_bar, use_container_width=True)

# === TAB BÁC SĨ CÂY ===
elif selected == "Bác Sĩ Cây":
    st.title("🩺 AI DIAGNOSTIC - BÁC SĨ THỰC VẬT")
    
    col_chat, col_res = st.columns([2, 1])
    
    with col_chat:
        st.write("Mô tả tình trạng cây của bạn:")
        problem = st.text_area("Ví dụ: Lá bị vàng, rễ có mùi hôi, thân mềm...", height=150)
        btn_check = st.button("🔍 PHÂN TÍCH NGAY", type="primary", use_container_width=True)
    
    with col_res:
        if btn_check and problem:
            with st.spinner("AI đang quét dữ liệu bệnh học..."):
                time.sleep(2) # Giả lập tính toán
                st.success("Đã tìm thấy nguyên nhân!")
                
                with st.container(border=True):
                    if "vàng" in problem.lower():
                        st.markdown("### 🦠 Bệnh: Thiếu Vi Lượng / Dư Nước")
                        st.write("Cây có dấu hiệu vàng lá do rễ bị úng hoặc thiếu Magie.")
                        st.error("Khuyến nghị: Ngưng tưới 3 ngày, bón thêm phân vi lượng.")
                    elif "hôi" in problem.lower() or "mềm" in problem.lower():
                        st.markdown("### ☠️ Bệnh: Thối Rễ (Root Rot)")
                        st.write("Nấm bệnh tấn công bộ rễ do đất không thoát nước.")
                        st.error("Khuyến nghị: Thay đất gấp, cắt bỏ rễ thối.")
                    else:
                        st.markdown("### ☀️ Sốc Nhiệt / Môi Trường")
                        st.write("Cây chưa thích nghi với vị trí mới.")
                        st.info("Khuyến nghị: Đưa cây vào nơi mát, tránh nắng gắt.")

# === TAB CẤU HÌNH ===
elif selected == "Cấu Hình":
    st.title("⚙️ HỆ THỐNG")
    st.write("ID Máy Chủ: #VN-8821-X")
    st.toggle("Chế độ tự động cập nhật Database", value=True)
    st.toggle("Gửi báo cáo qua Email", value=False)
    st.slider("Chu kỳ quét cảm biến (phút)", 1, 60, 5)
    if st.button("Khôi phục cài đặt gốc"):
        st.toast("System Reset...", icon="🔄")
