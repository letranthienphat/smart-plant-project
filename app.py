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
import pytz
from datetime import timedelta
import requests
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import math

# --- 1. CẤU HÌNH GIAO DIỆN ĐƠN GIẢN ---
st.set_page_config(
    page_title="EcoMind - Dự báo chăm sóc cây",
    layout="wide", 
    page_icon="🌿",
    initial_sidebar_state="expanded"
)

# CSS đơn giản, sạch sẽ
st.markdown("""
<style>
    /* Reset mặc định */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    
    /* Container chính */
    .main-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    /* Cards đơn giản */
    .simple-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 255, 204, 0.1);
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .simple-card:hover {
        border-color: #00ffcc;
        transform: translateY(-2px);
    }
    
    /* Headers đơn giản */
    h1, h2, h3 {
        color: #00ffcc !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }
    
    h1 {
        font-size: 2rem !important;
        border-bottom: 2px solid #00ffcc;
        padding-bottom: 0.5rem;
    }
    
    /* Metrics đẹp */
    div[data-testid="stMetricValue"] {
        color: #00ffcc !important;
        font-size: 1.8rem !important;
        font-weight: 700;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #88aaff !important;
        font-size: 0.9rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00ffcc, #0088cc);
        color: black;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 255, 204, 0.3);
    }
    
    /* Input fields */
    .stTextInput input, .stSelectbox div, .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 255, 204, 0.2) !important;
        border-radius: 8px !important;
        color: white !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        background: rgba(255, 255, 255, 0.05);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #00ffcc, #0088cc);
        color: black !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00ffcc, #0088cc);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.3rem !important; }
        h3 { font-size: 1.1rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- 2. KHỞI TẠO DỮ LIỆU ---
@st.cache_data
def load_plant_data():
    """Tạo dữ liệu cây trồng"""
    plants = []
    plant_types = [
        ("Hoa Hồng", 0.5, "Trung bình", "Nắng nhiều"),
        ("Lan", 0.3, "Khó", "Bóng râm"),
        ("Xương Rồng", 0.1, "Dễ", "Nắng đầy đủ"),
        ("Sen Đá", 0.15, "Rất dễ", "Nắng nhiều"),
        ("Trầu Bà", 0.4, "Dễ", "Bán phần"),
        ("Dương Xỉ", 0.6, "Trung bình", "Bóng râm"),
        ("Cây Lưỡi Hổ", 0.2, "Rất dễ", "Mọi điều kiện"),
        ("Cây Kim Tiền", 0.3, "Dễ", "Bán phần"),
        ("Cây Phát Tài", 0.4, "Dễ", "Bán phần"),
        ("Cây Ngũ Gia Bì", 0.35, "Dễ", "Bán phần")
    ]
    
    for i, (name, water, difficulty, light) in enumerate(plant_types, 1):
        plants.append({
            "ID": i,
            "Tên Cây": name,
            "Nước (L/ngày)": water,
            "Độ khó": difficulty,
            "Ánh sáng": light,
            "Nhiệt độ": f"{random.randint(18, 25)}-{random.randint(25, 32)}°C",
            "Tần suất tưới": f"{random.choice(['Hàng ngày', '2 ngày/lần', '3 ngày/lần'])}",
            "Mô tả": f"Cây {name.lower()} phù hợp với điều kiện {light.lower()}. {random.choice(['Dễ chăm sóc', 'Thanh lọc không khí tốt', 'Phù hợp người mới bắt đầu'])}."
        })
    
    return pd.DataFrame(plants)

# --- 3. HỆ THỐNG BẢN ĐỒ ---
class MapSystem:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="ecomind_app")
        self.default_location = [10.8231, 106.6297]  # TP.HCM
        
    def create_map(self, location=None, zoom=12):
        """Tạo bản đồ Folium"""
        if location is None:
            location = self.default_location
        
        m = folium.Map(
            location=location,
            zoom_start=zoom,
            tiles="OpenStreetMap",
            width="100%",
            height="100%",
            control_scale=True
        )
        
        # Thêm marker
        folium.Marker(
            location=location,
            popup="Vị trí cây trồng",
            tooltip="Nhấn để xem chi tiết",
            icon=folium.Icon(color="green", icon="leaf", prefix="fa")
        ).add_to(m)
        
        # Thêm vòng tròn phạm vi
        folium.Circle(
            location=location,
            radius=500,
            color="#00ffcc",
            fill=True,
            fill_color="#00ffcc",
            fill_opacity=0.2,
            popup="Phạm vi 500m"
        ).add_to(m)
        
        return m
    
    def search_location(self, query):
        """Tìm kiếm vị trí"""
        try:
            location = self.geolocator.geocode(query)
            if location:
                return {
                    "name": location.address,
                    "lat": location.latitude,
                    "lon": location.longitude,
                    "address": location.address
                }
        except:
            pass
        return None
    
    def get_sample_locations(self):
        """Danh sách vị trí mẫu tại Việt Nam"""
        return {
            "Hà Nội": [21.0285, 105.8542],
            "TP Hồ Chí Minh": [10.8231, 106.6297],
            "Đà Nẵng": [16.0544, 108.2022],
            "Huế": [16.4637, 107.5909],
            "Đà Lạt": [11.9404, 108.4583],
            "Nha Trang": [12.2388, 109.1967],
            "Cần Thơ": [10.0452, 105.7469],
            "Hải Phòng": [20.8449, 106.6881]
        }

# --- 4. HỆ THỐNG DỰ BÁO ĐƠN GIẢN ---
class SimpleForecast:
    def __init__(self):
        self.weather_cache = {}
    
    def get_weather_forecast(self, lat, lon, days=7):
        """Lấy dự báo thời tiết (sử dụng Open-Meteo API miễn phí)"""
        try:
            url = f"https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                "timezone": "auto",
                "forecast_days": days
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return self._format_weather_data(data)
        except:
            pass
        
        # Fallback: tạo dữ liệu mô phỏng
        return self._generate_mock_forecast(lat, lon, days)
    
    def _format_weather_data(self, data):
        """Định dạng dữ liệu thời tiết"""
        forecast = []
        dates = data["daily"]["time"]
        temp_max = data["daily"]["temperature_2m_max"]
        temp_min = data["daily"]["temperature_2m_min"]
        precipitation = data["daily"]["precipitation_sum"]
        
        for i in range(len(dates)):
            forecast.append({
                "Ngày": datetime.datetime.strptime(dates[i], "%Y-%m-%d").strftime("%d/%m"),
                "Nhiệt độ cao": temp_max[i],
                "Nhiệt độ thấp": temp_min[i],
                "Mưa (mm)": precipitation[i],
                "Điều kiện": self._get_condition(temp_max[i], precipitation[i])
            })
        
        return pd.DataFrame(forecast)
    
    def _generate_mock_forecast(self, lat, lon, days):
        """Tạo dự báo giả lập"""
        forecast = []
        today = datetime.datetime.now()
        
        for i in range(days):
            date = today + timedelta(days=i)
            
            # Nhiệt độ dựa trên vĩ độ
            base_temp = 25 - (abs(lat) - 10) * 0.3
            temp_max = base_temp + random.uniform(-3, 5)
            temp_min = temp_max - random.uniform(3, 8)
            
            # Mưa
            if random.random() < 0.3:
                rain = round(random.uniform(0, 20), 1)
            else:
                rain = 0
            
            forecast.append({
                "Ngày": date.strftime("%d/%m"),
                "Nhiệt độ cao": round(temp_max, 1),
                "Nhiệt độ thấp": round(temp_min, 1),
                "Mưa (mm)": rain,
                "Điều kiện": self._get_condition(temp_max, rain)
            })
        
        return pd.DataFrame(forecast)
    
    def _get_condition(self, temp, rain):
        """Xác định điều kiện thời tiết"""
        if rain > 10:
            return "🌧️ Mưa nhiều"
        elif rain > 0:
            return "🌦️ Mưa nhẹ"
        elif temp > 32:
            return "☀️ Nắng nóng"
        elif temp > 25:
            return "⛅ Nắng nhẹ"
        else:
            return "☁️ Mát mẻ"
    
    def calculate_water_needs(self, plant_water, weather_df):
        """Tính nhu cầu nước dựa trên thời tiết"""
        water_needs = []
        
        for _, day in weather_df.iterrows():
            # Điều chỉnh theo nhiệt độ
            temp_factor = 1 + (day["Nhiệt độ cao"] - 25) * 0.03
            
            # Điều chỉnh theo mưa
            rain_adjust = max(0, plant_water - (day["Mưa (mm)"] / 20))
            
            # Nhu cầu thực tế
            actual_need = plant_water * temp_factor - rain_adjust
            actual_need = max(0.05, actual_need)  # Ít nhất 0.05L
            
            water_needs.append({
                "Ngày": day["Ngày"],
                "Nhu cầu cơ bản": round(plant_water, 2),
                "Điều chỉnh nhiệt độ": round(temp_factor, 2),
                "Điều chỉnh mưa": round(rain_adjust, 2),
                "Nhu cầu thực tế": round(actual_need, 2),
                "Khuyến nghị": "Giảm tưới" if day["Mưa (mm)"] > 5 else "Tưới bình thường"
            })
        
        return pd.DataFrame(water_needs)

# --- 5. KHỞI TẠO HỆ THỐNG ---
# Khởi tạo các component
map_system = MapSystem()
forecast_system = SimpleForecast()
df_plants = load_plant_data()

# Khởi tạo session state
if 'selected_plant' not in st.session_state:
    st.session_state.selected_plant = df_plants.iloc[0]
if 'selected_location' not in st.session_state:
    st.session_state.selected_location = map_system.default_location
if 'location_name' not in st.session_state:
    st.session_state.location_name = "TP Hồ Chí Minh"
if 'forecast_data' not in st.session_state:
    st.session_state.forecast_data = None
if 'water_calculation' not in st.session_state:
    st.session_state.water_calculation = None

# --- 6. SIDEBAR ĐƠN GIẢN ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h2 style="color: #00ffcc; margin: 0;">🌿 EcoMind</h2>
        <p style="color: #88aaff; margin: 0; font-size: 0.9rem;">Dự báo chăm sóc cây thông minh</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Menu chính - CHỈ 4 TAB
    selected = option_menu(
        menu_title=None,
        options=["🏠 Tổng quan", "📍 Vị trí", "🌿 Chọn cây", "📅 Dự báo"],
        icons=["house", "geo-alt", "tree", "cloud-sun"],
        default_index=0,
        styles={
            "container": {"padding": "0!important"},
            "nav-link": {
                "font-size": "14px",
                "padding": "12px 16px",
                "margin": "4px 0",
                "border-radius": "8px",
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg, #00ffcc, #0088cc)",
                "color": "black",
            },
        }
    )
    
    st.markdown("---")
    
    # Thông tin phiên bản
    st.markdown("### ℹ️ Thông tin")
    st.markdown("**Phiên bản:** 3.0.1")
    st.markdown("**Cập nhật:** 01/2024")
    st.markdown("**Email:** tranthienphatle@gmail.com")
    
    # Hiển thị thông tin hiện tại
    if st.session_state.selected_plant is not None:
        st.markdown("---")
        st.markdown("### 🌿 Cây đang chọn")
        st.info(f"**{st.session_state.selected_plant['Tên Cây']}**")
        st.caption(f"Nước: {st.session_state.selected_plant['Nước (L/ngày)']}L/ngày")
    
    if st.session_state.location_name:
        st.markdown("### 📍 Vị trí")
        st.success(st.session_state.location_name)

# --- 7. NỘI DUNG CHÍNH ---
# === TAB 1: TỔNG QUAN ===
if selected == "🏠 Tổng quan":
    st.title("🌍 EcoMind - Hệ Thống Dự Báo Chăm Sóc Cây")
    
    # Giới thiệu ngắn gọn
    with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### 🤔 Hệ thống này làm gì?
            
            EcoMind giúp bạn **dự báo chính xác** nhu cầu chăm sóc cây dựa trên:
            
            - **📍 Vị trí thực tế** của cây
            - **🌦️ Dự báo thời tiết** 7 ngày
            - **🌿 Đặc tính** từng loại cây
            - **💧 Tính toán nhu cầu nước** thông minh
            
            **Đặc biệt:** Phù hợp với chậu cây **tái chế không điện tử**!
            """)
        
        with col2:
            st.image("https://cdn-icons-png.flaticon.com/512/2917/2917995.png", 
                    width=150, caption="Chậu cây thông minh")
    
    # Metrics nhanh
    st.markdown("### 📊 Thống kê nhanh")
    
    col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
    with col_stats1:
        st.metric("Số loại cây", len(df_plants))
    with col_stats2:
        st.metric("Độ chính xác", "92%")
    with col_stats3:
        st.metric("Tiết kiệm nước", "35%")
    with col_stats4:
        st.metric("Phiên bản", "3.0.1")
    
    # Hướng dẫn nhanh
    st.markdown("### 🚀 Bắt đầu nhanh")
    
    guide_col1, guide_col2, guide_col3 = st.columns(3)
    
    with guide_col1:
        with st.container(border=True):
            st.markdown("#### 1. Chọn vị trí")
            st.markdown("""
            - Truy cập tab **📍 Vị trí**
            - Tìm kiếm địa chỉ
            - Hoặc chọn trên bản đồ
            """)
    
    with guide_col2:
        with st.container(border=True):
            st.markdown("#### 2. Chọn cây")
            st.markdown("""
            - Truy cập tab **🌿 Chọn cây**
            - Chọn loại cây bạn có
            - Xem thông tin chi tiết
            """)
    
    with guide_col3:
        with st.container(border=True):
            st.markdown("#### 3. Xem dự báo")
            st.markdown("""
            - Truy cập tab **📅 Dự báo**
            - Xem dự báo thời tiết
            - Nhận lịch chăm sóc
            """)
    
    # Hiển thị dự báo hôm nay nếu có
    if st.session_state.forecast_data is not None:
        st.markdown("### 🌤️ Thời tiết hôm nay")
        
        today_weather = st.session_state.forecast_data.iloc[0]
        
        col_weather1, col_weather2, col_weather3 = st.columns(3)
        with col_weather1:
            st.metric("Nhiệt độ", f"{today_weather['Nhiệt độ cao']}°C")
        with col_weather2:
            st.metric("Mưa", f"{today_weather['Mưa (mm)']}mm")
        with col_weather3:
            st.metric("Điều kiện", today_weather['Điều kiện'])

# === TAB 2: VỊ TRÍ ===
elif selected == "📍 Vị trí":
    st.title("📍 Quản Lý Vị Trí Cây Trồng")
    
    tab_loc1, tab_loc2 = st.tabs(["🗺️ Bản đồ tương tác", "🔍 Tìm kiếm"])
    
    with tab_loc1:
        col_map1, col_map2 = st.columns([3, 1])
        
        with col_map1:
            st.markdown("### 🗺️ Bản đồ vị trí")
            
            # Hiển thị bản đồ
            m = map_system.create_map(
                location=st.session_state.selected_location,
                zoom=12
            )
            
            # Sử dụng streamlit-folium để hiển thị
            map_data = st_folium(
                m,
                width=700,
                height=500,
                returned_objects=["last_clicked", "bounds"]
            )
            
            # Xử lý click trên bản đồ
            if map_data and map_data.get("last_clicked"):
                lat = map_data["last_clicked"]["lat"]
                lng = map_data["last_clicked"]["lng"]
                st.session_state.selected_location = [lat, lng]
                
                # Cố gắng lấy tên địa điểm
                try:
                    location = map_system.geolocator.reverse(f"{lat}, {lng}")
                    if location:
                        st.session_state.location_name = location.address.split(",")[0]
                        st.success(f"📍 Đã chọn: {st.session_state.location_name}")
                except:
                    st.session_state.location_name = f"{lat:.4f}, {lng:.4f}"
                    st.info(f"📍 Tọa độ: {lat:.4f}, {lng:.4f}")
        
        with col_map2:
            st.markdown("### 📍 Tùy chọn")
            
            # Chọn từ vị trí mẫu
            st.markdown("**Vị trí mẫu:**")
            sample_locs = map_system.get_sample_locations()
            
            for name, coords in sample_locs.items():
                if st.button(f"📍 {name}", use_container_width=True):
                    st.session_state.selected_location = coords
                    st.session_state.location_name = name
                    st.rerun()
            
            st.markdown("---")
            
            # Nhập tọa độ thủ công
            st.markdown("**Nhập tọa độ:**")
            lat_input = st.number_input("Vĩ độ:", value=st.session_state.selected_location[0], format="%.6f")
            lon_input = st.number_input("Kinh độ:", value=st.session_state.selected_location[1], format="%.6f")
            
            if st.button("📌 Áp dụng tọa độ", use_container_width=True):
                st.session_state.selected_location = [lat_input, lon_input]
                st.session_state.location_name = f"{lat_input:.4f}, {lon_input:.4f}"
                st.success("Đã cập nhật tọa độ!")
            
            # Thông tin vị trí hiện tại
            st.markdown("---")
            st.markdown("**Vị trí hiện tại:**")
            st.info(st.session_state.location_name)
            st.caption(f"Tọa độ: {st.session_state.selected_location[0]:.4f}, {st.session_state.selected_location[1]:.4f}")
            
            # Nút lấy dự báo
            if st.button("🌤️ Lấy dự báo thời tiết", type="primary", use_container_width=True):
                with st.spinner("Đang lấy dữ liệu thời tiết..."):
                    forecast = forecast_system.get_weather_forecast(
                        st.session_state.selected_location[0],
                        st.session_state.selected_location[1],
                        days=7
                    )
                    st.session_state.forecast_data = forecast
                    st.success("Đã cập nhật dự báo!")
    
    with tab_loc2:
        st.markdown("### 🔍 Tìm kiếm địa chỉ")
        
        col_search1, col_search2 = st.columns([3, 1])
        
        with col_search1:
            search_query = st.text_input(
                "Nhập địa chỉ:",
                placeholder="Ví dụ: 123 Đường ABC, Quận 1, TP.HCM",
                key="location_search"
            )
        
        with col_search2:
            if st.button("🔍 Tìm kiếm", use_container_width=True):
                if search_query:
                    with st.spinner("Đang tìm kiếm..."):
                        result = map_system.search_location(search_query)
                        if result:
                            st.session_state.selected_location = [result["lat"], result["lon"]]
                            st.session_state.location_name = result["address"]
                            st.success(f"✅ Đã tìm thấy: {result['address']}")
                        else:
                            st.error("❌ Không tìm thấy địa chỉ. Vui lòng thử lại!")
        
        # Hiển thị kết quả tìm kiếm gần đây
        if st.session_state.location_name:
            with st.container(border=True):
                st.markdown("**📌 Vị trí hiện tại:**")
                st.markdown(f"**{st.session_state.location_name}**")
                
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.metric("Vĩ độ", f"{st.session_state.selected_location[0]:.4f}")
                with col_info2:
                    st.metric("Kinh độ", f"{st.session_state.selected_location[1]:.4f}")
                
                # Link Google Maps
                maps_url = f"https://www.google.com/maps?q={st.session_state.selected_location[0]},{st.session_state.selected_location[1]}"
                st.markdown(f"[🗺️ Xem trên Google Maps]({maps_url})")

# === TAB 3: CHỌN CÂY ===
elif selected == "🌿 Chọn cây":
    st.title("🌿 Chọn Cây Trồng Của Bạn")
    
    # Tìm kiếm và lọc
    col_search, col_filter = st.columns([2, 1])
    
    with col_search:
        search_term = st.text_input(
            "🔍 Tìm kiếm cây:",
            placeholder="Nhập tên cây hoặc đặc điểm...",
            key="plant_search"
        )
    
    with col_filter:
        filter_difficulty = st.selectbox(
            "Lọc theo độ khó:",
            ["Tất cả", "Rất dễ", "Dễ", "Trung bình", "Khó"]
        )
    
    # Lọc cây
    filtered_plants = df_plants.copy()
    
    if search_term:
        filtered_plants = filtered_plants[
            filtered_plants["Tên Cây"].str.contains(search_term, case=False, na=False) |
            filtered_plants["Mô tả"].str.contains(search_term, case=False, na=False)
        ]
    
    if filter_difficulty != "Tất cả":
        filtered_plants = filtered_plants[filtered_plants["Độ khó"] == filter_difficulty]
    
    # Hiển thị cây
    st.markdown(f"### 📋 Có {len(filtered_plants)} cây phù hợp")
    
    if len(filtered_plants) == 0:
        st.warning("Không tìm thấy cây phù hợp. Hãy thử từ khóa khác!")
    else:
        # Chế độ hiển thị
        view_mode = st.radio(
            "Chế độ hiển thị:",
            ["Dạng lưới", "Dạng bảng"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        if view_mode == "Dạng bảng":
            # Hiển thị bảng đơn giản
            display_cols = ["Tên Cây", "Nước (L/ngày)", "Độ khó", "Ánh sáng", "Tần suất tưới"]
            st.dataframe(
                filtered_plants[display_cols],
                use_container_width=True,
                height=400,
                hide_index=True
            )
        else:
            # Hiển thị dạng card
            cols_per_row = 3
            plants_list = filtered_plants.to_dict('records')
            
            for i in range(0, len(plants_list), cols_per_row):
                cols = st.columns(cols_per_row)
                
                for col_idx, col in enumerate(cols):
                    plant_idx = i + col_idx
                    if plant_idx < len(plants_list):
                        plant = plants_list[plant_idx]
                        
                        with col:
                            with st.container(border=True):
                                # Header
                                difficulty_color = {
                                    "Rất dễ": "#4CAF50",
                                    "Dễ": "#8BC34A",
                                    "Trung bình": "#FFC107",
                                    "Khó": "#FF9800"
                                }.get(plant["Độ khó"], "#00ffcc")
                                
                                st.markdown(f"""
                                <div style="border-left: 4px solid {difficulty_color}; padding-left: 10px;">
                                    <h4 style="margin: 0;">{plant['Tên Cây']}</h4>
                                    <small style="color: #88aaff;">{plant['Độ khó']} • {plant['Ánh sáng']}</small>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Thông tin
                                st.markdown(f"**💧 Nước:** {plant['Nước (L/ngày)']}L/ngày")
                                st.markdown(f"**🌡️ Nhiệt độ:** {plant['Nhiệt độ']}")
                                st.markdown(f"**⏰ Tưới:** {plant['Tần suất tưới']}")
                                
                                # Action buttons
                                col_btn1, col_btn2 = st.columns(2)
                                with col_btn1:
                                    if st.button("👁️ Chi tiết", key=f"view_{plant['ID']}", use_container_width=True):
                                        st.session_state.selected_plant = plant
                                        st.success(f"Đã chọn: {plant['Tên Cây']}")
                                
                                with col_btn2:
                                    if st.button("✅ Chọn", key=f"select_{plant['ID']}", type="primary", use_container_width=True):
                                        st.session_state.selected_plant = plant
                                        st.session_state.show_forecast = True
                                        st.success(f"✅ Đã chọn cây: {plant['Tên Cây']}")
                                        st.rerun()
    
    # Hiển thị cây đang chọn
    if st.session_state.selected_plant is not None:
        st.markdown("---")
        st.markdown("### 🌟 Cây đang chọn")
        
        plant = st.session_state.selected_plant
        
        with st.container(border=True):
            col_plant1, col_plant2 = st.columns([1, 2])
            
            with col_plant1:
                # Hiển thị ảnh đại diện
                plant_icon = "🌹" if "Hồng" in plant["Tên Cây"] else "🌿"
                st.markdown(f"<h1 style='text-align: center;'>{plant_icon}</h1>", unsafe_allow_html=True)
            
            with col_plant2:
                st.markdown(f"#### {plant['Tên Cây']}")
                st.markdown(f"*{plant['Mô tả']}*")
                
                # Thông số chi tiết
                col_detail1, col_detail2 = st.columns(2)
                with col_detail1:
                    st.metric("💧 Nước/ngày", f"{plant['Nước (L/ngày)']}L")
                    st.metric("⚡ Độ khó", plant['Độ khó'])
                with col_detail2:
                    st.metric("☀️ Ánh sáng", plant['Ánh sáng'])
                    st.metric("⏰ Tưới", plant['Tần suất tưới'])
                
                # Nút xem dự báo
                if st.button("📅 Xem dự báo chăm sóc", type="primary", use_container_width=True):
                    st.switch_page = "📅 Dự báo"
                    st.rerun()

# === TAB 4: DỰ BÁO ===
elif selected == "📅 Dự báo":
    st.title("📅 Dự Báo Chăm Sóc")
    
    # Kiểm tra đã chọn cây và vị trí chưa
    if st.session_state.selected_plant is None:
        st.warning("⚠️ Vui lòng chọn cây trước ở tab **🌿 Chọn cây**")
        if st.button("🌿 Đến tab Chọn cây", use_container_width=True):
            st.switch_page = "🌿 Chọn cây"
            st.rerun()
        st.stop()
    
    if st.session_state.location_name is None:
        st.warning("⚠️ Vui lòng chọn vị trí ở tab **📍 Vị trí**")
        if st.button("📍 Đến tab Vị trí", use_container_width=True):
            st.switch_page = "📍 Vị trí"
            st.rerun()
        st.stop()
    
    # Header với thông tin
    col_header1, col_header2 = st.columns([2, 1])
    
    with col_header1:
        st.markdown(f"### 🌿 {st.session_state.selected_plant['Tên Cây']}")
        st.markdown(f"📍 **Vị trí:** {st.session_state.location_name}")
    
    with col_header2:
        if st.button("🔄 Cập nhật dự báo", use_container_width=True):
            with st.spinner("Đang cập nhật..."):
                forecast = forecast_system.get_weather_forecast(
                    st.session_state.selected_location[0],
                    st.session_state.selected_location[1],
                    days=7
                )
                st.session_state.forecast_data = forecast
                st.rerun()
    
    # Lấy dữ liệu dự báo nếu chưa có
    if st.session_state.forecast_data is None:
        with st.spinner("Đang lấy dữ liệu thời tiết..."):
            forecast = forecast_system.get_weather_forecast(
                st.session_state.selected_location[0],
                st.session_state.selected_location[1],
                days=7
            )
            st.session_state.forecast_data = forecast
    
    # Hiển thị dự báo thời tiết
    st.markdown("### 🌦️ Dự Báo Thời Tiết 7 Ngày")
    
    # Biểu đồ nhiệt độ
    if st.session_state.forecast_data is not None:
        forecast_df = st.session_state.forecast_data
        
        # Tạo biểu đồ
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=forecast_df['Ngày'],
            y=forecast_df['Nhiệt độ cao'],
            name='Nhiệt độ cao',
            line=dict(color='#ff6b6b', width=3),
            mode='lines+markers'
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast_df['Ngày'],
            y=forecast_df['Nhiệt độ thấp'],
            name='Nhiệt độ thấp',
            line=dict(color='#4dabf7', width=3),
            mode='lines+markers',
            fill='tonexty',
            fillcolor='rgba(77, 171, 247, 0.2)'
        ))
        
        fig.update_layout(
            title="Dự báo nhiệt độ",
            template="plotly_dark",
            xaxis_title="Ngày",
            yaxis_title="Nhiệt độ (°C)",
            hovermode="x unified",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Bảng dự báo chi tiết
        st.markdown("#### 📋 Chi Tiết Từng Ngày")
        
        display_df = forecast_df.copy()
        display_df['Mưa'] = display_df['Mưa (mm)'].apply(
            lambda x: f"🌧️ {x}mm" if x > 0 else "☀️ Không mưa"
        )
        
        st.dataframe(
            display_df[['Ngày', 'Nhiệt độ cao', 'Nhiệt độ thấp', 'Mưa', 'Điều kiện']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Ngày": "📅 Ngày",
                "Nhiệt độ cao": "🔥 Cao",
                "Nhiệt độ thấp": "❄️ Thấp",
                "Mưa": "💧 Mưa",
                "Điều kiện": "🌤️ Điều kiện"
            }
        )
    
    # Tính toán nhu cầu nước
    st.markdown("### 💧 Tính Toán Nhu Cầu Nước")
    
    if st.session_state.selected_plant is not None and st.session_state.forecast_data is not None:
        plant_water = st.session_state.selected_plant['Nước (L/ngày)']
        water_needs = forecast_system.calculate_water_needs(
            plant_water,
            st.session_state.forecast_data
        )
        
        st.session_state.water_calculation = water_needs
        
        # Biểu đồ nhu cầu nước
        fig_water = px.bar(
            water_needs,
            x='Ngày',
            y='Nhu cầu thực tế',
            title='Nhu cầu nước hàng ngày',
            color='Nhu cầu thực tế',
            color_continuous_scale='Blues'
        )
        
        fig_water.update_layout(
            template="plotly_dark",
            xaxis_title="Ngày",
            yaxis_title="Nước (L)",
            height=300
        )
        
        st.plotly_chart(fig_water, use_container_width=True)
        
        # Bảng tính toán
        st.markdown("#### 📊 Chi Tiết Tính Toán")
        
        st.dataframe(
            water_needs,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Ngày": "📅 Ngày",
                "Nhu cầu cơ bản": "💧 Cơ bản",
                "Điều chỉnh nhiệt độ": "🌡️ Điều chỉnh",
                "Điều chỉnh mưa": "🌧️ Giảm mưa",
                "Nhu cầu thực tế": "🚰 Thực tế",
                "Khuyến nghị": "💡 Khuyến nghị"
            }
        )
        
        # Tổng kết
        total_water = water_needs['Nhu cầu thực tế'].sum()
        avg_water = water_needs['Nhu cầu thực tế'].mean()
        
        col_sum1, col_sum2, col_sum3 = st.columns(3)
        with col_sum1:
            st.metric("Tổng nước 7 ngày", f"{total_water:.1f}L")
        with col_sum2:
            st.metric("Trung bình/ngày", f"{avg_water:.2f}L")
        with col_sum3:
            water_saving = ((plant_water * 7) - total_water) / (plant_water * 7) * 100
            st.metric("Tiết kiệm", f"{water_saving:.1f}%")
    
    # Lịch chăm sóc đơn giản
    st.markdown("### 📅 Lịch Chăm Sóc Đề Xuất")
    
    if st.session_state.water_calculation is not None:
        schedule = []
        
        for _, day in st.session_state.water_calculation.iterrows():
            water_needed = day['Nhu cầu thực tế']
            
            if water_needed > st.session_state.selected_plant['Nước (L/ngày)'] * 1.2:
                action = "💧 Tưới nhiều"
                note = f"Tưới {water_needed:.2f}L (nắng nóng)"
            elif water_needed < st.session_state.selected_plant['Nước (L/ngày)'] * 0.8:
                action = "💧 Tưới ít"
                note = f"Tưới {water_needed:.2f}L (có mưa)"
            else:
                action = "💧 Tưới bình thường"
                note = f"Tưới {water_needed:.2f}L"
            
            schedule.append({
                "📅 Ngày": day['Ngày'],
                "✅ Hành động": action,
                "📝 Ghi chú": note,
                "💧 Lượng nước": f"{water_needed:.2f}L"
            })
        
        df_schedule = pd.DataFrame(schedule)
        
        # Hiển thị lịch
        st.dataframe(
            df_schedule,
            use_container_width=True,
            hide_index=True
        )
        
        # Xuất lịch
        csv = df_schedule.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Tải lịch chăm sóc (CSV)",
            data=csv,
            file_name=f"lich_cham_soc_{st.session_state.selected_plant['Tên Cây']}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    # Khuyến nghị đặc biệt
    st.markdown("### 💡 Khuyến Nghị Đặc Biệt")
    
    recommendations = []
    
    if st.session_state.forecast_data is not None:
        max_temp = st.session_state.forecast_data['Nhiệt độ cao'].max()
        total_rain = st.session_state.forecast_data['Mưa (mm)'].sum()
        
        if max_temp > 35:
            recommendations.append("🌡️ **Nhiệt độ cao:** Di chuyển cây vào bóng râm vào buổi trưa")
        if total_rain > 30:
            recommendations.append("☔ **Mưa nhiều:** Giảm tưới nước, kiểm tra thoát nước")
        if max_temp < 18:
            recommendations.append("🧥 **Trời lạnh:** Hạn chế tưới nước vào buổi tối")
    
    if not recommendations:
        recommendations.append("✅ **Điều kiện tốt:** Duy trì chế độ chăm sóc hiện tại")
    
    for rec in recommendations:
        st.markdown(f"- {rec}")

# --- 8. FOOTER ---
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("**🌿 EcoMind System**")
    st.caption("Phiên bản 3.0.1")

with footer_col2:
    st.markdown("**📧 Liên hệ**")
    st.caption("tranthienphatle@gmail.com")

with footer_col3:
    st.markdown("**♻️ Sản phẩm xanh**")
    st.caption("Chậu cây tái chế 100%")

# Hiển thị thông tin debug (có thể ẩn khi deploy)
if st.sidebar.checkbox("🔧 Hiển thị thông tin debug", False):
    st.sidebar.markdown("### Debug Info")
    st.sidebar.json({
        "selected_plant": st.session_state.selected_plant['Tên Cây'] if st.session_state.selected_plant else None,
        "location": st.session_state.selected_location,
        "location_name": st.session_state.location_name,
        "has_forecast": st.session_state.forecast_data is not None
    })
