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
from datetime import timedelta
import folium
from streamlit_folium import st_folium
import math

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(
    page_title="EcoMind OS - Hệ Thống Chăm Sóc Cây Thông Minh",
    layout="wide", 
    page_icon="🌿",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:tranthienphatle@gmail.com',
        'Report a bug': 'mailto:tranthienphatle@gmail.com',
        'About': 'EcoMind OS - Phiên bản Cloud 1.0'
    }
)

# CSS
st.markdown("""
<style>
    :root {
        --primary-color: #00ffcc;
        --secondary-color: #0088cc;
        --dark-bg: #0a192f;
        --darker-bg: #0d1b2a;
        --card-bg: rgba(255, 255, 255, 0.07);
        --text-color: #e0e1dd;
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--dark-bg) 0%, var(--darker-bg) 100%);
        color: var(--text-color);
    }
    
    h1, h2, h3, h4 {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color)) !important;
        color: var(--dark-bg) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. HÀM HỖ TRỢ ---
def get_plant_type(plant_name):
    """Xác định loại cây"""
    if "Hoa" in plant_name:
        return "Hoa"
    elif any(x in plant_name for x in ["Xương Rồng", "Sen Đá"]):
        return "Mọng nước"
    elif any(x in plant_name for x in ["Chanh", "Ớt"]):
        return "Ăn quả"
    elif any(x in plant_name for x in ["Trầu", "Lưỡi Hổ"]):
        return "Cảnh lá"
    else:
        return "Cây cảnh"

# --- 3. TẢI DATABASE CÂY ---
@st.cache_data
def load_plant_database():
    """Tải database cây trồng với cache"""
    plants = []
    
    plant_types = [
        ["Hoa Hồng", 0.5, "Trung bình", "Nắng nhiều", "18-28°C", "40-60%", "6.0-7.0", "Hoa hồng là loài cây biểu tượng cho tình yêu"],
        ["Hoa Lan", 0.3, "Khó", "Bóng râm", "20-30°C", "50-70%", "5.5-6.5", "Lan là loài cây quý phái"],
        ["Hoa Cúc", 0.4, "Dễ", "Nắng nhiều", "15-25°C", "40-60%", "6.0-7.5", "Hoa cúc tượng trưng cho sự trường thọ"],
        ["Hoa Đồng Tiền", 0.45, "Trung bình", "Nắng đầy đủ", "18-24°C", "40-60%", "6.0-6.5", "Hoa đồng tiền mang ý nghĩa may mắn"],
        ["Trầu Bà", 0.4, "Dễ", "Bán phần", "20-32°C", "40-60%", "6.0-7.5", "Cây trầu bà thanh lọc không khí rất tốt"],
        ["Cây Lưỡi Hổ", 0.2, "Rất dễ", "Mọi điều kiện", "18-30°C", "30-50%", "6.0-8.0", "Cây lưỡi hổ hấp thụ độc tố"],
        ["Xương Rồng", 0.1, "Dễ", "Nắng đầy đủ", "20-35°C", "20-40%", "6.0-7.5", "Xương rồng chịu hạn tốt"],
        ["Sen Đá", 0.15, "Rất dễ", "Nắng nhiều", "18-30°C", "30-50%", "6.0-7.0", "Sen đá có nhiều loại với hình dáng đa dạng"],
        ["Chanh", 0.6, "Trung bình", "Nắng đầy đủ", "20-30°C", "50-70%", "5.5-7.0", "Chanh trồng chậu cho quả quanh năm"],
        ["Ớt", 0.5, "Dễ", "Nắng nhiều", "25-35°C", "40-60%", "6.0-7.0", "Ớt trồng chậu dễ chăm, cho quả nhiều màu sắc"],
    ]
    
    for i, (name, water, difficulty, light, temp, humidity, ph, desc) in enumerate(plant_types, 1):
        plants.append({
            "ID": i,
            "Tên Cây": name,
            "Nước (L/ngày)": water,
            "Độ khó": difficulty,
            "Ánh sáng": light,
            "Nhiệt độ": temp,
            "Độ ẩm": humidity,
            "Độ pH": ph,
            "Mô tả": desc,
            "Loại": get_plant_type(name)  # ĐÃ SỬA: dùng hàm trực tiếp
        })
    
    return pd.DataFrame(plants)

# --- 4. HỆ THỐNG DỰ BÁO THỜI TIẾT ---
class WeatherSystem:
    def __init__(self):
        self.version = "1.0.0"
        self.build_date = "2024-01-20"
        
    def get_weather_data(self, lat, lon, days=7):
        """Lấy dữ liệu thời tiết"""
        forecast = []
        today = datetime.datetime.now()
        
        # Xác định mùa
        month = today.month
        season = self._get_season(month, lat)
        
        for i in range(days):
            date = today + timedelta(days=i)
            
            # Tính nhiệt độ
            base_temp = self._calculate_base_temp(lat, month, i)
            temp_max = round(base_temp + random.uniform(-3, 5), 1)
            temp_min = round(temp_max - random.uniform(3, 8), 1)
            
            # Tính mưa
            precipitation = self._calculate_precipitation(season, i)
            
            # Các thông số khác
            humidity = random.randint(40, 90)
            wind_speed = round(random.uniform(1, 15), 1)
            wind_direction = random.choice(["Đông", "Tây", "Nam", "Bắc"])
            
            # Điều kiện thời tiết
            condition, icon = self._get_weather_condition(temp_max, precipitation)
            
            forecast.append({
                "date": date.strftime("%Y-%m-%d"),
                "day": date.strftime("%d/%m"),
                "temp_max": temp_max,
                "temp_min": temp_min,
                "precipitation": precipitation,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "wind_direction": wind_direction,
                "condition": condition,
                "icon": icon,
                "season": season
            })
        
        return pd.DataFrame(forecast)
    
    def _get_season(self, month, lat):
        """Xác định mùa"""
        if lat > 0:
            if month in [12, 1, 2]:
                return "Đông"
            elif month in [3, 4, 5]:
                return "Xuân"
            elif month in [6, 7, 8]:
                return "Hè"
            else:
                return "Thu"
        else:
            if month in [12, 1, 2]:
                return "Hè"
            elif month in [3, 4, 5]:
                return "Thu"
            elif month in [6, 7, 8]:
                return "Đông"
            else:
                return "Xuân"
    
    def _calculate_base_temp(self, lat, month, day_offset):
        """Tính nhiệt độ cơ bản"""
        equator_temp = 27
        lat_effect = abs(lat) * 0.5
        month_effect = math.sin((month - 3) * math.pi / 6) * 5
        base_temp = equator_temp - lat_effect + month_effect
        return round(base_temp, 1)
    
    def _calculate_precipitation(self, season, day_offset):
        """Tính lượng mưa"""
        if season == "Hè":
            if random.random() < 0.4:
                return round(random.uniform(5, 30), 1)
        elif season == "Đông":
            if random.random() < 0.2:
                return round(random.uniform(1, 10), 1)
        else:
            if random.random() < 0.3:
                return round(random.uniform(2, 20), 1)
        return 0.0
    
    def _get_weather_condition(self, temp, precipitation):
        """Xác định điều kiện thời tiết"""
        if precipitation > 20:
            return "Mưa rất to", "🌧️"
        elif precipitation > 10:
            return "Mưa to", "🌧️"
        elif precipitation > 0:
            return "Mưa nhẹ", "🌦️"
        elif temp > 35:
            return "Nắng nóng", "🔥"
        elif temp > 30:
            return "Nắng", "☀️"
        elif temp > 25:
            return "Nắng nhẹ", "⛅"
        elif temp < 15:
            return "Lạnh", "❄️"
        else:
            return "Ôn hòa", "🌤️"
    
    def calculate_water_needs(self, plant_water, weather_data):
        """Tính nhu cầu nước"""
        calculations = []
        
        for _, day in weather_data.iterrows():
            temp_factor = 1 + max(0, (day['temp_max'] - 25) * 0.03)
            humidity_factor = 1 - max(0, (day['humidity'] - 60) * 0.01)
            rain_factor = max(0, 1 - (day['precipitation'] / 20))
            
            base_need = plant_water * temp_factor * humidity_factor
            adjusted_need = base_need * rain_factor
            final_need = max(0.05, adjusted_need)
            
            calculations.append({
                "Ngày": day['day'],
                "Nhiệt độ": f"{day['temp_min']}°C - {day['temp_max']}°C",
                "Mưa": f"{day['precipitation']}mm",
                "Nhu cầu cơ bản": round(plant_water, 2),
                "Nhu cầu điều chỉnh": round(final_need, 2),
                "Khuyến nghị": self._get_watering_recommendation(final_need, plant_water, day['precipitation'])
            })
        
        return pd.DataFrame(calculations)
    
    def _get_watering_recommendation(self, actual_need, base_need, precipitation):
        """Đưa ra khuyến nghị tưới nước"""
        if precipitation > 15:
            return "Không cần tưới (mưa nhiều)"
        elif precipitation > 5:
            return "Giảm 50% lượng nước"
        elif actual_need > base_need * 1.3:
            return "Tăng 30% lượng nước (nắng nóng)"
        elif actual_need > base_need * 1.1:
            return "Tăng 10% lượng nước"
        elif actual_need < base_need * 0.7:
            return "Giảm 30% lượng nước"
        else:
            return "Tưới bình thường"

# --- 5. HỆ THỐNG BẢN ĐỒ ---
class MapSystem:
    def __init__(self):
        self.locations = {
            "Hà Nội": {"lat": 21.0285, "lon": 105.8542, "type": "Thủ đô", "region": "Miền Bắc"},
            "TP Hồ Chí Minh": {"lat": 10.8231, "lon": 106.6297, "type": "Thành phố", "region": "Miền Nam"},
            "Đà Nẵng": {"lat": 16.0544, "lon": 108.2022, "type": "Thành phố", "region": "Miền Trung"},
            "Tân Hiệp, Kiên Giang": {"lat": 10.1234, "lon": 106.5678, "type": "Huyện", "region": "Miền Nam"},
            "Phú Giáo, Bình Dương": {"lat": 11.2345, "lon": 106.7890, "type": "Huyện", "region": "Miền Nam"},
        }
    
    def search_location(self, query):
        """Tìm kiếm địa điểm"""
        results = []
        query = query.lower().strip()
        
        if not query:
            return results
        
        for name, data in self.locations.items():
            if query in name.lower():
                results.append({
                    "name": name,
                    "lat": data["lat"],
                    "lon": data["lon"],
                    "type": data["type"],
                    "region": data["region"]
                })
        
        return results
    
    def create_map(self, lat, lon):
        """Tạo bản đồ"""
        m = folium.Map(location=[lat, lon], zoom_start=12)
        folium.Marker([lat, lon], popup="Vị trí cây trồng").add_to(m)
        return m

# --- 6. KHỞI TẠO ---
weather_system = WeatherSystem()
map_system = MapSystem()
df_plants = load_plant_database()

# --- 7. KHỞI TẠO SESSION STATE ---
if 'selected_plant' not in st.session_state:
    st.session_state.selected_plant = df_plants.iloc[0].to_dict()

if 'selected_location' not in st.session_state:
    st.session_state.selected_location = [10.8231, 106.6297]  # TP.HCM

if 'location_name' not in st.session_state:
    st.session_state.location_name = "TP Hồ Chí Minh"

if 'forecast_data' not in st.session_state:
    st.session_state.forecast_data = None

if 'water_calculation' not in st.session_state:
    st.session_state.water_calculation = None

# --- 8. SIDEBAR ---
with st.sidebar:
    st.markdown("## 🌿 EcoMind")
    st.markdown("Hệ thống chăm sóc cây thông minh")
    
    # Menu
    selected = option_menu(
        menu_title=None,
        options=["🏠 Trang chủ", "🗺️ Bản đồ", "🌿 Cây trồng", "📊 Dự báo"],
        icons=["house", "map", "tree", "cloud-sun"],
        default_index=0,
        styles={
            "container": {"padding": "0!important"},
            "nav-link": {"font-size": "14px", "padding": "10px 15px"},
        }
    )
    
    # Thông tin
    st.markdown("---")
    st.markdown(f"**Vị trí:** {st.session_state.location_name}")
    st.markdown(f"**Cây:** {st.session_state.selected_plant.get('Tên Cây', 'Chưa chọn')}")
    
    if st.button("🔄 Làm mới"):
        st.cache_data.clear()
        st.rerun()

# --- 9. NỘI DUNG CHÍNH ---

# === TRANG CHỦ ===
if selected == "🏠 Trang chủ":
    st.title("🌿 EcoMind - Hệ Thống Chăm Sóc Cây")
    st.markdown("### Phiên bản đơn giản cho Streamlit Cloud")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Số cây", len(df_plants))
    with col2:
        st.metric("Phiên bản", "1.0.0")
    with col3:
        st.metric("Trạng thái", "✅ Online")
    
    st.markdown("""
    ### Tính năng chính:
    
    **🌿 Thư viện cây trồng:**
    - 10 loại cây phổ biến
    - Thông tin chi tiết về chăm sóc
    
    **🗺️ Bản đồ:**
    - 5 địa điểm Việt Nam
    - Chọn vị trí trồng cây
    
    **📊 Dự báo:**
    - Dự báo thời tiết 7 ngày
    - Tính toán nhu cầu nước
    - Khuyến nghị tưới nước
    
    **📧 Liên hệ:** tranthienphatle@gmail.com
    """)

# === BẢN ĐỒ ===
elif selected == "🗺️ Bản đồ":
    st.title("🗺️ Bản Đồ & Vị Trí")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Vị trí", st.session_state.location_name)
        st.metric("Vĩ độ", f"{st.session_state.selected_location[0]:.4f}")
    with col2:
        st.metric("Kinh độ", f"{st.session_state.selected_location[1]:.4f}")
    
    # Bản đồ
    m = map_system.create_map(
        st.session_state.selected_location[0],
        st.session_state.selected_location[1]
    )
    st_folium(m, width=700, height=400)
    
    # Tìm kiếm
    st.markdown("### 🔍 Tìm kiếm địa điểm")
    search_query = st.text_input("Nhập tên địa điểm:")
    
    if search_query:
        results = map_system.search_location(search_query)
        
        if results:
            for result in results:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{result['name']}**")
                    st.caption(f"{result['type']} • {result['region']}")
                with col2:
                    if st.button("Chọn", key=f"select_{result['name']}"):
                        st.session_state.selected_location = [result["lat"], result["lon"]]
                        st.session_state.location_name = result["name"]
                        st.rerun()
    
    # Địa điểm phổ biến
    st.markdown("### 📍 Địa điểm phổ biến")
    cols = st.columns(3)
    locations = ["Hà Nội", "TP Hồ Chí Minh", "Đà Nẵng", "Tân Hiệp", "Phú Giáo"]
    
    for idx, loc in enumerate(locations):
        with cols[idx % 3]:
            if st.button(f"📍 {loc}", use_container_width=True):
                results = map_system.search_location(loc)
                if results:
                    result = results[0]
                    st.session_state.selected_location = [result["lat"], result["lon"]]
                    st.session_state.location_name = result["name"]
                    st.rerun()

# === CÂY TRỒNG ===
elif selected == "🌿 Cây trồng":
    st.title("🌿 Thư Viện Cây Trồng")
    
    # Cây đang chọn
    plant = st.session_state.selected_plant
    st.markdown(f"### 🌟 Đang chọn: **{plant.get('Tên Cây', 'Chưa chọn')}**")
    
    # Tìm kiếm
    search_query = st.text_input("🔍 Tìm kiếm cây:")
    
    # Lọc cây
    filtered_plants = df_plants
    if search_query:
        filtered_plants = df_plants[df_plants["Tên Cây"].str.contains(search_query, case=False, na=False)]
    
    st.markdown(f"**Tìm thấy {len(filtered_plants)} cây**")
    
    # Hiển thị cây
    for _, plant in filtered_plants.iterrows():
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**{plant['Tên Cây']}**")
                st.caption(plant['Mô tả'])
            with col2:
                st.markdown(f"💧 {plant['Nước (L/ngày)']}L")
                st.markdown(f"⚡ {plant['Độ khó']}")
            with col3:
                if st.button("Chọn", key=f"plant_{plant['ID']}"):
                    st.session_state.selected_plant = plant.to_dict()
                    st.success(f"✅ Đã chọn {plant['Tên Cây']}!")
                    st.rerun()

# === DỰ BÁO ===
elif selected == "📊 Dự báo":
    st.title("📊 Dự Báo Thời Tiết")
    
    # Kiểm tra
    if not st.session_state.selected_plant:
        st.warning("Vui lòng chọn cây trước!")
        st.stop()
    
    if not st.session_state.location_name:
        st.warning("Vui lòng chọn vị trí trước!")
        st.stop()
    
    # Thông tin
    plant = st.session_state.selected_plant
    location = st.session_state.location_name
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Cây", plant.get('Tên Cây', 'Chưa chọn'))
    with col2:
        st.metric("Vị trí", location)
    with col3:
        st.metric("Nước cơ bản", f"{plant.get('Nước (L/ngày)', 0)}L/ngày")
    
    # Lấy dự báo
    if st.button("🌤️ Lấy dự báo 7 ngày", use_container_width=True):
        with st.spinner("Đang tạo dự báo..."):
            forecast = weather_system.get_weather_data(
                st.session_state.selected_location[0],
                st.session_state.selected_location[1],
                days=7
            )
            st.session_state.forecast_data = forecast
            st.success("✅ Đã tạo dự báo!")
    
    # Hiển thị dự báo
    if st.session_state.forecast_data is not None:
        forecast_df = st.session_state.forecast_data
        
        # Biểu đồ
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=forecast_df['day'],
            y=forecast_df['temp_max'],
            name='Nhiệt độ cao',
            line=dict(color='red')
        ))
        fig.add_trace(go.Scatter(
            x=forecast_df['day'],
            y=forecast_df['temp_min'],
            name='Nhiệt độ thấp',
            line=dict(color='blue'),
            fill='tonexty'
        ))
        fig.update_layout(title="Dự báo nhiệt độ 7 ngày", height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Bảng
        st.dataframe(
            forecast_df[['day', 'temp_min', 'temp_max', 'precipitation', 'humidity', 'condition']],
            use_container_width=True,
            hide_index=True
        )
        
        # Tính toán nước
        st.markdown("### 💧 Tính toán nhu cầu nước")
        
        water_calc = weather_system.calculate_water_needs(
            plant.get('Nước (L/ngày)', 0),
            forecast_df
        )
        st.session_state.water_calculation = water_calc
        
        st.dataframe(water_calc, use_container_width=True, hide_index=True)
        
        # Tổng kết
        total_water = water_calc['Nhu cầu điều chỉnh'].sum()
        st.metric("Tổng nước cần trong 7 ngày", f"{total_water:.2f}L")

# --- 10. FOOTER ---
st.markdown("---")
st.markdown(f"🕐 {datetime.datetime.now().strftime('%H:%M %d/%m/%Y')} • 🌿 EcoMind • 📧 tranthienphatle@gmail.com")
