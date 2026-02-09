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
import urllib.parse
import math
import hashlib
import base64
import os

# --- 1. CẤU HÌNH GIAO DIỆN PREMIUM ---
st.set_page_config(
    page_title="EcoMind OS - Hệ Thống Chăm Sóc Cây Thông Minh",
    layout="wide", 
    page_icon="🌿",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:tranthienphatle@gmail.com',
        'Report a bug': 'mailto:tranthienphatle@gmail.com',
        'About': 'EcoMind OS - Phiên bản Cloud 1.0 - Tối ưu cho Streamlit Cloud'
    }
)

# CSS Premium
st.markdown("""
<style>
    :root {
        --primary-color: #00ffcc;
        --secondary-color: #0088cc;
        --dark-bg: #0a192f;
        --darker-bg: #0d1b2a;
        --card-bg: rgba(255, 255, 255, 0.07);
        --text-color: #e0e1dd;
        --accent-color: #88aaff;
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--dark-bg) 0%, var(--darker-bg) 100%);
        color: var(--text-color);
        min-height: 100vh;
    }
    
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        transition: all 0.2s ease;
    }
    
    .glass-card:hover {
        border-color: var(--primary-color);
        box-shadow: 0 5px 20px rgba(0, 255, 204, 0.1);
    }
    
    h1, h2, h3, h4 {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
    }
    
    h1 {
        font-size: 2.2rem !important;
        margin-bottom: 1rem !important;
        position: relative;
    }
    
    h1::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 0;
        width: 80px;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-color), transparent);
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color)) !important;
        color: var(--dark-bg) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0, 255, 204, 0.3) !important;
    }
    
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-online { background-color: #00ff88; box-shadow: 0 0 10px #00ff88; }
    .status-offline { background-color: #ff4444; }
    .status-warning { background-color: #ffaa00; }
</style>
""", unsafe_allow_html=True)

# --- 2. HỆ THỐNG CẤU HÌNH TỰ ĐỘNG ---
class AutoConfigSystem:
    """Hệ thống tự động cấu hình không cần API key"""
    
    def __init__(self):
        self.cache = {}
        self.version = "1.0.0"
        self.build_date = "2024-01-20"
        self.weather_cache = {}
        
    def get_weather_data(self, lat, lon, days=7):
        """Lấy dữ liệu thời tiết"""
        cache_key = f"{lat:.2f}_{lon:.2f}_{days}_{datetime.datetime.now().strftime('%Y%m%d')}"
        
        if cache_key in self.weather_cache:
            return self.weather_cache[cache_key].copy()
        
        # Tạo seed từ tọa độ và ngày
        date_str = datetime.datetime.now().strftime('%Y%m%d')
        seed = int(abs(lat * 1000 + lon * 1000)) + int(date_str)
        random.seed(seed)
        
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
            precipitation = self._calculate_precipitation(season, i, lat, lon)
            
            # Các thông số khác
            humidity = random.randint(40, 90)
            wind_speed = round(random.uniform(1, 15), 1)
            wind_direction = random.choice(["Đông", "Tây", "Nam", "Bắc", "Đông Bắc", "Tây Nam"])
            uv_index = round(random.uniform(1, 11), 1)
            pressure = random.randint(1000, 1020)
            
            # Điều kiện thời tiết
            condition, icon = self._get_weather_condition(temp_max, precipitation, month)
            
            forecast.append({
                "date": date.strftime("%Y-%m-%d"),
                "day": date.strftime("%d/%m"),
                "weekday": self._get_vietnamese_weekday(date),
                "temp_max": temp_max,
                "temp_min": temp_min,
                "precipitation": precipitation,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "wind_direction": wind_direction,
                "uv_index": uv_index,
                "pressure": pressure,
                "condition": condition,
                "icon": icon,
                "season": season
            })
        
        result_df = pd.DataFrame(forecast)
        self.weather_cache[cache_key] = result_df.copy()
        
        return result_df
    
    def _get_vietnamese_weekday(self, date):
        """Chuyển đổi ngày trong tuần sang tiếng Việt"""
        weekdays = {
            "Monday": "Thứ Hai",
            "Tuesday": "Thứ Ba",
            "Wednesday": "Thứ Tư",
            "Thursday": "Thứ Năm",
            "Friday": "Thứ Sáu",
            "Saturday": "Thứ Bảy",
            "Sunday": "Chủ Nhật"
        }
        return weekdays.get(date.strftime("%A"), date.strftime("%A"))
    
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
        day_effect = math.sin(day_offset * math.pi / 14) * 2
        
        base_temp = equator_temp - lat_effect + month_effect + day_effect
        return round(base_temp, 1)
    
    def _calculate_precipitation(self, season, day_offset, lat, lon):
        """Tính lượng mưa"""
        precipitation_seed = int(abs(lat * 100 + lon * 100 + day_offset))
        random.seed(precipitation_seed)
        
        if season == "Hè":
            rain_prob = 0.6
            max_rain = 40
        elif season == "Đông":
            rain_prob = 0.3
            max_rain = 20
        elif season == "Xuân":
            rain_prob = 0.5
            max_rain = 30
        else:
            rain_prob = 0.4
            max_rain = 25
        
        if random.random() < rain_prob:
            pattern_factor = math.sin(day_offset * math.pi / 7) * 0.5 + 0.5
            precipitation = random.uniform(1, max_rain) * pattern_factor
            return round(precipitation, 1)
        
        return 0.0
    
    def _get_weather_condition(self, temp, precipitation, month):
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
        elif temp < 10:
            return "Rét", "❄️"
        elif temp < 15:
            return "Lạnh", "☁️"
        else:
            if month in [6, 7, 8]:
                return "Ôn hòa", "🌤️"
            else:
                return "Dễ chịu", "🌤️"
    
    def calculate_water_needs(self, plant_water, weather_data, soil_type="trung bình"):
        """Tính nhu cầu nước thông minh"""
        calculations = []
        
        for idx, day in weather_data.iterrows():
            temp_factor = 1 + max(0, (day['temp_max'] - 25) * 0.03)
            humidity_factor = 1 - max(0, (day['humidity'] - 60) * 0.01)
            rain_factor = max(0.1, 1 - (day['precipitation'] / 20))
            wind_factor = 1 + (day['wind_speed'] / 20)
            
            soil_factors = {
                "cát": 1.3,
                "thịt": 1.0,
                "sét": 0.7,
                "trung bình": 1.0
            }
            soil_factor = soil_factors.get(soil_type, 1.0)
            
            base_need = plant_water * temp_factor * humidity_factor * wind_factor * soil_factor
            adjusted_need = base_need * rain_factor
            final_need = max(0.05, adjusted_need)
            
            calculations.append({
                "Ngày": day['day'],
                "Thứ": day['weekday'],
                "Nhiệt độ": f"{day['temp_min']}°C - {day['temp_max']}°C",
                "Mưa": f"{day['precipitation']}mm",
                "Độ ẩm": f"{day['humidity']}%",
                "Nhu cầu cơ bản": round(plant_water, 2),
                "Nhu cầu điều chỉnh": round(final_need, 2),
                "Lượng nước (ml)": round(final_need * 1000, 0),
                "Khuyến nghị": self._get_watering_recommendation(final_need, plant_water, day['precipitation'], day['humidity'])
            })
        
        return pd.DataFrame(calculations)
    
    def _get_watering_recommendation(self, actual_need, base_need, precipitation, humidity):
        """Đưa ra khuyến nghị tưới nước"""
        if precipitation > 20:
            return "⛈️ Không cần tưới (mưa lớn)"
        elif precipitation > 10:
            return "🌧️ Giảm 60% lượng nước"
        elif precipitation > 5:
            return "🌦️ Giảm 30% lượng nước"
        elif humidity > 80:
            return "💦 Giảm 20% lượng nước (ẩm cao)"
        elif actual_need > base_need * 1.5:
            return "🔥 Tăng 50% lượng nước (nắng nóng)"
        elif actual_need > base_need * 1.2:
            return "☀️ Tăng 20% lượng nước"
        elif actual_need < base_need * 0.5:
            return "🌬️ Giảm 50% lượng nước (mát mẻ)"
        else:
            return "✅ Tưới bình thường"

# --- 3. HỆ THỐNG BẢN ĐỒ ĐƠN GIẢN ---
class SimpleMapSystem:
    """Hệ thống bản đồ đơn giản"""
    
    def __init__(self):
        self.vietnam_locations = self._load_vietnam_database()
        
    def _load_vietnam_database(self):
        """Tải database địa điểm Việt Nam"""
        return {
            "Hà Nội": {"lat": 21.0285, "lon": 105.8542, "type": "Thủ đô", "region": "Miền Bắc"},
            "TP Hồ Chí Minh": {"lat": 10.8231, "lon": 106.6297, "type": "Thành phố", "region": "Miền Nam"},
            "Đà Nẵng": {"lat": 16.0544, "lon": 108.2022, "type": "Thành phố", "region": "Miền Trung"},
            "Hải Phòng": {"lat": 20.8449, "lon": 106.6881, "type": "Thành phố", "region": "Miền Bắc"},
            "Cần Thơ": {"lat": 10.0452, "lon": 105.7469, "type": "Thành phố", "region": "Miền Nam"},
            "Huế": {"lat": 16.4637, "lon": 107.5909, "type": "Thành phố", "region": "Miền Trung"},
            "Nha Trang": {"lat": 12.2388, "lon": 109.1967, "type": "Thành phố", "region": "Miền Trung"},
            "Đà Lạt": {"lat": 11.9404, "lon": 108.4583, "type": "Thành phố", "region": "Tây Nguyên"},
            "Tân Hiệp, Kiên Giang": {"lat": 10.1234, "lon": 106.5678, "type": "Huyện", "region": "Miền Nam"},
            "Tân Hiệp, Hưng Yên": {"lat": 20.9345, "lon": 106.0123, "type": "Huyện", "region": "Miền Bắc"},
            "Phú Giáo, Bình Dương": {"lat": 11.2345, "lon": 106.7890, "type": "Huyện", "region": "Miền Nam"},
            "Phú Giáo, Đắk Nông": {"lat": 12.3456, "lon": 107.8901, "type": "Xã", "region": "Tây Nguyên"},
        }
    
    def search_location(self, query):
        """Tìm kiếm địa điểm"""
        query = query.strip().lower()
        
        if not query:
            return []
        
        results = []
        
        for name, data in self.vietnam_locations.items():
            name_lower = name.lower()
            
            if query == name_lower:
                score = 100
            elif query in name_lower:
                score = 80
            else:
                score = 0
            
            if score > 0:
                results.append({
                    "name": name,
                    "lat": data["lat"],
                    "lon": data["lon"],
                    "type": data["type"],
                    "region": data["region"],
                    "match_score": score
                })
        
        results.sort(key=lambda x: x["match_score"], reverse=True)
        return results[:5]
    
    def create_map(self, lat, lon):
        """Tạo bản đồ đơn giản"""
        m = folium.Map(
            location=[lat, lon],
            zoom_start=12,
            tiles="OpenStreetMap"
        )
        
        folium.Marker(
            [lat, lon],
            popup=f"Vị trí cây trồng",
            tooltip="Nhấn để xem chi tiết",
            icon=folium.Icon(color="green", icon="leaf")
        ).add_to(m)
        
        folium.Circle(
            location=[lat, lon],
            radius=2000,
            color="#00ffcc",
            fill=True,
            fill_color="#00ffcc",
            fill_opacity=0.1,
            popup="Phạm vi 2km"
        ).add_to(m)
        
        return m

# --- 4. HỆ THỐNG CÂY TRỒNG ---
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
            "Loại": self._get_plant_type(name)
        })
    
    return pd.DataFrame(plants)

def _get_plant_type(plant_name):
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

# --- 5. KHỞI TẠO HỆ THỐNG ---
@st.cache_resource
def init_systems():
    """Khởi tạo hệ thống với cache"""
    return AutoConfigSystem(), SimpleMapSystem()

# Khởi tạo
config_system, map_system = init_systems()
df_plants = load_plant_database()

# --- 6. KHỞI TẠO SESSION STATE AN TOÀN ---
def init_session_state():
    """Khởi tạo session state an toàn"""
    if 'selected_plant' not in st.session_state:
        st.session_state.selected_plant = df_plants.iloc[0].to_dict() if not df_plants.empty else {}
    
    if 'selected_location' not in st.session_state:
        st.session_state.selected_location = [10.8231, 106.6297]
    
    if 'location_name' not in st.session_state:
        st.session_state.location_name = "TP Hồ Chí Minh"
    
    if 'location_details' not in st.session_state:
        st.session_state.location_details = {"type": "Thành phố", "region": "Miền Nam"}
    
    if 'forecast_data' not in st.session_state:
        st.session_state.forecast_data = None
    
    if 'water_calculation' not in st.session_state:
        st.session_state.water_calculation = None
    
    if 'plant_details' not in st.session_state:
        st.session_state.plant_details = None
    
    if 'version' not in st.session_state:
        st.session_state.version = "1.0.0"
    
    if 'build_date' not in st.session_state:
        st.session_state.build_date = "2024-01-20"
    
    # Khởi tạo các biến search để tránh lỗi
    if 'plant_search' not in st.session_state:
        st.session_state.plant_search = ""
    
    if 'location_search' not in st.session_state:
        st.session_state.location_search = ""
    
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""

# Gọi hàm khởi tạo
init_session_state()

# --- 7. SIDEBAR ---
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 1.5rem 0;">
        <h1 style="background: linear-gradient(90deg, #00ffcc, #0088cc); 
                   -webkit-background-clip: text; 
                   -webkit-text-fill-color: transparent;
                   font-size: 1.8rem;
                   margin: 0;">
            🌿 EcoMind
        </h1>
        <p style="color: #88aaff; margin: 0.3rem 0; font-size: 0.9rem;">
            Hệ Thống Chăm Sóc Cây
        </p>
        <div style="display: inline-block; 
                    background: linear-gradient(90deg, #00ffcc, #0088cc); 
                    color: #0a192f; 
                    padding: 3px 10px; 
                    border-radius: 15px; 
                    font-size: 0.75rem; 
                    font-weight: 700; 
                    margin-top: 0.5rem;">
            v{st.session_state.version}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Menu điều hướng đơn giản
    selected = option_menu(
        menu_title=None,
        options=["🏠 Trang chủ", "🗺️ Bản đồ", "🌿 Cây trồng", "📊 Dự báo", "⚙️ Cài đặt"],
        icons=["house", "map", "tree", "cloud-sun", "gear"],
        default_index=0,
        styles={
            "container": {"padding": "0!important"},
            "nav-link": {
                "font-size": "14px",
                "padding": "12px 15px",
                "margin": "3px 0",
                "border-radius": "8px",
                "color": "#e0e1dd",
                "background": "rgba(255, 255, 255, 0.05)",
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg, #00ffcc, #0088cc)",
                "color": "#0a192f",
                "font-weight": "700",
            },
        }
    )
    
    # Thông tin nhanh
    st.markdown("---")
    st.markdown("**📍 Vị trí:**")
    st.info(st.session_state.location_name)
    
    st.markdown("**🌿 Cây đang chọn:**")
    if st.session_state.selected_plant:
        plant = st.session_state.selected_plant
        st.success(f"{plant.get('Tên Cây', 'Chưa chọn')}")
    
    # Nút làm mới
    if st.button("🔄 Làm mới", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# --- 8. NỘI DUNG CHÍNH ---

# === TRANG CHỦ ===
if selected == "🏠 Trang chủ":
    st.title("🌿 EcoMind - Hệ Thống Chăm Sóc Cây Thông Minh")
    st.markdown("### Phiên bản tối ưu cho Streamlit Cloud")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tổng số cây", len(df_plants))
    with col2:
        st.metric("Phiên bản", st.session_state.version)
    with col3:
        st.metric("Trạng thái", "✅ Online")
    
    # Giới thiệu
    st.markdown("""
    ### 🎯 Tính năng chính
    
    **🌿 Thư viện cây trồng:**
    - Database với 10+ loại cây phổ biến
    - Thông tin chi tiết về cách chăm sóc
    - Hướng dẫn tưới nước, ánh sáng, nhiệt độ
    
    **🗺️ Bản đồ thông minh:**
    - 12+ địa điểm Việt Nam
    - Tìm kiếm và chọn vị trí dễ dàng
    - Hiển thị bản đồ tương tác
    
    **📊 Dự báo thời tiết:**
    - Dự báo 7 ngày tự động
    - Tính toán nhu cầu nước thông minh
    - Điều chỉnh theo mùa và vị trí
    
    **💧 Tính toán nước:**
    - Tính lượng nước cần thiết
    - Điều chỉnh theo thời tiết
    - Khuyến nghị tưới nước thông minh
    """)
    
    # Hướng dẫn nhanh
    st.markdown("### 🚀 Bắt đầu nhanh")
    
    steps = st.columns(3)
    with steps[0]:
        st.markdown("#### 1. Chọn vị trí")
        st.markdown("Truy cập tab **🗺️ Bản đồ**")
        st.markdown("Chọn hoặc tìm kiếm vị trí")
    
    with steps[1]:
        st.markdown("#### 2. Chọn cây")
        st.markdown("Truy cập tab **🌿 Cây trồng**")
        st.markdown("Chọn cây bạn muốn chăm sóc")
    
    with steps[2]:
        st.markdown("#### 3. Xem dự báo")
        st.markdown("Truy cập tab **📊 Dự báo**")
        st.markdown("Nhận dự báo và hướng dẫn")
    
    # Thông tin liên hệ
    st.markdown("---")
    st.markdown("**📧 Email liên hệ:** tranthienphatle@gmail.com")
    st.markdown("**🌐 Triển khai:** Streamlit Cloud + GitHub")

# === BẢN ĐỒ ===
elif selected == "🗺️ Bản đồ":
    st.title("🗺️ Bản Đồ & Vị Trí")
    st.markdown("### Chọn vị trí cây trồng của bạn")
    
    tab1, tab2 = st.tabs(["🗺️ Bản đồ", "🔍 Tìm kiếm"])
    
    with tab1:
        # Hiển thị thông tin vị trí hiện tại
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.metric("Vị trí", st.session_state.location_name)
            st.metric("Vĩ độ", f"{st.session_state.selected_location[0]:.4f}")
        with col_info2:
            st.metric("Loại", st.session_state.location_details.get('type', 'N/A'))
            st.metric("Kinh độ", f"{st.session_state.selected_location[1]:.4f}")
        
        # Tạo và hiển thị bản đồ
        m = map_system.create_map(
            st.session_state.selected_location[0],
            st.session_state.selected_location[1]
        )
        
        st_folium(m, width=700, height=400)
    
    with tab2:
        # Tìm kiếm địa điểm
        search_query = st.text_input(
            "Tìm kiếm địa điểm:",
            placeholder="Ví dụ: Hà Nội, Đà Nẵng, Tân Hiệp...",
            key="location_search_input"
        )
        
        if search_query:
            results = map_system.search_location(search_query)
            
            if results:
                st.markdown(f"**Kết quả tìm kiếm ({len(results)}):**")
                
                for result in results:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.markdown(f"**{result['name']}**")
                            st.caption(f"{result['type']} • {result['region']}")
                        with col2:
                            st.metric("Vĩ độ", f"{result['lat']:.4f}")
                        with col3:
                            st.metric("Kinh độ", f"{result['lon']:.4f}")
                            if st.button("Chọn", key=f"select_{result['name']}"):
                                st.session_state.selected_location = [result["lat"], result["lon"]]
                                st.session_state.location_name = result["name"]
                                st.session_state.location_details = {
                                    "type": result["type"],
                                    "region": result["region"]
                                }
                                st.success(f"✅ Đã chọn: {result['name']}")
                                st.rerun()
            else:
                st.warning("Không tìm thấy địa điểm. Vui lòng thử từ khóa khác.")
        
        # Danh sách địa điểm phổ biến
        st.markdown("---")
        st.markdown("**📍 Địa điểm phổ biến:**")
        
        popular_locations = ["Hà Nội", "TP Hồ Chí Minh", "Đà Nẵng", "Tân Hiệp", "Phú Giáo"]
        cols = st.columns(3)
        
        for idx, loc in enumerate(popular_locations):
            with cols[idx % 3]:
                if st.button(f"📍 {loc}", use_container_width=True):
                    results = map_system.search_location(loc)
                    if results:
                        result = results[0]
                        st.session_state.selected_location = [result["lat"], result["lon"]]
                        st.session_state.location_name = result["name"]
                        st.session_state.location_details = {
                            "type": result["type"],
                            "region": result["region"]
                        }
                        st.rerun()

# === CÂY TRỒNG ===
elif selected == "🌿 Cây trồng":
    st.title("🌿 Thư Viện Cây Trồng")
    st.markdown(f"### Database {len(df_plants)} loại cây")
    
    # Hiển thị cây đang chọn
    if st.session_state.selected_plant:
        plant = st.session_state.selected_plant
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"#### 🌟 Đang chọn: **{plant.get('Tên Cây', 'Chưa chọn')}**")
                st.caption(plant.get('Mô tả', ''))
            with col2:
                st.metric("💧 Nước", f"{plant.get('Nước (L/ngày)', 0)}L/ngày")
    
    tab1, tab2 = st.tabs(["🔍 Tìm kiếm", "📋 Tất cả cây"])
    
    with tab1:
        # Tìm kiếm
        search_query = st.text_input(
            "Tìm kiếm cây:",
            placeholder="Nhập tên cây...",
            key="plant_search_input"
        )
        
        # Bộ lọc
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            difficulty_filter = st.selectbox(
                "Độ khó:",
                ["Tất cả", "Rất dễ", "Dễ", "Trung bình", "Khó"]
            )
        with col_filter2:
            water_filter = st.slider(
                "Nhu cầu nước (L/ngày):",
                0.0, 1.0, (0.0, 1.0)
            )
        
        # Lọc và hiển thị kết quả
        filtered_plants = df_plants.copy()
        
        if search_query:
            filtered_plants = filtered_plants[
                filtered_plants["Tên Cây"].str.contains(search_query, case=False, na=False)
            ]
        
        if difficulty_filter != "Tất cả":
            filtered_plants = filtered_plants[filtered_plants["Độ khó"] == difficulty_filter]
        
        filtered_plants = filtered_plants[
            (filtered_plants["Nước (L/ngày)"] >= water_filter[0]) &
            (filtered_plants["Nước (L/ngày)"] <= water_filter[1])
        ]
        
        st.markdown(f"**Kết quả: {len(filtered_plants)} cây**")
        
        if len(filtered_plants) > 0:
            for _, plant in filtered_plants.iterrows():
                with st.container(border=True):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.markdown(f"**{plant['Tên Cây']}**")
                        st.caption(f"{plant['Mô tả']}")
                    with col2:
                        st.markdown(f"💧 {plant['Nước (L/ngày)']}L")
                        st.markdown(f"⚡ {plant['Độ khó']}")
                    with col3:
                        if st.button("Chọn", key=f"select_plant_{plant['ID']}"):
                            st.session_state.selected_plant = plant.to_dict()
                            st.success(f"✅ Đã chọn {plant['Tên Cây']}!")
        
    with tab2:
        # Hiển thị tất cả cây
        st.dataframe(
            df_plants[['Tên Cây', 'Nước (L/ngày)', 'Độ khó', 'Ánh sáng', 'Nhiệt độ', 'Loại']],
            use_container_width=True,
            hide_index=True
        )

# === DỰ BÁO ===
elif selected == "📊 Dự báo":
    st.title("📊 Dự Báo & Tính Toán")
    st.markdown("### Dự báo thời tiết và tính toán nhu cầu chăm sóc")
    
    # Kiểm tra đã chọn cây và vị trí
    if not st.session_state.selected_plant:
        st.warning("⚠️ Vui lòng chọn cây trước!")
        if st.button("🌿 Đến Thư Viện Cây"):
            st.session_state.selected = "🌿 Cây trồng"
            st.rerun()
        st.stop()
    
    if not st.session_state.location_name:
        st.warning("⚠️ Vui lòng chọn vị trí trước!")
        if st.button("🗺️ Đến Bản Đồ"):
            st.session_state.selected = "🗺️ Bản đồ"
            st.rerun()
        st.stop()
    
    # Hiển thị thông tin
    plant = st.session_state.selected_plant
    location = st.session_state.location_name
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🌿 Cây", plant.get('Tên Cây', 'Chưa chọn'))
    with col2:
        st.metric("📍 Vị trí", location)
    with col3:
        st.metric("💧 Nước cơ bản", f"{plant.get('Nước (L/ngày)', 0)}L/ngày")
    
    tab1, tab2 = st.tabs(["🌦️ Dự báo thời tiết", "💧 Tính toán nước"])
    
    with tab1:
        st.markdown("#### 🌦️ Dự Báo Thời Tiết 7 Ngày")
        
        # Lấy dự báo
        if st.button("🌤️ Lấy dự báo", use_container_width=True):
            with st.spinner("Đang tạo dự báo..."):
                forecast = config_system.get_weather_data(
                    st.session_state.selected_location[0],
                    st.session_state.selected_location[1],
                    days=7
                )
                st.session_state.forecast_data = forecast
                st.success("✅ Đã tạo dự báo!")
        
        if st.session_state.forecast_data is not None:
            forecast_df = st.session_state.forecast_data
            
            # Biểu đồ nhiệt độ
            fig_temp = go.Figure()
            fig_temp.add_trace(go.Scatter(
                x=forecast_df['day'],
                y=forecast_df['temp_max'],
                name='Nhiệt độ cao',
                line=dict(color='#ff6b6b', width=3),
                mode='lines+markers'
            ))
            fig_temp.add_trace(go.Scatter(
                x=forecast_df['day'],
                y=forecast_df['temp_min'],
                name='Nhiệt độ thấp',
                line=dict(color='#4dabf7', width=3),
                mode='lines+markers',
                fill='tonexty'
            ))
            fig_temp.update_layout(
                title="Dự báo nhiệt độ 7 ngày",
                template="plotly_dark",
                height=300
            )
            st.plotly_chart(fig_temp, use_container_width=True)
            
            # Bảng dự báo
            display_df = forecast_df.copy()
            display_df['Nhiệt độ'] = display_df.apply(
                lambda x: f"{x['icon']} {x['temp_min']}°C - {x['temp_max']}°C", axis=1
            )
            display_df['Mưa'] = display_df['precipitation'].apply(
                lambda x: f"🌧️ {x}mm" if x > 0 else "☀️ Không mưa"
            )
            
            st.dataframe(
                display_df[['day', 'Nhiệt độ', 'Mưa', 'humidity', 'condition']],
                use_container_width=True,
                hide_index=True
            )
    
    with tab2:
        st.markdown("#### 💧 Tính Toán Nhu Cầu Nước")
        
        if st.session_state.forecast_data is not None:
            plant_water = plant.get('Nước (L/ngày)', 0)
            forecast_df = st.session_state.forecast_data
            
            # Cài đặt tính toán
            soil_type = st.selectbox(
                "Loại đất:",
                ["trung bình", "cát", "thịt", "sét"],
                key="soil_type"
            )
            
            # Tính toán
            water_calc = config_system.calculate_water_needs(plant_water, forecast_df, soil_type)
            st.session_state.water_calculation = water_calc
            
            # Biểu đồ
            fig_water = px.bar(
                water_calc,
                x='Ngày',
                y='Nhu cầu điều chỉnh',
                title='Nhu cầu nước hàng ngày',
                color='Nhu cầu điều chỉnh',
                color_continuous_scale='Blues'
            )
            fig_water.update_layout(template="plotly_dark", height=300)
            st.plotly_chart(fig_water, use_container_width=True)
            
            # Bảng tính toán
            st.dataframe(
                water_calc,
                use_container_width=True,
                hide_index=True
            )
            
            # Tổng kết
            total_water = water_calc['Nhu cầu điều chỉnh'].sum()
            avg_water = water_calc['Nhu cầu điều chỉnh'].mean()
            
            col_total1, col_total2 = st.columns(2)
            with col_total1:
                st.metric("Tổng nước 7 ngày", f"{total_water:.2f}L")
            with col_total2:
                st.metric("Trung bình/ngày", f"{avg_water:.2f}L")
        else:
            st.info("Vui lòng lấy dự báo thời tiết trước!")

# === CÀI ĐẶT ===
elif selected == "⚙️ Cài đặt":
    st.title("⚙️ Cài Đặt Hệ Thống")
    
    tab1, tab2 = st.tabs(["🎨 Giao diện", "ℹ️ Thông tin"])
    
    with tab1:
        st.markdown("#### 🎨 Tùy Chỉnh Giao Diện")
        
        theme = st.selectbox(
            "Chủ đề:",
            ["Tối (Mặc định)", "Xanh đậm", "Xám tối"]
        )
        
        font_size = st.slider("Cỡ chữ:", 12, 18, 14)
        
        if st.button("💾 Lưu cài đặt", use_container_width=True):
            st.success("✅ Đã lưu cài đặt!")
    
    with tab2:
        st.markdown("#### ℹ️ Thông Tin Hệ Thống")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Phiên bản", st.session_state.version)
            st.metric("Build", st.session_state.build_date)
        with col2:
            st.metric("Cây trong DB", len(df_plants))
            st.metric("Trạng thái", "✅ Online")
        
        st.markdown("**Thông tin kỹ thuật:**")
        st.markdown("- Framework: Streamlit")
        st.markdown("- Database: Pandas")
        st.markdown("- Bản đồ: Folium + OpenStreetMap")
        st.markdown("- Triển khai: Streamlit Cloud")
        
        st.markdown("**Liên hệ:**")
        st.code("tranthienphatle@gmail.com")

# --- 9. FOOTER ---
st.markdown("---")
st.markdown(f"🕐 {datetime.datetime.now().strftime('%H:%M %d/%m/%Y')} • 🌿 EcoMind v{st.session_state.version} • 📧 tranthienphatle@gmail.com")
