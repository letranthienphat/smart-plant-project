import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import time
import random
import json
import datetime
from io import BytesIO

# --- 1. CẤU HÌNH GIAO DIỆN "VIP" NÂNG CẤP ---
st.set_page_config(
    page_title="EcoMind OS - Global Database", 
    layout="wide", 
    page_icon="🧬",
    initial_sidebar_state="expanded"
)

# CSS Tùy biến giao diện Đen-Xanh Cyberpunk nâng cấp
st.markdown("""
<style>
    .stApp { 
        background: linear-gradient(135deg, #0a0e17 0%, #1a1f2e 100%);
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: #1a1f2e; }
    ::-webkit-scrollbar-thumb { 
        background: linear-gradient(180deg, #00ffcc 0%, #0088cc 100%);
        border-radius: 5px;
    }
    
    /* Cards và Containers */
    .custom-card {
        background: rgba(30, 35, 50, 0.8);
        border: 1px solid rgba(0, 255, 204, 0.2);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        border-color: #00ffcc;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.3);
        transform: translateY(-2px);
    }
    
    /* Metrics và KPIs */
    div[data-testid="stMetricValue"] { 
        color: #00ffcc !important; 
        font-weight: bold;
        font-size: 2rem !important;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
    }
    
    div[data-testid="stMetricLabel"] { 
        color: #88aaff !important;
        font-size: 0.9rem !important;
    }
    
    /* Headers */
    h1, h2, h3 { 
        color: #00ffcc !important; 
        text-shadow: 0 0 15px rgba(0, 255, 204, 0.3);
        border-left: 4px solid #00ffcc;
        padding-left: 15px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00ffcc 0%, #0088cc 100%);
        color: #000;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.5);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: rgba(20, 25, 40, 0.8);
        padding: 5px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        background-color: transparent;
        color: #88aaff;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #00ffcc 0%, #0088cc 100%);
        color: #000 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0e17 0%, #151a28 100%);
        border-right: 1px solid rgba(0, 255, 204, 0.1);
    }
    
    /* Dataframe */
    .stDataFrame {
        border: 1px solid #00ffcc;
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background: rgba(30, 35, 50, 0.8);
        border: 1px solid rgba(0, 255, 204, 0.3);
        color: white;
        border-radius: 8px;
    }
    
    .stSelectbox > div > div {
        background: rgba(30, 35, 50, 0.8);
        border: 1px solid rgba(0, 255, 204, 0.3);
        border-radius: 8px;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00ffcc 0%, #0088cc 100%);
    }
    
    /* Success/Error/Info boxes */
    .stAlert {
        border-radius: 10px;
        border: 1px solid rgba(0, 255, 204, 0.3);
        background: rgba(30, 35, 50, 0.9);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. CẢI TIẾN BỘ MÁY "BIG DATA" ---
@st.cache_data(show_spinner="🚀 Đang khởi tạo siêu cơ sở dữ liệu thực vật...")
def generate_enhanced_db():
    """Tạo cơ sở dữ liệu nâng cao với nhiều thuộc tính hơn"""
    
    # Mở rộng từ điển dữ liệu
    loai = ["Hoa Hồng", "Lan", "Xương Rồng", "Sen Đá", "Trầu Bà", "Dương Xỉ", "Cây Cọ", "Trúc", "Tùng", "Cúc", 
            "Mai", "Đào", "Sung", "Si", "Đa", "Phong Lan", "Cẩm Tú Cầu", "Tulip", "Hoa Quỳnh", "Bonsai"]
    
    tinh_tu = ["Hoàng Gia", "Cẩm Thạch", "Bạch Tạng", "Hắc Kim", "Lửa", "Tuyết", "Đại Đế", "Tiểu Thư", 
               "Phú Quý", "Thần Tài", "Vương Giả", "Thiên Nga", "Rồng", "Phượng", "Huyền Bí"]
    
    xuat_xu = ["Nhật Bản", "Thái Lan", "Mỹ", "Đà Lạt", "Cổ Đại", "Đột Biến", "Rừng Mưa", "Sa Mạc", 
               "Himalaya", "Amazon", "Châu Phi", "Đông Nam Á", "Việt Nam", "Hà Lan", "Pháp"]
    
    ho_khoa_hoc = ["Rosa spp.", "Orchidaceae var.", "Cactaceae spp.", "Araceae hbr.", "Polypodiopsida", 
                   "Arecaceae", "Ficus", "Bambusoideae", "Pinus", "Chrysanthemum"]
    
    muc_do_quy_hien = ["Phổ biến", "Hiếm", "Rất hiếm", "Cực kỳ hiếm", "Đột biến độc nhất"]
    
    # Danh sách môi trường sống
    moi_truong = ["Trong nhà", "Ngoài trời", "Ban công", "Sân vườn", "Thủy canh", "Khí canh", "Terrarium"]
    
    data = []
    
    # Tạo 3500 bản ghi với dữ liệu phong phú
    for i in range(1, 3501):
        ten_cay = f"{random.choice(loai)} {random.choice(tinh_tu)} {random.choice(xuat_xu)}"
        ten_kh = f"{random.choice(ho_khoa_hoc)} {'-'.join(random.sample(['alpha', 'beta', 'gamma', 'delta'], 2))}"
        
        # Tạo giá trị sinh học hợp lý
        nuoc = round(random.uniform(0.05, 2.0), 2)
        anh_sang = random.choice(["Bóng râm", "Tán xạ", "Trực tiếp 50%", "Full nắng", "Đèn UV", "Bán phần"])
        nhiet_do = f"{random.randint(10, 18)}-{random.randint(25, 38)}°C"
        do_kho = random.choice(["Dễ (Người mới)", "Trung bình", "Khó", "Chuyên gia", "Master"])
        pet_safe = random.choice(["✅ An toàn", "❌ Độc hại", "⚠️ Hạn chế tiếp xúc"])
        
        # Thêm các thuộc tính mới
        do_am_dat = f"{random.randint(40, 90)}%"
        do_pH = round(random.uniform(5.0, 7.5), 1)
        toc_do_sinh_truong = random.choice(["Chậm", "Trung bình", "Nhanh", "Rất nhanh"])
        che_do_bo_phan = random.choice(["2 tuần/lần", "1 tháng/lần", "3 tháng/lần", "6 tháng/lần"])
        thanh_loc_khong_khi = random.choice(["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"])
        quy_hien = random.choice(muc_do_quy_hien)
        gia_du_kien = random.randint(50000, 50000000)
        moi_truong_song = random.choice(moi_truong)
        
        # Tỉ lệ sống
        ti_le_song = random.randint(70, 99)
        
        # Chu kỳ sống
        chu_ky_song = random.choice(["Hàng năm", "Lâu năm", "Hai năm", "Ngắn ngày"])
        
        # Tạo mô tả chi tiết
        mo_ta = f"Cây {ten_cay.lower()} là loài thực vật độc đáo với khả năng thích nghi cao. " \
                f"Thích hợp cho {moi_truong_song.lower()}, có khả năng thanh lọc không khí {thanh_loc_khong_khi}."
        
        data.append([
            i, ten_cay, ten_kh, nuoc, anh_sang, nhiet_do, do_kho, pet_safe,
            do_am_dat, do_pH, toc_do_sinh_truong, che_do_bo_phan, thanh_loc_khong_khi,
            quy_hien, gia_du_kien, moi_truong_song, ti_le_song, chu_ky_song, mo_ta
        ])
    
    columns = [
        "ID", "Tên Thương Mại", "Tên Khoa Học", "Nước (L/ngày)", "Ánh Sáng", "Nhiệt Độ", 
        "Độ Khó", "Thú Cưng", "Độ Ẩm Đất", "Độ pH", "Tốc Độ Sinh Trưởng", 
        "Chế Độ Bón Phân", "Thanh Lọc KK", "Độ Quý Hiếm", "Giá Dự Kiến (VND)", 
        "Môi Trường Sống", "Tỉ Lệ Sống (%)", "Chu Kỳ Sống", "Mô Tả Chi Tiết"
    ]
    
    df = pd.DataFrame(data, columns=columns)
    return df

# --- 3. HỆ THỐNG QUẢN LÝ NGƯỜI DÙNG ĐƠN GIẢN ---
@st.cache_data
def init_user_data():
    return {
        "favorites": [],
        "recent_views": [],
        "garden": [],
        "notes": {},
        "preferences": {
            "theme": "dark",
            "notifications": True,
            "auto_save": True
        }
    }

# --- 4. THANH ĐIỀU HƯỚNG NÂNG CẤP ---
with st.sidebar:
    # Header với animation
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #00ffcc; font-size: 2rem; margin-bottom: 0;">🧬 ECO-MIND OS</h1>
        <p style="color: #88aaff; font-size: 0.9rem; margin-top: 0;">v8.5.1 Enterprise Edition</p>
        <div style="height: 2px; background: linear-gradient(90deg, transparent, #00ffcc, transparent); margin: 10px 0;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # User profile mini
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("👤")
    with col2:
        st.markdown("**Admin User**")
        st.caption("Premium Account")
    
    # Menu chính
    selected = option_menu(
        menu_title=None,
        options=["🏠 Tổng Quan", "📚 Thư Viện", "🔍 Tra Cứu", "🩺 Bác Sĩ Cây", 
                "🌿 Vườn Của Tôi", "📊 Analytics", "⚙️ Cấu Hình"],
        icons=["house", "book", "search", "activity", "tree", "graph-up", "gear"],
        default_index=1,
        styles={
            "container": {
                "padding": "0!important", 
                "background-color": "transparent",
                "border-radius": "10px"
            },
            "icon": {
                "color": "#00ffcc", 
                "font-size": "18px"
            }, 
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "5px 0",
                "border-radius": "8px",
                "padding": "12px 15px",
                "color": "#ffffff"
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg, #00ffcc 0%, #0088cc 100%)",
                "color": "#000000",
                "font-weight": "bold",
                "box-shadow": "0 0 10px rgba(0, 255, 204, 0.3)"
            },
        }
    )
    
    # Thống kê nhanh
    st.markdown("---")
    st.markdown("### 📊 Thống Kê Nhanh")
    
    # Khởi tạo df nếu chưa có
    if 'df' not in st.session_state:
        st.session_state.df = generate_enhanced_db()
    
    df = st.session_state.df
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Tổng Loài", f"{len(df):,}")
    with col_b:
        rare_count = len(df[df['Độ Quý Hiếm'].isin(['Rất hiếm', 'Cực kỳ hiếm', 'Đột biến độc nhất'])])
        st.metric("Loài Quý", rare_count)
    
    # System status
    st.markdown("---")
    st.markdown("### 🖥️ Trạng Thái")
    
    status_col1, status_col2 = st.columns(2)
    with status_col1:
        st.success("**Online**")
    with status_col2:
        st.info(f"**{datetime.datetime.now().strftime('%H:%M')}**")
    
    # Quick actions
    st.markdown("---")
    st.markdown("### ⚡ Hành Động Nhanh")
    
    if st.button("🔄 Làm Mới Dữ Liệu", use_container_width=True):
        st.cache_data.clear()
        st.session_state.df = generate_enhanced_db()
        st.rerun()
    
    if st.button("📥 Xuất Dữ Liệu", use_container_width=True):
        # This will be implemented in the main content
        pass

# --- 5. NỘI DUNG CHÍNH ---
# Khởi tạo session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = init_user_data()
if 'df' not in st.session_state:
    st.session_state.df = generate_enhanced_db()

df = st.session_state.df
user_data = st.session_state.user_data

# === TAB TỔNG QUAN NÂNG CẤP ===
if selected == "🏠 Tổng Quan":
    st.title("🌍 DASHBOARD QUẢN LÝ THỰC VẬT TOÀN CẦU")
    
    # Row 1: KPI Cards
    st.markdown("### 📈 CHỈ SỐ CHÍNH")
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        total_plants = len(df)
        st.metric("Tổng Số Loài", f"{total_plants:,}", "🌱")
    
    with k2:
        pet_safe_count = len(df[df['Thú Cưng'].str.contains('✅')])
        st.metric("An Toàn Thú Cưng", pet_safe_count, "🐕")
    
    with k3:
        avg_water = df['Nước (L/ngày)'].mean()
        st.metric("Nước TB/Ngày", f"{avg_water:.2f}L", "💧")
    
    with k4:
        high_value = len(df[df['Giá Dự Kiến (VND)'] > 10000000])
        st.metric("Cây Cao Cấp", high_value, "💰")
    
    st.markdown("---")
    
    # Row 2: Biểu đồ
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Phân Bố Độ Khó")
        difficulty_dist = df['Độ Khó'].value_counts()
        fig1 = px.pie(
            values=difficulty_dist.values,
            names=difficulty_dist.index,
            hole=0.6,
            color_discrete_sequence=px.colors.sequential.Viridis,
            template="plotly_dark"
        )
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        fig1.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("#### 💰 Phân Khúc Giá")
        price_bins = pd.cut(df['Giá Dự Kiến (VND)'], 
                           bins=[0, 100000, 1000000, 10000000, 1000000000],
                           labels=['Dưới 100k', '100k-1Tr', '1Tr-10Tr', 'Trên 10Tr'])
        price_dist = price_bins.value_counts().sort_index()
        
        fig2 = px.bar(
            x=price_dist.index.astype(str),
            y=price_dist.values,
            color=price_dist.values,
            color_continuous_scale="Viridis",
            template="plotly_dark"
        )
        fig2.update_layout(
            xaxis_title="Phân Khúc Giá",
            yaxis_title="Số Lượng Loài",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            coloraxis_showscale=False
        )
        fig2.update_traces(
            hovertemplate="<b>%{x}</b><br>Số loài: %{y}<extra></extra>",
            marker_line_color='#00ffcc',
            marker_line_width=1
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Row 3: Top cây và thống kê
    st.markdown("---")
    col3, col4 = st.columns([2, 1])
    
    with col3:
        st.markdown("#### 🌟 TOP 10 CÂY QUÝ HIẾM")
        top_rare = df[df['Độ Quý Hiếm'].isin(['Cực kỳ hiếm', 'Đột biến độc nhất'])].head(10)
        st.dataframe(
            top_rare[['Tên Thương Mại', 'Độ Quý Hiếm', 'Giá Dự Kiến (VND)', 'Tỉ Lệ Sống (%)']],
            use_container_width=True,
            height=350
        )
    
    with col4:
        st.markdown("#### 📈 THỐNG KÊ HỆ THỐNG")
        
        # Tạo thẻ thống kê
        stats_data = {
            "Độ khó phổ biến": df['Độ Khó'].mode()[0],
            "Môi trường phổ biến": df['Môi Trường Sống'].mode()[0],
            "Tỉ lệ sống TB": f"{df['Tỉ Lệ Sống (%)'].mean():.1f}%",
            "Giá trung bình": f"{df['Giá Dự Kiến (VND)'].mean():,.0f} VND",
            "Loài trong nhà": len(df[df['Môi Trường Sống'] == 'Trong nhà']),
            "Cây thanh lọc 5⭐": len(df[df['Thanh Lọc KK'] == '⭐⭐⭐⭐⭐'])
        }
        
        for key, value in stats_data.items():
            with st.container(border=True):
                st.markdown(f"**{key}**")
                st.markdown(f"<h4 style='color: #00ffcc; margin: 0;'>{value}</h4>", unsafe_allow_html=True)
    
    # Row 4: Thông tin hệ thống
    st.markdown("---")
    with st.expander("ℹ️ THÔNG TIN HỆ THỐNG", expanded=False):
        sys_col1, sys_col2, sys_col3 = st.columns(3)
        
        with sys_col1:
            st.markdown("**💻 Server Info**")
            st.code(f"""
            CPU Usage: {random.randint(10, 50)}%
            Memory: {random.randint(60, 90)}%
            Uptime: 99.9%
            Last Update: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
            """)
        
        with sys_col2:
            st.markdown("**🔐 Bảo Mật**")
            st.success("✓ Mã hóa AES-256")
            st.success("✓ Xác thực 2 lớp")
            st.warning("⚠️ Backup hàng tuần")
        
        with sys_col3:
            st.markdown("**📊 Data Health**")
            st.progress(0.95, text="Data Quality: 95%")
            st.progress(0.98, text="Completeness: 98%")
            st.progress(1.0, text="Consistency: 100%")

# === TAB THƯ VIỆN NÂNG CẤP ===
elif selected == "📚 Thư Viện":
    st.title("📚 KHO DỮ LIỆU THỰC VẬT TOÀN CẦU")
    st.markdown(f"*Đang hiển thị {len(df):,} loài thực vật từ cơ sở dữ liệu*")
    
    # Bộ lọc nâng cao
    with st.expander("🔍 BỘ LỌC NÂNG CAO", expanded=True):
        col_filter1, col_filter2, col_filter3, col_filter4 = st.columns(4)
        
        with col_filter1:
            search_txt = st.text_input(
                "Tìm kiếm tên cây:", 
                placeholder="Nhập tên cây hoặc từ khóa...",
                help="Tìm kiếm theo tên thương mại, tên khoa học, mô tả"
            )
        
        with col_filter2:
            filter_difficulty = st.multiselect(
                "Độ khó chăm sóc:",
                options=df["Độ Khó"].unique(),
                default=[]
            )
        
        with col_filter3:
            filter_environment = st.multiselect(
                "Môi trường sống:",
                options=df["Môi Trường Sống"].unique(),
                default=[]
            )
        
        with col_filter4:
            filter_rarity = st.multiselect(
                "Độ quý hiếm:",
                options=df["Độ Quý Hiếm"].unique(),
                default=[]
            )
        
        # More filters in second row
        col_filter5, col_filter6, col_filter7, col_filter8 = st.columns(4)
        
        with col_filter5:
            filter_pet_safe = st.selectbox(
                "An toàn thú cưng:",
                options=["Tất cả", "✅ An toàn", "❌ Độc hại", "⚠️ Hạn chế tiếp xúc"]
            )
        
        with col_filter6:
            water_range = st.slider(
                "Nhu cầu nước (L/ngày):",
                min_value=float(df["Nước (L/ngày)"].min()),
                max_value=float(df["Nước (L/ngày)"].max()),
                value=(0.0, 2.0),
                step=0.1
            )
        
        with col_filter7:
            price_range = st.slider(
                "Khoảng giá (VND):",
                min_value=int(df["Giá Dự Kiến (VND)"].min()),
                max_value=int(df["Giá Dự Kiến (VND)"].max()),
                value=(0, 50000000),
                step=100000
            )
        
        with col_filter8:
            survival_rate = st.slider(
                "Tỉ lệ sống tối thiểu (%):",
                min_value=0,
                max_value=100,
                value=70,
                step=5
            )
    
    # Áp dụng bộ lọc
    df_filtered = df.copy()
    
    if search_txt:
        mask = (
            df_filtered["Tên Thương Mại"].str.contains(search_txt, case=False, na=False) |
            df_filtered["Tên Khoa Học"].str.contains(search_txt, case=False, na=False) |
            df_filtered["Mô Tả Chi Tiết"].str.contains(search_txt, case=False, na=False)
        )
        df_filtered = df_filtered[mask]
    
    if filter_difficulty:
        df_filtered = df_filtered[df_filtered["Độ Khó"].isin(filter_difficulty)]
    
    if filter_environment:
        df_filtered = df_filtered[df_filtered["Môi Trường Sống"].isin(filter_environment)]
    
    if filter_rarity:
        df_filtered = df_filtered[df_filtered["Độ Quý Hiếm"].isin(filter_rarity)]
    
    if filter_pet_safe != "Tất cả":
        df_filtered = df_filtered[df_filtered["Thú Cưng"] == filter_pet_safe]
    
    df_filtered = df_filtered[
        (df_filtered["Nước (L/ngày)"] >= water_range[0]) &
        (df_filtered["Nước (L/ngày)"] <= water_range[1])
    ]
    
    df_filtered = df_filtered[
        (df_filtered["Giá Dự Kiến (VND)"] >= price_range[0]) &
        (df_filtered["Giá Dự Kiến (VND)"] <= price_range[1])
    ]
    
    df_filtered = df_filtered[df_filtered["Tỉ Lệ Sống (%)"] >= survival_rate]
    
    # Hiển thị kết quả
    result_count = len(df_filtered)
    st.markdown(f"### 📊 Kết quả tìm thấy: **{result_count}** loài cây")
    
    if result_count == 0:
        st.warning("Không tìm thấy cây nào phù hợp với bộ lọc của bạn!")
        st.info("💡 Thử mở rộng bộ lọc hoặc sử dụng từ khóa khác")
    else:
        # Tùy chọn hiển thị
        view_mode = st.radio(
            "Chế độ hiển thị:",
            ["📋 Bảng dữ liệu", "🃏 Thẻ bài (Card View)"],
            horizontal=True
        )
        
        if view_mode == "📋 Bảng dữ liệu":
            # Hiển thị dataframe với cấu hình cột
            column_config = {
                "ID": st.column_config.NumberColumn(format="#%d"),
                "Nước (L/ngày)": st.column_config.ProgressColumn(
                    "💧 Nước",
                    min_value=0,
                    max_value=2.0,
                    format="%.2f L"
                ),
                "Tỉ Lệ Sống (%)": st.column_config.ProgressColumn(
                    "❤️ Sống",
                    min_value=0,
                    max_value=100,
                    format="%.0f%%"
                ),
                "Giá Dự Kiến (VND)": st.column_config.NumberColumn(
                    "💰 Giá",
                    format="%,.0f VND"
                ),
                "Thú Cưng": st.column_config.TextColumn("🐕 An toàn"),
                "Mô Tả Chi Tiết": st.column_config.TextColumn("📝 Mô tả", width="large")
            }
            
            # Chọn cột để hiển thị
            default_columns = [
                "ID", "Tên Thương Mại", "Tên Khoa Học", "Nước (L/ngày)", 
                "Độ Khó", "Thú Cưng", "Độ Quý Hiếm", "Giá Dự Kiến (VND)"
            ]
            
            selectable_columns = st.multiselect(
                "Chọn cột hiển thị:",
                options=df_filtered.columns.tolist(),
                default=default_columns
            )
            
            if selectable_columns:
                st.dataframe(
                    df_filtered[selectable_columns],
                    use_container_width=True,
                    height=600,
                    column_config=column_config,
                    hide_index=True
                )
        
        else:  # Card View
            st.markdown("---")
            items_per_row = 3
            items = df_filtered.head(30).to_dict('records')  # Giới hạn 30 item để hiệu năng
            
            for i in range(0, len(items), items_per_row):
                cols = st.columns(items_per_row)
                for col_idx, col in enumerate(cols):
                    item_idx = i + col_idx
                    if item_idx < len(items):
                        item = items[item_idx]
                        with col:
                            with st.container(border=True):
                                # Header với màu theo độ quý hiếm
                                rarity_colors = {
                                    "Phổ biến": "#4CAF50",
                                    "Hiếm": "#FF9800",
                                    "Rất hiếm": "#F44336",
                                    "Cực kỳ hiếm": "#9C27B0",
                                    "Đột biến độc nhất": "#FF4081"
                                }
                                
                                st.markdown(f"""
                                <div style="background: linear-gradient(90deg, {rarity_colors.get(item['Độ Quý Hiếm'], '#00ffcc')}, transparent); 
                                            padding: 10px; border-radius: 8px; margin: -10px -10px 10px -10px;">
                                    <h4 style="margin: 0; color: white;">{item['Tên Thương Mại']}</h4>
                                    <small style="color: #cccccc;">{item['Tên Khoa Học']}</small>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Thông tin chính
                                col_info1, col_info2 = st.columns(2)
                                with col_info1:
                                    st.markdown(f"**💧 Nước:** {item['Nước (L/ngày)']}L")
                                    st.markdown(f"**🌡️ Nhiệt độ:** {item['Nhiệt Độ']}")
                                
                                with col_info2:
                                    st.markdown(f"**⚡ Độ khó:** {item['Độ Khó']}")
                                    st.markdown(f"**💰 Giá:** {item['Giá Dự Kiến (VND)']:,} VND")
                                
                                # Progress bars
                                st.progress(item['Tỉ Lệ Sống (%)']/100, 
                                          text=f"Tỉ lệ sống: {item['Tỉ Lệ Sống (%)']}%")
                                
                                # Actions
                                btn_col1, btn_col2 = st.columns(2)
                                with btn_col1:
                                    if st.button("👁️ Chi tiết", key=f"view_{item['ID']}", use_container_width=True):
                                        st.session_state.selected_plant = item['ID']
                                        st.switch_page("?selected=🔍 Tra Cứu")
                                
                                with btn_col2:
                                    if st.button("⭐ Yêu thích", key=f"fav_{item['ID']}", use_container_width=True):
                                        if item['ID'] not in user_data['favorites']:
                                            user_data['favorites'].append(item['ID'])
                                            st.success("Đã thêm vào yêu thích!")
    
    # Export và thao tác
    st.markdown("---")
    col_exp1, col_exp2, col_exp3 = st.columns(3)
    
    with col_exp1:
        if st.button("📥 Xuất CSV", use_container_width=True):
            csv = df_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Tải xuống CSV",
                data=csv,
                file_name=f"plant_database_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col_exp2:
        if st.button("📊 Xuất Excel", use_container_width=True):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_filtered.to_excel(writer, index=False, sheet_name='Plant Database')
            excel_data = output.getvalue()
            
            st.download_button(
                label="⬇️ Tải xuống Excel",
                data=excel_data,
                file_name=f"plant_database_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    with col_exp3:
        if st.button("🖨️ In Báo Cáo", use_container_width=True):
            st.info("Tính năng in ấn đang được phát triển...")

# === TAB TRA CỨU CHI TIẾT ===
elif selected == "🔍 Tra Cứu":
    st.title("🔬 HỒ SƠ SINH HỌC CHI TIẾT")
    
    # Tìm kiếm và chọn cây
    search_col1, search_col2 = st.columns([3, 1])
    
    with search_col1:
        plant_search = st.selectbox(
            "Tìm và chọn cây cần xem hồ sơ:",
            options=df["Tên Thương Mại"].tolist(),
            index=0,
            placeholder="Gõ tên cây để tìm kiếm...",
            help="Có thể tìm kiếm bằng tên thương mại hoặc tên khoa học"
        )
    
    with search_col2:
        random_plant = st.button("🎲 Cây ngẫu nhiên", use_container_width=True)
        if random_plant:
            random_idx = random.randint(0, len(df)-1)
            plant_search = df.iloc[random_idx]["Tên Thương Mại"]
    
    if plant_search:
        plant_data = df[df["Tên Thương Mại"] == plant_search].iloc[0]
        
        # Layout chính
        col_main1, col_main2 = st.columns([1, 2])
        
        with col_main1:
            # Ảnh minh họa với Unsplash
            keyword = plant_data["Tên Thương Mại"].split()[0].lower()
            st.image(
                f"https://source.unsplash.com/600x800/?{keyword}-plant",
                caption=f"Ảnh minh họa: {plant_data['Tên Thương Mại']}",
                use_container_width=True
            )
            
            # Quick stats
            with st.container(border=True):
                st.markdown("### 📊 Chỉ số nhanh")
                
                metrics_col1, metrics_col2 = st.columns(2)
                with metrics_col1:
                    st.metric("💧 Nước", f"{plant_data['Nước (L/ngày)']} L/ngày")
                    st.metric("❤️ Sống", f"{plant_data['Tỉ Lệ Sống (%)']}%")
                
                with metrics_col2:
                    st.metric("💰 Giá", f"{plant_data['Giá Dự Kiến (VND)']:,} VND")
                    st.metric("⚡ Độ khó", plant_data['Độ Khó'])
        
        with col_main2:
            # Header với badge
            rarity_badge = {
                "Phổ biến": "🟢",
                "Hiếm": "🟡", 
                "Rất hiếm": "🟠",
                "Cực kỳ hiếm": "🔴",
                "Đột biến độc nhất": "💎"
            }
            
            st.markdown(f"""
            <div style="border-left: 5px solid #00ffcc; padding-left: 20px;">
                <h1 style="margin-bottom: 5px;">{plant_data['Tên Thương Mại']}</h1>
                <h3 style="color: #88aaff; margin-top: 0;">
                    {rarity_badge.get(plant_data['Độ Quý Hiếm'], '📌')} {plant_data['Tên Khoa Học']}
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Tabs chi tiết
            tab1, tab2, tab3, tab4 = st.tabs(["📋 Thông Tin", "🌡️ Môi Trường", "⚕️ Chăm Sóc", "📝 Ghi Chú"])
            
            with tab1:
                col_info1, col_info2 = st.columns(2)
                
                with col_info1:
                    st.markdown("#### 🏷️ Thông tin cơ bản")
                    st.write(f"**Môi trường:** {plant_data['Môi Trường Sống']}")
                    st.write(f"**Chu kỳ sống:** {plant_data['Chu Kỳ Sống']}")
                    st.write(f"**Tốc độ sinh trưởng:** {plant_data['Tốc Độ Sinh Trưởng']}")
                    st.write(f"**Độ quý hiếm:** {plant_data['Độ Quý Hiếm']}")
                
                with col_info2:
                    st.markdown("#### ⚠️ Lưu ý đặc biệt")
                    st.write(f"**An toàn thú cưng:** {plant_data['Thú Cưng']}")
                    st.write(f"**Thanh lọc không khí:** {plant_data['Thanh Lọc KK']}")
                    st.write(f"**Độ ẩm đất:** {plant_data['Độ Ẩm Đất']}")
                    st.write(f"**Độ pH:** {plant_data['Độ pH']}")
            
            with tab2:
                col_env1, col_env2 = st.columns(2)
                
                with col_env1:
                    st.markdown("#### 🌞 Điều kiện ánh sáng")
                    light_info = plant_data['Ánh Sáng']
                    if "Full" in light_info or "Trực tiếp" in light_info:
                        st.success(f"**Cần nhiều ánh sáng:** {light_info}")
                    elif "Bóng" in light_info or "Tán xạ" in light_info:
                        st.info(f"**Ưa bóng râm:** {light_info}")
                    else:
                        st.info(f"**Ánh sáng:** {light_info}")
                    
                    # Visual indicator
                    light_level = random.randint(30, 100)  # Simulate light level
                    st.progress(light_level/100, text=f"Cường độ ánh sáng: {light_level}%")
                
                with col_env2:
                    st.markdown("#### 🌡️ Nhiệt độ & Ẩm độ")
                    temp_range = plant_data['Nhiệt Độ'].replace('°C', '').split('-')
                    if len(temp_range) == 2:
                        min_temp, max_temp = map(int, temp_range)
                        optimal_temp = (min_temp + max_temp) // 2
                        
                        st.metric("Nhiệt độ tối ưu", f"{optimal_temp}°C")
                        st.metric("Khoảng an toàn", f"{min_temp}°C - {max_temp}°C")
                    
                    # Humidity gauge
                    humidity = random.randint(40, 90)
                    st.progress(humidity/100, text=f"Độ ẩm lý tưởng: {humidity}%")
            
            with tab3:
                st.markdown("#### 💧 Hướng dẫn chăm sóc")
                
                care_col1, care_col2 = st.columns(2)
                
                with care_col1:
                    st.markdown("**Tưới nước:**")
                    water_needs = plant_data['Nước (L/ngày)']
                    if water_needs < 0.3:
                        st.success("Ít nước (cây chịu hạn)")
                    elif water_needs < 0.8:
                        st.info("Vừa phải")
                    else:
                        st.warning("Nhiều nước")
                    
                    st.write(f"**Lượng nước:** {water_needs} L/ngày")
                    st.write(f"**Tần suất bón:** {plant_data['Chế Độ Bón Phân']}")
                
                with care_col2:
                    st.markdown("**Mẹo chăm sóc:**")
                    tips = [
                        "Không tưới quá nhiều vào mùa đông",
                        "Thay chậu 1-2 năm/lần",
                        "Cắt tỉa lá vàng thường xuyên",
                        "Vệ sinh lá để tăng khả năng quang hợp",
                        "Tránh di chuyển cây thường xuyên"
                    ]
                    
                    for tip in random.sample(tips, 3):
                        st.write(f"• {tip}")
            
            with tab4:
                # User notes
                plant_id = str(plant_data['ID'])
                current_note = user_data['notes'].get(plant_id, "")
                
                new_note = st.text_area(
                    "Ghi chú cá nhân về cây này:",
                    value=current_note,
                    height=150,
                    placeholder="Ghi chú về lịch sử chăm sóc, vấn đề gặp phải, hoặc bất kỳ điều gì bạn muốn lưu ý..."
                )
                
                if new_note != current_note:
                    user_data['notes'][plant_id] = new_note
                    if st.button("💾 Lưu ghi chú"):
                        st.success("Đã lưu ghi chú!")
                
                # Recent activities (simulated)
                st.markdown("#### 📅 Hoạt động gần đây")
                activities = [
                    f"**{random.choice(['Hôm nay', 'Hôm qua', '3 ngày trước'])}**: {random.choice(['Tưới nước', 'Bón phân', 'Kiểm tra sâu bệnh', 'Thay đất'])}",
                    f"**Tuần trước**: {random.choice(['Cắt tỉa', 'Phun thuốc', 'Di chuyển vị trí'])}",
                    f"**Tháng trước**: {random.choice(['Thay chậu', 'Nhân giống', 'Xử lý bệnh'])}"
                ]
                
                for activity in activities:
                    st.write(f"• {activity}")
        
        # Action buttons
        st.markdown("---")
        action_col1, action_col2, action_col3, action_col4 = st.columns(4)
        
        with action_col1:
            if st.button("⭐ Thêm vào yêu thích", use_container_width=True):
                if plant_data['ID'] not in user_data['favorites']:
                    user_data['favorites'].append(plant_data['ID'])
                    st.success("Đã thêm vào danh sách yêu thích!")
                else:
                    st.info("Cây đã có trong danh sách yêu thích")
        
        with action_col2:
            if st.button("🌿 Thêm vào vườn", use_container_width=True):
                if plant_data['ID'] not in user_data['garden']:
                    user_data['garden'].append(plant_data['ID'])
                    st.success("Đã thêm vào vườn của bạn!")
                else:
                    st.info("Cây đã có trong vườn")
        
        with action_col3:
            if st.button("🖨️ In hồ sơ", use_container_width=True):
                st.info("Tính năng in ấn đang được phát triển...")
        
        with action_col4:
            share_text = f"Khám phá cây {plant_data['Tên Thương Mại']} trên EcoMind OS!"
            st.write(f"**Chia sẻ:** {share_text}")

# === TAB BÁC SĨ CÂY NÂNG CẤP ===
elif selected == "🩺 Bác Sĩ Cây":
    st.title("🤖 AI DIAGNOSTIC - BÁC SĨ THỰC VẬT THÔNG MINH")
    
    # Layout chính
    col_diag1, col_diag2 = st.columns([2, 1])
    
    with col_diag1:
        # Input triệu chứng
        st.markdown("### 📝 Mô tả vấn đề của cây")
        
        symptom_tabs = st.tabs(["✍️ Mô tả bằng văn bản", "🎯 Chọn triệu chứng"])
        
        with symptom_tabs[0]:
            problem = st.text_area(
                "Mô tả chi tiết tình trạng cây:",
                height=200,
                placeholder="""Ví dụ:
- Lá vàng từ mép vào trong
- Xuất hiện đốm nâu trên lá
- Rễ có mùi hôi, thối nhũn
- Cây rụng lá nhiều
- Thân mềm, không cứng cáp
- Xuất hiện nấm trắng trên đất"""
            )
        
        with symptom_tabs[1]:
            symptoms = st.multiselect(
                "Chọn các triệu chứng quan sát được:",
                [
                    "Lá vàng", "Lá nâu", "Lá rụng", "Lá cuộn", "Lá đốm",
                    "Thân mềm", "Thân thối", "Rễ thối", "Rễ đen",
                    "Nấm trắng", "Côn trùng", "Chậm lớn", "Không ra hoa"
                ]
            )
            
            if symptoms:
                problem = "Triệu chứng: " + ", ".join(symptoms)
        
        # Thông tin bổ sung
        with st.expander("➕ Thông tin bổ sung"):
            col_add1, col_add2, col_add3 = st.columns(3)
            
            with col_add1:
                plant_type = st.selectbox("Loại cây:", ["Cây trong nhà", "Cây ngoài trời", "Cây cảnh", "Cây ăn quả", "Hoa"])
            
            with col_add2:
                environment = st.selectbox("Môi trường:", ["Phòng khách", "Ban công", "Sân vườn", "Văn phòng", "Nhà tắm"])
            
            with col_add3:
                care_frequency = st.selectbox("Tần suất chăm sóc:", ["Hàng ngày", "2-3 ngày/lần", "Tuần/lần", "Thỉnh thoảng"])
        
        # Nút phân tích
        analyze_btn = st.button("🔬 PHÂN TÍCH VỚI AI", type="primary", use_container_width=True)
    
    with col_diag2:
        # Panel kết quả
        st.markdown("### 📊 KẾT QUẢ PHÂN TÍCH")
        
        if analyze_btn and (problem or symptoms):
            with st.spinner("🤖 AI đang phân tích triệu chứng..."):
                time.sleep(2)
                
                # Mô phỏng phân tích AI
                if "vàng" in problem.lower() and "lá" in problem.lower():
                    diagnosis = {
                        "bệnh": "🟡 THIẾU DINH DƯỠNG / ÚNG NƯỚC",
                        "nguyên_nhan": "Lá vàng thường do thiếu sắt, magie hoặc rễ bị úng nước",
                        "giai_doan": "Giai đoạn đầu",
                        "do_lanh": 65,
                        "khuyen_nghi": [
                            "Kiểm tra độ ẩm đất - chỉ tưới khi đất khô 2-3cm bề mặt",
                            "Bổ sung phân vi lượng (sắt, magie)",
                            "Đảm bảo chậu có lỗ thoát nước",
                            "Giảm 30% lượng nước tưới trong 1 tuần"
                        ]
                    }
                elif "thối" in problem.lower() or "hôi" in problem.lower():
                    diagnosis = {
                        "bệnh": "🔴 THỐI RỄ (ROOT ROT)",
                        "nguyên_nhan": "Nấm Pythium hoặc Phytophthora tấn công do đất ẩm ướt kéo dài",
                        "giai_doan": "Giai đoạn nghiêm trọng",
                        "do_lanh": 85,
                        "khuyen_nghi": [
                            "NGỪNG TƯỚI NGAY LẬP TỨC",
                            "Thay toàn bộ đất, cắt bỏ rễ thối",
                            "Xử lý rễ bằng thuốc Physan 20",
                            "Trồng lại với đất mới, thoát nước tốt"
                        ]
                    }
                elif "nấm" in problem.lower() or "trắng" in problem.lower():
                    diagnosis = {
                        "bệnh": "⚪ BỆNH PHẤN TRẮNG / NẤM ĐẤT",
                        "nguyên_nhan": "Độ ẩm cao, thiếu ánh sáng, không khí không lưu thông",
                        "giai_doan": "Giai đoạn trung bình",
                        "do_lanh": 45,
                        "khuyen_nghi": [
                            "Giảm tưới nước, tăng cường thông gió",
                            "Phun thuốc trị nấm (Neem oil hoặc baking soda)",
                            "Loại bỏ phần bị nhiễm nấm",
                            "Đưa cây ra nơi có ánh sáng"
                        ]
                    }
                else:
                    diagnosis = {
                        "bệnh": "🔵 SỐC MÔI TRƯỜNG / STRESS",
                        "nguyên_nhan": "Thay đổi đột ngột về nhiệt độ, ánh sáng hoặc vị trí",
                        "giai_doan": "Giai đoạn nhẹ",
                        "do_lanh": 30,
                        "khuyen_nghi": [
                            "Giữ cây ở vị trí ổn định",
                            "Không thay đổi chế độ chăm sóc đột ngột",
                            "Theo dõi trong 1 tuần",
                            "Che chắn nếu có ánh nắng gắt"
                        ]
                    }
                
                # Hiển thị kết quả
                st.success("✅ ĐÃ PHÂN TÍCH XONG!")
                
                # Container kết quả
                with st.container(border=True):
                    st.markdown(f"### {diagnosis['bệnh']}")
                    
                    st.markdown(f"**Nguyên nhân:** {diagnosis['nguyên_nhan']}")
                    st.markdown(f"**Giai đoạn:** {diagnosis['giai_doan']}")
                    
                    # Độ lành
                    st.progress(diagnosis['do_lanh']/100, 
                              text=f"Độ lành bệnh dự kiến: {diagnosis['do_lanh']}%")
                    
                    # Khuyến nghị
                    st.markdown("#### 💡 KHuyẾN NGHỊ XỬ LÝ:")
                    for i, rec in enumerate(diagnosis['khuyen_nghi'], 1):
                        st.write(f"{i}. {rec}")
                    
                    # Timeline recovery
                    st.markdown("#### 📅 LỊCH TRÌNH PHỤC HỒI:")
                    timeline = [
                        ("24h đầu", "Ngưng tưới, quan sát"),
                        ("3-5 ngày", "Áp dụng biện pháp xử lý"),
                        ("1 tuần", "Bắt đầu cải thiện"),
                        ("2-4 tuần", "Phục hồi hoàn toàn")
                    ]
                    
                    for time, action in timeline:
                        st.write(f"⏰ **{time}:** {action}")
        
        else:
            # Placeholder khi chưa phân tích
            st.info("""
            **Hướng dẫn sử dụng:**
            
            1. Mô tả triệu chứng ở ô bên trái
            2. Hoặc chọn triệu chứng từ danh sách
            3. Nhấn nút **PHÂN TÍCH VỚI AI**
            
            **AI sẽ cung cấp:**
            - Chẩn đoán bệnh
            - Nguyên nhân
            - Hướng xử lý chi tiết
            - Lịch trình phục hồi
            """)
    
    # Database triệu chứng
    st.markdown("---")
    st.markdown("### 📚 CƠ SỞ DỮ LIỆU BỆNH THỰC VẬT")
    
    # Tạo dataframe bệnh
    diseases = [
        ["Thối rễ", "Pythium spp.", "Rễ thối đen, mùi hôi", "Đất ẩm kéo dài", "Thay đất, cắt rễ thối"],
        ["Phấn trắng", "Erysiphe", "Bột trắng trên lá", "Ẩm cao, thiếu nắng", "Phun sulfur, tăng thông gió"],
        ["Đốm lá", "Cercospora", "Đốm nâu/vàng trên lá", "Nước đọng trên lá", "Cắt lá bệnh, phun thuốc"],
        ["Rệp sáp", "Pseudococcidae", "Côn trùng trắng nhỏ", "Cây yếu, thiếu dinh dưỡng", "Xịt cồn/neem oil"],
        ["Vàng lá", "Thiếu vi lượng", "Lá vàng gân xanh", "Đất nghèo dinh dưỡng", "Bổ sung phân vi lượng"]
    ]
    
    df_diseases = pd.DataFrame(diseases, columns=["Bệnh", "Tác nhân", "Triệu chứng", "Nguyên nhân", "Xử lý"])
    st.dataframe(df_diseases, use_container_width=True, hide_index=True)

# === TAB VƯỜN CỦA TÔI ===
elif selected == "🌿 Vườn Của Tôi":
    st.title("🌿 VƯỜN CÂY CÁ NHÂN")
    
    if not user_data['garden'] and not user_data['favorites']:
        st.warning("Vườn của bạn chưa có cây nào!")
        st.info("Thêm cây vào vườn từ tab **Thư Viện** hoặc **Tra Cứu**")
    else:
        # Tabs quản lý
        tab_garden, tab_fav, tab_care = st.tabs(["🏡 Vườn cây", "⭐ Yêu thích", "📅 Lịch chăm sóc"])
        
        with tab_garden:
            if user_data['garden']:
                st.markdown(f"### 🌱 Bạn đang có {len(user_data['garden'])} cây trong vườn")
                
                # Hiển thị cây trong vườn
                garden_plants = df[df['ID'].isin(user_data['garden'])]
                
                for idx, plant in garden_plants.iterrows():
                    with st.container(border=True):
                        col_plant1, col_plant2, col_plant3 = st.columns([1, 2, 1])
                        
                        with col_plant1:
                            st.image(
                                f"https://source.unsplash.com/200x200/?{plant['Tên Thương Mại'].split()[0].lower()}-plant",
                                use_container_width=True
                            )
                        
                        with col_plant2:
                            st.markdown(f"#### {plant['Tên Thương Mại']}")
                            st.markdown(f"*{plant['Tên Khoa Học']}*")
                            
                            # Health status (simulated)
                            health = random.randint(60, 100)
                            if health > 85:
                                status = "✅ Khỏe mạnh"
                            elif health > 70:
                                status = "⚠️ Cần quan tâm"
                            else:
                                status = "❌ Cần chăm sóc"
                            
                            st.progress(health/100, text=f"Sức khỏe: {health}% - {status}")
                            
                            # Next care date
                            next_care = datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 7))
                            st.caption(f"⏰ Chăm sóc tiếp theo: {next_care.strftime('%d/%m/%Y')}")
                        
                        with col_plant3:
                            if st.button("🗑️ Xóa", key=f"del_{plant['ID']}"):
                                user_data['garden'].remove(plant['ID'])
                                st.rerun()
                            
                            if st.button("📝 Ghi chú", key=f"note_{plant['ID']}"):
                                st.session_state.edit_note = plant['ID']
            else:
                st.info("Chưa có cây nào trong vườn. Hãy thêm cây từ tab Thư Viện!")
        
        with tab_fav:
            if user_data['favorites']:
                st.markdown(f"### ❤️ {len(user_data['favorites'])} cây yêu thích")
                
                fav_plants = df[df['ID'].isin(user_data['favorites'])]
                
                # Grid view
                items_per_row = 4
                fav_items = fav_plants.head(12).to_dict('records')
                
                for i in range(0, len(fav_items), items_per_row):
                    cols = st.columns(items_per_row)
                    for col_idx, col in enumerate(cols):
                        item_idx = i + col_idx
                        if item_idx < len(fav_items):
                            item = fav_items[item_idx]
                            with col:
                                with st.container(border=True):
                                    st.image(
                                        f"https://source.unsplash.com/150x150/?{item['Tên Thương Mại'].split()[0].lower()}",
                                        use_container_width=True
                                    )
                                    st.caption(item['Tên Thương Mại'])
                                    
                                    if st.button("➕ Thêm vườn", key=f"add_{item['ID']}", use_container_width=True):
                                        if item['ID'] not in user_data['garden']:
                                            user_data['garden'].append(item['ID'])
                                            st.success("Đã thêm!")
            else:
                st.info("Chưa có cây nào trong mục yêu thích")
        
        with tab_care:
            st.markdown("### 📅 LỊCH CHĂM SÓC THÔNG MINH")
            
            # Tạo lịch giả lập
            care_schedule = []
            today = datetime.datetime.now()
            
            for plant_id in user_data['garden'][:5]:  # Giới hạn 5 cây
                plant = df[df['ID'] == plant_id].iloc[0]
                
                # Tạo các công việc
                tasks = [
                    {
                        "task": "💧 Tưới nước",
                        "frequency": random.choice(["Hàng ngày", "2 ngày/lần", "3 ngày/lần"]),
                        "next_date": today + datetime.timedelta(days=random.randint(0, 3))
                    },
                    {
                        "task": "🌿 Bón phân",
                        "frequency": random.choice(["Tuần/lần", "2 tuần/lần", "Tháng/lần"]),
                        "next_date": today + datetime.timedelta(days=random.randint(3, 7))
                    },
                    {
                        "task": "✂️ Cắt tỉa",
                        "frequency": "Tháng/lần",
                        "next_date": today + datetime.timedelta(days=random.randint(10, 30))
                    }
                ]
                
                for task in tasks:
                    care_schedule.append({
                        "Cây": plant['Tên Thương Mại'],
                        "Công việc": task['task'],
                        "Tần suất": task['frequency'],
                        "Ngày tiếp theo": task['next_date'].strftime('%d/%m/%Y'),
                        "Ưu tiên": "🟢" if task['task'] == "💧 Tưới nước" else "🟡"
                    })
            
            if care_schedule:
                df_care = pd.DataFrame(care_schedule)
                df_care = df_care.sort_values('Ngày tiếp theo')
                
                st.dataframe(
                    df_care,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Today's tasks
                st.markdown("#### 📌 CÔNG VIỆC HÔM NAY")
                today_tasks = [t for t in care_schedule 
                              if datetime.datetime.strptime(t['Ngày tiếp theo'], '%d/%m/%Y').date() == today.date()]
                
                if today_tasks:
                    for task in today_tasks:
                        with st.container(border=True):
                            st.markdown(f"**{task['Cây']}** - {task['Công việc']}")
                            st.caption(f"Tần suất: {task['Tần suất']}")
                            
                            col_t1, col_t2 = st.columns(2)
                            with col_t1:
                                if st.button("✅ Hoàn thành", key=f"done_{task['Cây']}_{task['Công việc']}"):
                                    st.success("Đã đánh dấu hoàn thành!")
                            with col_t2:
                                if st.button("⏰ Hoãn", key=f"delay_{task['Cây']}_{task['Công việc']}"):
                                    st.info("Đã hoãn đến ngày mai")
                else:
                    st.success("🎉 Không có công việc nào cho hôm nay!")
            else:
                st.info("Thêm cây vào vườn để tạo lịch chăm sóc tự động")

# === TAB ANALYTICS NÂNG CẤP ===
elif selected == "📊 Analytics":
    st.title("📈 PHÂN TÍCH DỮ LIỆU NÂNG CAO")
    
    # Analytics dashboard
    tab_ana1, tab_ana2, tab_ana3 = st.tabs(["📊 Tổng quan", "📈 Xu hướng", "🔍 Phân tích chuyên sâu"])
    
    with tab_ana1:
        st.markdown("### 📊 PHÂN TÍCH TỔNG THỂ")
        
        # Metrics row
        m1, m2, m3, m4 = st.columns(4)
        
        with m1:
            avg_price = df['Giá Dự Kiến (VND)'].mean()
            st.metric("💰 Giá trung bình", f"{avg_price:,.0f} VND")
        
        with m2:
            avg_survival = df['Tỉ Lệ Sống (%)'].mean()
            st.metric("❤️ Tỉ lệ sống TB", f"{avg_survival:.1f}%")
        
        with m3:
            indoor_count = len(df[df['Môi Trường Sống'] == 'Trong nhà'])
            st.metric("🏠 Cây trong nhà", indoor_count)
        
        with m4:
            pet_safe_percent = len(df[df['Thú Cưng'].str.contains('✅')]) / len(df) * 100
            st.metric("🐕 An toàn thú cưng", f"{pet_safe_percent:.1f}%")
        
        # Biểu đồ chính
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("#### 📈 Phân bố theo môi trường")
            env_dist = df['Môi Trường Sống'].value_counts()
            
            fig_env = px.bar(
                x=env_dist.index,
                y=env_dist.values,
                color=env_dist.values,
                color_continuous_scale="Viridis",
                template="plotly_dark"
            )
            
            fig_env.update_layout(
                xaxis_title="Môi trường sống",
                yaxis_title="Số lượng loài",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_env, use_container_width=True)
        
        with col_chart2:
            st.markdown("#### 💰 Phân phối giá")
            
            # Lấy mẫu cho biểu đồ mượt mà
            sample_prices = df.sample(min(100, len(df)))['Giá Dự Kiến (VND)']
            
            fig_price = px.histogram(
                sample_prices,
                nbins=20,
                color_discrete_sequence=['#00ffcc'],
                template="plotly_dark"
            )
            
            fig_price.update_layout(
                xaxis_title="Giá (VND)",
                yaxis_title="Số lượng loài",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_price, use_container_width=True)
    
    with tab_ana2:
        st.markdown("### 📈 XU HƯỚNG & DỰ BÁO")
        
        # Tạo dữ liệu giả cho xu hướng
        dates = pd.date_range(end=datetime.datetime.now(), periods=12, freq='M')
        trend_data = {
            'Tháng': dates.strftime('%Y-%m'),
            'Số loài mới': np.random.randint(50, 200, 12),
            'Giá trung bình': np.random.randint(500000, 2000000, 12),
            'Độ phổ biến': np.random.uniform(0.5, 0.95, 12)
        }
        
        df_trend = pd.DataFrame(trend_data)
        
        # Biểu đồ xu hướng
        fig_trend = px.line(
            df_trend,
            x='Tháng',
            y=['Số loài mới', 'Giá trung bình'],
            template="plotly_dark",
            color_discrete_sequence=['#00ffcc', '#0088cc']
        )
        
        fig_trend.update_layout(
            title="Xu hướng phát triển database",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Dự báo
        st.markdown("#### 🔮 DỰ BÁO THỊ TRƯỜNG")
        
        forecast_col1, forecast_col2, forecast_col3 = st.columns(3)
        
        with forecast_col1:
            with st.container(border=True):
                st.markdown("**Xu hướng nổi bật**")
                st.success("Cây thanh lọc không khí +15%")
                st.info("Cây mini +8%")
                st.warning("Cây quý hiếm -5%")
        
        with forecast_col2:
            with st.container(border=True):
                st.markdown("**Mùa vụ**")
                st.write("📈 **Mùa xuân:** Tăng trưởng mạnh")
                st.write("📉 **Mùa hè:** Nhu cầu giảm")
                st.write("📈 **Mùa thu:** Phục hồi")
                st.write("📊 **Mùa đông:** Ổn định")
        
        with forecast_col3:
            with st.container(border=True):
                st.markdown("**Khuyến nghị**")
                st.info("• Tập trung cây dễ chăm")
                st.info("• Phát triển dòng cây mini")
                st.info("• Mở rộng cây thủy canh")
    
    with tab_ana3:
        st.markdown("### 🔍 PHÂN TÍCH CHUYÊN SÂU")
        
        # Correlation matrix (giả lập)
        st.markdown("#### 🔗 MA TRẬN TƯƠNG QUAN")
        
        # Tạo dữ liệu correlation giả
        corr_data = pd.DataFrame({
            'Nước': df['Nước (L/ngày)'],
            'Tỉ lệ sống': df['Tỉ Lệ Sống (%)'],
            'Giá': np.log(df['Giá Dự Kiến (VND)']),
            'Độ khó': pd.Categorical(df['Độ Khó']).codes
        })
        
        corr_matrix = corr_data.corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r",
            template="plotly_dark"
        )
        
        fig_corr.update_layout(
            title="Tương quan giữa các yếu tố",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Phân cụm (Clustering - giả lập)
        st.markdown("#### 🎯 PHÂN NHÓM TỰ ĐỘNG")
        
        cluster_col1, cluster_col2 = st.columns(2)
        
        with cluster_col1:
            st.markdown("**Nhóm 1: Cây dễ chăm**")
            st.write("• Nhu cầu nước thấp")
            st.write("• Tỉ lệ sống cao")
            st.write("• Giá phổ thông")
            st.metric("Số lượng", f"{random.randint(800, 1200):,}")
        
        with cluster_col2:
            st.markdown("**Nhóm 2: Cây cao cấp**")
            st.write("• Chăm sóc chuyên nghiệp")
            st.write("• Độ quý hiếm cao")
            st.write("• Giá trị lớn")
            st.metric("Số lượng", f"{random.randint(200, 400):,}")

# === TAB CẤU HÌNH NÂNG CẤP ===
elif selected == "⚙️ Cấu Hình":
    st.title("⚙️ HỆ THỐNG & CÀI ĐẶT")
    
    # Tabs cài đặt
    tab_set1, tab_set2, tab_set3, tab_set4 = st.tabs(["🎨 Giao diện", "🔔 Thông báo", "🗃️ Dữ liệu", "ℹ️ Hệ thống"])
    
    with tab_set1:
        st.markdown("### 🎨 TÙY CHỈNH GIAO DIỆN")
        
        theme = st.selectbox(
            "Chọn chủ đề:",
            ["Dark Cyberpunk", "Light Mode", "Forest Green", "Ocean Blue", "Sunset Purple"]
        )
        
        col_theme1, col_theme2 = st.columns(2)
        
        with col_theme1:
            primary_color = st.color_picker("Màu chính:", "#00ffcc")
            font_size = st.slider("Cỡ chữ:", 12, 20, 14)
            rounded_corners = st.toggle("Góc bo tròn", value=True)
        
        with col_theme2:
            animations = st.toggle("Hiệu ứng động", value=True)
            compact_mode = st.toggle("Chế độ compact", value=False)
            high_contrast = st.toggle("Độ tương phản cao", value=False)
        
        if st.button("💾 Áp dụng cài đặt", use_container_width=True):
            st.success("Đã lưu cài đặt giao diện!")
    
    with tab_set2:
        st.markdown("### 🔔 CÀI ĐẶT THÔNG BÁO")
        
        notif_col1, notif_col2 = st.columns(2)
        
        with notif_col1:
            st.markdown("**Thông báo hệ thống**")
            email_notif = st.toggle("Email thông báo", value=True)
            push_notif = st.toggle("Push notification", value=True)
            care_reminders = st.toggle("Nhắc lịch chăm cây", value=True)
        
        with notif_col2:
            st.markdown("**Tần suất**")
            report_frequency = st.selectbox(
                "Báo cáo hàng tuần:",
                ["Không gửi", "Hàng tuần", "Hàng tháng", "Hàng quý"]
            )
            update_notif = st.toggle("Cập nhật database", value=True)
        
        st.markdown("### 📧 CẤU HÌNH EMAIL")
        email_address = st.text_input("Email nhận thông báo:", placeholder="your.email@example.com")
        
        if st.button("💾 Lưu cài đặt thông báo", use_container_width=True):
            st.success("Đã lưu cài đặt thông báo!")
    
    with tab_set3:
        st.markdown("### 🗃️ QUẢN LÝ DỮ LIỆU")
        
        data_col1, data_col2 = st.columns(2)
        
        with data_col1:
            st.markdown("**Tự động sao lưu**")
            auto_backup = st.toggle("Tự động sao lưu", value=True)
            backup_freq = st.selectbox(
                "Tần suất sao lưu:",
                ["Hàng ngày", "Hàng tuần", "Hàng tháng"]
            )
            
            st.markdown("**Xuất dữ liệu**")
            export_format = st.radio(
                "Định dạng xuất:",
                ["CSV", "Excel", "JSON", "Tất cả"]
            )
        
        with data_col2:
            st.markdown("**Dọn dẹp**")
            cache_days = st.slider("Xóa cache cũ (ngày):", 1, 365, 30)
            
            if st.button("🧹 Dọn dẹp cache", use_container_width=True):
                st.cache_data.clear()
                st.success("Đã dọn dẹp cache!")
            
            st.markdown("**Khôi phục**")
            backup_file = st.file_uploader("Chọn file backup:", type=['csv', 'json'])
            
            if backup_file and st.button("🔄 Khôi phục", use_container_width=True):
                st.info("Tính năng đang phát triển...")
        
        # Backup now button
        if st.button("💾 Sao lưu ngay", type="primary", use_container_width=True):
            with st.spinner("Đang sao lưu dữ liệu..."):
                time.sleep(2)
                st.success("✅ Sao lưu hoàn tất!")
    
    with tab_set4:
        st.markdown("### ℹ️ THÔNG TIN HỆ THỐNG")
        
        sys_info_col1, sys_info_col2 = st.columns(2)
        
        with sys_info_col1:
            st.markdown("**Phiên bản**")
            st.write(f"**EcoMind OS:** v8.5.1 Enterprise")
            st.write(f"**Streamlit:** {st.__version__}")
            st.write(f"**Pandas:** {pd.__version__}")
            st.write(f"**Cập nhật cuối:** 2024-01-15")
        
        with sys_info_col2:
            st.markdown("**Tài nguyên**")
            
            # Simulated resource usage
            cpu_usage = random.randint(15, 45)
            memory_usage = random.randint(40, 75)
            disk_usage = random.randint(60, 85)
            
            st.progress(cpu_usage/100, text=f"CPU: {cpu_usage}%")
            st.progress(memory_usage/100, text=f"RAM: {memory_usage}%")
            st.progress(disk_usage/100, text=f"Disk: {disk_usage}%")
        
        st.markdown("---")
        st.markdown("#### ⚠️ HÀNH ĐỘNG NGUY HIỂM")
        
        danger_col1, danger_col2, danger_col3 = st.columns(3)
        
        with danger_col1:
            if st.button("🔄 Khởi động lại", use_container_width=True):
                st.warning("Hệ thống sẽ khởi động lại...")
                time.sleep(1)
                st.rerun()
        
        with danger_col2:
            if st.button("🗑️ Xóa dữ liệu", use_container_width=True):
                st.error("Tính năng này sẽ xóa tất cả dữ liệu!")
        
        with danger_col3:
            if st.button("🔒 Đăng xuất", use_container_width=True):
                st.info("Đang đăng xuất...")
                time.sleep(1)
                st.rerun()
        
        # System logs (simulated)
        st.markdown("---")
        with st.expander("📋 NHẬT KÝ HỆ THỐNG"):
            logs = [
                f"[{datetime.datetime.now().strftime('%H:%M:%S')}] INFO: System started",
                f"[{(datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime('%H:%M:%S')}] INFO: Database loaded successfully",
                f"[{(datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime('%H:%M:%S')}] INFO: User session started",
                f"[{(datetime.datetime.now() - datetime.timedelta(minutes=30)).strftime('%H:%M:%S')}] WARNING: Cache cleared",
                f"[{(datetime.datetime.now() - datetime.timedelta(hours=1)).strftime('%H:%M:%S')}] INFO: Backup completed"
            ]
            
            for log in logs:
                st.code(log)

# --- 6. FOOTER ---
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("**© 2024 EcoMind OS**")
    st.caption("Enterprise Edition v8.5.1")

with footer_col2:
    st.markdown("**📞 Hỗ trợ**")
    st.caption("support@ecomind.com")

with footer_col3:
    st.markdown("**🌐 Kết nối**")
    st.caption("GitHub | Discord | LinkedIn")

# Sidebar footer
with st.sidebar:
    st.markdown("---")
    st.caption(f"© 2024 EcoMind OS • {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
