import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import wikipedia
import requests
import random
import time

# --- 1. CẤU HÌNH GIAO DIỆN "NEON CYBERPUNK" (BẢN V8.0 ĐẸP NHẤT) ---
st.set_page_config(page_title="EcoMind OS - Ultimate", layout="wide", page_icon="🧬")
wikipedia.set_lang("vi")

# CSS: Giữ lại giao diện Đen-Xanh Neon mà bạn thích
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .stDataFrame { border: 1px solid #00ffcc; border-radius: 5px; }
    div[data-testid="stMetricValue"] { color: #00ffcc !important; font-weight: bold; font-size: 26px; }
    h1, h2, h3 { color: #00ffcc !important; }
    .css-1r6slb0 { background-color: #1f2937; border: 1px solid #374151; }
    /* Khung bản đồ đẹp hơn */
    iframe { border-radius: 10px; border: 2px solid #00ffcc; }
</style>
""", unsafe_allow_html=True)

# --- 2. HỆ THỐNG XỬ LÝ DỮ LIỆU & API ---

@st.cache_data(show_spinner="Đang tải dữ liệu thực vật...")
def generate_instant_db():
    """Tạo 3500 cây (Giữ nguyên từ bản v8)"""
    loai = ["Hoa Hồng", "Lan", "Xương Rồng", "Sen Đá", "Trầu Bà", "Dương Xỉ", "Cây Cọ", "Trúc", "Tùng", "Cúc"]
    tinh_tu = ["Hoàng Gia", "Cẩm Thạch", "Bạch Tạng", "Hắc Kim", "Lửa", "Tuyết", "Đại Đế", "Phú Quý"]
    data = []
    for i in range(1, 3501):
        ten = f"{random.choice(loai)} {random.choice(tinh_tu)}"
        nuoc = round(random.uniform(0.1, 1.5), 2)
        anh_sang = random.choice(["Bóng râm", "Tán xạ", "Full nắng"])
        data.append([i, ten, f"Species {i}", nuoc, anh_sang])
    return pd.DataFrame(data, columns=["ID", "Tên Cây", "Tên Khoa Học", "Nước (L)", "Ánh Sáng"])

df = generate_instant_db()

def strict_wiki_search(query):
    """Hàm tìm kiếm Wikipedia CHỈ TRẢ VỀ CÂY"""
    # Tự động thêm từ khóa ngữ cảnh để wikipedia không tìm nhầm
    search_terms = [f"Cây {query}", f"Hoa {query}", f"Thực vật {query}"]
    
    for term in search_terms:
        try:
            results = wikipedia.search(term)
            if results:
                # Lấy kết quả đầu tiên
                page = wikipedia.page(results[0])
                # Kiểm tra sơ bộ xem nội dung có liên quan đến thực vật không
                keywords = ["cây", "hoa", "lá", "thực vật", "loài", "họ", "trồng"]
                if any(k in page.summary.lower() for k in keywords):
                    return {
                        "found": True,
                        "title": page.title,
                        "summary": wikipedia.summary(results[0], sentences=4),
                        "url": page.url,
                        "img": page.images[0] if page.images else "https://via.placeholder.com/400"
                    }
        except:
            continue
    return {"found": False}

def get_location_data(city_name):
    """Lấy tọa độ từ tên thành phố (Open-Meteo Geocoding)"""
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=vi&format=json"
        res = requests.get(url).json()
        if "results" in res:
            return res["results"][0]["latitude"], res["results"][0]["longitude"], res["results"][0]["name"]
    except:
        pass
    return 10.8231, 106.6297, "Không tìm thấy (Mặc định: TP.HCM)" # Mặc định

def get_weather_realtime(lat, lon):
    """Lấy thời tiết thật"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relativehumidity_2m"
        res = requests.get(url).json()
        temp = res['current_weather']['temperature']
        hum = res['hourly']['relativehumidity_2m'][0]
        return temp, hum
    except:
        return 30, 70 # Giá trị dự phòng

# --- 3. THANH ĐIỀU HƯỚNG BÊN TRÁI ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2964/2964514.png", width=80)
    st.title("ECO-MIND V10")
    
    selected = option_menu(
        menu_title=None,
        options=["Trung Tâm Điều Khiển", "Vị Trí & Môi Trường", "Thư Viện (3500+)", "Tra Cứu Wiki"],
        icons=["speedometer2", "geo-alt", "book", "search"],
        default_index=1,
        styles={
            "container": {"background-color": "#0e1117"},
            "nav-link-selected": {"background-color": "#00ffcc", "color": "black"},
        }
    )

# --- 4. LOGIC CHÍNH ---

# === TAB VỊ TRÍ & MÔI TRƯỜNG (TÍNH NĂNG MỚI) ===
if selected == "Vị Trí & Môi Trường":
    st.title("🌍 CẤU HÌNH VỊ TRÍ VƯỜN")
    
    col_map, col_controls = st.columns([2, 1])
    
    with col_controls:
        st.subheader("🛠️ Chế độ Dữ liệu")
        mode = st.radio("Nguồn dữ liệu môi trường:", ["☁️ Tự động (Online API)", "🖐️ Nhập thủ công"], horizontal=True)
        
        # Biến lưu trữ môi trường
        env_temp, env_hum, env_lat, env_lon = 0, 0, 0, 0
        
        if "Tự động" in mode:
            st.info("📡 Hệ thống đang định vị vệ tinh...")
            city_input = st.text_input("🔍 Nhập địa điểm vườn của bạn:", "Ho Chi Minh City")
            
            # Lấy tọa độ & Thời tiết
            lat, lon, city_real = get_location_data(city_input)
            temp, hum = get_weather_realtime(lat, lon)
            
            st.success(f"📍 Đã định vị: **{city_real}**")
            env_lat, env_lon = lat, lon
            env_temp, env_hum = temp, hum
            
            # Hiển thị thông số Auto
            st.metric("Nhiệt độ (Real-time)", f"{temp} °C")
            st.metric("Độ ẩm (Real-time)", f"{hum} %")
            
        else: # Chế độ thủ công
            st.warning("🖐️ Bạn đang nhập dữ liệu bằng tay")
            env_lat = st.number_input("Vĩ độ (Latitude)", value=10.7769)
            env_lon = st.number_input("Kinh độ (Longitude)", value=106.7009)
            env_temp = st.slider("Nhiệt độ hiện tại (°C)", 10, 50, 30)
            env_hum = st.slider("Độ ẩm đất/khí (%)", 0, 100, 65)

        # Lưu vào Session State để các Tab khác dùng
        st.session_state['env'] = {'temp': env_temp, 'hum': env_hum, 'lat': env_lat, 'lon': env_lon}

    with col_map:
        st.subheader("🗺️ Bản đồ Vị trí Cây trồng")
        # Tạo dữ liệu bản đồ
        map_data = pd.DataFrame({'lat': [env_lat], 'lon': [env_lon], 'name': ['Vị trí Vườn']})
        
        # Hiển thị bản đồ (Zoom vào vị trí)
        st.map(map_data, zoom=13, use_container_width=True)
        st.caption("🔴 Chấm đỏ là vị trí vườn/thiết bị của bạn.")

# === TAB TRA CỨU WIKI (STRICT MODE) ===
elif selected == "Tra Cứu Wiki":
    st.title("🧠 TRA CỨU THỰC VẬT (STRICT MODE)")
    st.caption("Hệ thống chỉ tìm kiếm thông tin về Cây cối/Thực vật. Các từ khóa khác sẽ bị loại bỏ.")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        query = st.text_input("Nhập tên cây:", placeholder="Ví dụ: Lưỡi hổ, Python...")
        btn = st.button("🔍 Phân tích AI", type="primary")
        
    with c2:
        if btn and query:
            with st.spinner(f"Đang lọc dữ liệu rác để tìm '{query}'..."):
                res = strict_wiki_search(query)
                
                if res["found"]:
                    st.success(f"✅ Đã tìm thấy thực vật: {res['title']}")
                    st.image(res['img'], height=300)
                    st.markdown(f"### 📖 Tóm tắt:")
                    st.write(res['summary'])
                    st.markdown(f"[🔗 Đọc chi tiết trên Wikipedia]({res['url']})")
                else:
                    st.error("❌ Không tìm thấy loài cây này!")
                    st.write("Hệ thống đã loại bỏ các kết quả không phải là thực vật (Ví dụ: Ngôn ngữ lập trình, Địa danh...). Hãy thử tên chính xác hơn.")

# === TAB TRUNG TÂM ĐIỀU KHIỂN (DASHBOARD) ===
elif selected == "Trung Tâm Điều Khiển":
    st.title("📈 DASHBOARD GIÁM SÁT")
    
    # Lấy dữ liệu môi trường từ Session
    if 'env' not in st.session_state:
        st.warning("⚠️ Vui lòng qua Tab 'Vị Trí & Môi Trường' để cấu hình trước!")
        env = {'temp': 30, 'hum': 70}
    else:
        env = st.session_state['env']

    # Metrics đẹp
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Nhiệt độ Vườn", f"{env['temp']} °C", "Môi trường")
    col2.metric("Độ ẩm", f"{env['hum']} %", "Hiện tại")
    col3.metric("Số lượng cây", "3,500", "Database")
    col4.metric("Trạng thái", "Ổn định", "System OK")
    
    st.divider()
    
    # Biểu đồ phân tích (Giả lập dựa trên nhiệt độ nhập vào)
    st.subheader("📊 Dự báo sức khỏe cây trồng")
    
    # Logic: Nếu nhiệt độ quá cao -> Cây thoát nước nhanh
    loss_rate = 0.5 * (1 + (env['temp'] - 25)/10)
    days = list(range(1, 8))
    water_remain = [5 - (loss_rate * d) for d in days]
    
    fig = px.area(x=days, y=water_remain, 
                  title=f"Dự báo lượng nước trong 7 ngày tới (Tại {env['temp']}°C)",
                  labels={'x': 'Ngày tới', 'y': 'Lít nước còn lại'},
                  template="plotly_dark")
    fig.update_traces(line_color='#00ffcc')
    st.plotly_chart(fig, use_container_width=True)

# === TAB THƯ VIỆN ===
elif selected == "Thư Viện (3500+)":
    st.title("📚 KHO DỮ LIỆU (V8 CORE)")
    
    # Tính năng tìm kiếm trong bảng
    search = st.text_input("🔍 Tìm nhanh trong database:", "")
    if search:
        df_show = df[df["Tên Cây"].str.contains(search, case=False)]
    else:
        df_show = df
        
    st.dataframe(df_show, use_container_width=True, height=600, hide_index=True)
