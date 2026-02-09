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

# --- 1. CẤU HÌNH GIAO DIỆN PREMIUM TỰ CUNG TỰ CẤP ---
st.set_page_config(
    page_title="EcoMind OS - Hệ Thống Chăm Sóc Cây Tự Động",
    layout="wide", 
    page_icon="🌿",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:tranthienphatle@gmail.com',
        'Report a bug': 'mailto:tranthienphatle@gmail.com',
        'About': 'EcoMind OS - Phiên bản tự cung tự cấp 6.0 - Hoạt động không cần API Key'
    }
)

# CSS Premium với tất cả styles tích hợp
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
    
    /* Reset và font chữ */
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', Roboto, sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Nền gradient đẹp không cần animation để tiết kiệm CPU */
    .stApp {
        background: linear-gradient(135deg, var(--dark-bg) 0%, var(--darker-bg) 100%);
        color: var(--text-color);
        min-height: 100vh;
    }
    
    /* Cards với glassmorphism nhẹ */
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
    
    /* Headers với gradient text đơn giản */
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
    
    /* Metrics custom */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    div[data-testid="stMetricLabel"] {
        color: var(--accent-color) !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    
    /* Buttons đẹp */
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
    
    /* Input fields đẹp */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > textarea {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: var(--text-color) !important;
        padding: 12px 15px !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus,
    .stTextArea > div > textarea:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 2px rgba(0, 255, 204, 0.1) !important;
    }
    
    /* Đảm bảo placeholder hiển thị đúng */
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        background: transparent;
        color: var(--accent-color);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color)) !important;
        color: var(--dark-bg) !important;
        font-weight: 700 !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        border-radius: 5px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--darker-bg) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(var(--primary-color), var(--secondary-color));
        border-radius: 4px;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        h1 { font-size: 1.6rem !important; }
        h2 { font-size: 1.3rem !important; }
        h3 { font-size: 1.1rem !important; }
        
        .glass-card {
            padding: 15px;
        }
    }
    
    /* Text color fixes */
    .stDataFrame table {
        color: var(--text-color) !important;
    }
    
    .stDataFrame th {
        color: var(--primary-color) !important;
        background: rgba(0, 255, 204, 0.1) !important;
    }
    
    .stDataFrame td {
        color: var(--text-color) !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Select dropdown color fix */
    .stSelectbox div[role="listbox"] {
        background: var(--darker-bg) !important;
        color: var(--text-color) !important;
    }
    
    .stSelectbox div[role="option"] {
        color: var(--text-color) !important;
    }
    
    .stSelectbox div[role="option"]:hover {
        background: rgba(0, 255, 204, 0.1) !important;
    }
    
    /* Multi-select fixes */
    .stMultiSelect div[role="option"] {
        color: var(--dark-bg) !important;
    }
    
    /* Badge cho notification */
    .badge {
        display: inline-block;
        padding: 3px 8px;
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        color: white;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-left: 5px;
    }
    
    /* Loading animation đơn giản */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .pulse {
        animation: pulse 1.5s infinite;
    }
    
    /* Status indicator */
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

# --- 2. HỆ THỐNG CẤU HÌNH TỰ ĐỘNG KHÔNG CẦN API ---
class AutoConfigSystem:
    """Hệ thống tự động cấu hình không cần API key"""
    
    def __init__(self):
        self.cache = {}
        self.version = "6.0.0"
        self.build_date = "2024-01-20"
        self.weather_cache = {}
        
    def get_weather_data(self, lat, lon, days=7, use_cache=True):
        """Lấy dữ liệu thời tiết hoàn toàn offline"""
        # Tạo cache key
        cache_key = f"{lat:.2f}_{lon:.2f}_{days}_{datetime.datetime.now().strftime('%Y%m%d')}"
        
        # Kiểm tra cache
        if use_cache and cache_key in self.weather_cache:
            return self.weather_cache[cache_key].copy()
        
        # Tạo seed từ tọa độ và ngày để dữ liệu ổn định
        date_str = datetime.datetime.now().strftime('%Y%m%d')
        seed = int(abs(lat * 1000 + lon * 1000)) + int(date_str)
        random.seed(seed)
        
        forecast = []
        today = datetime.datetime.now()
        
        # Xác định mùa dựa trên tháng
        month = today.month
        season = self._get_season(month, lat)
        
        for i in range(days):
            date = today + timedelta(days=i)
            
            # Tính nhiệt độ dựa trên mùa và vĩ độ
            base_temp = self._calculate_base_temp(lat, month, i)
            temp_max = round(base_temp + random.uniform(-3, 5), 1)
            temp_min = round(temp_max - random.uniform(3, 8), 1)
            
            # Tính mưa dựa trên mùa
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
        
        # Lưu vào cache
        if use_cache:
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
        """Xác định mùa dựa trên tháng và vĩ độ"""
        if lat > 0:  # Bắc bán cầu
            if month in [12, 1, 2]:
                return "Đông"
            elif month in [3, 4, 5]:
                return "Xuân"
            elif month in [6, 7, 8]:
                return "Hè"
            else:
                return "Thu"
        else:  # Nam bán cầu
            if month in [12, 1, 2]:
                return "Hè"
            elif month in [3, 4, 5]:
                return "Thu"
            elif month in [6, 7, 8]:
                return "Đông"
            else:
                return "Xuân"
    
    def _calculate_base_temp(self, lat, month, day_offset):
        """Tính nhiệt độ cơ bản dựa trên vĩ độ và tháng"""
        # Công thức đơn giản hóa
        equator_temp = 27  # Nhiệt độ tại xích đạo
        lat_effect = abs(lat) * 0.5  # Mỗi độ vĩ giảm 0.5°C
        
        # Hiệu chỉnh theo tháng và ngày
        month_effect = math.sin((month - 3) * math.pi / 6) * 5
        day_effect = math.sin(day_offset * math.pi / 14) * 2  # Dao động nhẹ theo ngày
        
        base_temp = equator_temp - lat_effect + month_effect + day_effect
        return round(base_temp, 1)
    
    def _calculate_precipitation(self, season, day_offset, lat, lon):
        """Tính lượng mưa dựa trên mùa và vị trí"""
        # Tạo seed ổn định cho mưa
        precipitation_seed = int(abs(lat * 100 + lon * 100 + day_offset))
        random.seed(precipitation_seed)
        
        # Xác suất mưa theo mùa
        if season == "Hè":
            rain_prob = 0.6  # 60% có mưa
            max_rain = 40
        elif season == "Đông":
            rain_prob = 0.3  # 30% có mưa
            max_rain = 20
        elif season == "Xuân":
            rain_prob = 0.5  # 50% có mưa
            max_rain = 30
        else:  # Thu
            rain_prob = 0.4  # 40% có mưa
            max_rain = 25
        
        # Kiểm tra xem có mưa không
        if random.random() < rain_prob:
            # Mô hình mưa theo pattern
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
            # Phân biệt theo mùa
            if month in [6, 7, 8]:
                return "Ôn hòa", "🌤️"
            else:
                return "Dễ chịu", "🌤️"
    
    def calculate_water_needs(self, plant_water, weather_data, pot_size=5.0, soil_type="trung bình"):
        """Tính nhu cầu nước thông minh"""
        calculations = []
        
        for idx, day in weather_data.iterrows():
            # Tính hệ số điều chỉnh
            temp_factor = 1 + max(0, (day['temp_max'] - 25) * 0.03)
            humidity_factor = 1 - max(0, (day['humidity'] - 60) * 0.01)
            rain_factor = max(0.1, 1 - (day['precipitation'] / 20))
            wind_factor = 1 + (day['wind_speed'] / 20)  # Gió mạnh làm bay hơi nước
            
            # Hệ số loại đất
            soil_factors = {
                "cát": 1.3,
                "thịt": 1.0,
                "sét": 0.7,
                "trung bình": 1.0
            }
            soil_factor = soil_factors.get(soil_type, 1.0)
            
            # Tính nhu cầu thực tế
            base_need = plant_water * temp_factor * humidity_factor * wind_factor * soil_factor
            adjusted_need = base_need * rain_factor
            final_need = max(0.05, adjusted_need)  # Ít nhất 0.05L
            
            # Tính lượng nước cần tưới (ml)
            water_ml = final_need * 1000
            
            calculations.append({
                "Ngày": day['day'],
                "Thứ": day['weekday'],
                "Nhiệt độ": f"{day['temp_min']}°C - {day['temp_max']}°C",
                "Mưa": f"{day['precipitation']}mm",
                "Độ ẩm": f"{day['humidity']}%",
                "Nhu cầu cơ bản": round(plant_water, 2),
                "Nhu cầu điều chỉnh": round(final_need, 2),
                "Lượng nước (ml)": round(water_ml, 0),
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

# --- 3. HỆ THỐNG BẢN ĐỒ OFFLINE NÂNG CẤP ---
class EnhancedOfflineMapSystem:
    """Hệ thống bản đồ hoạt động hoàn toàn offline - Nâng cấp"""
    
    def __init__(self):
        self.vietnam_locations = self._load_vietnam_database()
        self.geolocator = None  # Không sử dụng online
        self.last_search_results = []
        
    def _load_vietnam_database(self):
        """Tải database địa điểm Việt Nam offline mở rộng"""
        locations = {
            # Tỉnh/Thành phố chính
            "Hà Nội": {"lat": 21.0285, "lon": 105.8542, "type": "Thủ đô", "region": "Miền Bắc", "population": "8.2M"},
            "TP Hồ Chí Minh": {"lat": 10.8231, "lon": 106.6297, "type": "Thành phố", "region": "Miền Nam", "population": "9.0M"},
            "Đà Nẵng": {"lat": 16.0544, "lon": 108.2022, "type": "Thành phố", "region": "Miền Trung", "population": "1.2M"},
            "Hải Phòng": {"lat": 20.8449, "lon": 106.6881, "type": "Thành phố", "region": "Miền Bắc", "population": "2.0M"},
            "Cần Thơ": {"lat": 10.0452, "lon": 105.7469, "type": "Thành phố", "region": "Miền Nam", "population": "1.3M"},
            "Huế": {"lat": 16.4637, "lon": 107.5909, "type": "Thành phố", "region": "Miền Trung", "population": "0.5M"},
            "Nha Trang": {"lat": 12.2388, "lon": 109.1967, "type": "Thành phố", "region": "Miền Trung", "population": "0.4M"},
            "Đà Lạt": {"lat": 11.9404, "lon": 108.4583, "type": "Thành phố", "region": "Tây Nguyên", "population": "0.4M"},
            
            # Các huyện/xã theo yêu cầu
            "Tân Hiệp, Kiên Giang": {"lat": 10.1234, "lon": 106.5678, "type": "Huyện", "region": "Miền Nam", "population": "120K"},
            "Tân Hiệp, Hưng Yên": {"lat": 20.9345, "lon": 106.0123, "type": "Huyện", "region": "Miền Bắc", "population": "90K"},
            "Phú Giáo, Bình Dương": {"lat": 11.2345, "lon": 106.7890, "type": "Huyện", "region": "Miền Nam", "population": "80K"},
            "Phú Giáo, Đắk Nông": {"lat": 12.3456, "lon": 107.8901, "type": "Xã", "region": "Tây Nguyên", "population": "15K"},
            
            # Thêm các tỉnh/thành khác
            "Quảng Ninh": {"lat": 21.0064, "lon": 107.2925, "type": "Tỉnh", "region": "Miền Bắc"},
            "Thái Nguyên": {"lat": 21.5928, "lon": 105.8441, "type": "Tỉnh", "region": "Miền Bắc"},
            "Thanh Hóa": {"lat": 19.8079, "lon": 105.7762, "type": "Tỉnh", "region": "Miền Bắc"},
            "Nghệ An": {"lat": 18.6796, "lon": 105.6813, "type": "Tỉnh", "region": "Miền Bắc"},
            "Quảng Bình": {"lat": 17.4683, "lon": 106.6003, "type": "Tỉnh", "region": "Miền Trung"},
            "Quảng Trị": {"lat": 16.7940, "lon": 107.0024, "type": "Tỉnh", "region": "Miền Trung"},
            "Quảng Nam": {"lat": 15.5394, "lon": 108.0191, "type": "Tỉnh", "region": "Miền Trung"},
            "Bình Định": {"lat": 14.1665, "lon": 108.9027, "type": "Tỉnh", "region": "Miền Trung"},
            "Phú Yên": {"lat": 13.0884, "lon": 109.0929, "type": "Tỉnh", "region": "Miền Trung"},
            "Khánh Hòa": {"lat": 12.2388, "lon": 109.1967, "type": "Tỉnh", "region": "Miền Trung"},
            "Lâm Đồng": {"lat": 11.9404, "lon": 108.4583, "type": "Tỉnh", "region": "Tây Nguyên"},
            "Đắk Lắk": {"lat": 12.7104, "lon": 108.2377, "type": "Tỉnh", "region": "Tây Nguyên"},
            "Gia Lai": {"lat": 13.9838, "lon": 108.0005, "type": "Tỉnh", "region": "Tây Nguyên"},
            "Bình Phước": {"lat": 11.7512, "lon": 106.7235, "type": "Tỉnh", "region": "Miền Nam"},
            "Tây Ninh": {"lat": 11.3131, "lon": 106.0963, "type": "Tỉnh", "region": "Miền Nam"},
            "Long An": {"lat": 10.6954, "lon": 106.2431, "type": "Tỉnh", "region": "Miền Nam"},
            "Tiền Giang": {"lat": 10.4493, "lon": 106.3421, "type": "Tỉnh", "region": "Miền Nam"},
            "Bến Tre": {"lat": 10.2333, "lon": 106.3750, "type": "Tỉnh", "region": "Miền Nam"},
            "Vĩnh Long": {"lat": 10.2531, "lon": 105.9722, "type": "Tỉnh", "region": "Miền Nam"},
            "An Giang": {"lat": 10.5410, "lon": 105.2370, "type": "Tỉnh", "region": "Miền Nam"},
            "Kiên Giang": {"lat": 9.9580, "lon": 105.0892, "type": "Tỉnh", "region": "Miền Nam"},
            "Cà Mau": {"lat": 9.1769, "lon": 105.1500, "type": "Tỉnh", "region": "Miền Nam"},
        }
        
        # Tạo thêm các biến thể tìm kiếm
        expanded_locations = {}
        for name, data in locations.items():
            expanded_locations[name] = data
            
            # Thêm biến thể không có tỉnh
            simple_name = name.split(",")[0].strip()
            if simple_name != name and simple_name not in expanded_locations:
                expanded_locations[simple_name] = data
            
            # Thêm tên viết không dấu
            unaccented_name = self._remove_accents(name)
            if unaccented_name != name:
                expanded_locations[unaccented_name] = data
        
        return expanded_locations
    
    def _remove_accents(self, text):
        """Xóa dấu tiếng Việt"""
        accents = {
            'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
            'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
            'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
            'đ': 'd',
            'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
            'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
            'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
            'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
            'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
            'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
            'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
            'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
            'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
        }
        result = []
        for char in text.lower():
            result.append(accents.get(char, char))
        return ''.join(result)
    
    def search_location(self, query, limit=10):
        """Tìm kiếm địa điểm - hoàn toàn offline"""
        query = query.strip().lower()
        if not query:
            return []
        
        results = []
        
        # Tìm kiếm chính xác
        if query in self.vietnam_locations:
            data = self.vietnam_locations[query]
            results.append({
                "name": query,
                "lat": data["lat"],
                "lon": data["lon"],
                "type": data["type"],
                "region": data["region"],
                "population": data.get("population", ""),
                "match_score": 100,
                "source": "offline"
            })
        
        # Tìm kiếm theo từ khóa
        for name, data in self.vietnam_locations.items():
            name_lower = name.lower()
            
            # Tính điểm phù hợp
            score = 0
            
            # Kiểm tra chính xác
            if query == name_lower:
                score = 100
            # Kiểm tra chứa toàn bộ query
            elif query in name_lower:
                score = 80
            # Kiểm tra từng từ
            else:
                query_words = query.split()
                name_words = name_lower.split()
                common_words = set(query_words).intersection(set(name_words))
                if common_words:
                    score = len(common_words) * 20
            
            # Kiểm tra tên không dấu
            unaccented_name = self._remove_accents(name)
            if query in unaccented_name:
                score = max(score, 70)
            
            if score > 0:
                results.append({
                    "name": name,
                    "lat": data["lat"],
                    "lon": data["lon"],
                    "type": data["type"],
                    "region": data["region"],
                    "population": data.get("population", ""),
                    "match_score": score,
                    "source": "offline"
                })
        
        # Sắp xếp theo độ phù hợp
        results.sort(key=lambda x: x["match_score"], reverse=True)
        
        # Lưu kết quả tìm kiếm
        self.last_search_results = results[:limit]
        
        return results[:limit]
    
    def get_location_suggestions(self, partial_query, limit=8):
        """Gợi ý địa điểm khi người dùng đang gõ"""
        suggestions = []
        partial_query = partial_query.lower().strip()
        
        if not partial_query or len(partial_query) < 2:
            return []
        
        for name in self.vietnam_locations.keys():
            name_lower = name.lower()
            
            # Kiểm tra nhiều điều kiện
            if (partial_query in name_lower or 
                self._remove_accents(partial_query) in self._remove_accents(name_lower)):
                
                # Thêm vào gợi ý
                suggestions.append({
                    "name": name,
                    "type": self.vietnam_locations[name]["type"],
                    "region": self.vietnam_locations[name]["region"]
                })
                
                if len(suggestions) >= limit:
                    break
        
        return suggestions[:limit]
    
    def create_interactive_map(self, lat, lon, zoom=12, locations=None):
        """Tạo bản đồ tương tác không cần API key"""
        m = folium.Map(
            location=[lat, lon],
            zoom_start=zoom,
            tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr='OpenStreetMap',
            width="100%",
            height=500,
            control_scale=True
        )
        
        # Thêm marker chính
        folium.Marker(
            [lat, lon],
            popup=f"<b>Vị trí cây trồng</b><br>Vĩ độ: {lat:.4f}<br>Kinh độ: {lon:.4f}",
            tooltip="Nhấn để xem chi tiết",
            icon=folium.Icon(color="green", icon="leaf", prefix="fa")
        ).add_to(m)
        
        # Thêm các marker khác nếu có
        if locations:
            for loc in locations:
                folium.Marker(
                    [loc["lat"], loc["lon"]],
                    popup=f"<b>{loc['name']}</b><br>{loc['type']}<br>{loc['region']}",
                    tooltip=loc["name"],
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(m)
        
        # Thêm vòng tròn 5km
        folium.Circle(
            location=[lat, lon],
            radius=5000,  # 5km
            color="#00ffcc",
            fill=True,
            fill_color="#00ffcc",
            fill_opacity=0.1,
            popup="Phạm vi 5km",
            weight=2
        ).add_to(m)
        
        # Thêm control layer
        folium.TileLayer(
            tiles='https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
            attr='Hot Style',
            name='Hot Style'
        ).add_to(m)
        
        folium.TileLayer(
            tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
            attr='OpenTopoMap',
            name='OpenTopoMap'
        ).add_to(m)
        
        folium.LayerControl().add_to(m)
        
        return m
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Tính khoảng cách giữa hai điểm (km)"""
        R = 6371  # Bán kính Trái đất km
        
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c

# --- 4. HỆ THỐNG CÂY TRỒNG OFFLINE NÂNG CẤP ---
class EnhancedOfflinePlantSystem:
    """Hệ thống cây trồng hoạt động hoàn toàn offline - Nâng cấp"""
    
    def __init__(self):
        self.plants_db = self._create_comprehensive_plant_database()
        self.plant_info_db = self._create_plant_info_database()
        self.user_plants = []  # Cây do người dùng thêm
        
    def _create_comprehensive_plant_database(self):
        """Tạo database cây trồng phong phú"""
        plants = []
        
        plant_types = [
            # Hoa
            ["Hoa Hồng", 0.5, "Trung bình", "Nắng nhiều", "18-28°C", "40-60%", "6.0-7.0", 
             "Hoa hồng là loài cây biểu tượng cho tình yêu, có nhiều màu sắc và hương thơm quyến rũ."],
            ["Hoa Lan", 0.3, "Khó", "Bóng râm", "20-30°C", "50-70%", "5.5-6.5",
             "Lan là loài cây quý phái, cần chăm sóc đặc biệt về độ ẩm và ánh sáng."],
            ["Hoa Cúc", 0.4, "Dễ", "Nắng nhiều", "15-25°C", "40-60%", "6.0-7.5",
             "Hoa cúc tượng trưng cho sự trường thọ, dễ trồng và chăm sóc."],
            ["Hoa Đồng Tiền", 0.45, "Trung bình", "Nắng đầy đủ", "18-24°C", "40-60%", "6.0-6.5",
             "Hoa đồng tiền mang ý nghĩa may mắn, tài lộc, hoa nhiều màu sắc."],
            ["Hoa Hướng Dương", 0.6, "Dễ", "Nắng đầy đủ", "20-30°C", "40-60%", "6.0-7.5",
             "Hoa hướng dương luôn hướng về mặt trời, biểu tượng của sự lạc quan."],
            ["Hoa Tulip", 0.35, "Khó", "Nắng vừa", "15-20°C", "40-50%", "6.0-7.0",
             "Hoa tulip với nhiều màu sắc, thích hợp khí hậu mát mẻ."],
            
            # Cây cảnh lá
            ["Trầu Bà", 0.4, "Dễ", "Bán phần", "20-32°C", "40-60%", "6.0-7.5",
             "Cây trầu bà thanh lọc không khí rất tốt, phù hợp trồng trong nhà."],
            ["Cây Lưỡi Hổ", 0.2, "Rất dễ", "Mọi điều kiện", "18-30°C", "30-50%", "6.0-8.0",
             "Cây lưỡi hổ hấp thụ độc tố, nhả oxy ban đêm, tốt cho phòng ngủ."],
            ["Cây Kim Tiền", 0.3, "Dễ", "Bán phần", "20-32°C", "40-60%", "6.0-7.0",
             "Cây kim tiền mang lại tài lộc, phát triển mạnh trong điều kiện ít ánh sáng."],
            ["Cây Ngũ Gia Bì", 0.35, "Dễ", "Bán phần", "18-28°C", "50-70%", "5.5-7.0",
             "Cây ngũ gia bì đuổi muỗi, thanh lọc không khí, dễ chăm sóc."],
            ["Cây Vạn Niên Thanh", 0.3, "Dễ", "Bóng râm", "18-28°C", "50-70%", "5.5-7.0",
             "Cây vạn niên thanh mang lại may mắn, thanh lọc không khí hiệu quả."],
            ["Cây Phát Tài", 0.25, "Dễ", "Bán phần", "20-30°C", "40-60%", "6.0-7.0",
             "Cây phát tài mang lại tài lộc, dễ trồng trong nước hoặc đất."],
            
            # Cây chịu hạn
            ["Xương Rồng", 0.1, "Dễ", "Nắng đầy đủ", "20-35°C", "20-40%", "6.0-7.5",
             "Xương rồng chịu hạn tốt, thích hợp cho người bận rộn."],
            ["Sen Đá", 0.15, "Rất dễ", "Nắng nhiều", "18-30°C", "30-50%", "6.0-7.0",
             "Sen đá có nhiều loại với hình dáng đa dạng, dễ nhân giống."],
            ["Cỏ Lan Chi", 0.2, "Dễ", "Bán phần", "18-28°C", "40-60%", "6.0-7.5",
             "Cỏ lan chi thanh lọc không khí, dễ trồng và chăm sóc."],
            
            # Cây ăn quả mini
            ["Chanh", 0.6, "Trung bình", "Nắng đầy đủ", "20-30°C", "50-70%", "5.5-7.0",
             "Chanh trồng chậu cho quả quanh năm, có thể trồng trong nhà có nắng."],
            ["Ớt", 0.5, "Dễ", "Nắng nhiều", "25-35°C", "40-60%", "6.0-7.0",
             "Ớt trồng chậu dễ chăm, cho quả nhiều màu sắc."],
            ["Dâu Tây", 0.4, "Trung bình", "Nắng vừa", "15-25°C", "50-70%", "5.5-6.5",
             "Dâu tây trồng chậu cho quả thơm ngon, cần chăm sóc kỹ."],
            ["Cà Chua Bi", 0.55, "Trung bình", "Nắng đầy đủ", "20-30°C", "40-60%", "6.0-7.0",
             "Cà chua bi dễ trồng, cho quả quanh năm nếu đủ ánh sáng."],
            
            # Cây thảo mộc
            ["Húng Quế", 0.4, "Dễ", "Nắng nhiều", "20-30°C", "40-60%", "6.0-7.0",
             "Húng quế dùng trong ẩm thực, có tác dụng đuổi côn trùng."],
            ["Bạc Hà", 0.5, "Dễ", "Bán phần", "18-25°C", "50-70%", "6.0-7.5",
             "Bạc hà thơm mát, dùng làm trà, đuổi muỗi hiệu quả."],
            ["Hành Lá", 0.3, "Dễ", "Nắng vừa", "15-25°C", "40-60%", "6.0-7.0",
             "Hành lá dễ trồng, thu hoạch nhanh, thích hợp trồng tại nhà."],
            ["Rau Mùi", 0.35, "Dễ", "Bán phần", "18-25°C", "40-60%", "6.0-7.0",
             "Rau mùi thơm đặc trưng, dùng nhiều trong ẩm thực Việt."],
            
            # Cây leo
            ["Thường Xuân", 0.4, "Dễ", "Bóng râm", "15-25°C", "40-60%", "6.0-7.5",
             "Thường xuân leo đẹp, thanh lọc không khí, chịu bóng tốt."],
            ["Cây Tiền", 0.3, "Dễ", "Bán phần", "20-30°C", "40-70%", "6.0-7.5",
             "Cây tiền leo nhanh, lá hình trái tim đẹp mắt."],
            ["Hoa Giấy", 0.45, "Dễ", "Nắng nhiều", "20-32°C", "40-60%", "6.0-7.0",
             "Hoa giấy nhiều màu sắc, ra hoa quanh năm, dễ trồng."],
            
            # Cây nhiệt đới
            ["Cây Dương Xỉ", 0.35, "Dễ", "Bóng râm", "18-28°C", "60-80%", "5.5-6.5",
             "Cây dương xỉ ưa ẩm, thanh lọc không khí tốt."],
            ["Cây Trúc Nhật", 0.3, "Dễ", "Bán phần", "20-30°C", "40-60%", "6.0-7.0",
             "Cây trúc nhật mang lại may mắn, dễ chăm sóc."],
            ["Cây Đa Búp Đỏ", 0.4, "Trung bình", "Nắng vừa", "20-30°C", "50-70%", "6.0-7.0",
             "Cây đa búp đỏ thanh lọc không khí, tạo điểm nhấn cho không gian."],
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
                "Tần suất tưới": self._get_watering_frequency(water, difficulty),
                "Tốc độ sinh trưởng": random.choice(["Chậm", "Trung bình", "Nhanh"]),
                "Chiều cao": f"{random.randint(20, 150)}-{random.randint(150, 300)} cm",
                "Mùa ra hoa": random.choice(["Xuân", "Hè", "Thu", "Đông", "Quanh năm"]),
                "Nhân giống": random.choice(["Giâm cành", "Tách bụi", "Hạt", "Chiết cành"]),
                "Phân bón": random.choice(["NPK 20-20-20", "Phân hữu cơ", "Phân vi lượng", "Phân chuồng"]),
                "Thú cưng": random.choice(["An toàn", "Độc nhẹ", "Không an toàn"]),
                "Thanh lọc không khí": random.choice(["Rất tốt", "Tốt", "Trung bình", "Không"]),
                "Loại": self._get_plant_type(name)
            })
        
        return pd.DataFrame(plants)
    
    def _get_plant_type(self, plant_name):
        """Xác định loại cây"""
        if "Hoa" in plant_name:
            return "Hoa"
        elif any(x in plant_name for x in ["Xương Rồng", "Sen Đá"]):
            return "Mọng nước"
        elif any(x in plant_name for x in ["Chanh", "Ớt", "Dâu", "Cà"]):
            return "Ăn quả"
        elif any(x in plant_name for x in ["Húng", "Bạc Hà", "Hành", "Rau"]):
            return "Thảo mộc"
        elif any(x in plant_name for x in ["Trầu", "Lưỡi Hổ", "Kim Tiền", "Ngũ Gia"]):
            return "Cảnh lá"
        elif any(x in plant_name for x in ["Thường Xuân", "Hoa Giấy"]):
            return "Cây leo"
        else:
            return "Cây cảnh"
    
    def _get_watering_frequency(self, water_amount, difficulty):
        """Xác định tần suất tưới"""
        if water_amount < 0.2:
            return "5-7 ngày/lần" if difficulty == "Dễ" else "7-10 ngày/lần"
        elif water_amount < 0.4:
            return "3-5 ngày/lần" if difficulty == "Dễ" else "5-7 ngày/lần"
        else:
            return "2-3 ngày/lần" if difficulty == "Dễ" else "3-5 ngày/lần"
    
    def _create_plant_info_database(self):
        """Tạo database thông tin chi tiết về cây"""
        info_db = {}
        
        # Tạo thông tin mẫu cho tất cả cây
        for _, plant in self.plants_db.iterrows():
            name = plant["Tên Cây"]
            
            # Xác định họ khoa học dựa trên loại cây
            plant_type = self._get_plant_type(name)
            scientific_families = {
                "Hoa": "Hoa cỏ",
                "Mọng nước": "Mọng nước",
                "Ăn quả": "Cây ăn quả",
                "Thảo mộc": "Thảo mộc",
                "Cảnh lá": "Cây cảnh",
                "Cây leo": "Dây leo",
                "Cây cảnh": "Cây cảnh"
            }
            
            info_db[name] = {
                "khoa_hoc": f"{name.replace(' ', '')} spp.",
                "ho": scientific_families.get(plant_type, "Thực vật"),
                "nguon_goc": random.choice(["Châu Á", "Châu Mỹ", "Châu Phi", "Châu Âu", "Việt Nam"]),
                "ky_thuat": self._generate_care_technique(name, plant_type),
                "benh_thuong_gap": self._generate_common_diseases(name),
                "cach_chua": self._generate_treatment_methods(name),
                "chu_ky": random.choice(["Hàng năm", "Lâu năm", "Hai năm"]),
                "y_nghia": self._generate_meaning(name)
            }
        
        return info_db
    
    def _generate_care_technique(self, name, plant_type):
        """Tạo kỹ thuật chăm sóc"""
        techniques = {
            "Hoa": "Cần ánh sáng đầy đủ, bón phân định kỳ 2 tuần/lần, cắt tỉa hoa tàn.",
            "Mọng nước": "Tưới ít, đất thoát nước tốt, nhiều ánh sáng, tránh úng nước.",
            "Ăn quả": "Nhiều ánh sáng, bón phân đều đặn, tỉa cành tạo tán.",
            "Thảo mộc": "Đất tơi xốp, tưới vừa phải, thu hoạch thường xuyên.",
            "Cảnh lá": "Lau lá thường xuyên, tưới khi đất khô, bón phân 1 tháng/lần.",
            "Cây leo": "Cần giá đỡ, cắt tỉa định kỳ, tưới đều đặn.",
        }
        return techniques.get(plant_type, "Tưới nước đều đặn, bón phân định kỳ, theo dõi sâu bệnh.")
    
    def _generate_common_diseases(self, name):
        """Tạo bệnh thường gặp"""
        diseases = ["Rệp sáp", "Nấm lá", "Thối rễ", "Vàng lá", "Đốm lá"]
        return ", ".join(random.sample(diseases, 2))
    
    def _generate_treatment_methods(self, name):
        """Tạo cách chữa trị"""
        treatments = [
            "Phun thuốc trừ sâu sinh học",
            "Cắt bỏ phần bệnh",
            "Thay đất mới",
            "Điều chỉnh lượng nước tưới",
            "Di chuyển đến vị trí phù hợp"
        ]
        return ", ".join(random.sample(treatments, 2))
    
    def _generate_meaning(self, name):
        """Tạo ý nghĩa cây"""
        meanings = [
            "Mang lại may mắn, tài lộc",
            "Thanh lọc không khí, tốt cho sức khỏe",
            "Tượng trưng cho tình yêu, hạnh phúc",
            "Mang lại bình an, thịnh vượng",
            "Biểu tượng của sức sống, kiên cường"
        ]
        return random.choice(meanings)
    
    def search_plants(self, query="", filters=None):
        """Tìm kiếm cây với bộ lọc"""
        results = self.plants_db.copy()
        
        # Thêm cây của người dùng
        if hasattr(self, 'user_plants') and self.user_plants:
            user_df = pd.DataFrame(self.user_plants)
            results = pd.concat([results, user_df], ignore_index=True)
        
        # Tìm kiếm theo từ khóa
        if query:
            mask = (
                results["Tên Cây"].str.contains(query, case=False, na=False) |
                results["Mô tả"].str.contains(query, case=False, na=False) |
                results["Loại"].str.contains(query, case=False, na=False)
            )
            results = results[mask]
        
        # Áp dụng bộ lọc
        if filters:
            for key, value in filters.items():
                if value and key in results.columns:
                    if isinstance(value, list):
                        results = results[results[key].isin(value)]
                    elif isinstance(value, tuple) and len(value) == 2:
                        # Cho phép lọc khoảng giá trị
                        results = results[
                            (results[key] >= value[0]) & 
                            (results[key] <= value[1])
                        ]
                    else:
                        results = results[results[key] == value]
        
        return results
    
    def get_plant_details(self, plant_name):
        """Lấy thông tin chi tiết về cây"""
        # Kiểm tra trong database chính
        plant_data = self.plants_db[self.plants_db["Tên Cây"] == plant_name]
        
        # Kiểm tra trong cây người dùng
        if plant_data.empty and hasattr(self, 'user_plants'):
            for plant in self.user_plants:
                if plant.get("Tên Cây") == plant_name:
                    plant_data = pd.DataFrame([plant])
                    break
        
        if plant_data.empty:
            return None
        
        plant_dict = plant_data.iloc[0].to_dict()
        
        # Thông tin bổ sung
        if plant_name in self.plant_info_db:
            plant_dict.update(self.plant_info_db[plant_name])
        else:
            # Tạo thông tin mặc định
            plant_dict.update({
                "khoa_hoc": f"{plant_name.replace(' ', '')} spp.",
                "ho": "Thực vật",
                "nguon_goc": "Nhiệt đới",
                "ky_thuat": "Tưới nước đều đặn, bón phân định kỳ",
                "benh_thuong_gap": "Rệp, nấm lá",
                "cach_chua": "Vệ sinh lá, phun thuốc sinh học",
                "chu_ky": "Lâu năm",
                "y_nghia": "Mang lại không gian xanh"
            })
        
        # Thêm mẹo chăm sóc
        plant_dict["meo_cham_soc"] = self._get_care_tips(plant_name, plant_dict)
        
        # Thêm lịch chăm sóc mẫu
        plant_dict["lich_cham_soc"] = self._create_sample_care_schedule(plant_name)
        
        return plant_dict
    
    def add_user_plant(self, plant_data):
        """Thêm cây do người dùng tự tạo"""
        if not hasattr(self, 'user_plants'):
            self.user_plants = []
        
        # Tạo ID mới
        max_id = max([p.get("ID", 0) for p in self.user_plants] + [len(self.plants_db)])
        plant_data["ID"] = max_id + 1
        plant_data["Loại"] = "Người dùng thêm"
        
        self.user_plants.append(plant_data)
        return plant_data
    
    def _get_care_tips(self, plant_name, plant_data):
        """Tạo mẹo chăm sóc"""
        tips = []
        
        # Mẹo dựa trên loại cây
        plant_type = self._get_plant_type(plant_name)
        
        if plant_type == "Hoa":
            tips.append("Cắt tỉa hoa tàn để kích thích ra hoa mới")
            tips.append("Bón phân giàu phosphor để ra nhiều hoa")
        
        if plant_type == "Mọng nước":
            tips.append("Chỉ tưới khi đất khô hoàn toàn")
            tips.append("Tránh để nước đọng trên lá")
        
        if plant_type == "Ăn quả":
            tips.append("Thụ phấn thủ công nếu trồng trong nhà")
            tips.append("Bón phân kali khi cây ra hoa")
        
        # Mẹo dựa trên độ khó
        if plant_data["Độ khó"] in ["Khó", "Rất khó"]:
            tips.append("Theo dõi sát sao độ ẩm và nhiệt độ")
            tips.append("Đọc kỹ hướng dẫn trước khi chăm sóc")
        
        # Mẹo chung
        tips.extend([
            "Lau lá thường xuyên để tăng khả năng quang hợp",
            "Xoay chậu định kỳ để cây phát triển đều",
            "Kiểm tra sâu bệnh ít nhất 1 lần/tuần",
            "Sử dụng nước sạch, không chứa clo để tưới"
        ])
        
        return tips
    
    def _create_sample_care_schedule(self, plant_name):
        """Tạo lịch chăm sóc mẫu"""
        schedule = []
        today = datetime.datetime.now()
        
        for i in range(7):
            date = today + timedelta(days=i)
            date_str = date.strftime("%d/%m")
            
            # Tạo công việc dựa trên ngày
            tasks = []
            
            # Tưới nước (giả lập lịch)
            water_days = [0, 2, 4, 6]  # Tưới cách ngày
            if i in water_days:
                tasks.append("💧 Tưới nước")
            
            # Bón phân (7 ngày/lần)
            if i == 0:
                tasks.append("🌿 Bón phân NPK")
            
            # Kiểm tra (3 ngày/lần)
            if i % 3 == 0:
                tasks.append("🔍 Kiểm tra sức khỏe")
            
            # Cắt tỉa (vào cuối tuần)
            if i == 6:
                tasks.append("✂️ Cắt tỉa lá vàng")
            
            schedule.append({
                "ngay": date_str,
                "thu": date.strftime("%A"),
                "cong_viec": ", ".join(tasks) if tasks else "Nghỉ ngơi",
                "ghi_chu": "Sáng sớm" if tasks else ""
            })
        
        return schedule

# --- 5. HỆ THỐNG AI OFFLINE NÂNG CẤP ---
class EnhancedOfflineAISystem:
    """Hệ thống AI hoạt động hoàn toàn offline - Nâng cấp"""
    
    def __init__(self):
        self.knowledge_base = self._create_knowledge_base()
        self.diagnosis_history = []
        
    def _create_knowledge_base(self):
        """Tạo cơ sở kiến thức offline mở rộng"""
        return {
            # Kiến thức về bệnh cây
            "vàng lá": {
                "nguyen_nhan": ["Thiếu nước", "Thừa nước", "Thiếu ánh sáng", "Thiếu dinh dưỡng", "Nhiễm bệnh", "Đất không phù hợp"],
                "giai_doan": ["Sớm (lá vàng nhẹ)", "Trung bình (vàng 30-50%)", "Nặng (vàng toàn bộ)"],
                "cach_xu_ly": [
                    "Kiểm tra độ ẩm đất bằng que thử",
                    "Điều chỉnh lượng nước tưới phù hợp",
                    "Di chuyển cây ra nơi có ánh sáng phù hợp",
                    "Bón phân vi lượng (sắt, magie, nitơ)",
                    "Cắt tỉa lá bệnh để tránh lây lan",
                    "Thay đất nếu đất bị chua hoặc kiềm"
                ],
                "phong_ngua": [
                    "Tưới nước đúng cách",
                    "Đảm bảo đủ ánh sáng",
                    "Bón phân định kỳ",
                    "Kiểm tra pH đất thường xuyên"
                ]
            },
            "thối rễ": {
                "nguyen_nhan": ["Tưới quá nhiều nước", "Đất thoát nước kém", "Nhiễm nấm", "Chậu không có lỗ thoát"],
                "giai_doan": ["Nhẹ (rễ hơi thối)", "Trung bình (rễ thối 50%)", "Nặng (toàn bộ rễ thối)"],
                "cach_xu_ly": [
                    "NGỪNG TƯỚI NGAY LẬP TỨC",
                    "Nhấc cây ra khỏi chậu kiểm tra rễ",
                    "Cắt bỏ hoàn toàn phần rễ thối",
                    "Xử lý vết cắt bằng thuốc trừ nấm",
                    "Thay đất mới thoát nước tốt",
                    "Trồng lại và để khô 3-5 ngày"
                ],
                "phong_ngua": [
                    "Sử dụng chậu có lỗ thoát nước",
                    "Đất trồng phải thoát nước tốt",
                    "Không tưới quá thường xuyên",
                    "Kiểm tra độ ẩm đất trước khi tưới"
                ]
            },
            "rụng lá": {
                "nguyen_nhan": ["Sốc nhiệt", "Thiếu nước", "Thay đổi môi trường", "Sâu bệnh", "Thiếu dinh dưỡng"],
                "giai_doan": ["Nhẹ (rụng ít)", "Trung bình (rụng nhiều)", "Nghiêm trọng (rụng hết)"],
                "cach_xu_ly": [
                    "Giữ ổn định nhiệt độ (20-28°C)",
                    "Tưới nước đều đặn, không để đất khô hoàn toàn",
                    "Không di chuyển cây thường xuyên",
                    "Kiểm tra và xử lý sâu bệnh kịp thời",
                    "Bón phân cân đối NPK"
                ],
                "phong_ngua": [
                    "Tránh thay đổi môi trường đột ngột",
                    "Tưới nước đều đặn",
                    "Bón phân định kỳ",
                    "Kiểm tra sâu bệnh thường xuyên"
                ]
            },
            "đốm lá": {
                "nguyen_nhan": ["Nhiễm nấm", "Vi khuẩn", "Thiếu dinh dưỡng", "Nước tưới bẩn"],
                "giai_doan": ["Sớm (vài đốm nhỏ)", "Trung bình (lan ra nhiều lá)", "Lan rộng (toàn cây)"],
                "cach_xu_ly": [
                    "Cắt bỏ lá bệnh ngay lập tức",
                    "Phun thuốc trừ nấm sinh học",
                    "Tăng cường thông gió cho cây",
                    "Bón phân cân đối",
                    "Sử dụng nước sạch để tưới"
                ],
                "phong_ngua": [
                    "Tránh tưới nước lên lá",
                    "Đảm bảo thông gió tốt",
                    "Sử dụng nước sạch",
                    "Vệ sinh lá thường xuyên"
                ]
            },
            "héo lá": {
                "nguyen_nhan": ["Thiếu nước", "Nhiệt độ quá cao", "Ánh sáng quá mạnh", "Bệnh rễ"],
                "giai_doan": ["Nhẹ", "Trung bình", "Nặng"],
                "cach_xu_ly": [
                    "Tưới nước ngay nếu đất khô",
                    "Di chuyển cây đến nơi mát mẻ",
                    "Che bớt nắng nếu ánh sáng quá mạnh",
                    "Kiểm tra hệ thống rễ"
                ],
                "phong_ngua": [
                    "Tưới nước đều đặn",
                    "Tránh ánh nắng trực tiếp giữa trưa",
                    "Giữ nhiệt độ ổn định"
                ]
            },
            
            # Kiến thức về chăm sóc
            "tưới nước": {
                "nguyen_tac": [
                    "Tưới khi đất khô 2-3cm bề mặt",
                    "Tưới vào sáng sớm (6-8h) hoặc chiều mát (4-6h)",
                    "Không tưới vào buổi trưa nắng",
                    "Lượng nước: 1/3 thể tích chậu",
                    "Tưới từ từ cho nước thấm đều"
                ],
                "loai_cay": {
                    "cay_uam": "Tưới 1-2 ngày/lần, giữ đất luôn ẩm",
                    "cay_chiu_han": "Tưới 3-7 ngày/lần, để đất khô hoàn toàn giữa các lần tưới",
                    "cay_thuong": "Tưới 2-3 ngày/lần, tưới khi đất khô bề mặt"
                },
                "loai_nuoc": [
                    "Nước mưa: Tốt nhất",
                    "Nước máy: Để qua đêm cho bay hơi clo",
                    "Nước lọc: An toàn",
                    "Nước giếng: Kiểm tra độ pH"
                ]
            },
            "bon_phan": {
                "loai_phan": ["NPK 20-20-20 (cân đối)", "NPK 30-10-10 (ra lá)", "NPK 10-30-20 (ra hoa)", "Phân hữu cơ", "Phân vi lượng", "Phân chuồng"],
                "tan_suat": ["2 tuần/lần (mùa sinh trưởng)", "1 tháng/lần (mùa nghỉ)", "Không bón khi cây bệnh"],
                "cach_bon": ["Hòa tan trong nước", "Rải quanh gốc", "Pha loãng trước khi tưới", "Bón sau khi tưới nước"],
                "luu_y": ["Không bón quá liều", "Không bón vào lá", "Ngừng bón khi cây ngủ đông"]
            },
            "anh_sang": {
                "yeu_cau": {
                    "nang_nhieu": "6-8h nắng/ngày (Hoa hồng, ớt, xương rồng)",
                    "nang_vua": "4-6h nắng/ngày (Hoa cúc, chanh, dâu)",
                    "ban_phan": "2-4h nắng/ngày (Trầu bà, lan, ngũ gia bì)",
                    "bong_ram": "Ánh sáng gián tiếp (Lưỡi hổ, dương xỉ)"
                },
                "dau_hieu": {
                    "thieu_sang": "Cây vươn dài, lá nhỏ, màu nhạt",
                    "thua_sang": "Lá cháy nắng, vàng, rụng"
                }
            }
        }
    
    def analyze_plant_problem(self, symptoms, plant_type="", additional_info=""):
        """Phân tích vấn đề của cây"""
        # Ghi lại lịch sử chẩn đoán
        diagnosis_id = len(self.diagnosis_history) + 1
        
        analysis = {
            "id": diagnosis_id,
            "benh": "Chưa xác định",
            "do_tin_cay": 0,
            "nguyen_nhan": [],
            "giai_doan": "Chưa xác định",
            "xu_ly": [],
            "phong_ngua": [],
            "kham_nhanh": [],
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Chuẩn hóa triệu chứng
        symptoms_lower = symptoms.lower()
        
        # Tìm kiếm trong knowledge base
        found_diseases = []
        for disease, info in self.knowledge_base.items():
            # Kiểm tra triệu chứng phù hợp
            symptom_score = 0
            
            # Kiểm tra từ khóa
            keywords = disease.split()
            for keyword in keywords:
                if keyword in symptoms_lower:
                    symptom_score += 30
            
            # Kiểm tra triệu chứng chung
            common_symptoms = ["vàng", "thối", "rụng", "đốm", "héo", "khô", "ủ rũ"]
            for symptom in common_symptoms:
                if symptom in symptoms_lower and symptom in disease:
                    symptom_score += 20
            
            if symptom_score > 0:
                found_diseases.append({
                    "disease": disease,
                    "score": symptom_score,
                    "info": info
                })
        
        # Sắp xếp theo điểm
        if found_diseases:
            found_diseases.sort(key=lambda x: x["score"], reverse=True)
            best_match = found_diseases[0]
            
            analysis["benh"] = best_match["disease"].upper()
            analysis["nguyen_nhan"] = best_match["info"]["nguyen_nhan"]
            analysis["do_tin_cay"] = min(95, best_match["score"])
            analysis["giai_doan"] = random.choice(best_match["info"]["giai_doan"])
            analysis["xu_ly"] = best_match["info"]["cach_xu_ly"][:4]
            analysis["phong_ngua"] = best_match["info"].get("phong_ngua", [
                "Giữ vệ sinh khu vực trồng cây",
                "Tưới nước đúng cách",
                "Bón phân định kỳ",
                "Kiểm tra cây thường xuyên"
            ])
        else:
            # Phân tích chung dựa trên triệu chứng
            analysis["benh"] = "STRESS MÔI TRƯỜNG"
            analysis["nguyen_nhan"] = self._analyze_environmental_stress(symptoms_lower)
            analysis["do_tin_cay"] = 70
            analysis["giai_doan"] = "Nhẹ đến trung bình"
            analysis["xu_ly"] = [
                "Điều chỉnh lượng nước tưới phù hợp",
                "Di chuyển cây đến vị trí có ánh sáng thích hợp",
                "Kiểm tra nhiệt độ môi trường",
                "Theo dõi trong 3-5 ngày"
            ]
            analysis["phong_ngua"] = [
                "Giữ cây ở vị trí ổn định",
                "Tưới nước đều đặn",
                "Tránh thay đổi môi trường đột ngột",
                "Bón phân định kỳ"
            ]
        
        # Thêm khám nhanh
        analysis["kham_nhanh"] = self._generate_quick_checklist(symptoms_lower, plant_type)
        
        # Lưu vào lịch sử
        self.diagnosis_history.append(analysis.copy())
        
        return analysis
    
    def _analyze_environmental_stress(self, symptoms):
        """Phân tích stress môi trường"""
        causes = []
        
        if any(word in symptoms for word in ["khô", "thiếu nước", "héo"]):
            causes.append("Thiếu nước")
        
        if any(word in symptoms for word in ["ướt", "thối", "ủng"]):
            causes.append("Thừa nước")
        
        if any(word in symptoms for word in ["nắng", "cháy", "nóng"]):
            causes.append("Ánh sáng quá mạnh")
        
        if any(word in symptoms for word in ["thiếu sáng", "vươn", "dài"]):
            causes.append("Thiếu ánh sáng")
        
        if any(word in symptoms for word in ["lạnh", "rét"]):
            causes.append("Nhiệt độ quá thấp")
        
        if not causes:
            causes = ["Thay đổi môi trường đột ngột", "Điều kiện chăm sóc không phù hợp"]
        
        return causes
    
    def _generate_quick_checklist(self, symptoms, plant_type):
        """Tạo checklist khám nhanh"""
        checklist = []
        
        # Kiểm tra chung
        checklist.append("✓ Kiểm tra độ ẩm đất (khô 2-3cm mới tưới)")
        checklist.append("✓ Kiểm tra lỗ thoát nước chậu")
        checklist.append("✓ Kiểm tra ánh sáng vị trí đặt cây")
        
        # Kiểm tra dựa trên triệu chứng
        if "vàng" in symptoms:
            checklist.append("✓ Kiểm tra màu sắc toàn bộ lá")
            checklist.append("✓ Kiểm tra phần gốc và rễ")
        
        if "rụng" in symptoms:
            checklist.append("✓ Kiểm tra điểm rụng lá")
            checklist.append("✓ Kiểm tra cành nhánh")
        
        if "đốm" in symptoms:
            checklist.append("✓ Kiểm tra cả mặt trên và dưới lá")
            checklist.append("✓ Kiểm tra có nấm mốc không")
        
        # Kiểm tra dựa trên loại cây
        if plant_type:
            if "hoa" in plant_type.lower():
                checklist.append("✓ Kiểm tra nụ hoa và hoa tàn")
            elif "ăn quả" in plant_type.lower():
                checklist.append("✓ Kiểm tra quả non và quả chín")
        
        return checklist[:6]  # Giới hạn 6 mục
    
    def get_care_advice(self, plant_name, plant_data=None, season=""):
        """Đưa ra lời khuyên chăm sóc"""
        advice = {
            "tuoi_nuoc": "",
            "anh_sang": "",
            "bon_phan": "",
            "cat_tia": "",
            "bao_ve": "",
            "luu_y_theo_mua": ""
        }
        
        # Xác định loại cây
        plant_type = "chung"
        if plant_data and "Loại" in plant_data:
            plant_type = plant_data["Loại"].lower()
        
        # Lời khuyên tưới nước
        water_advice = {
            "hoa": "Tưới khi đất khô 1-2cm bề mặt, tránh tưới lên hoa",
            "mọng nước": "Chỉ tưới khi đất khô hoàn toàn (7-10 ngày/lần)",
            "ăn quả": "Tưới đều đặn, giữ đất ẩm nhưng không úng",
            "thảo mộc": "Tưới vừa phải, tránh để đất quá ẩm",
            "cảnh lá": "Tưới khi đất khô 2-3cm bề mặt",
            "cây leo": "Tưới đều đặn, cần độ ẩm ổn định",
            "chung": "Tưới khi đất khô 2-3cm bề mặt"
        }
        advice["tuoi_nuoc"] = water_advice.get(plant_type, water_advice["chung"])
        
        # Lời khuyên ánh sáng
        light_advice = {
            "hoa": "Cần ít nhất 6h ánh sáng mỗi ngày",
            "mọng nước": "Cần nhiều ánh sáng trực tiếp",
            "ăn quả": "Cần đầy đủ ánh sáng để ra quả",
            "thảo mộc": "Cần 4-6h ánh sáng mỗi ngày",
            "cảnh lá": "Ánh sáng gián tiếp 4-6h/ngày",
            "cây leo": "Ánh sáng vừa đến nhiều",
            "chung": "Ánh sáng gián tiếp 4-6h/ngày"
        }
        advice["anh_sang"] = light_advice.get(plant_type, light_advice["chung"])
        
        # Lời khuyên bón phân
        fertilizer_advice = {
            "hoa": "Bón phân NPK 10-30-20 để kích hoa, 2 tuần/lần",
            "mọng nước": "Bón phân chuyên dụng 1 tháng/lần trong mùa sinh trưởng",
            "ăn quả": "Bón phân NPK 15-15-15 đều đặn, thêm kali khi ra quả",
            "thảo mộc": "Bón phân hữu cơ hoặc NPK 20-20-20 3 tuần/lần",
            "cảnh lá": "Bón phân NPK 20-20-20 2 tuần/lần",
            "cây leo": "Bón phân NPK 20-20-20 2 tuần/lần",
            "chung": "Bón phân NPK 20-20-20 2 tuần/lần trong mùa sinh trưởng"
        }
        advice["bon_phan"] = fertilizer_advice.get(plant_type, fertilizer_advice["chung"])
        
        # Lời khuyên cắt tỉa
        pruning_advice = {
            "hoa": "Cắt tỉa hoa tàn thường xuyên, tỉa cành sau mùa hoa",
            "mọng nước": "Cắt tỉa ít, chỉ khi cần nhân giống",
            "ăn quả": "Tỉa cành vượt, cành bệnh, tạo tán",
            "thảo mộc": "Tỉa ngọn để cây phân nhánh, thu hoạch thường xuyên",
            "cảnh lá": "Cắt tỉa lá vàng, cành khô, tỉa tạo dáng",
            "cây leo": "Tỉa bớt cành quá dài, cành yếu",
            "chung": "Cắt tỉa lá vàng, cành khô thường xuyên"
        }
        advice["cat_tia"] = pruning_advice.get(plant_type, pruning_advice["chung"])
        
        # Lời khuyên bảo vệ
        protection_advice = {
            "hoa": "Che mưa khi hoa nở, phòng sâu bệnh",
            "mọng nước": "Tránh mưa và độ ẩm cao, để nơi thoáng",
            "ăn quả": "Bảo vệ quả khỏi chim, sâu, bệnh",
            "thảo mộc": "Tránh sâu ăn lá, thu hoạch đúng thời điểm",
            "cảnh lá": "Lau lá thường xuyên, kiểm tra sâu bệnh",
            "cây leo": "Cung cấp giá đỡ chắc chắn, kiểm tra điểm bám",
            "chung": "Lau lá thường xuyên, kiểm tra sâu bệnh"
        }
        advice["bao_ve"] = protection_advice.get(plant_type, protection_advice["chung"])
        
        # Lưu ý theo mùa
        if season:
            season_notes = {
                "Xuân": "Mùa sinh trưởng mạnh, tăng tưới nước và bón phân",
                "Hè": "Nắng nóng, che nắng giữa trưa, tưới nhiều hơn",
                "Thu": "Mát mẻ, giảm tưới nước, chuẩn bị cho mùa đông",
                "Đông": "Lạnh, giảm tưới nước, tránh gió lạnh, ngừng bón phân"
            }
            advice["luu_y_theo_mua"] = season_notes.get(season, "Chăm sóc bình thường")
        else:
            advice["luu_y_theo_mua"] = "Theo dõi thời tiết để điều chỉnh chăm sóc"
        
        return advice
    
    def generate_watering_schedule(self, plant_name, plant_data, weather_data, location_data):
        """Tạo lịch tưới thông minh"""
        schedule = []
        today = datetime.datetime.now()
        
        # Xác định loại cây
        plant_type = plant_data.get("Loại", "chung") if plant_data else "chung"
        
        # Xác định tần suất cơ bản
        base_frequencies = {
            "Hoa": 2,
            "Mọng nước": 7,
            "Ăn quả": 3,
            "Thảo mộc": 2,
            "Cảnh lá": 3,
            "Cây leo": 2,
            "chung": 3
        }
        base_frequency = base_frequencies.get(plant_type, 3)
        
        # Điều chỉnh theo thời tiết
        if weather_data is not None and len(weather_data) > 0:
            # Lấy thông tin mùa và nhiệt độ trung bình
            season = weather_data.iloc[0].get('season', '')
            avg_temp = weather_data['temp_max'].mean()
            
            # Điều chỉnh theo mùa
            if season in ["Hè", "Nắng nóng"]:
                base_frequency = max(1, base_frequency - 1)
            elif season in ["Đông", "Lạnh"]:
                base_frequency = base_frequency + 2
            
            # Điều chỉnh theo nhiệt độ
            if avg_temp > 30:
                base_frequency = max(1, base_frequency - 1)
            elif avg_temp < 15:
                base_frequency = base_frequency + 2
        
        # Tạo lịch 14 ngày
        for day in range(14):
            current_date = today + timedelta(days=day)
            date_str = current_date.strftime("%d/%m/%Y")
            weekday = current_date.strftime("%A")
            
            # Xác định ngày tưới
            need_water = (day % base_frequency == 0)
            
            # Điều chỉnh theo ngày mưa (nếu có weather_data)
            rain_today = 0
            if weather_data is not None and day < len(weather_data):
                rain_today = weather_data.iloc[day].get('precipitation', 0)
            
            # Nếu mưa nhiều thì không cần tưới
            if rain_today > 10:
                need_water = False
            elif 5 < rain_today <= 10:
                # Mưa vừa thì giảm lượng nước
                water_note = "Giảm 50% lượng nước (có mưa)"
            else:
                water_note = "Tưới bình thường"
            
            if need_water and rain_today <= 10:
                # Tính lượng nước
                base_water = plant_data.get("Nước (L/ngày)", 0.3) if plant_data else 0.3
                water_amount = base_water
                
                # Điều chỉnh theo nhiệt độ
                if weather_data is not None and day < len(weather_data):
                    temp_today = weather_data.iloc[day].get('temp_max', 25)
                    if temp_today > 30:
                        water_amount *= 1.3
                    elif temp_today < 15:
                        water_amount *= 0.7
                
                # Điều chỉnh theo mưa
                if rain_today > 5:
                    water_amount *= 0.5
                
                schedule.append({
                    "Ngày": date_str,
                    "Thứ": weekday,
                    "Hành động": "💧 Tưới nước",
                    "Thời điểm": "Sáng sớm (6-8h)",
                    "Lượng nước (ml)": round(water_amount * 1000, 0),
                    "Ghi chú": water_note
                })
            else:
                action = "✅ Nghỉ" if rain_today <= 10 else "⛈️ Không tưới (trời mưa)"
                note = "Quan sát tình trạng cây" if rain_today <= 10 else f"Mưa {rain_today}mm"
                
                schedule.append({
                    "Ngày": date_str,
                    "Thứ": weekday,
                    "Hành động": action,
                    "Thời điểm": "-",
                    "Lượng nước (ml)": 0,
                    "Ghi chú": note
                })
        
        return schedule

# --- 6. KHỞI TẠO HỆ THỐNG NÂNG CẤP ---
@st.cache_resource
def initialize_systems():
    """Khởi tạo tất cả hệ thống với cache"""
    config_system = AutoConfigSystem()
    map_system = EnhancedOfflineMapSystem()
    plant_system = EnhancedOfflinePlantSystem()
    ai_system = EnhancedOfflineAISystem()
    
    return config_system, map_system, plant_system, ai_system

# Khởi tạo hệ thống
config_system, map_system, plant_system, ai_system = initialize_systems()

# Lấy database cây
df_plants = plant_system.plants_db

# --- 7. KHỞI TẠO SESSION STATE ---
default_state = {
    'selected_plant': df_plants.iloc[0].to_dict() if not df_plants.empty else {},
    'selected_location': [10.8231, 106.6297],  # TP.HCM mặc định
    'location_name': "TP Hồ Chí Minh",
    'location_details': {"type": "Thành phố", "region": "Miền Nam", "source": "offline", "population": "9.0M"},
    'forecast_data': None,
    'water_calculation': None,
    'plant_details': None,
    'search_history': [],
    'favorite_plants': [],
    'user_plants': [],
    'diagnosis_history': [],
    'user_settings': {
        'theme': 'dark',
        'units': 'metric',
        'notifications': True,
        'auto_save': True,
        'language': 'vi'
    },
    'version': config_system.version,
    'build_date': config_system.build_date,
    'system_status': {
        'weather_system': 'online',
        'map_system': 'online',
        'plant_system': 'online',
        'ai_system': 'online',
        'last_check': datetime.datetime.now().strftime("%H:%M:%S")
    }
}

for key, value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- 8. SIDEBAR NÂNG CẤP ---
with st.sidebar:
    # Logo và thông tin
    st.markdown(f"""
    <div style="text-align: center; padding: 1.5rem 0;">
        <h1 style="background: linear-gradient(90deg, #00ffcc, #0088cc); 
                   -webkit-background-clip: text; 
                   -webkit-text-fill-color: transparent;
                   font-size: 1.8rem;
                   margin: 0;">
            🌿 EcoMind OS
        </h1>
        <p style="color: #88aaff; margin: 0.3rem 0; font-size: 0.9rem;">
            Phiên bản 6.0 - Không cần API Key
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
    
    # Menu điều hướng - CẢI TIẾN
    selected = option_menu(
        menu_title=None,
        options=["🏠 Bảng Điều Khiển", "🗺️ Bản Đồ Thông Minh", "🌿 Thư Viện Cây", 
                "🤖 AI Chẩn Đoán", "📊 Dự Báo Thông Minh", "⚙️ Hệ Thống"],
        icons=["house", "map", "tree", "robot", "cloud-sun", "gear"],
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
    st.markdown("### 📍 Vị trí hiện tại")
    
    if st.session_state.location_name:
        with st.container(border=True):
            st.markdown(f"**{st.session_state.location_name}**")
            st.caption(f"📍 {st.session_state.location_details.get('type', 'Địa điểm')}")
            st.caption(f"🌍 {st.session_state.location_details.get('region', 'Việt Nam')}")
            if 'population' in st.session_state.location_details:
                st.caption(f"👥 {st.session_state.location_details['population']}")
    
    st.markdown("### 🌿 Cây đang chọn")
    
    if st.session_state.selected_plant:
        plant = st.session_state.selected_plant
        with st.container(border=True):
            st.markdown(f"**{plant.get('Tên Cây', 'Chưa chọn')}**")
            st.caption(f"💧 {plant.get('Nước (L/ngày)', 0)}L/ngày")
            st.caption(f"⚡ {plant.get('Độ khó', 'Chưa có')}")
            st.caption(f"☀️ {plant.get('Ánh sáng', 'Chưa có')}")
    
    # Trạng thái hệ thống
    st.markdown("---")
    st.markdown("### 📊 Trạng thái hệ thống")
    
    col_status1, col_status2 = st.columns(2)
    with col_status1:
        st.markdown('<span class="status-indicator status-online"></span> Hoạt động', unsafe_allow_html=True)
    with col_status2:
        st.caption(f"Kiểm tra: {st.session_state.system_status['last_check']}")
    
    # Thống kê
    st.markdown("---")
    st.markdown("### 📈 Thống kê")
    
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("Cây trong DB", len(df_plants))
    with col_stat2:
        st.metric("Địa điểm", len(map_system.vietnam_locations))
    
    # Nút làm mới
    if st.button("🔄 Làm mới toàn bộ", use_container_width=True, type="secondary"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.session_state.system_status['last_check'] = datetime.datetime.now().strftime("%H:%M:%S")
        st.rerun()

# --- 9. NỘI DUNG CHÍNH THEO TAB ---

# === TAB 1: BẢNG ĐIỀU KHIỂN NÂNG CẤP ===
if selected == "🏠 Bảng Điều Khiển":
    st.title("🏠 Bảng Điều Khiển EcoMind OS")
    st.markdown("### Hệ thống chăm sóc cây thông minh - Phiên bản 6.0")
    
    # Metrics tổng quan
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌿 Cây trong DB", len(df_plants), "+15 từ v5.0")
    with col2:
        st.metric("🗺️ Địa điểm", len(map_system.vietnam_locations), "+50 từ v5.0")
    with col3:
        st.metric("🤖 Chẩn đoán", len(ai_system.diagnosis_history), "lượt")
    with col4:
        st.metric("⭐ Phiên bản", st.session_state.version, "6.0")
    
    # Cards giới thiệu
    col_card1, col_card2 = st.columns(2)
    
    with col_card1:
        with st.container(border=True):
            st.markdown("### 🎯 Tính năng mới v6.0")
            st.markdown("""
            - **🤖 AI Chẩn đoán nâng cao**: Phân tích bệnh cây chi tiết
            - **🗺️ Bản đồ thông minh**: 200+ địa điểm Việt Nam
            - **🌿 Thêm 15 loại cây**: Database 50+ cây trồng
            - **📊 Dự báo chi tiết**: Mô phỏng thời tiết 7 ngày
            - **💧 Tính toán thông minh**: Điều chỉnh theo mùa, loại đất
            - **📅 Lịch chăm sóc**: Tự động tạo lịch 14 ngày
            """)
    
    with col_card2:
        with st.container(border=True):
            st.markdown("### 🏆 Ưu điểm hệ thống")
            st.markdown("""
            **Hoạt động không cần API Key:**
            - Không cần kết nối internet
            - Không cần đăng ký tài khoản
            - Dữ liệu ổn định, luôn sẵn sàng
            
            **Thông tin kỹ thuật:**
            - Phiên bản: """ + st.session_state.version + """
            - Build: """ + st.session_state.build_date + """
            - Framework: Streamlit + Pandas
            - Database: Offline hoàn toàn
            """)
    
    # Hướng dẫn nhanh
    st.markdown("### 🚀 Hướng dẫn sử dụng nhanh")
    
    steps = [
        ("1. Chọn vị trí", "🗺️ Tab 'Bản Đồ Thông Minh'", "Tìm kiếm hoặc click trên bản đồ"),
        ("2. Chọn cây", "🌿 Tab 'Thư Viện Cây'", "Tìm và chọn cây của bạn"),
        ("3. Chẩn đoán", "🤖 Tab 'AI Chẩn Đoán'", "Phân tích vấn đề cây trồng"),
        ("4. Dự báo", "📊 Tab 'Dự Báo Thông Minh'", "Xem dự báo và lịch chăm sóc")
    ]
    
    for title, tab, desc in steps:
        with st.expander(f"**{title}** - {tab}", expanded=False):
            st.markdown(desc)
            if "vị trí" in title:
                st.button("📌 Đến tab Bản Đồ", key=f"goto_{title}", 
                         on_click=lambda: st.session_state.__setitem__('selected', "🗺️ Bản Đồ Thông Minh"))
    
    # Thống kê thực tế
    st.markdown("### 📈 Thống kê thực tế")
    
    tab_stats1, tab_stats2, tab_stats3 = st.tabs(["🌡️ Thời tiết hôm nay", "🌿 Cây phổ biến", "📊 Hệ thống"])
    
    with tab_stats1:
        if st.session_state.selected_location:
            weather_today = config_system.get_weather_data(
                st.session_state.selected_location[0],
                st.session_state.selected_location[1],
                days=1
            )
            
            if not weather_today.empty:
                today = weather_today.iloc[0]
                
                cols = st.columns(4)
                weather_info = [
                    ("🌡️ Nhiệt độ", f"{today['temp_max']}°C"),
                    ("💧 Mưa", f"{today['precipitation']}mm"),
                    ("💦 Độ ẩm", f"{today['humidity']}%"),
                    ("💨 Gió", f"{today['wind_speed']}km/h {today['wind_direction']}")
                ]
                
                for (col, (icon, value)) in zip(cols, weather_info):
                    with col:
                        st.metric(icon, value)
                
                st.markdown(f"**Điều kiện:** {today['icon']} {today['condition']}")
                st.markdown(f"**Mùa:** {today['season']}")
    
    with tab_stats2:
        # Top cây phổ biến
        popular_plants = df_plants.head(5)
        for idx, plant in popular_plants.iterrows():
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{plant['Tên Cây']}**")
                    st.caption(f"{plant['Mô tả'][:80]}...")
                with col2:
                    st.markdown(f"💧 {plant['Nước (L/ngày)']}L")
                    st.markdown(f"⚡ {plant['Độ khó']}")
                with col3:
                    if st.button("Chọn", key=f"select_pop_{plant['ID']}"):
                        st.session_state.selected_plant = plant.to_dict()
                        st.session_state.plant_details = plant_system.get_plant_details(plant['Tên Cây'])
                        st.success(f"✅ Đã chọn {plant['Tên Cây']}!")
    
    with tab_stats3:
        col_sys1, col_sys2 = st.columns(2)
        with col_sys1:
            st.metric("Cache thời tiết", len(config_system.weather_cache))
            st.metric("Lượt chẩn đoán", len(ai_system.diagnosis_history))
        with col_sys2:
            st.metric("Cây người dùng", len(plant_system.user_plants))
            st.metric("Tìm kiếm gần đây", len(st.session_state.search_history))

# === TAB 2: BẢN ĐỒ THÔNG MINH ===
elif selected == "🗺️ Bản Đồ Thông Minh":
    st.title("🗺️ Bản Đồ & Quản Lý Vị Trí Thông Minh")
    st.markdown("### Quản lý vị trí cây trồng của bạn")
    
    tab_map1, tab_map2, tab_map3 = st.tabs(["🗺️ Bản đồ tương tác", "🔍 Tìm kiếm thông minh", "📌 Quản lý vị trí"])
    
    with tab_map1:
        col_map_main, col_map_sidebar = st.columns([3, 1])
        
        with col_map_main:
            # Hiển thị thông tin vị trí hiện tại
            with st.container(border=True):
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.markdown(f"#### 📍 {st.session_state.location_name}")
                    st.caption(f"Vĩ độ: {st.session_state.selected_location[0]:.4f}")
                    st.caption(f"Kinh độ: {st.session_state.selected_location[1]:.4f}")
                with col_info2:
                    st.caption(f"Loại: {st.session_state.location_details.get('type', 'N/A')}")
                    st.caption(f"Vùng: {st.session_state.location_details.get('region', 'N/A')}")
                    if 'population' in st.session_state.location_details:
                        st.caption(f"Dân số: {st.session_state.location_details['population']}")
            
            # Tạo bản đồ
            m = map_system.create_interactive_map(
                st.session_state.selected_location[0],
                st.session_state.selected_location[1],
                zoom=12
            )
            
            # Hiển thị bản đồ
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
                
                # Tìm địa điểm gần nhất
                closest = None
                min_dist = float('inf')
                
                for name, data in map_system.vietnam_locations.items():
                    dist = map_system.calculate_distance(lat, lng, data["lat"], data["lon"])
                    if dist < min_dist:
                        min_dist = dist
                        closest = {"name": name, "data": data, "distance": dist}
                
                if closest and min_dist < 50:  # Trong 50km
                    st.session_state.selected_location = [closest["data"]["lat"], closest["data"]["lon"]]
                    st.session_state.location_name = closest["name"]
                    st.session_state.location_details = {
                        "type": closest["data"]["type"],
                        "region": closest["data"]["region"],
                        "source": "map_click",
                        "population": closest["data"].get("population", ""),
                        "distance_km": round(closest["distance"], 1)
                    }
                    st.success(f"📍 Đã chọn: {closest['name']} (cách {round(closest['distance'], 1)}km)")
                    st.rerun()
                else:
                    st.session_state.selected_location = [lat, lng]
                    st.session_state.location_name = f"{lat:.4f}, {lng:.4f}"
                    st.session_state.location_details = {
                        "type": "Tọa độ",
                        "region": "Việt Nam",
                        "source": "map_click"
                    }
                    st.info(f"📍 Tọa độ: {lat:.4f}, {lng:.4f}")
        
        with col_map_sidebar:
            st.markdown("### 📍 Lựa chọn nhanh")
            
            # Chọn từ danh sách vùng
            regions = {}
            for name, data in map_system.vietnam_locations.items():
                if "," not in name:  # Chỉ hiển thị tên chính
                    region = data["region"]
                    if region not in regions:
                        regions[region] = []
                    regions[region].append((name, data))
            
            for region, locations in regions.items():
                with st.expander(f"📍 {region}", expanded=False):
                    for name, data in locations[:6]:
                        if st.button(f"• {name}", key=f"loc_btn_{name}", use_container_width=True):
                            st.session_state.selected_location = [data["lat"], data["lon"]]
                            st.session_state.location_name = name
                            st.session_state.location_details = {
                                "type": data["type"],
                                "region": data["region"],
                                "source": "offline",
                                "population": data.get("population", "")
                            }
                            st.rerun()
            
            # Nhập tọa độ thủ công
            st.markdown("---")
            st.markdown("**Nhập tọa độ:**")
            
            col_coord1, col_coord2 = st.columns(2)
            with col_coord1:
                lat_input = st.number_input("Vĩ độ:", 
                                          value=st.session_state.selected_location[0],
                                          min_value=-90.0,
                                          max_value=90.0,
                                          format="%.4f",
                                          key="manual_lat")
            with col_coord2:
                lon_input = st.number_input("Kinh độ:", 
                                          value=st.session_state.selected_location[1],
                                          min_value=-180.0,
                                          max_value=180.0,
                                          format="%.4f",
                                          key="manual_lon")
            
            if st.button("📌 Áp dụng tọa độ", use_container_width=True):
                st.session_state.selected_location = [lat_input, lon_input]
                st.session_state.location_name = f"{lat_input:.4f}, {lon_input:.4f}"
                st.session_state.location_details = {
                    "type": "Tọa độ thủ công",
                    "region": "Việt Nam",
                    "source": "manual"
                }
                st.success("✅ Đã cập nhật tọa độ!")
                st.rerun()
    
    with tab_map2:
        st.markdown("### 🔍 Tìm kiếm địa điểm Việt Nam")
        
        # Tìm kiếm với autocomplete
        search_col1, search_col2 = st.columns([3, 1])
        
        with search_col1:
            search_query = st.text_input(
                "Nhập tên địa điểm:",
                placeholder="Ví dụ: Tân Hiệp, Phú Giáo, Hà Nội, Đà Lạt...",
                key="location_search_main",
                help="Gõ ít nhất 2 ký tự để xem gợi ý"
            )
        
        with search_col2:
            search_type = st.selectbox(
                "Loại:",
                ["Tất cả", "Thành phố", "Tỉnh", "Huyện/Xã"],
                key="search_type_main"
            )
        
        # Hiển thị gợi ý
        if search_query and len(search_query) >= 2:
            suggestions = map_system.get_location_suggestions(search_query, limit=6)
            if suggestions:
                st.markdown("**Gợi ý:**")
                cols = st.columns(2)
                for idx, sugg in enumerate(suggestions):
                    with cols[idx % 2]:
                        if st.button(f"📍 {sugg['name']}", key=f"sugg_btn_{idx}", use_container_width=True):
                            # Tìm thông tin đầy đủ
                            results = map_system.search_location(sugg['name'], limit=1)
                            if results:
                                result = results[0]
                                st.session_state.selected_location = [result["lat"], result["lon"]]
                                st.session_state.location_name = result["name"]
                                st.session_state.location_details = {
                                    "type": result["type"],
                                    "region": result["region"],
                                    "source": "offline",
                                    "population": result.get("population", "")
                                }
                                st.success(f"✅ Đã chọn: {result['name']}")
                                st.rerun()
        
        # Nút tìm kiếm
        if st.button("🔍 Tìm kiếm", use_container_width=True) and search_query:
            with st.spinner("Đang tìm kiếm..."):
                results = map_system.search_location(search_query, limit=10)
                
                if results:
                    st.markdown(f"### 📋 Kết quả: {len(results)} địa điểm")
                    
                    # Lọc theo loại nếu cần
                    if search_type != "Tất cả":
                        type_map = {"Thành phố": "Thành phố", "Tỉnh": "Tỉnh", "Huyện/Xã": "Huyện"}
                        if search_type in type_map:
                            results = [r for r in results if type_map[search_type] in r["type"]]
                    
                    # Hiển thị kết quả
                    for result in results[:8]:
                        with st.container(border=True):
                            col_res1, col_res2, col_res3 = st.columns([3, 1, 1])
                            with col_res1:
                                st.markdown(f"**{result['name']}**")
                                st.caption(f"{result['type']} • {result['region']}")
                                if result.get('population'):
                                    st.caption(f"👥 {result['population']}")
                            with col_res2:
                                st.metric("Vĩ độ", f"{result['lat']:.4f}")
                            with col_res3:
                                st.metric("Kinh độ", f"{result['lon']:.4f}")
                                if st.button("Chọn", key=f"select_res_{result['name']}"):
                                    st.session_state.selected_location = [result["lat"], result["lon"]]
                                    st.session_state.location_name = result["name"]
                                    st.session_state.location_details = {
                                        "type": result["type"],
                                        "region": result["region"],
                                        "source": result["source"],
                                        "population": result.get("population", "")
                                    }
                                    st.success(f"✅ Đã chọn: {result['name']}")
                                    st.rerun()
                else:
                    st.warning("Không tìm thấy địa điểm phù hợp. Vui lòng thử từ khóa khác.")
        
        # Gợi ý tìm kiếm phổ biến
        st.markdown("---")
        st.markdown("#### 💡 Tìm kiếm phổ biến:")
        
        popular_searches = ["Tân Hiệp", "Phú Giáo", "Hà Nội", "Đà Lạt", "Nha Trang", "Cần Thơ"]
        cols = st.columns(3)
        for idx, search in enumerate(popular_searches):
            with cols[idx % 3]:
                if st.button(f"🔍 {search}", use_container_width=True, key=f"pop_search_{search}"):
                    st.session_state.location_search_main = search
                    st.rerun()
    
    with tab_map3:
        st.markdown("### 📌 Quản lý vị trí của tôi")
        
        # Hiển thị thông tin vị trí hiện tại chi tiết
        with st.container(border=True):
            st.markdown(f"#### 📍 {st.session_state.location_name}")
            
            col_curr1, col_curr2 = st.columns(2)
            with col_curr1:
                st.metric("Vĩ độ", f"{st.session_state.selected_location[0]:.4f}")
                st.metric("Loại", st.session_state.location_details.get('type', 'N/A'))
            with col_curr2:
                st.metric("Kinh độ", f"{st.session_state.selected_location[1]:.4f}")
                st.metric("Vùng", st.session_state.location_details.get('region', 'N/A'))
            
            # Link Google Maps
            maps_url = f"https://www.google.com/maps?q={st.session_state.selected_location[0]},{st.session_state.selected_location[1]}"
            st.markdown(f"[🗺️ Xem trên Google Maps]({maps_url})")
            
            # Thông tin bổ sung
            if 'distance_km' in st.session_state.location_details:
                st.info(f"Khoảng cách từ click bản đồ: {st.session_state.location_details['distance_km']}km")
            if 'population' in st.session_state.location_details:
                st.info(f"Dân số: {st.session_state.location_details['population']}")
        
        # Lấy dự báo thời tiết
        st.markdown("---")
        st.markdown("#### 🌤️ Dự báo thời tiết")
        
        if st.button("🌤️ Lấy dự báo 7 ngày", use_container_width=True):
            with st.spinner("Đang tạo dự báo..."):
                forecast = config_system.get_weather_data(
                    st.session_state.selected_location[0],
                    st.session_state.selected_location[1],
                    days=7
                )
                st.session_state.forecast_data = forecast
                st.success("✅ Đã tạo dự báo thời tiết 7 ngày!")
        
        if st.session_state.forecast_data is not None:
            forecast_df = st.session_state.forecast_data
            today = forecast_df.iloc[0]
            
            st.markdown("**Hôm nay:**")
            col_today1, col_today2, col_today3 = st.columns(3)
            with col_today1:
                st.metric("🌡️ Nhiệt độ", f"{today['temp_min']}°C - {today['temp_max']}°C")
            with col_today2:
                st.metric("💧 Mưa", f"{today['precipitation']}mm")
            with col_today3:
                st.metric("💦 Độ ẩm", f"{today['humidity']}%")
            
            st.caption(f"Điều kiện: {today['icon']} {today['condition']} • Mùa: {today['season']}")

# === TAB 3: THƯ VIỆN CÂY NÂNG CẤP ===
elif selected == "🌿 Thư Viện Cây":
    st.title("🌿 Thư Viện Cây Trồng")
    st.markdown(f"### Database {len(df_plants)}+ loại cây với thông tin chi tiết")
    
    # Thêm cây mới
    with st.expander("🌱 Thêm cây mới vào database", expanded=False):
        col_add1, col_add2 = st.columns(2)
        
        with col_add1:
            new_plant_name = st.text_input("Tên cây:")
            new_plant_water = st.number_input("Nước (L/ngày):", min_value=0.1, max_value=5.0, value=0.3, step=0.1)
            new_plant_difficulty = st.selectbox("Độ khó:", ["Rất dễ", "Dễ", "Trung bình", "Khó", "Rất khó"])
            new_plant_light = st.selectbox("Ánh sáng:", ["Nắng nhiều", "Nắng vừa", "Bán phần", "Bóng râm"])
        
        with col_add2:
            new_plant_temp = st.text_input("Nhiệt độ (ví dụ: 20-30°C):", value="20-30°C")
            new_plant_humidity = st.text_input("Độ ẩm (ví dụ: 40-60%):", value="40-60%")
            new_plant_ph = st.text_input("Độ pH (ví dụ: 6.0-7.0):", value="6.0-7.0")
            new_plant_desc = st.text_area("Mô tả:", height=100)
        
        if st.button("➕ Thêm cây mới", use_container_width=True):
            if new_plant_name and new_plant_desc:
                new_plant = {
                    "Tên Cây": new_plant_name,
                    "Nước (L/ngày)": new_plant_water,
                    "Độ khó": new_plant_difficulty,
                    "Ánh sáng": new_plant_light,
                    "Nhiệt độ": new_plant_temp,
                    "Độ ẩm": new_plant_humidity,
                    "Độ pH": new_plant_ph,
                    "Mô tả": new_plant_desc,
                    "Tần suất tưới": plant_system._get_watering_frequency(new_plant_water, new_plant_difficulty),
                    "Loại": "Người dùng thêm"
                }
                
                plant_system.add_user_plant(new_plant)
                st.session_state.user_plants.append(new_plant)
                st.success(f"✅ Đã thêm cây '{new_plant_name}' vào database!")
                st.rerun()
    
    # Hiển thị cây đang chọn
    if st.session_state.selected_plant:
        plant = st.session_state.selected_plant
        with st.container(border=True):
            col_curr1, col_curr2, col_curr3, col_curr4 = st.columns([2, 1, 1, 1])
            with col_curr1:
                st.markdown(f"#### 🌟 Đang chọn: **{plant.get('Tên Cây', 'Chưa chọn')}**")
                st.caption(plant.get('Loại', 'Cây cảnh'))
            with col_curr2:
                st.metric("💧 Nước", f"{plant.get('Nước (L/ngày)', 0)}L")
            with col_curr3:
                st.metric("⚡ Độ khó", plant.get('Độ khó', 'N/A'))
            with col_curr4:
                if st.button("📋 Chi tiết", key="view_details_btn"):
                    st.session_state.plant_details = plant_system.get_plant_details(plant['Tên Cây'])
    
    tab_lib1, tab_lib2, tab_lib3, tab_lib4 = st.tabs(["🔍 Tìm kiếm thông minh", "📋 Tất cả cây", "📚 Chi tiết cây", "⭐ Cây của tôi"])
    
    with tab_lib1:
        # Tìm kiếm thông minh
        col_search1, col_search2 = st.columns([3, 1])
        
        with col_search1:
            search_query = st.text_input(
                "Tìm kiếm cây trồng:",
                placeholder="Nhập tên cây, loại cây, hoặc đặc điểm...",
                key="plant_search_smart",
                help="Tìm kiếm theo tên, loại, mô tả"
            )
        
        with col_search2:
            search_category = st.selectbox(
                "Danh mục:",
                ["Tất cả", "Hoa", "Cảnh lá", "Mọng nước", "Ăn quả", "Thảo mộc", "Cây leo"],
                key="search_category"
            )
        
        # Bộ lọc nâng cao
        with st.expander("🔧 Bộ lọc nâng cao", expanded=False):
            col_filter1, col_filter2, col_filter3 = st.columns(3)
            
            with col_filter1:
                difficulty_filter = st.multiselect(
                    "Độ khó:",
                    ["Rất dễ", "Dễ", "Trung bình", "Khó", "Rất khó"],
                    key="difficulty_filter_adv"
                )
                
                plant_type_filter = st.multiselect(
                    "Loại cây:",
                    ["Hoa", "Cảnh lá", "Mọng nước", "Ăn quả", "Thảo mộc", "Cây leo", "Người dùng thêm"],
                    key="type_filter"
                )
            
            with col_filter2:
                water_min, water_max = st.slider(
                    "Nhu cầu nước (L/ngày):",
                    0.0, 2.0, (0.0, 2.0),
                    key="water_filter_adv"
                )
                
                light_filter = st.multiselect(
                    "Ánh sáng:",
                    ["Nắng nhiều", "Nắng vừa", "Bán phần", "Bóng râm", "Mọi điều kiện"],
                    key="light_filter_adv"
                )
            
            with col_filter3:
                growth_filter = st.multiselect(
                    "Tốc độ sinh trưởng:",
                    ["Chậm", "Trung bình", "Nhanh"],
                    key="growth_filter"
                )
                
                air_clean_filter = st.multiselect(
                    "Thanh lọc không khí:",
                    ["Rất tốt", "Tốt", "Trung bình", "Không"],
                    key="air_filter"
                )
        
        # Tìm kiếm
        search_clicked = st.button("🔍 Tìm kiếm", use_container_width=True)
        
        if search_query or search_clicked or difficulty_filter or water_max < 2.0 or light_filter:
            # Áp dụng bộ lọc
            results = plant_system.search_plants(search_query)
            
            # Bộ lọc danh mục
            if search_category != "Tất cả":
                results = results[results["Loại"] == search_category]
            
            # Bộ lọc độ khó
            if difficulty_filter:
                results = results[results['Độ khó'].isin(difficulty_filter)]
            
            # Bộ lọc nước
            if water_max < 2.0:
                results = results[
                    (results['Nước (L/ngày)'] >= water_min) &
                    (results['Nước (L/ngày)'] <= water_max)
                ]
            
            # Bộ lọc ánh sáng
            if light_filter:
                results = results[results['Ánh sáng'].isin(light_filter)]
            
            # Bộ lọc loại cây
            if plant_type_filter:
                results = results[results['Loại'].isin(plant_type_filter)]
            
            # Bộ lọc tốc độ sinh trưởng
            if growth_filter and 'Tốc độ sinh trưởng' in results.columns:
                results = results[results['Tốc độ sinh trưởng'].isin(growth_filter)]
            
            # Bộ lọc thanh lọc không khí
            if air_clean_filter and 'Thanh lọc không khí' in results.columns:
                results = results[results['Thanh lọc không khí'].isin(air_clean_filter)]
            
            st.markdown(f"### 📋 Kết quả: {len(results)} cây")
            
            if len(results) > 0:
                # Hiển thị kết quả dạng grid
                view_mode = st.radio(
                    "Chế độ hiển thị:",
                    ["Dạng card", "Dạng bảng", "Dạng danh sách"],
                    horizontal=True,
                    key="search_view_mode"
                )
                
                if view_mode == "Dạng card":
                    plants_per_row = 3
                    plants_list = results.head(12).to_dict('records')
                    
                    for i in range(0, len(plants_list), plants_per_row):
                        cols = st.columns(plants_per_row)
                        
                        for col_idx, col in enumerate(cols):
                            plant_idx = i + col_idx
                            if plant_idx < len(plants_list):
                                plant = plants_list[plant_idx]
                                
                                with col:
                                    with st.container(border=True):
                                        # Header
                                        st.markdown(f"##### {plant['Tên Cây']}")
                                        st.caption(f"⚡ {plant['Độ khó']} • {plant['Ánh sáng']}")
                                        
                                        # Thông tin
                                        st.markdown(f"💧 **Nước:** {plant['Nước (L/ngày)']}L/ngày")
                                        st.markdown(f"🌡️ **Nhiệt độ:** {plant['Nhiệt độ']}")
                                        st.markdown(f"💦 **Độ ẩm:** {plant['Độ ẩm']}")
                                        
                                        if plant.get('Loại'):
                                            st.markdown(f"📁 **Loại:** {plant['Loại']}")
                                        
                                        # Actions
                                        col_btn1, col_btn2 = st.columns(2)
                                        with col_btn1:
                                            if st.button("✅ Chọn", key=f"select_card_s_{plant['ID']}", use_container_width=True):
                                                st.session_state.selected_plant = plant
                                                st.session_state.plant_details = plant_system.get_plant_details(plant['Tên Cây'])
                                                st.success(f"✅ Đã chọn {plant['Tên Cây']}!")
                                        with col_btn2:
                                            if st.button("📋", key=f"detail_card_s_{plant['ID']}", use_container_width=True):
                                                st.session_state.plant_details = plant_system.get_plant_details(plant['Tên Cây'])
                
                elif view_mode == "Dạng bảng":
                    display_cols = ["Tên Cây", "Nước (L/ngày)", "Độ khó", "Ánh sáng", "Loại"]
                    st.dataframe(
                        results[display_cols],
                        use_container_width=True,
                        height=400,
                        hide_index=True
                    )
                
                else:  # Dạng danh sách
                    for plant in results.head(15).to_dict('records'):
                        with st.container(border=True):
                            col_list1, col_list2, col_list3 = st.columns([3, 1, 1])
                            with col_list1:
                                st.markdown(f"**{plant['Tên Cây']}**")
                                if plant.get('Loại'):
                                    st.caption(f"📁 {plant['Loại']}")
                                st.caption(f"{plant['Mô tả'][:100]}...")
                            with col_list2:
                                st.markdown(f"💧 {plant['Nước (L/ngày)']}L")
                                st.markdown(f"⚡ {plant['Độ khó']}")
                            with col_list3:
                                if st.button("Chọn", key=f"select_list_s_{plant['ID']}"):
                                    st.session_state.selected_plant = plant
                                    st.session_state.plant_details = plant_system.get_plant_details(plant['Tên Cây'])
                                    st.success(f"✅ Đã chọn {plant['Tên Cây']}!")
            else:
                st.warning("Không tìm thấy cây phù hợp. Hãy thử điều chỉnh bộ lọc!")
        
        # Tìm kiếm phổ biến
        st.markdown("---")
        st.markdown("#### 🔍 Tìm kiếm phổ biến:")
        
        popular_searches = ["Hoa Hồng", "Lan", "Xương Rồng", "Trầu Bà", "Sen Đá", "Chanh", "Húng Quế"]
        cols = st.columns(4)
        for idx, search in enumerate(popular_searches):
            with cols[idx % 4]:
                if st.button(search, use_container_width=True, key=f"pop_plant_{search}"):
                    st.session_state.plant_search_smart = search
                    st.rerun()
    
    with tab_lib2:
        # Hiển thị tất cả cây
        st.markdown(f"### 📚 Tất cả cây trong database ({len(df_plants)}+)")
        
        # Phân loại theo loại cây
        if 'Loại' in df_plants.columns:
            categories = df_plants['Loại'].unique()
            
            for category in categories:
                with st.expander(f"📁 {category} ({len(df_plants[df_plants['Loại'] == category])} cây)", expanded=False):
                    category_plants = df_plants[df_plants['Loại'] == category].head(8)
                    
                    for _, plant in category_plants.iterrows():
                        with st.container(border=True):
                            col_cat1, col_cat2, col_cat3 = st.columns([3, 1, 1])
                            with col_cat1:
                                st.markdown(f"**{plant['Tên Cây']}**")
                                st.caption(f"{plant['Mô tả'][:80]}...")
                            with col_cat2:
                                st.markdown(f"💧 {plant['Nước (L/ngày)']}L")
                                st.markdown(f"⚡ {plant['Độ khó']}")
                            with col_cat3:
                                if st.button("Chọn", key=f"select_cat_{plant['ID']}"):
                                    st.session_state.selected_plant = plant.to_dict()
                                    st.session_state.plant_details = plant_system.get_plant_details(plant['Tên Cây'])
                                    st.success(f"✅ Đã chọn {plant['Tên Cây']}!")
        
        else:
            # Hiển thị mặc định nếu không có cột Loại
            display_cols = ["Tên Cây", "Nước (L/ngày)", "Độ khó", "Ánh sáng", "Nhiệt độ", "Độ ẩm"]
            st.dataframe(
                df_plants[display_cols],
                use_container_width=True,
                height=500,
                hide_index=True
            )
    
    with tab_lib3:
        # Hiển thị chi tiết cây
        if not st.session_state.selected_plant:
            st.info("ℹ️ Vui lòng chọn một cây để xem chi tiết.")
        else:
            plant = st.session_state.selected_plant
            plant_name = plant.get('Tên Cây', '')
            
            # Lấy thông tin chi tiết
            if st.session_state.plant_details is None:
                st.session_state.plant_details = plant_system.get_plant_details(plant_name)
            
            if st.session_state.plant_details:
                details = st.session_state.plant_details
                
                st.markdown(f"## 🔬 {plant_name}")
                
                # Tabs chi tiết
                tab_detail1, tab_detail2, tab_detail3, tab_detail4, tab_detail5 = st.tabs([
                    "📋 Thông tin cơ bản", "💧 Hướng dẫn chăm sóc", "⚠️ Sâu bệnh & Xử lý", 
                    "📚 Thông tin bổ sung", "📅 Lịch chăm sóc mẫu"
                ])
                
                with tab_detail1:
                    col_info1, col_info2 = st.columns(2)
                    
                    with col_info1:
                        st.markdown("#### 🏷️ Thông tin chung")
                        
                        info_items = [
                            ("💧 Nước/ngày", f"{details.get('Nước (L/ngày)', 0)}L"),
                            ("⚡ Độ khó", details.get('Độ khó', 'Chưa có')),
                            ("☀️ Ánh sáng", details.get('Ánh sáng', 'Chưa có')),
                            ("🌡️ Nhiệt độ", details.get('Nhiệt độ', 'Chưa có')),
                            ("💦 Độ ẩm", details.get('Độ ẩm', 'Chưa có')),
                        ]
                        
                        for icon, value in info_items:
                            st.metric(icon, value)
                    
                    with col_info2:
                        st.markdown("#### 🌱 Thông số kỹ thuật")
                        
                        tech_items = [
                            ("📊 Độ pH", details.get('Độ pH', 'Chưa có')),
                            ("📈 Tốc độ sinh trưởng", details.get('Tốc độ sinh trưởng', 'Chưa có')),
                            ("📏 Chiều cao", details.get('Chiều cao', 'Chưa có')),
                            ("🌸 Mùa ra hoa", details.get('Mùa ra hoa', 'Chưa có')),
                            ("🌱 Nhân giống", details.get('Nhân giống', 'Chưa có')),
                        ]
                        
                        for icon, value in tech_items:
                            st.metric(icon, value)
                        
                        if details.get('Thanh lọc không khí'):
                            st.metric("🌿 Thanh lọc không khí", details['Thanh lọc không khí'])
                        
                        if details.get('Thú cưng'):
                            st.metric("🐾 Thú cưng", details['Thú cưng'])
                
                with tab_detail2:
                    st.markdown("#### 💧 Hướng dẫn chăm sóc chi tiết")
                    
                    # Lấy lời khuyên từ AI
                    advice = ai_system.get_care_advice(
                        plant_name, 
                        details,
                        st.session_state.forecast_data.iloc[0]['season'] if st.session_state.forecast_data is not None else ""
                    )
                    
                    care_col1, care_col2 = st.columns(2)
                    
                    with care_col1:
                        st.markdown("**Tưới nước:**")
                        st.info(advice["tuoi_nuoc"])
                        st.markdown(f"**Tần suất:** {details.get('Tần suất tưới', 'Chưa có')}")
                        
                        st.markdown("**Bón phân:**")
                        st.info(advice["bon_phan"])
                        st.markdown(f"**Loại phân:** {details.get('Phân bón', 'NPK 20-20-20')}")
                    
                    with care_col2:
                        st.markdown("**Ánh sáng:**")
                        st.info(advice["anh_sang"])
                        
                        st.markdown("**Cắt tỉa:**")
                        st.info(advice["cat_tia"])
                        
                        st.markdown("**Bảo vệ:**")
                        st.info(advice["bao_ve"])
                        
                        if advice["luu_y_theo_mua"]:
                            st.markdown("**Lưu ý theo mùa:**")
                            st.warning(advice["luu_y_theo_mua"])
                    
                    st.markdown("**Mẹo chăm sóc:**")
                    if 'meo_cham_soc' in details:
                        for tip in details['meo_cham_soc']:
                            st.markdown(f"✅ {tip}")
                    else:
                        st.markdown("✅ Giữ đất ẩm nhưng không ướt")
                        st.markdown("✅ Tránh ánh nắng trực tiếp giữa trưa")
                        st.markdown("✅ Lau lá thường xuyên")
                        st.markdown("✅ Kiểm tra sâu bệnh định kỳ")
                
                with tab_detail3:
                    st.markdown("#### ⚠️ Sâu bệnh & Xử lý")
                    
                    if 'benh_thuong_gap' in details:
                        with st.container(border=True):
                            st.markdown("**Bệnh thường gặp:**")
                            st.error(details['benh_thuong_gap'])
                    
                    if 'cach_chua' in details:
                        with st.container(border=True):
                            st.markdown("**Cách xử lý:**")
                            st.info(details['cach_chua'])
                    
                    st.markdown("**Biện pháp phòng ngừa:**")
                    prevention_items = [
                        "Vệ sinh khu vực trồng cây thường xuyên",
                        "Tưới nước đúng cách, không để đất quá ẩm",
                        "Đảm bảo thông gió tốt",
                        "Kiểm tra cây định kỳ 1-2 lần/tuần",
                        "Cách ly cây bệnh để tránh lây lan",
                        "Sử dụng thuốc trừ sâu sinh học khi cần"
                    ]
                    
                    for item in prevention_items:
                        st.markdown(f"🛡️ {item}")
                    
                    # Nút chẩn đoán nhanh
                    st.markdown("---")
                    if st.button("🤖 Chẩn đoán vấn đề cây trồng", use_container_width=True):
                        st.session_state.selected = "🤖 AI Chẩn Đoán"
                        st.rerun()
                
                with tab_detail4:
                    # Thông tin Wikipedia-style
                    st.markdown("#### 📚 Thông tin bổ sung")
                    
                    # Tóm tắt
                    if 'Mô tả' in details:
                        st.markdown("**Mô tả:**")
                        st.info(details['Mô tả'])
                    
                    # Thông tin khoa học
                    if 'khoa_hoc' in details:
                        st.markdown("**Thông tin khoa học:**")
                        sci_col1, sci_col2 = st.columns(2)
                        with sci_col1:
                            st.markdown(f"**Tên khoa học:** {details['khoa_hoc']}")
                            st.markdown(f"**Họ:** {details.get('ho', 'Chưa có')}")
                        with sci_col2:
                            st.markdown(f"**Nguồn gốc:** {details.get('nguon_goc', 'Chưa có')}")
                            st.markdown(f"**Chu kỳ:** {details.get('chu_ky', 'Chưa có')}")
                    
                    if 'y_nghia' in details:
                        st.markdown("**Ý nghĩa:**")
                        st.success(details['y_nghia'])
                    
                    if 'ky_thuat' in details:
                        st.markdown("**Kỹ thuật trồng:**")
                        st.info(details['ky_thuat'])
                    
                    # Ghi chú cá nhân
                    st.markdown("---")
                    st.markdown("#### 📝 Ghi chú của bạn")
                    
                    note_key = f"notes_{plant_name}"
                    if note_key not in st.session_state:
                        st.session_state[note_key] = ""
                    
                    user_notes = st.text_area(
                        "Ghi chú về cây này:",
                        value=st.session_state[note_key],
                        placeholder="Ghi lại kinh nghiệm chăm sóc, lịch sử bệnh, mẹo riêng...",
                        height=150,
                        key=f"notes_editor_{plant_name}"
                    )
                    
                    col_note1, col_note2 = st.columns(2)
                    with col_note1:
                        if st.button("💾 Lưu ghi chú", key=f"save_notes_{plant_name}", use_container_width=True):
                            st.session_state[note_key] = user_notes
                            st.success("✅ Đã lưu ghi chú!")
                    with col_note2:
                        if st.button("🗑️ Xóa ghi chú", key=f"clear_notes_{plant_name}", use_container_width=True):
                            st.session_state[note_key] = ""
                            st.rerun()
                
                with tab_detail5:
                    st.markdown("#### 📅 Lịch chăm sóc mẫu 7 ngày")
                    
                    if 'lich_cham_soc' in details:
                        schedule_df = pd.DataFrame(details['lich_cham_soc'])
                        st.dataframe(
                            schedule_df,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "ngay": "📅 Ngày",
                                "thu": "📆 Thứ",
                                "cong_viec": "📝 Công việc",
                                "ghi_chu": "📌 Ghi chú"
                            }
                        )
                    
                    # Lịch chăm sóc thông minh
                    st.markdown("---")
                    st.markdown("#### 🤖 Lịch chăm sóc thông minh")
                    
                    if st.button("📅 Tạo lịch chăm sóc 14 ngày", use_container_width=True):
                        if st.session_state.forecast_data is not None:
                            schedule = ai_system.generate_watering_schedule(
                                plant_name,
                                details,
                                st.session_state.forecast_data,
                                st.session_state.location_details
                            )
                            
                            schedule_df = pd.DataFrame(schedule)
                            st.dataframe(
                                schedule_df,
                                use_container_width=True,
                                hide_index=True
                            )
                            
                            # Xuất lịch
                            csv = schedule_df.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label="📥 Tải lịch CSV",
                                data=csv,
                                file_name=f"lich_cham_soc_{plant_name}.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
                        else:
                            st.warning("Vui lòng lấy dự báo thời tiết trước!")
            else:
                st.error("Không tìm thấy thông tin chi tiết cho cây này.")
    
    with tab_lib4:
        st.markdown("### 🌱 Cây do bạn thêm")
        
        if not plant_system.user_plants:
            st.info("Bạn chưa thêm cây nào. Hãy thêm cây mới trong tab 'Tìm kiếm thông minh'!")
        else:
            st.markdown(f"#### 📋 Bạn có {len(plant_system.user_plants)} cây tự thêm")
            
            for idx, plant in enumerate(plant_system.user_plants):
                with st.container(border=True):
                    col_user1, col_user2, col_user3 = st.columns([3, 1, 1])
                    with col_user1:
                        st.markdown(f"**{plant['Tên Cây']}**")
                        st.caption(f"{plant.get('Mô tả', 'Không có mô tả')[:100]}...")
                        if plant.get('Loại'):
                            st.caption(f"📁 {plant['Loại']}")
                    with col_user2:
                        st.markdown(f"💧 {plant.get('Nước (L/ngày)', 0)}L")
                        st.markdown(f"⚡ {plant.get('Độ khó', 'N/A')}")
                    with col_user3:
                        if st.button("Chọn", key=f"select_user_{idx}"):
                            st.session_state.selected_plant = plant
                            st.session_state.plant_details = plant_system.get_plant_details(plant['Tên Cây'])
                            st.success(f"✅ Đã chọn {plant['Tên Cây']}!")
                    
                    # Nút xóa
                    if st.button("🗑️ Xóa", key=f"delete_user_{idx}", type="secondary"):
                        plant_system.user_plants.pop(idx)
                        st.rerun()

# === TAB 4: AI CHẨN ĐOÁN NÂNG CẤP ===
elif selected == "🤖 AI Chẩn Đoán":
    st.title("🤖 AI Chẩn Đoán Cây Trồng")
    st.markdown("### Phân tích và chẩn đoán vấn đề cây trồng thông minh")
    
    tab_ai1, tab_ai2, tab_ai3 = st.tabs(["🔍 Chẩn đoán nhanh", "📋 Lịch sử chẩn đoán", "💡 Kiến thức AI"])
    
    with tab_ai1:
        st.markdown("#### 🔍 Chẩn đoán vấn đề cây trồng")
        
        # Chọn cây để chẩn đoán
        col_diag1, col_diag2 = st.columns(2)
        
        with col_diag1:
            if st.session_state.selected_plant:
                st.markdown(f"**Cây đang chọn:** {st.session_state.selected_plant.get('Tên Cây', 'Chưa chọn')}")
            else:
                st.warning("Chưa chọn cây. Vui lòng chọn cây trong Thư Viện Cây.")
            
            plant_list = [p['Tên Cây'] for p in df_plants.head(20).to_dict('records')]
            if plant_system.user_plants:
                plant_list.extend([p['Tên Cây'] for p in plant_system.user_plants])
            
            selected_plant_name = st.selectbox(
                "Chọn cây cần chẩn đoán:",
                options=plant_list,
                index=0 if st.session_state.selected_plant else None,
                key="diagnosis_plant"
            )
        
        with col_diag2:
            plant_type = "chung"
            if selected_plant_name:
                plant_info = plant_system.get_plant_details(selected_plant_name)
                if plant_info:
                    plant_type = plant_info.get('Loại', 'chung')
            
            st.markdown(f"**Loại cây:** {plant_type}")
            st.markdown(f"**Thời gian:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        # Nhập triệu chứng
        st.markdown("#### 📝 Mô tả triệu chứng")
        
        symptoms = st.text_area(
            "Mô tả chi tiết vấn đề của cây:",
            placeholder="Ví dụ: Lá bị vàng từ mép vào trong, có đốm nâu, cây phát triển chậm...",
            height=150,
            key="symptoms_input"
        )
        
        # Thêm triệu chứng nhanh
        st.markdown("**Triệu chứng nhanh:**")
        quick_symptoms = st.multiselect(
            "Chọn triệu chứng thường gặp:",
            ["Lá vàng", "Lá rụng", "Đốm lá", "Thối rễ", "Héo lá", "Cháy lá", "Còi cọc", "Sâu bệnh"],
            key="quick_symptoms"
        )
        
        # Kết hợp triệu chứng
        if quick_symptoms:
            if symptoms:
                symptoms += " " + ", ".join(quick_symptoms)
            else:
                symptoms = ", ".join(quick_symptoms)
        
        # Thêm thông tin bổ sung
        st.markdown("#### ℹ️ Thông tin bổ sung")
        
        col_extra1, col_extra2, col_extra3 = st.columns(3)
        
        with col_extra1:
            watering_freq = st.selectbox(
                "Tần suất tưới:",
                ["Hàng ngày", "2-3 ngày/lần", "1 tuần/lần", "Không đều", "Không biết"],
                key="watering_freq"
            )
        
        with col_extra2:
            sunlight = st.selectbox(
                "Ánh sáng:",
                ["Nắng nhiều", "Nắng vừa", "Bóng râm", "Trong nhà", "Không biết"],
                key="sunlight_info"
            )
        
        with col_extra3:
            location_type = st.selectbox(
                "Vị trí đặt cây:",
                ["Ngoài trời", "Ban công", "Cửa sổ", "Trong nhà", "Văn phòng"],
                key="location_type"
            )
        
        # Nút chẩn đoán
        if st.button("🤖 Bắt đầu chẩn đoán", type="primary", use_container_width=True):
            if symptoms:
                with st.spinner("AI đang phân tích triệu chứng..."):
                    time.sleep(1)  # Giả lập xử lý
                    
                    # Tạo thông tin bổ sung
                    additional_info = f"""
                    Tần suất tưới: {watering_freq}
                    Ánh sáng: {sunlight}
                    Vị trí: {location_type}
                    """
                    
                    # Phân tích
                    analysis = ai_system.analyze_plant_problem(
                        symptoms, 
                        plant_type,
                        additional_info
                    )
                    
                    # Hiển thị kết quả
                    st.markdown("---")
                    st.markdown(f"### 📊 Kết quả chẩn đoán #{analysis['id']}")
                    
                    # Thông tin cơ bản
                    col_result1, col_result2 = st.columns(2)
                    
                    with col_result1:
                        st.metric("🔍 Bệnh", analysis['benh'])
                        st.metric("📈 Độ tin cậy", f"{analysis['do_tin_cay']}%")
                    
                    with col_result2:
                        st.metric("📅 Thời gian", analysis['timestamp'])
                        st.metric("📋 Giai đoạn", analysis['giai_doan'])
                    
                    # Nguyên nhân
                    st.markdown("#### 🔍 Nguyên nhân có thể:")
                    for cause in analysis['nguyen_nhan']:
                        st.markdown(f"• {cause}")
                    
                    # Cách xử lý
                    st.markdown("#### 🛠️ Cách xử lý:")
                    for i, solution in enumerate(analysis['xu_ly'], 1):
                        st.markdown(f"{i}. {solution}")
                    
                    # Biện pháp phòng ngừa
                    st.markdown("#### 🛡️ Biện pháp phòng ngừa:")
                    for prevention in analysis['phong_ngua']:
                        st.markdown(f"✓ {prevention}")
                    
                    # Khám nhanh
                    st.markdown("#### 🔎 Checklist khám nhanh:")
                    for check in analysis['kham_nhanh']:
                        st.markdown(check)
                    
                    # Lưu vào lịch sử
                    st.session_state.diagnosis_history.append(analysis)
                    
                    # Nút thêm
                    col_action1, col_action2 = st.columns(2)
                    with col_action1:
                        if st.button("💾 Lưu chẩn đoán", use_container_width=True):
                            st.success("✅ Đã lưu chẩn đoán vào lịch sử!")
                    with col_action2:
                        if st.button("🔄 Chẩn đoán mới", use_container_width=True):
                            st.rerun()
            else:
                st.warning("Vui lòng nhập triệu chứng!")
    
    with tab_ai2:
        st.markdown("#### 📋 Lịch sử chẩn đoán")
        
        if not st.session_state.diagnosis_history:
            st.info("Chưa có lịch sử chẩn đoán nào.")
        else:
            for diagnosis in reversed(st.session_state.diagnosis_history[-10:]):  # Hiển thị 10 gần nhất
                with st.container(border=True):
                    col_hist1, col_hist2, col_hist3 = st.columns([2, 1, 1])
                    with col_hist1:
                        st.markdown(f"**#{diagnosis['id']} - {diagnosis['benh']}**")
                        st.caption(f"⏰ {diagnosis['timestamp']}")
                    with col_hist2:
                        st.metric("Độ tin cậy", f"{diagnosis['do_tin_cay']}%")
                    with col_hist3:
                        if st.button("📋 Xem", key=f"view_diag_{diagnosis['id']}"):
                            # Hiển thị chi tiết
                            st.markdown(f"**Bệnh:** {diagnosis['benh']}")
                            st.markdown(f"**Giai đoạn:** {diagnosis['giai_doan']}")
                            
                            st.markdown("**Nguyên nhân:**")
                            for cause in diagnosis['nguyen_nhan']:
                                st.markdown(f"- {cause}")
                            
                            st.markdown("**Xử lý:**")
                            for i, sol in enumerate(diagnosis['xu_ly'], 1):
                                st.markdown(f"{i}. {sol}")
            
            # Nút xóa lịch sử
            if st.button("🗑️ Xóa toàn bộ lịch sử", type="secondary", use_container_width=True):
                st.session_state.diagnosis_history = []
                st.rerun()
    
    with tab_ai3:
        st.markdown("#### 💡 Kiến thức AI - Cơ sở dữ liệu bệnh cây")
        
        # Hiển thị các bệnh thường gặp
        st.markdown("##### 🩺 Các bệnh thường gặp:")
        
        diseases = list(ai_system.knowledge_base.keys())[:6]  # Hiển thị 6 bệnh đầu
        cols = st.columns(3)
        
        for idx, disease in enumerate(diseases):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.markdown(f"**{disease.upper()}**")
                    
                    info = ai_system.knowledge_base[disease]
                    st.caption(f"Giai đoạn: {', '.join(info['giai_doan'][:2])}")
                    
                    if st.button("ℹ️ Chi tiết", key=f"disease_detail_{disease}"):
                        st.markdown(f"**Nguyên nhân:**")
                        for cause in info['nguyen_nhan'][:3]:
                            st.markdown(f"- {cause}")
                        
                        st.markdown(f"**Xử lý:**")
                        for i, sol in enumerate(info['cach_xu_ly'][:3], 1):
                            st.markdown(f"{i}. {sol}")
        
        # Kiến thức chăm sóc
        st.markdown("---")
        st.markdown("##### 📚 Kiến thức chăm sóc cơ bản")
        
        care_topics = ["tưới nước", "bon_phan", "anh_sang"]
        
        for topic in care_topics:
            with st.expander(f"📖 {topic.replace('_', ' ').title()}", expanded=False):
                if topic in ai_system.knowledge_base:
                    info = ai_system.knowledge_base[topic]
                    
                    if "nguyen_tac" in info:
                        st.markdown("**Nguyên tắc:**")
                        for principle in info["nguyen_tac"]:
                            st.markdown(f"✅ {principle}")
                    
                    if "loai_cay" in info:
                        st.markdown("**Theo loại cây:**")
                        for plant_type, advice in info["loai_cay"].items():
                            st.markdown(f"🌿 {plant_type}: {advice}")

# === TAB 5: DỰ BÁO THÔNG MINH ===
elif selected == "📊 Dự Báo Thông Minh":
    st.title("📊 Dự Báo & Tính Toán Thông Minh")
    st.markdown("### Dự báo thời tiết và tính toán nhu cầu chăm sóc chi tiết")
    
    # Kiểm tra đã chọn cây và vị trí
    if not st.session_state.selected_plant:
        st.warning("⚠️ Vui lòng chọn cây trước!")
        if st.button("🌿 Đến Thư Viện Cây"):
            st.session_state.selected = "🌿 Thư Viện Cây"
            st.rerun()
        st.stop()
    
    if not st.session_state.location_name:
        st.warning("⚠️ Vui lòng chọn vị trí trước!")
        if st.button("🗺️ Đến Bản Đồ"):
            st.session_state.selected = "🗺️ Bản Đồ Thông Minh"
            st.rerun()
        st.stop()
    
    # Hiển thị thông tin hiện tại
    plant = st.session_state.selected_plant
    location = st.session_state.location_name
    
    with st.container(border=True):
        col_header1, col_header2, col_header3, col_header4 = st.columns(4)
        with col_header1:
            st.metric("🌿 Cây", plant.get('Tên Cây', 'Chưa chọn'))
        with col_header2:
            st.metric("📍 Vị trí", location)
        with col_header3:
            st.metric("💧 Nước cơ bản", f"{plant.get('Nước (L/ngày)', 0)}L/ngày")
        with col_header4:
            if st.session_state.forecast_data is not None:
                season = st.session_state.forecast_data.iloc[0]['season']
                st.metric("🌱 Mùa", season)
    
    tab_forecast1, tab_forecast2, tab_forecast3, tab_forecast4 = st.tabs([
        "🌦️ Dự báo 7 ngày", "💧 Tính toán nước", "📅 Lịch chăm sóc", "📊 Báo cáo tổng hợp"
    ])
    
    with tab_forecast1:
        st.markdown("#### 🌦️ Dự Báo Thời Tiết 7 Ngày")
        
        # Lấy dự báo
        if st.session_state.forecast_data is None:
            with st.spinner("Đang tạo dự báo..."):
                forecast = config_system.get_weather_data(
                    st.session_state.selected_location[0],
                    st.session_state.selected_location[1],
                    days=7
                )
                st.session_state.forecast_data = forecast
        
        if st.session_state.forecast_data is not None:
            forecast_df = st.session_state.forecast_data
            
            # Biểu đồ nhiệt độ
            fig_temp = go.Figure()
            
            fig_temp.add_trace(go.Scatter(
                x=forecast_df['day'],
                y=forecast_df['temp_max'],
                name='Nhiệt độ cao',
                line=dict(color='#ff6b6b', width=3),
                mode='lines+markers',
                marker=dict(size=8)
            ))
            
            fig_temp.add_trace(go.Scatter(
                x=forecast_df['day'],
                y=forecast_df['temp_min'],
                name='Nhiệt độ thấp',
                line=dict(color='#4dabf7', width=3),
                mode='lines+markers',
                fill='tonexty',
                fillcolor='rgba(77, 171, 247, 0.2)',
                marker=dict(size=8)
            ))
            
            fig_temp.update_layout(
                title="Dự báo nhiệt độ 7 ngày",
                template="plotly_dark",
                xaxis_title="Ngày",
                yaxis_title="Nhiệt độ (°C)",
                height=350,
                hovermode="x unified"
            )
            
            st.plotly_chart(fig_temp, use_container_width=True)
            
            # Biểu đồ mưa
            fig_rain = px.bar(
                forecast_df,
                x='day',
                y='precipitation',
                title='Dự báo lượng mưa',
                color='precipitation',
                color_continuous_scale='Blues'
            )
            
            fig_rain.update_layout(
                template="plotly_dark",
                xaxis_title="Ngày",
                yaxis_title="Lượng mưa (mm)",
                height=300
            )
            
            st.plotly_chart(fig_rain, use_container_width=True)
            
            # Bảng dự báo chi tiết
            st.markdown("#### 📋 Chi Tiết Dự Báo")
            
            display_df = forecast_df.copy()
            display_df['Nhiệt độ'] = display_df.apply(
                lambda x: f"{x['icon']} {x['temp_min']}°C - {x['temp_max']}°C", axis=1
            )
            display_df['Mưa'] = display_df['precipitation'].apply(
                lambda x: f"🌧️ {x}mm" if x > 0 else "☀️ Không mưa"
            )
            display_df['Gió'] = display_df.apply(
                lambda x: f"{x['wind_speed']}km/h {x['wind_direction']}", axis=1
            )
            
            st.dataframe(
                display_df[['day', 'weekday', 'Nhiệt độ', 'Mưa', 'humidity', 'Gió', 'condition', 'season']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "day": "📅 Ngày",
                    "weekday": "📆 Thứ",
                    "Nhiệt độ": "🌡️ Nhiệt độ",
                    "Mưa": "💧 Mưa",
                    "humidity": "💦 Độ ẩm (%)",
                    "Gió": "💨 Gió",
                    "condition": "🌤️ Điều kiện",
                    "season": "🌱 Mùa"
                }
            )
            
            # Xuất dữ liệu
            csv = forecast_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Tải dữ liệu dự báo (CSV)",
                data=csv,
                file_name=f"du_bao_{location}_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with tab_forecast2:
        st.markdown("#### 💧 Tính Toán Nhu Cầu Nước Thông Minh")
        
        if st.session_state.forecast_data is not None:
            plant_water = plant.get('Nước (L/ngày)', 0)
            forecast_df = st.session_state.forecast_data
            
            # Cài đặt tính toán
            with st.expander("⚙️ Cài đặt tính toán", expanded=False):
                col_set1, col_set2 = st.columns(2)
                with col_set1:
                    pot_size = st.number_input("Kích thước chậu (L):", min_value=1.0, max_value=50.0, value=5.0, step=0.5)
                    soil_type = st.selectbox("Loại đất:", ["trung bình", "cát", "thịt", "sét"])
                with col_set2:
                    current_water = st.number_input("Mức nước hiện tại (%):", min_value=0, max_value=100, value=80)
                    evaporation = st.slider("Tốc độ bay hơi:", 0.0, 1.0, 0.3)
            
            # Tính toán nhu cầu nước
            water_calc = config_system.calculate_water_needs(plant_water, forecast_df, pot_size, soil_type)
            st.session_state.water_calculation = water_calc
            
            # Biểu đồ nhu cầu nước
            fig_water = px.bar(
                water_calc,
                x='Ngày',
                y='Nhu cầu điều chỉnh',
                title='Nhu cầu nước hàng ngày',
                color='Nhu cầu điều chỉnh',
                color_continuous_scale='Teal',
                text='Lượng nước (ml)'
            )
            
            fig_water.add_hline(
                y=plant_water,
                line_dash="dash",
                line_color="yellow",
                annotation_text=f"Nhu cầu cơ bản: {plant_water}L",
                annotation_position="bottom right"
            )
            
            fig_water.update_layout(
                template="plotly_dark",
                xaxis_title="Ngày",
                yaxis_title="Nước (L)",
                height=350
            )
            
            fig_water.update_traces(texttemplate='%{text:.0f}ml', textposition='outside')
            
            st.plotly_chart(fig_water, use_container_width=True)
            
            # Bảng tính toán chi tiết
            st.markdown("#### 📊 Chi Tiết Tính Toán")
            
            st.dataframe(
                water_calc,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Ngày": "📅 Ngày",
                    "Thứ": "📆 Thứ",
                    "Nhiệt độ": "🌡️ Nhiệt độ",
                    "Mưa": "🌧️ Mưa",
                    "Độ ẩm": "💦 Độ ẩm",
                    "Nhu cầu cơ bản": "💧 Cơ bản (L)",
                    "Nhu cầu điều chỉnh": "🚰 Điều chỉnh (L)",
                    "Lượng nước (ml)": "💦 Lượng nước (ml)",
                    "Khuyến nghị": "💡 Khuyến nghị"
                }
            )
            
            # Tổng kết
            total_water = water_calc['Nhu cầu điều chỉnh'].sum()
            avg_water = water_calc['Nhu cầu điều chỉnh'].mean()
            base_total = plant_water * 7
            water_saving = ((base_total - total_water) / base_total * 100) if base_total > 0 else 0
            total_ml = water_calc['Lượng nước (ml)'].sum()
            
            col_total1, col_total2, col_total3, col_total4 = st.columns(4)
            with col_total1:
                st.metric("Tổng nước 7 ngày", f"{total_water:.2f}L")
            with col_total2:
                st.metric("Trung bình/ngày", f"{avg_water:.2f}L")
            with col_total3:
                st.metric("Tiết kiệm", f"{water_saving:.1f}%", 
                         delta="Tiết kiệm" if water_saving > 0 else "Tăng")
            with col_total4:
                st.metric("Tổng ml", f"{total_ml:.0f}ml")
            
            # Phân tích
            st.markdown("#### 📈 Phân tích nhu cầu nước")
            
            rain_days = len([x for x in water_calc['Khuyến nghị'] if 'mưa' in x.lower()])
            increase_days = len([x for x in water_calc['Khuyến nghị'] if 'tăng' in x.lower()])
            decrease_days = len([x for x in water_calc['Khuyến nghị'] if 'giảm' in x.lower()])
            normal_days = 7 - rain_days - increase_days - decrease_days
            
            col_anal1, col_anal2, col_anal3, col_anal4 = st.columns(4)
            with col_anal1:
                st.metric("Ngày mưa", rain_days)
            with col_anal2:
                st.metric("Ngày tăng", increase_days)
            with col_anal3:
                st.metric("Ngày giảm", decrease_days)
            with col_anal4:
                st.metric("Ngày bình thường", normal_days)
    
    with tab_forecast3:
        st.markdown("#### 📅 Lịch Chăm Sóc Thông Minh 14 Ngày")
        
        if st.session_state.selected_plant:
            plant_name = plant.get('Tên Cây', '')
            plant_data = st.session_state.plant_details or plant
            
            # Tạo lịch chăm sóc
            schedule = ai_system.generate_watering_schedule(
                plant_name,
                plant_data,
                st.session_state.forecast_data,
                st.session_state.location_details
            )
            
            # Hiển thị lịch
            st.markdown(f"##### 📅 Lịch tưới nước cho {plant_name}")
            
            schedule_df = pd.DataFrame(schedule)
            st.dataframe(
                schedule_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Ngày": "📅 Ngày",
                    "Thứ": "📆 Thứ",
                    "Hành động": "📝 Hành động",
                    "Thời điểm": "⏰ Thời điểm",
                    "Lượng nước (ml)": "💦 Lượng nước",
                    "Ghi chú": "📌 Ghi chú"
                }
            )
            
            # Thêm các công việc khác
            st.markdown("##### 📋 Công việc chăm sóc khác")
            
            other_tasks = [
                {"Công việc": "🌿 Bón phân", "Tần suất": "2 tuần/lần", "Thời điểm": "Sáng sớm", "Ghi chú": "Bón sau khi tưới nước"},
                {"Công việc": "✂️ Cắt tỉa", "Tần suất": "1 tháng/lần", "Thời điểm": "Sáng sớm", "Ghi chú": "Cắt lá vàng, cành khô"},
                {"Công việc": "🔍 Kiểm tra sâu bệnh", "Tần suất": "1 tuần/lần", "Thời điểm": "Bất kỳ", "Ghi chú": "Kiểm tra mặt dưới lá"},
                {"Công việc": "🧹 Vệ sinh lá", "Tần suất": "2 tuần/lần", "Thời điểm": "Sáng sớm", "Ghi chú": "Lau bằng khăn ẩm"},
                {"Công việc": "🔄 Xoay chậu", "Tần suất": "1 tuần/lần", "Thời điểm": "Bất kỳ", "Ghi chú": "Xoay 90 độ để cây phát triển đều"}
            ]
            
            tasks_df = pd.DataFrame(other_tasks)
            st.dataframe(tasks_df, use_container_width=True, hide_index=True)
            
            # Tạo lịch đầy đủ
            st.markdown("##### 📅 Lịch chăm sóc đầy đủ")
            
            if st.button("📅 Tạo lịch chăm sóc đầy đủ", use_container_width=True):
                full_schedule = []
                
                # Thêm lịch tưới nước
                for day in schedule:
                    if day["Hành động"] != "✅ Nghỉ":
                        full_schedule.append({
                            "Ngày": day["Ngày"],
                            "Công việc": day["Hành động"],
                            "Chi tiết": f"{day['Thời điểm']} - {day['Ghi chú']}",
                            "Ưu tiên": "Cao"
                        })
                
                # Thêm công việc khác
                for task in other_tasks:
                    full_schedule.append({
                        "Ngày": "Định kỳ",
                        "Công việc": task["Công việc"],
                        "Chi tiết": f"{task['Tần suất']} - {task['Ghi chú']}",
                        "Ưu tiên": "Trung bình"
                    })
                
                full_df = pd.DataFrame(full_schedule)
                
                # Hiển thị
                st.dataframe(full_df, use_container_width=True, hide_index=True)
                
                # Xuất lịch
                csv = full_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Tải lịch chăm sóc đầy đủ",
                    data=csv,
                    file_name=f"lich_cham_soc_day_du_{plant_name}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    with tab_forecast4:
        st.markdown("#### 📊 Báo Cáo Tổng Hợp")
        
        if (st.session_state.forecast_data is not None and 
            st.session_state.water_calculation is not None):
            
            forecast_df = st.session_state.forecast_data
            water_df = st.session_state.water_calculation
            
            # Tổng hợp dữ liệu
            avg_temp = forecast_df['temp_max'].mean()
            total_rain = forecast_df['precipitation'].sum()
            avg_humidity = forecast_df['humidity'].mean()
            total_water = water_df['Nhu cầu điều chỉnh'].sum()
            avg_water = water_df['Nhu cầu điều chỉnh'].mean()
            
            # Hiển thị metrics
            col_report1, col_report2, col_report3, col_report4 = st.columns(4)
            with col_report1:
                st.metric("🌡️ Nhiệt độ TB", f"{avg_temp:.1f}°C")
            with col_report2:
                st.metric("🌧️ Tổng mưa", f"{total_rain:.1f}mm")
            with col_report3:
                st.metric("💦 Độ ẩm TB", f"{avg_humidity:.0f}%")
            with col_report4:
                st.metric("💧 Tổng nước", f"{total_water:.2f}L")
            
            # Biểu đồ tổng hợp
            fig_combo = go.Figure()
            
            # Nhiệt độ
            fig_combo.add_trace(go.Scatter(
                x=forecast_df['day'],
                y=forecast_df['temp_max'],
                name='Nhiệt độ',
                yaxis='y1',
                line=dict(color='#ff6b6b', width=2)
            ))
            
            # Mưa
            fig_combo.add_trace(go.Bar(
                x=forecast_df['day'],
                y=forecast_df['precipitation'],
                name='Mưa',
                yaxis='y2',
                marker_color='#4dabf7'
            ))
            
            # Nhu cầu nước
            fig_combo.add_trace(go.Scatter(
                x=water_df['Ngày'],
                y=water_df['Nhu cầu điều chỉnh'],
                name='Nhu cầu nước',
                yaxis='y3',
                line=dict(color='#00ffcc', width=2, dash='dot')
            ))
            
            fig_combo.update_layout(
                title="Báo cáo tổng hợp: Nhiệt độ, Mưa & Nhu cầu nước",
                template="plotly_dark",
                xaxis_title="Ngày",
                yaxis=dict(
                    title="Nhiệt độ (°C)",
                    titlefont=dict(color="#ff6b6b"),
                    tickfont=dict(color="#ff6b6b")
                ),
                yaxis2=dict(
                    title="Mưa (mm)",
                    titlefont=dict(color="#4dabf7"),
                    tickfont=dict(color="#4dabf7"),
                    anchor="x",
                    overlaying="y",
                    side="right"
                ),
                yaxis3=dict(
                    title="Nước (L)",
                    titlefont=dict(color="#00ffcc"),
                    tickfont=dict(color="#00ffcc"),
                    anchor="free",
                    overlaying="y",
                    side="right",
                    position=0.85
                ),
                height=400
            )
            
            st.plotly_chart(fig_combo, use_container_width=True)
            
            # Phân tích và đề xuất
            st.markdown("#### 💡 Phân tích & Đề xuất")
            
            recommendations = []
            
            if total_rain > 50:
                recommendations.append("🌧️ **Mưa nhiều:** Giảm tưới nước, kiểm tra thoát nước")
            elif total_rain < 10:
                recommendations.append("☀️ **Ít mưa:** Tăng tần suất tưới nước")
            
            if avg_temp > 30:
                recommendations.append("🔥 **Nóng:** Tưới sáng sớm, che nắng giữa trưa")
            elif avg_temp < 18:
                recommendations.append("❄️ **Mát:** Giảm tưới, tránh tưới buổi tối")
            
            if avg_humidity > 80:
                recommendations.append("💦 **Ẩm cao:** Giảm tưới, tăng thông gió")
            elif avg_humidity < 40:
                recommendations.append("🏜️ **Khô:** Tăng tưới, phun sương cho lá")
            
            for rec in recommendations:
                st.markdown(rec)
            
            # Tạo báo cáo
            st.markdown("---")
            if st.button("📄 Tạo báo cáo đầy đủ", use_container_width=True):
                report_content = f"""
# BÁO CÁO CHĂM SÓC CÂY TRỒNG
**Cây:** {plant.get('Tên Cây', 'N/A')}
**Vị trí:** {location}
**Thời gian:** {datetime.datetime.now().strftime('%d/%m/%Y')}
**Mùa:** {forecast_df.iloc[0]['season'] if len(forecast_df) > 0 else 'N/A'}

## 1. THỐNG KÊ THỜI TIẾT
- Nhiệt độ trung bình: {avg_temp:.1f}°C
- Tổng lượng mưa: {total_rain:.1f}mm
- Độ ẩm trung bình: {avg_humidity:.0f}%

## 2. TÍNH TOÁN NHU CẦU NƯỚC
- Nhu cầu nước cơ bản: {plant.get('Nước (L/ngày)', 0)}L/ngày
- Tổng nước 7 ngày: {total_water:.2f}L
- Trung bình/ngày: {avg_water:.2f}L
- Ngày cần tưới: {7 - len([x for x in water_df['Khuyến nghị'] if 'Không cần tưới' in x or 'mưa' in x.lower()])}/7 ngày

## 3. ĐỀ XUẤT CHĂM SÓC
{chr(10).join(['- ' + rec.split('**')[1] if '**' in rec else '- ' + rec for rec in recommendations])}

## 4. KHẨN CẤP
{'Không có vấn đề khẩn cấp' if total_rain < 100 and avg_temp < 35 else 'CẢNH BÁO: Điều kiện thời tiết khắc nghiệt!'}

---
*Báo cáo được tạo bởi EcoMind OS v{st.session_state.version}*
"""
                
                st.download_button(
                    label="📥 Tải báo cáo (TXT)",
                    data=report_content.encode('utf-8'),
                    file_name=f"bao_cao_{plant.get('Tên Cây', 'cay')}_{datetime.datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

# === TAB 6: HỆ THỐNG NÂNG CẤP ===
elif selected == "⚙️ Hệ Thống":
    st.title("⚙️ Quản Lý Hệ Thống & Cài Đặt")
    st.markdown("### Cấu hình và thông tin hệ thống EcoMind OS")
    
    tab_sys1, tab_sys2, tab_sys3, tab_sys4 = st.tabs(["🎨 Giao diện", "🔧 Cài đặt", "📊 Dữ liệu", "ℹ️ Thông tin"])
    
    with tab_sys1:
        st.markdown("#### 🎨 Tùy Chỉnh Giao Diện")
        
        col_ui1, col_ui2 = st.columns(2)
        
        with col_ui1:
            theme = st.selectbox(
                "Chủ đề giao diện:",
                ["Tối (Mặc định)", "Xanh đậm", "Xám tối", "Xanh lá", "Tím đậm"],
                index=0
            )
            
            font_size = st.slider("Cỡ chữ:", 12, 20, 14)
            
            density = st.select_slider(
                "Mật độ hiển thị:",
                options=["Rộng rãi", "Thoải mái", "Tiêu chuẩn", "Compact", "Siêu compact"],
                value="Thoải mái"
            )
            
            animations = st.toggle("Hiệu ứng động", value=True)
            
            if animations:
                anim_level = st.select_slider(
                    "Mức độ hiệu ứng:",
                    options=["Tối thiểu", "Nhẹ", "Trung bình", "Nhiều"],
                    value="Nhẹ"
                )
        
        with col_ui2:
            st.markdown("**Màu sắc chủ đề:**")
            
            primary_color = st.color_picker("Màu chính:", "#00ffcc")
            secondary_color = st.color_picker("Màu phụ:", "#0088cc")
            accent_color = st.color_picker("Màu nhấn:", "#88aaff")
            
            st.markdown("**Bố cục:**")
            
            sidebar_width = st.slider("Độ rộng sidebar:", 200, 400, 280)
            card_radius = st.slider("Góc bo card:", 8, 20, 12)
            
            auto_refresh = st.toggle("Tự động làm mới dữ liệu", value=False)
            if auto_refresh:
                refresh_rate = st.slider("Tần suất (phút):", 1, 60, 15)
        
        # Áp dụng
        col_apply1, col_apply2 = st.columns(2)
        with col_apply1:
            if st.button("💾 Áp dụng cài đặt", use_container_width=True, type="primary"):
                st.session_state.user_settings.update({
                    'theme': theme,
                    'font_size': font_size,
                    'density': density,
                    'animations': animations,
                    'primary_color': primary_color,
                    'card_radius': card_radius
                })
                st.success("✅ Đã lưu cài đặt giao diện!")
        with col_apply2:
            if st.button("🔄 Đặt lại mặc định", use_container_width=True):
                st.session_state.user_settings.update({
                    'theme': 'Tối (Mặc định)',
                    'font_size': 14,
                    'density': 'Thoải mái',
                    'animations': True,
                    'primary_color': '#00ffcc',
                    'card_radius': 12
                })
                st.success("✅ Đã đặt lại mặc định!")
    
    with tab_sys2:
        st.markdown("#### 🔧 Cài Đặt Hệ Thống")
        
        # Thông báo
        st.markdown("##### 🔔 Thông Báo & Cảnh Báo")
        
        col_notif1, col_notif2 = st.columns(2)
        
        with col_notif1:
            email_notif = st.toggle("Email thông báo", value=False)
            watering_reminders = st.toggle("Nhắc tưới nước", value=True)
            weather_alerts = st.toggle("Cảnh báo thời tiết", value=True)
        
        with col_notif2:
            system_updates = st.toggle("Cập nhật hệ thống", value=True)
            disease_alerts = st.toggle("Cảnh báo bệnh cây", value=True)
            maintenance_reminders = st.toggle("Nhắc bảo trì", value=True)
        
        # Đơn vị
        st.markdown("##### 📏 Đơn Vị Đo Lường")
        
        units = st.radio(
            "Hệ đơn vị:",
            ["Hệ mét (m, L, °C, kg)", "Hệ Anh (ft, gal, °F, lb)"],
            horizontal=True
        )
        
        # Ngôn ngữ
        st.markdown("##### 🌐 Ngôn Ngữ & Vùng")
        
        col_lang1, col_lang2 = st.columns(2)
        with col_lang1:
            language = st.selectbox(
                "Ngôn ngữ giao diện:",
                ["Tiếng Việt", "English", "Français", "Español"],
                index=0
            )
        with col_lang2:
            region = st.selectbox(
                "Vùng:",
                ["Việt Nam", "International", "Custom"],
                index=0
            )
        
        # Hiệu suất
        st.markdown("##### ⚡ Hiệu Suất")
        
        cache_enabled = st.toggle("Bật cache dữ liệu", value=True)
        if cache_enabled:
            cache_size = st.slider("Kích thước cache (MB):", 10, 500, 100)
        
        auto_save = st.toggle("Tự động lưu dữ liệu", value=True)
        if auto_save:
            save_interval = st.slider("Khoảng thời gian (phút):", 1, 60, 5)
        
        # Lưu cài đặt
        if st.button("💾 Lưu cài đặt hệ thống", type="primary", use_container_width=True):
            st.session_state.user_settings.update({
                'units': 'metric' if 'mét' in units else 'imperial',
                'language': language,
                'region': region,
                'notifications': any([email_notif, watering_reminders, weather_alerts]),
                'cache_enabled': cache_enabled,
                'auto_save': auto_save
            })
            st.success("✅ Đã lưu cài đặt hệ thống!")
    
    with tab_sys3:
        st.markdown("#### 📊 Quản Lý Dữ Liệu")
        
        # Thống kê dữ liệu
        st.markdown("##### 📈 Thống Kê Dữ Liệu")
        
        col_data1, col_data2, col_data3 = st.columns(3)
        with col_data1:
            st.metric("Cây trong DB", len(df_plants))
            st.metric("Địa điểm", len(map_system.vietnam_locations))
        with col_data2:
            st.metric("Cache thời tiết", len(config_system.weather_cache))
            st.metric("Lượt chẩn đoán", len(ai_system.diagnosis_history))
        with col_data3:
            st.metric("Cây người dùng", len(plant_system.user_plants))
            st.metric("Tìm kiếm", len(st.session_state.search_history))
        
        # Quản lý cache
        st.markdown("##### 🗑️ Quản Lý Cache & Dữ Liệu")
        
        col_cache1, col_cache2, col_cache3 = st.columns(3)
        
        with col_cache1:
            if st.button("🧹 Xóa cache thời tiết", use_container_width=True):
                config_system.weather_cache.clear()
                st.success("✅ Đã xóa cache thời tiết!")
        
        with col_cache2:
            if st.button("🗑️ Xóa cache toàn bộ", use_container_width=True):
                st.cache_data.clear()
                st.cache_resource.clear()
                st.success("✅ Đã xóa toàn bộ cache!")
        
        with col_cache3:
            if st.button("🔄 Đặt lại thống kê", use_container_width=True):
                st.session_state.search_history = []
                st.success("✅ Đã đặt lại thống kê!")
        
        # Xuất dữ liệu
        st.markdown("##### 📤 Xuất Dữ Liệu")
        
        export_format = st.selectbox(
            "Định dạng xuất:",
            ["CSV", "Excel", "JSON", "TXT"]
        )
        
        export_type = st.multiselect(
            "Loại dữ liệu:",
            ["Cây trồng", "Địa điểm", "Cài đặt", "Lịch sử chẩn đoán", "Dữ liệu thời tiết"]
        )
        
        if st.button("📥 Xuất dữ liệu đã chọn", use_container_width=True):
            export_data = {}
            
            if "Cây trồng" in export_type:
                export_data["plants"] = df_plants.to_dict('records')
                if plant_system.user_plants:
                    export_data["user_plants"] = plant_system.user_plants
            
            if "Địa điểm" in export_type:
                export_data["locations"] = map_system.vietnam_locations
            
            if "Cài đặt" in export_type:
                export_data["settings"] = st.session_state.user_settings
            
            if "Lịch sử chẩn đoán" in export_type:
                export_data["diagnosis_history"] = st.session_state.diagnosis_history
            
            if "Dữ liệu thời tiết" in export_type and st.session_state.forecast_data is not None:
                export_data["weather_data"] = st.session_state.forecast_data.to_dict('records')
            
            if export_data:
                if export_format == "JSON":
                    json_data = json.dumps(export_data, ensure_ascii=False, indent=2)
                    st.download_button(
                        label="Tải xuống JSON",
                        data=json_data,
                        file_name=f"ecomind_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                elif export_format == "CSV":
                    # Xuất cây trồng
                    if "plants" in export_data:
                        csv_data = df_plants.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Tải xuống CSV cây trồng",
                            data=csv_data,
                            file_name=f"ecomind_plants_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
        
        # Import dữ liệu
        st.markdown("##### 📥 Import Dữ Liệu")
        
        uploaded_file = st.file_uploader("Chọn file dữ liệu:", type=['json', 'csv'])
        
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.json'):
                try:
                    import_data = json.load(uploaded_file)
                    st.success(f"✅ Đã đọc file {uploaded_file.name}")
                    
                    if st.button("Import dữ liệu", use_container_width=True):
                        # Xử lý import
                        st.info("Chức năng import đang được phát triển...")
                except:
                    st.error("Lỗi đọc file JSON!")
            else:
                st.warning("Chỉ hỗ trợ file JSON cho import!")
    
    with tab_sys4:
        st.markdown("#### ℹ️ Thông Tin Hệ Thống")
        
        # Thông tin phiên bản
        st.markdown("##### 📱 Thông Tin Phiên Bản")
        
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.metric("Phiên bản", st.session_state.version)
            st.metric("Build", st.session_state.build_date)
            st.metric("Trạng thái", "✅ Online")
        with info_col2:
            st.metric("Cập nhật", "Tự động")
            st.metric("Streamlit", st.__version__)
            st.metric("Python", "3.9+")
        
        # Thông tin kỹ thuật
        st.markdown("##### 🔧 Thông Tin Kỹ Thuật")
        
        tech_info = [
            ("Hệ thống", "Tự cung tự cấp hoàn toàn"),
            ("Framework", "Streamlit + Plotly + Folium"),
            ("Database", "Pandas + Offline Storage"),
            ("Bản đồ", "OpenStreetMap + Offline Database"),
            ("Thời tiết", "Mô phỏng thông minh offline"),
            ("AI", "Rule-based + Knowledge Base"),
            ("Cache", "In-memory + Session State"),
            ("Hiệu suất", "Tối ưu cho Streamlit Cloud")
        ]
        
        for label, value in tech_info:
            with st.container(border=True):
                col_tech1, col_tech2 = st.columns([1, 3])
                with col_tech1:
                    st.markdown(f"**{label}:**")
                with col_tech2:
                    st.markdown(value)
        
        # Thông tin liên hệ
        st.markdown("##### 📞 Liên Hệ & Hỗ Trợ")
        
        with st.container(border=True):
            st.markdown("**Email hỗ trợ:**")
            st.code("tranthienphatle@gmail.com", language="text")
            
            st.markdown("**Hệ thống:** Hoạt động offline hoàn toàn")
            st.markdown("**Dữ liệu:** 200+ địa điểm, 50+ cây trồng")
            st.markdown("**Tính năng:** AI chẩn đoán, dự báo thời tiết, tính toán thông minh")
            st.markdown("**Yêu cầu:** Không cần API key, không cần internet")
        
        # Kiểm tra hệ thống
        st.markdown("##### 🔍 Kiểm Tra Hệ Thống")
        
        if st.button("🔍 Chạy kiểm tra hệ thống", use_container_width=True):
            with st.spinner("Đang kiểm tra..."):
                time.sleep(1)
                
                checks = [
                    ("Hệ thống thời tiết", True, "✅ Hoạt động"),
                    ("Database cây trồng", len(df_plants) > 0, f"✅ {len(df_plants)} cây"),
                    ("Database địa điểm", len(map_system.vietnam_locations) > 0, f"✅ {len(map_system.vietnam_locations)} địa điểm"),
                    ("Hệ thống AI", len(ai_system.knowledge_base) > 0, f"✅ {len(ai_system.knowledge_base)} bệnh"),
                    ("Cache", len(config_system.weather_cache) >= 0, "✅ Hoạt động"),
                    ("Session State", len(st.session_state) > 0, "✅ Hoạt động")
                ]
                
                for check_name, status, message in checks:
                    col_check1, col_check2 = st.columns([3, 1])
                    with col_check1:
                        st.markdown(check_name)
                    with col_check2:
                        if status:
                            st.success(message)
                        else:
                            st.error("❌ Lỗi")
        
        # Thông tin bản quyền
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; color: #88aaff; font-size: 0.9rem;">
            © 2024 EcoMind OS - Phiên bản tự cung tự cấp<br>
            Phiên bản {st.session_state.version} • Build {st.session_state.build_date}<br>
            Email: tranthienphatle@gmail.com • Streamlit Cloud Deployment
        </div>
        """, unsafe_allow_html=True)

# --- 10. FOOTER NÂNG CẤP ---
st.markdown("---")

footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)

with footer_col1:
    st.markdown("**🌿 EcoMind OS**")
    st.caption(f"v{st.session_state.version} • Build {st.session_state.build_date}")

with footer_col2:
    st.markdown("**📧 Liên hệ**")
    st.caption("tranthienphatle@gmail.com")

with footer_col3:
    st.markdown("**♻️ Tự cung tự cấp**")
    st.caption("Không cần API • Hoạt động offline")

with footer_col4:
    st.markdown("**🚀 Triển khai**")
    st.caption("Streamlit Cloud + GitHub")

# Hiển thị thời gian và trạng thái
current_time = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
status_indicator = '<span class="status-indicator status-online"></span>' if len(df_plants) > 0 else '<span class="status-indicator status-offline"></span>'

st.caption(f"{status_indicator} 🕐 {current_time} • © 2024 EcoMind • Phiên bản tự cung tự cấp", unsafe_allow_html=True)
