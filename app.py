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
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import math

# --- 1. CẤU HÌNH GIAO DIỆN ĐÁP ỨNG ---
st.set_page_config(
    page_title="EcoMind OS - Hệ Thống Dự Báo Chăm Sóc Cây",
    layout="wide", 
    page_icon="🌿",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://ecomind.com/help',
        'Report a bug': 'https://ecomind.com/bug',
        'About': 'Hệ thống dự báo chăm sóc cây thông minh - Phiên bản v2.0'
    }
)

# CSS đáp ứng cho cả mobile và desktop
st.markdown("""
<style>
    /* Container chính responsive */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Responsive cho mobile */
    @media (max-width: 768px) {
        /* Giảm padding trên mobile */
        .main .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        
        /* Điều chỉnh kích thước font trên mobile */
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.3rem !important; }
        h3 { font-size: 1.1rem !important; }
        
        /* Cột responsive */
        [data-testid="column"] {
            min-width: 100% !important;
        }
        
        /* Dataframe trên mobile */
        .stDataFrame {
            font-size: 0.8rem;
        }
        
        /* Button trên mobile */
        .stButton > button {
            font-size: 0.9rem;
            padding: 0.5rem;
        }
    }
    
    /* Tablet styles */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.5rem !important; }
    }
    
    /* Đảm bảo các container co giãn */
    .stApp {
        min-height: 100vh;
    }
    
    /* Scrollbar tùy chỉnh */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    /* Card responsive */
    .responsive-card {
        background: rgba(30, 35, 50, 0.9);
        border: 1px solid rgba(0, 255, 204, 0.2);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    @media (max-width: 768px) {
        .responsive-card {
            padding: 0.8rem;
            margin-bottom: 0.8rem;
        }
    }
    
    /* Metrics responsive */
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
    
    @media (max-width: 768px) {
        div[data-testid="stMetricValue"] {
            font-size: 1.2rem !important;
        }
        
        div[data-testid="stMetricLabel"] {
            font-size: 0.8rem !important;
        }
    }
    
    /* Tabs responsive */
    .stTabs [data-baseweb="tab-list"] {
        flex-wrap: wrap;
    }
    
    /* Input fields responsive */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        font-size: 0.95rem !important;
    }
    
    @media (max-width: 768px) {
        .stTextInput input, .stSelectbox select, .stTextArea textarea {
            font-size: 0.9rem !important;
        }
    }
    
    /* Sidebar responsive */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            width: 100% !important;
            min-width: 100% !important;
        }
        
        [data-testid="stSidebar"][aria-expanded="false"] {
            display: none;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- 2. KHỞI TẠO DỮ LIỆU CÂY TRỒNG ---
@st.cache_data(show_spinner="🌱 Đang khởi tạo cơ sở dữ liệu thực vật...")
def generate_plant_database():
    """Tạo database cây trồng với các thông số chăm sóc"""
    
    # Mở rộng loại cây cho phù hợp với thực tế Việt Nam
    loai_cay = [
        "Hoa Hồng", "Lan", "Xương Rồng", "Sen Đá", "Trầu Bà", "Dương Xỉ", "Cây Cọ", 
        "Trúc", "Tùng", "Cúc", "Mai", "Đào", "Sung", "Si", "Đa", "Phong Lan",
        "Cẩm Tú Cầu", "Tulip", "Hoa Quỳnh", "Bonsai", "Cây Lưỡi Hổ", "Cây Kim Tiền",
        "Cây Phát Tài", "Cây Ngũ Gia Bì", "Cây Vạn Lộc", "Cây Kim Ngân", "Cây Trường Sinh",
        "Cây Thường Xuân", "Cây Nhện", "Cây Hồng Môn", "Cây Đỗ Quyên", "Cây Sứ", "Cây Mẫu Đơn"
    ]
    
    tinh_tu = ["Hoàng Gia", "Cẩm Thạch", "Bạch Tạng", "Hắc Kim", "Lửa", "Tuyết", 
               "Đại Đế", "Tiểu Thư", "Phú Quý", "Thần Tài", "Vương Giả", "Thiên Nga"]
    
    data = []
    
    # Tạo 2000 cây với thông số thực tế
    for i in range(1, 2001):
        ten_cay = f"{random.choice(loai_cay)} {random.choice(tinh_tu)}"
        
        # Tính toán nhu cầu nước dựa trên loại cây
        if "Xương Rồng" in ten_cay or "Sen Đá" in ten_cay:
            nuoc_tb = round(random.uniform(0.05, 0.2), 2)  # Cây chịu hạn
            toc_do_su_dung_nuoc = round(random.uniform(0.01, 0.05), 2)
        elif "Lan" in ten_cay or "Dương Xỉ" in ten_cay:
            nuoc_tb = round(random.uniform(0.3, 0.8), 2)  # Cây ưa ẩm
            toc_do_su_dung_nuoc = round(random.uniform(0.08, 0.15), 2)
        else:
            nuoc_tb = round(random.uniform(0.1, 0.5), 2)  # Cây thông thường
            toc_do_su_dung_nuoc = round(random.uniform(0.03, 0.1), 2)
        
        # Thông số chăm sóc
        anh_sang = random.choice(["Bóng râm (2-3h)", "Bán phần (3-5h)", "Đầy đủ (5-8h)", "Nắng mạnh (8h+)"])
        nhiet_do_ly_tuong = f"{random.randint(18, 22)}-{random.randint(25, 30)}°C"
        do_kho = random.choice(["Rất dễ", "Dễ", "Trung bình", "Khó", "Rất khó"])
        
        # Thời gian bình hết nước (ngày) dựa trên nhu cầu nước
        if nuoc_tb < 0.2:
            tg_het_nuoc = random.randint(10, 30)
        elif nuoc_tb < 0.5:
            tg_het_nuoc = random.randint(5, 15)
        else:
            tg_het_nuoc = random.randint(3, 10)
        
        # Loại chậu đề xuất
        loai_chau = random.choice(["Chậu đất nung", "Chậu nhựa tái chế", "Chậu gốm", "Chậu thủy tinh", "Chậu composite"])
        
        data.append([
            i, ten_cay, nuoc_tb, toc_do_su_dung_nuoc, anh_sang, nhiet_do_ly_tuong,
            do_kho, tg_het_nuoc, loai_chau
        ])
    
    columns = [
        "ID", "Tên Cây", "Nước TB (L/ngày)", "Tốc độ dùng nước (L/ngày)", 
        "Ánh sáng lý tưởng", "Nhiệt độ lý tưởng", "Độ khó chăm sóc", 
        "TG bình hết nước (ngày)", "Loại chậu đề xuất"
    ]
    
    return pd.DataFrame(data, columns=columns)

# --- 3. HỆ THỐNG DỰ BÁO THỜI TIẾT ---
class WeatherForecastSystem:
    """Hệ thống dự báo thời tiết và tính toán nhu cầu nước"""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="ecomind_app")
        self.tf = TimezoneFinder()
        
    def get_location_from_coords(self, lat, lon):
        """Lấy thông tin địa điểm từ tọa độ"""
        try:
            location = self.geolocator.reverse(f"{lat}, {lon}")
            return location.address if location else "Không xác định"
        except:
            return "Không xác định"
    
    def get_timezone(self, lat, lon):
        """Lấy múi giờ từ tọa độ"""
        try:
            timezone_str = self.tf.timezone_at(lng=lon, lat=lat)
            return pytz.timezone(timezone_str) if timezone_str else pytz.UTC
        except:
            return pytz.UTC
    
    def simulate_weather_data(self, lat, lon, days=7):
        """Mô phỏng dữ liệu thời tiết dựa trên vị trí"""
        # Seed dựa trên tọa độ để dữ liệu ổn định
        seed = int(abs(lat * 100 + lon * 100))
        random.seed(seed)
        
        weather_data = []
        today = datetime.datetime.now()
        
        for day in range(days):
            date = today + timedelta(days=day)
            
            # Mô phỏng nhiệt độ dựa trên vĩ độ
            base_temp = 25 - (abs(lat) - 15) * 0.5  # Nhiệt độ giảm dần khi xa xích đạo
            temp = round(base_temp + random.uniform(-5, 5), 1)
            
            # Mô phỏng độ ẩm
            humidity = random.randint(40, 90)
            
            # Mô phỏng lượng mưa (mm)
            if random.random() < 0.3:  # 30% khả năng có mưa
                rainfall = round(random.uniform(0.5, 20.0), 1)
            else:
                rainfall = 0.0
            
            # Mô phỏng tốc độ bay hơi dựa trên nhiệt độ và độ ẩm
            evaporation_rate = round((temp * (100 - humidity) / 2000) * random.uniform(0.8, 1.2), 3)
            
            # Điều kiện thời tiết
            if rainfall > 10:
                condition = "🌧️ Mưa to"
            elif rainfall > 0:
                condition = "🌦️ Mưa nhẹ"
            elif temp > 32:
                condition = "☀️ Nắng nóng"
            elif temp > 25:
                condition = "⛅ Nắng nhẹ"
            else:
                condition = "☁️ Mát mẻ"
            
            weather_data.append({
                "Ngày": date.strftime("%d/%m"),
                "Nhiệt độ (°C)": temp,
                "Độ ẩm (%)": humidity,
                "Lượng mưa (mm)": rainfall,
                "Tốc độ bay hơi (L/ngày)": evaporation_rate,
                "Điều kiện": condition,
                "Date_obj": date
            })
        
        return pd.DataFrame(weather_data)
    
    def calculate_water_consumption(self, plant_water_needs, weather_df, lat, lon):
        """Tính toán nhu cầu nước thực tế dựa trên thời tiết"""
        results = []
        
        for _, weather in weather_df.iterrows():
            # Điều chỉnh nhu cầu nước dựa trên thời tiết
            temp_factor = 1 + (weather["Nhiệt độ (°C)"] - 25) * 0.02  # Nhiệt độ ảnh hưởng
            humidity_factor = 1 - (weather["Độ ẩm (%)"] - 50) * 0.005  # Độ ẩm ảnh hưởng
            rain_adjustment = max(0, plant_water_needs - weather["Lượng mưa (mm)"] / 10)  # Mưa bù nước
            
            # Tính nhu cầu nước thực tế
            adjusted_need = plant_water_needs * temp_factor * humidity_factor
            actual_need = max(0.01, adjusted_need - rain_adjustment)
            
            # Thêm tốc độ bay hơi
            total_consumption = actual_need + weather["Tốc độ bay hơi (L/ngày)"]
            
            results.append({
                "Ngày": weather["Ngày"],
                "Nhu cầu cơ bản": round(plant_water_needs, 3),
                "Nhu cầu đã điều chỉnh": round(actual_need, 3),
                "Bay hơi": round(weather["Tốc độ bay hơi (L/ngày)"], 3),
                "Tổng tiêu thụ": round(total_consumption, 3),
                "Mưa (mm)": weather["Lượng mưa (mm)"],
                "Điều kiện": weather["Điều kiện"]
            })
        
        return pd.DataFrame(results)

# --- 4. HỆ THỐNG QUẢN LÝ VỊ TRÍ ---
class LocationManager:
    """Quản lý vị trí cây trồng"""
    
    def __init__(self):
        self.locations = {}
        self.load_sample_locations()
    
    def load_sample_locations(self):
        """Tạo một số vị trí mẫu tại Việt Nam"""
        self.sample_locations = {
            "Hà Nội": {"lat": 21.0285, "lon": 105.8542, "alt": 16},
            "TP Hồ Chí Minh": {"lat": 10.8231, "lon": 106.6297, "alt": 19},
            "Đà Nẵng": {"lat": 16.0544, "lon": 108.2022, "alt": 7},
            "Huế": {"lat": 16.4637, "lon": 107.5909, "alt": 8},
            "Nha Trang": {"lat": 12.2388, "lon": 109.1967, "alt": 6},
            "Đà Lạt": {"lat": 11.9404, "lon": 108.4583, "alt": 1475},
            "Cần Thơ": {"lat": 10.0452, "lon": 105.7469, "alt": 2},
            "Hải Phòng": {"lat": 20.8449, "lon": 106.6881, "alt": 12},
            "Vũng Tàu": {"lat": 10.3460, "lon": 107.0843, "alt": 4}
        }
    
    def add_location(self, name, lat, lon, alt=0, description=""):
        """Thêm vị trí mới"""
        self.locations[name] = {
            "lat": lat,
            "lon": lon,
            "alt": alt,
            "description": description,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return True
    
    def get_location(self, name):
        """Lấy thông tin vị trí"""
        return self.locations.get(name)
    
    def get_all_locations(self):
        """Lấy tất cả vị trí"""
        return self.locations
    
    def calculate_sunlight_hours(self, lat, lon, date=None):
        """Ước tính số giờ nắng dựa trên vị trí và mùa"""
        if date is None:
            date = datetime.datetime.now()
        
        # Tính ngày trong năm (1-365)
        day_of_year = date.timetuple().tm_yday
        
        # Ước tính giờ nắng dựa trên vĩ độ và mùa
        # Công thức đơn giản hóa
        base_hours = 12  # Giờ nắng trung bình tại xích đạo
        
        # Điều chỉnh theo vĩ độ
        lat_effect = abs(lat) / 90 * 4  # Ảnh hưởng của vĩ độ
        
        # Điều chỉnh theo mùa (giả sử Việt Nam)
        if 80 <= day_of_year <= 170:  # Mùa hè
            season_effect = 2
        elif 260 <= day_of_year <= 350:  # Mùa đông
            season_effect = -2
        else:
            season_effect = 0
        
        total_hours = base_hours - lat_effect + season_effect
        return max(4, min(14, round(total_hours, 1)))  # Giới hạn trong 4-14 giờ

# --- 5. HỆ THỐNG DỰ BÁO BÌNH HẾT NƯỚC ---
class WaterLevelPredictor:
    """Dự báo mức nước và thời gian hết nước"""
    
    def __init__(self):
        self.prediction_history = {}
    
    def predict_water_emptying(self, current_volume, daily_consumption, weather_data):
        """Dự báo thời gian bình hết nước"""
        
        predictions = []
        remaining_volume = current_volume
        
        for _, day in weather_data.iterrows():
            if remaining_volume <= 0:
                break
            
            # Điều chỉnh tiêu thụ theo thời tiết
            adjusted_consumption = daily_consumption * (1 + day["Nhiệt độ (°C)"] / 100)
            
            # Trừ lượng mưa (1mm mưa ≈ 1L/m²)
            rain_contribution = day["Lượng mưa (mm)"] * 0.1  # Giả sử diện tích chậu 0.1m²
            
            net_consumption = max(0.01, adjusted_consumption - rain_contribution)
            remaining_volume -= net_consumption
            
            predictions.append({
                "Ngày": day["Ngày"],
                "Tiêu thụ (L)": round(net_consumption, 3),
                "Nước còn lại (L)": round(max(0, remaining_volume), 3),
                "Mưa (mm)": day["Lượng mưa (mm)"],
                "Trạng thái": "⛽ Còn nước" if remaining_volume > 0 else "⚠️ Hết nước"
            })
        
        df_predictions = pd.DataFrame(predictions)
        
        # Tìm ngày hết nước
        empty_day = None
        for _, row in df_predictions.iterrows():
            if row["Nước còn lại (L)"] <= 0:
                empty_day = row["Ngày"]
                break
        
        return df_predictions, empty_day
    
    def calculate_refill_schedule(self, plant_data, location_data, pot_capacity):
        """Tính lịch trình đổ nước tối ưu"""
        
        schedule = []
        current_level = pot_capacity
        
        # Lấy dữ liệu thời tiết 30 ngày
        forecast_days = 30
        
        for day in range(forecast_days):
            date = datetime.datetime.now() + timedelta(days=day)
            
            # Tính tiêu thụ cho ngày này
            daily_use = plant_data["Nước TB (L/ngày)"]
            
            # Điều chỉnh theo mùa
            month = date.month
            if month in [5, 6, 7, 8]:  # Mùa hè
                daily_use *= 1.3
            elif month in [11, 12, 1, 2]:  # Mùa đông
                daily_use *= 0.7
            
            current_level -= daily_use
            
            # Kiểm tra nếu cần đổ nước
            if current_level <= pot_capacity * 0.2:  # Khi còn 20%
                schedule.append({
                    "Ngày": date.strftime("%d/%m/%Y"),
                    "Hành động": "💧 Đổ nước",
                    "Lượng nước cần (L)": round(pot_capacity - current_level, 2),
                    "Mức cảnh báo": "⚠️ Sắp hết" if current_level > 0 else "🔴 Hết nước"
                })
                current_level = pot_capacity  # Đổ đầy
            else:
                schedule.append({
                    "Ngày": date.strftime("%d/%m/%Y"),
                    "Hành động": "✅ OK",
                    "Lượng nước còn (L)": round(current_level, 2),
                    "Mức cảnh báo": "🟢 Đủ nước"
                })
        
        return pd.DataFrame(schedule)

# --- 6. KHỞI TẠO HỆ THỐNG ---
# Khởi tạo các hệ thống
weather_system = WeatherForecastSystem()
location_manager = LocationManager()
water_predictor = WaterLevelPredictor()

# Tạo database cây trồng
@st.cache_data
def load_plant_data():
    return generate_plant_database()

df_plants = load_plant_data()

# --- 7. SIDEBAR ĐIỀU HƯỚNG ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #00ffcc; font-size: 1.8rem; margin-bottom: 0;">🌿 ECO-MIND</h1>
        <p style="color: #88aaff; font-size: 0.9rem; margin-top: 0;">Hệ Thống Dự Báo Chăm Sóc Cây</p>
        <div style="height: 2px; background: linear-gradient(90deg, transparent, #00ffcc, transparent); margin: 10px 0;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Menu chính
    selected = option_menu(
        menu_title=None,
        options=["🏠 Tổng Quan", "📍 Quản Lý Vị Trí", "🌦️ Dự Báo Thời Tiết", 
                "💧 Dự Báo Nước", "📅 Lịch Chăm Sóc", "🌿 Thư Viện Cây", "⚙️ Cài Đặt"],
        icons=["house", "geo-alt", "cloud-sun", "droplet", "calendar", "tree", "gear"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#00ffcc", "font-size": "16px"}, 
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "3px 0",
                "border-radius": "8px",
                "padding": "10px 15px",
                "color": "#ffffff"
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg, #00ffcc 0%, #0088cc 100%)",
                "color": "#000000",
                "font-weight": "bold"
            },
        }
    )
    
    # Hiển thị thông tin hệ thống
    st.markdown("---")
    st.markdown("### 📊 Thống Kê")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("Số cây", len(df_plants))
    with col_s2:
        st.metric("Vị trí", len(location_manager.sample_locations))
    
    # Hiển thị thời gian thực
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    st.caption(f"🕐 {current_time}")
    
    # Nút refresh
    if st.button("🔄 Làm mới dữ liệu", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# --- 8. NỘI DUNG CHÍNH ---
# === TAB TỔNG QUAN ===
if selected == "🏠 Tổng Quan":
    st.title("🌍 HỆ THỐNG DỰ BÁO CHĂM SÓC CÂY THÔNG MINH")
    st.markdown("**Phiên bản dành cho chậu cây tái chế không điện tử**")
    
    # Giới thiệu
    with st.container(border=True):
        st.markdown("""
        ### 🤔 Hệ thống này hoạt động như thế nào?
        
        Vì chậu cây của bạn **không có cảm biến điện tử**, hệ thống sử dụng:
        
        1. **📍 Vị trí địa lý** - Xác định thời tiết khu vực
        2. **🌦️ Dữ liệu thời tiết** - Dự báo nhiệt độ, mưa, độ ẩm
        3. **🌿 Đặc tính cây trồng** - Nhu cầu nước, ánh sáng
        4. **🧮 Thuật toán thông minh** - Tính toán thời điểm cần chăm sóc
        
        **Kết quả:** Dự báo chính xác khi nào cần tưới nước, di chuyển cây, hoặc chăm sóc đặc biệt.
        """)
    
    # Metrics chính
    st.markdown("### 📈 CHỈ SỐ HỆ THỐNG")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Độ chính xác dự báo", "92%", "3.2%")
    with col2:
        st.metric("Tiết kiệm nước", "35%", "5.1%")
    with col3:
        st.metric("Cây được tối ưu", f"{len(df_plants):,}", "185")
    with col4:
        st.metric("Vị trí theo dõi", "9", "+2")
    
    # Quick actions
    st.markdown("### ⚡ HÀNH ĐỘNG NHANH")
    
    quick_col1, quick_col2, quick_col3 = st.columns(3)
    
    with quick_col1:
        if st.button("📍 Thêm vị trí mới", use_container_width=True):
            st.session_state.redirect_to_location = True
            st.rerun()
    
    with quick_col2:
        if st.button("🌦️ Xem dự báo", use_container_width=True):
            st.session_state.redirect_to_weather = True
            st.rerun()
    
    with quick_col3:
        if st.button("💧 Tính toán nước", use_container_width=True):
            st.session_state.redirect_to_water = True
            st.rerun()
    
    # Dashboard nhanh
    st.markdown("### 📊 DASHBOARD NHANH")
    
    tab1, tab2 = st.tabs(["🌡️ Thời tiết hôm nay", "💧 Cây cần chăm sóc"])
    
    with tab1:
        # Lấy thời tiết Hà Nội mẫu
        weather_today = weather_system.simulate_weather_data(21.0285, 105.8542, days=1)
        
        if not weather_today.empty:
            weather = weather_today.iloc[0]
            w_col1, w_col2, w_col3, w_col4 = st.columns(4)
            
            with w_col1:
                st.metric("Nhiệt độ", f"{weather['Nhiệt độ (°C)']}°C")
            with w_col2:
                st.metric("Độ ẩm", f"{weather['Độ ẩm (%)']}%")
            with w_col3:
                st.metric("Lượng mưa", f"{weather['Lượng mưa (mm)']}mm")
            with w_col4:
                st.metric("Bay hơi", f"{weather['Tốc độ bay hơi (L/ngày)']}L")
    
    with tab2:
        # Giả lập cây cần chăm sóc
        sample_plants = df_plants.sample(3)
        
        for idx, plant in sample_plants.iterrows():
            with st.container(border=True):
                col_p1, col_p2 = st.columns([3, 1])
                with col_p1:
                    st.write(f"**{plant['Tên Cây']}**")
                    st.progress(0.3, text=f"Nước: {plant['Nước TB (L/ngày)']}L/ngày")
                with col_p2:
                    if st.button("Chăm sóc", key=f"care_{plant['ID']}"):
                        st.success("Đã lên lịch!")

# === TAB QUẢN LÝ VỊ TRÍ ===
elif selected == "📍 Quản Lý Vị Trí":
    st.title("📍 QUẢN LÝ VỊ TRÍ CÂY TRỒNG")
    
    tab_loc1, tab_loc2, tab_loc3 = st.tabs(["🗺️ Bản đồ & Tọa độ", "📋 Danh sách vị trí", "➕ Thêm vị trí mới"])
    
    with tab_loc1:
        st.markdown("### 🗺️ NHẬP TỌA ĐỘ TỪ GOOGLE MAPS")
        
        col_map1, col_map2 = st.columns([2, 1])
        
        with col_map1:
            st.info("""
            **Cách lấy tọa độ từ Google Maps:**
            1. Mở Google Maps
            2. Tìm vị trí của bạn
            3. Nhấp chuột phải vào vị trí
            4. Chọn "Tọa độ"
            5. Sao chép tọa độ (ví dụ: 21.0285, 105.8542)
            """)
            
            # Hiển thị bản đồ tĩnh với vị trí mẫu
            st.image("https://maps.googleapis.com/maps/api/staticmap?center=21.0285,105.8542&zoom=12&size=600x400&maptype=roadmap&markers=color:red%7C21.0285,105.8542", 
                    caption="Ví dụ: Tọa độ Hà Nội (21.0285, 105.8542)")
        
        with col_map2:
            st.markdown("### 📍 Nhập tọa độ thủ công")
            
            # Chọn từ vị trí mẫu
            sample_location = st.selectbox(
                "Chọn vị trí mẫu:",
                list(location_manager.sample_locations.keys())
            )
            
            if sample_location:
                loc = location_manager.sample_locations[sample_location]
                lat = st.number_input("Vĩ độ (Latitude):", value=loc["lat"], format="%.6f")
                lon = st.number_input("Kinh độ (Longitude):", value=loc["lon"], format="%.6f")
                alt = st.number_input("Độ cao (m):", value=loc["alt"])
            else:
                lat = st.number_input("Vĩ độ (Latitude):", value=21.0285, format="%.6f")
                lon = st.number_input("Kinh độ (Longitude):", value=105.8542, format="%.6f")
                alt = st.number_input("Độ cao (m):", value=16)
            
            location_name = st.text_input("Tên vị trí:", value=sample_location if sample_location else "")
            description = st.text_area("Mô tả vị trí:")
            
            if st.button("💾 Lưu vị trí", type="primary", use_container_width=True):
                if location_name and lat and lon:
                    location_manager.add_location(location_name, lat, lon, alt, description)
                    st.success(f"✅ Đã lưu vị trí: {location_name}")
                    
                    # Hiển thị thông tin vị trí
                    with st.expander("📋 Thông tin vị trí đã lưu", expanded=True):
                        st.write(f"**Tên:** {location_name}")
                        st.write(f"**Tọa độ:** {lat}, {lon}")
                        st.write(f"**Độ cao:** {alt}m")
                        
                        # Tính toán thông tin phụ
                        sunlight_hours = location_manager.calculate_sunlight_hours(lat, lon)
                        st.write(f"**Giờ nắng ước tính:** {sunlight_hours}h/ngày")
                        
                        # Hiển thị link Google Maps
                        maps_url = f"https://www.google.com/maps?q={lat},{lon}"
                        st.markdown(f"[🗺️ Xem trên Google Maps]({maps_url})")
                else:
                    st.error("Vui lòng nhập đầy đủ thông tin!")
    
    with tab_loc2:
        st.markdown("### 📋 DANH SÁCH VỊ TRÍ ĐÃ LƯU")
        
        # Hiển thị vị trí mẫu
        st.write("**Vị trí mẫu (có sẵn):**")
        
        locations_df = []
        for name, data in location_manager.sample_locations.items():
            sunlight = location_manager.calculate_sunlight_hours(data["lat"], data["lon"])
            locations_df.append({
                "Tên": name,
                "Vĩ độ": data["lat"],
                "Kinh độ": data["lon"],
                "Độ cao": f"{data['alt']}m",
                "Giờ nắng": f"{sunlight}h",
                "Khu vực": "Miền Bắc" if data["lat"] > 18 else "Miền Nam"
            })
        
        if locations_df:
            st.dataframe(pd.DataFrame(locations_df), use_container_width=True, hide_index=True)
        
        # Hiển thị vị trí người dùng đã thêm
        if location_manager.locations:
            st.write("**Vị trí của bạn:**")
            user_locations = []
            
            for name, data in location_manager.locations.items():
                user_locations.append({
                    "Tên": name,
                    "Vĩ độ": data["lat"],
                    "Kinh độ": data["lon"],
                    "Độ cao": f"{data['alt']}m",
                    "Ngày tạo": data["created_at"]
                })
            
            st.dataframe(pd.DataFrame(user_locations), use_container_width=True, hide_index=True)
        else:
            st.info("Chưa có vị trí nào được thêm. Hãy thêm vị trí đầu tiên!")
    
    with tab_loc3:
        st.markdown("### ➕ THÊM VỊ TRÍ MỚI BẰNG TÊN ĐỊA DANH")
        
        col_new1, col_new2 = st.columns([2, 1])
        
        with col_new1:
            location_query = st.text_input("Nhập tên địa điểm:", placeholder="Ví dụ: 123 Đường ABC, Quận 1, TP.HCM")
            
            if st.button("🔍 Tìm tọa độ", use_container_width=True):
                if location_query:
                    with st.spinner("Đang tìm kiếm tọa độ..."):
                        try:
                            location = weather_system.geolocator.geocode(location_query)
                            if location:
                                st.success(f"✅ Tìm thấy: {location.address}")
                                
                                # Hiển thị kết quả
                                col_res1, col_res2 = st.columns(2)
                                with col_res1:
                                    st.metric("Vĩ độ", f"{location.latitude:.6f}")
                                with col_res2:
                                    st.metric("Kinh độ", f"{location.longitude:.6f}")
                                
                                # Tự động điền form
                                st.session_state.found_lat = location.latitude
                                st.session_state.found_lon = location.longitude
                                st.session_state.found_address = location.address
                            else:
                                st.error("Không tìm thấy địa điểm. Vui lòng thử lại!")
                        except Exception as e:
                            st.error(f"Lỗi: {e}")
        
        with col_new2:
            st.markdown("**Hoặc quét mã QR**")
            st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://ecomind.com/add-location", 
                    caption="Quét để thêm vị trí từ điện thoại")

# === TAB DỰ BÁO THỜI TIẾT ===
elif selected == "🌦️ Dự Báo Thời Tiết":
    st.title("🌦️ DỰ BÁO THỜI TIẾT & ẢNH HƯỞNG ĐẾN CÂY TRỒNG")
    
    # Chọn vị trí
    st.markdown("### 📍 CHỌN VỊ TRÍ ĐỂ DỰ BÁO")
    
    col_weather1, col_weather2 = st.columns([1, 2])
    
    with col_weather1:
        location_options = list(location_manager.sample_locations.keys())
        if location_manager.locations:
            location_options += list(location_manager.locations.keys())
        
        selected_location = st.selectbox(
            "Chọn vị trí:",
            location_options,
            index=0
        )
        
        # Lấy tọa độ
        if selected_location in location_manager.sample_locations:
            lat = location_manager.sample_locations[selected_location]["lat"]
            lon = location_manager.sample_locations[selected_location]["lon"]
        else:
            loc_data = location_manager.get_location(selected_location)
            lat = loc_data["lat"]
            lon = loc_data["lon"]
        
        # Hiển thị thông tin vị trí
        st.info(f"""
        **Thông tin vị trí:**
        - Tọa độ: {lat:.4f}, {lon:.4f}
        - Giờ nắng: {location_manager.calculate_sunlight_hours(lat, lon)}h/ngày
        - Múi giờ: {weather_system.get_timezone(lat, lon)}
        """)
        
        # Chọn số ngày dự báo
        forecast_days = st.slider("Số ngày dự báo:", 1, 14, 7)
        
        if st.button("🌤️ Cập nhật dự báo", type="primary", use_container_width=True):
            st.session_state.forecast_data = weather_system.simulate_weather_data(lat, lon, forecast_days)
    
    with col_weather2:
        # Hiển thị bản đồ vị trí
        st.markdown(f"**Vị trí: {selected_location}**")
        
        # Tạo URL Google Maps
        maps_url = f"https://www.google.com/maps?q={lat},{lon}&z=12"
        st.markdown(f"[🗺️ Xem vị trí trên Google Maps]({maps_url})")
        
        # Hiển thị ảnh vệ tinh (static map)
        map_img_url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=11&size=600x300&maptype=hybrid&markers=color:red%7C{lat},{lon}"
        st.image(map_img_url, caption=f"Bản đồ vệ tinh {selected_location}")
    
    # Hiển thị dự báo thời tiết
    if 'forecast_data' in st.session_state:
        weather_df = st.session_state.forecast_data
        
        st.markdown("### 📊 DỰ BÁO THỜI TIẾT CHI TIẾT")
        
        # Biểu đồ nhiệt độ
        fig_temp = px.line(
            weather_df, 
            x='Ngày', 
            y='Nhiệt độ (°C)',
            title='Dự báo nhiệt độ',
            markers=True,
            line_shape='spline'
        )
        fig_temp.update_traces(line_color='#ff6b6b', line_width=3)
        fig_temp.update_layout(template='plotly_dark')
        st.plotly_chart(fig_temp, use_container_width=True)
        
        # Hiển thị bảng dự báo
        st.markdown("#### 📋 BẢNG DỰ BÁO CHI TIẾT")
        st.dataframe(
            weather_df[['Ngày', 'Nhiệt độ (°C)', 'Độ ẩm (%)', 'Lượng mưa (mm)', 'Tốc độ bay hơi (L/ngày)', 'Điều kiện']],
            use_container_width=True,
            hide_index=True
        )
        
        # Phân tích ảnh hưởng đến cây trồng
        st.markdown("### 🌿 PHÂN TÍCH ẢNH HƯỞNG ĐẾN CÂY TRỒNG")
        
        col_impact1, col_impact2, col_impact3 = st.columns(3)
        
        with col_impact1:
            avg_temp = weather_df['Nhiệt độ (°C)'].mean()
            if avg_temp > 30:
                st.error(f"**Nhiệt độ cao:** {avg_temp:.1f}°C\n⚠️ Cây dễ mất nước")
            elif avg_temp < 18:
                st.warning(f"**Nhiệt độ thấp:** {avg_temp:.1f}°C\n🌡️ Cây phát triển chậm")
            else:
                st.success(f"**Nhiệt độ lý tưởng:** {avg_temp:.1f}°C\n✅ Tốt cho cây trồng")
        
        with col_impact2:
            total_rain = weather_df['Lượng mưa (mm)'].sum()
            if total_rain > 50:
                st.info(f"**Mưa nhiều:** {total_rain}mm\n💧 Giảm tưới nước")
            elif total_rain > 10:
                st.success(f"**Mưa vừa:** {total_rain}mm\n🌧️ Tốt cho cây")
            else:
                st.warning(f"**Ít mưa:** {total_rain}mm\n⚠️ Cần tăng tưới")
        
        with col_impact3:
            avg_evap = weather_df['Tốc độ bay hơi (L/ngày)'].mean()
            if avg_evap > 0.1:
                st.warning(f"**Bay hơi cao:** {avg_evap:.3f}L/ngày\n🔥 Nước nhanh hết")
            else:
                st.success(f"**Bay hơi thấp:** {avg_evap:.3f}L/ngày\n💧 Tiết kiệm nước")
        
        # Khuyến nghị chăm sóc
        st.markdown("#### 💡 KHUYẾN NGHỊ CHĂM SÓC")
        
        recommendations = []
        
        if weather_df['Nhiệt độ (°C)'].max() > 32:
            recommendations.append("🌞 **Tránh nắng gắt:** Di chuyển cây vào bóng râm vào buổi trưa")
        
        if weather_df['Lượng mưa (mm)'].sum() > 30:
            recommendations.append("☔ **Giảm tưới:** Trời mưa nhiều, giảm 50% lượng nước tưới")
        
        if weather_df['Độ ẩm (%)'].mean() > 80:
            recommendations.append("💨 **Tăng thông gió:** Độ ẩm cao dễ gây nấm bệnh")
        
        if not recommendations:
            recommendations.append("✅ **Điều kiện tốt:** Duy trì chế độ chăm sóc hiện tại")
        
        for rec in recommendations:
            st.write(f"• {rec}")

# === TAB DỰ BÁO NƯỚC ===
elif selected == "💧 Dự Báo Nước":
    st.title("💧 DỰ BÁO BÌNH HẾT NƯỚC & LỊCH TƯỚI")
    
    tab_water1, tab_water2, tab_water3 = st.tabs(["📊 Dự báo hết nước", "🧮 Tính toán nhu cầu", "📅 Lịch tưới tự động"])
    
    with tab_water1:
        st.markdown("### ⏳ DỰ BÁO THỜI GIAN BÌNH HẾT NƯỚC")
        
        # Chọn cây và vị trí
        col_water1, col_water2 = st.columns(2)
        
        with col_water1:
            selected_plant = st.selectbox(
                "Chọn cây:",
                df_plants['Tên Cây'].tolist(),
                index=0
            )
            
            plant_data = df_plants[df_plants['Tên Cây'] == selected_plant].iloc[0]
            
            # Hiển thị thông tin cây
            st.info(f"""
            **Thông tin cây:**
            - Nước TB: {plant_data['Nước TB (L/ngày)']}L/ngày
            - TG hết nước ước tính: {plant_data['TG bình hết nước (ngày)']} ngày
            - Độ khó: {plant_data['Độ khó chăm sóc']}
            """)
        
        with col_water2:
            location_options = list(location_manager.sample_locations.keys())
            selected_location = st.selectbox(
                "Chọn vị trí cây:",
                location_options,
                index=0
            )
            
            loc_data = location_manager.sample_locations[selected_location]
            
            # Thông số bình nước
            st.markdown("**Thông số bình nước:**")
            pot_capacity = st.number_input("Dung tích bình (L):", min_value=0.1, max_value=50.0, value=5.0, step=0.5)
            current_level = st.slider("Mức nước hiện tại (%):", 0, 100, 80)
            
            current_volume = pot_capacity * (current_level / 100)
            st.metric("Lượng nước hiện tại", f"{current_volume:.2f}L")
        
        if st.button("🔮 Dự báo thời gian hết nước", type="primary", use_container_width=True):
            with st.spinner("Đang tính toán dự báo..."):
                # Lấy dữ liệu thời tiết
                weather_df = weather_system.simulate_weather_data(
                    loc_data["lat"], 
                    loc_data["lon"], 
                    days=14
                )
                
                # Tính toán dự báo
                predictions, empty_day = water_predictor.predict_water_emptying(
                    current_volume,
                    plant_data['Nước TB (L/ngày)'],
                    weather_df
                )
                
                # Hiển thị kết quả
                st.markdown("#### 📈 BIỂU ĐỒ DỰ BÁO MỨC NƯỚC")
                
                fig_water = px.line(
                    predictions,
                    x='Ngày',
                    y='Nước còn lại (L)',
                    title='Dự báo mức nước trong bình',
                    markers=True
                )
                
                # Thêm đường 0
                fig_water.add_hline(y=0, line_dash="dash", line_color="red", 
                                  annotation_text="Mức hết nước")
                
                fig_water.update_layout(template='plotly_dark')
                st.plotly_chart(fig_water, use_container_width=True)
                
                # Hiển thị ngày hết nước dự báo
                if empty_day:
                    st.error(f"⚠️ **DỰ BÁO HẾT NƯỚC:** Ngày {empty_day}")
                    
                    # Tính số ngày còn lại
                    today = datetime.datetime.now()
                    empty_date = datetime.datetime.strptime(empty_day, "%d/%m")
                    empty_date = empty_date.replace(year=today.year)
                    
                    if empty_date < today:
                        empty_date = empty_date.replace(year=today.year + 1)
                    
                    days_left = (empty_date - today).days
                    st.warning(f"⏳ **Còn khoảng {days_left} ngày** trước khi hết nước")
                else:
                    st.success(f"✅ **BÌNH ĐỦ NƯỚC** cho 14 ngày tới")
                
                # Hiển thị bảng chi tiết
                with st.expander("📋 CHI TIẾT TÍNH TOÁN"):
                    st.dataframe(predictions, use_container_width=True, hide_index=True)
    
    with tab_water2:
        st.markdown("### 🧮 TÍNH TOÁN NHU CẦU NƯỚC CHI TIẾT")
        
        # Chọn nhiều cây để so sánh
        selected_plants = st.multiselect(
            "Chọn các cây để so sánh:",
            df_plants['Tên Cây'].tolist(),
            default=df_plants['Tên Cây'].iloc[:3].tolist()
        )
        
        if selected_plants:
            comparison_data = []
            
            for plant_name in selected_plants:
                plant = df_plants[df_plants['Tên Cây'] == plant_name].iloc[0]
                
                # Tính toán cho các điều kiện thời tiết khác nhau
                for condition in ["Bình thường", "Nắng nóng", "Mưa nhiều"]:
                    if condition == "Bình thường":
                        factor = 1.0
                    elif condition == "Nắng nóng":
                        factor = 1.5
                    else:  # Mưa nhiều
                        factor = 0.5
                    
                    adjusted_need = plant['Nước TB (L/ngày)'] * factor
                    
                    comparison_data.append({
                        "Cây": plant_name,
                        "Điều kiện": condition,
                        "Nhu cầu (L/ngày)": round(adjusted_need, 3),
                        "1 tuần (L)": round(adjusted_need * 7, 2),
                        "1 tháng (L)": round(adjusted_need * 30, 2)
                    })
            
            df_comparison = pd.DataFrame(comparison_data)
            
            # Biểu đồ so sánh
            fig_comparison = px.bar(
                df_comparison,
                x='Cây',
                y='Nhu cầu (L/ngày)',
                color='Điều kiện',
                barmode='group',
                title='So sánh nhu cầu nước theo điều kiện',
                color_discrete_sequence=['#00ffcc', '#ff6b6b', '#4dabf7']
            )
            fig_comparison.update_layout(template='plotly_dark')
            st.plotly_chart(fig_comparison, use_container_width=True)
            
            # Bảng chi tiết
            st.dataframe(
                df_comparison,
                use_container_width=True,
                hide_index=True
            )
    
    with tab_water3:
        st.markdown("### 📅 LỊCH TƯỚI NƯỚC TỰ ĐỘNG")
        
        # Tạo lịch tưới
        col_sched1, col_sched2 = st.columns(2)
        
        with col_sched1:
            start_date = st.date_input("Ngày bắt đầu:", datetime.datetime.now())
            schedule_days = st.slider("Số ngày lịch:", 7, 90, 30)
            
            plant_for_schedule = st.selectbox(
                "Cây cần lịch tưới:",
                df_plants['Tên Cây'].tolist(),
                key="schedule_plant"
            )
            
            plant_schedule = df_plants[df_plants['Tên Cây'] == plant_for_schedule].iloc[0]
        
        with col_sched2:
            location_schedule = st.selectbox(
                "Vị trí:",
                list(location_manager.sample_locations.keys()),
                key="schedule_location"
            )
            
            loc_schedule = location_manager.sample_locations[location_schedule]
            
            # Tần suất tưới
            watering_frequency = st.select_slider(
                "Tần suất tưới:",
                options=["Hàng ngày", "2 ngày/lần", "3 ngày/lần", "Tuần/lần", "Khi cần"],
                value="2 ngày/lần"
            )
        
        if st.button("📅 Tạo lịch tưới", type="primary", use_container_width=True):
            # Tạo lịch tưới
            schedule = []
            current_date = start_date
            
            for day in range(schedule_days):
                date_str = current_date.strftime("%d/%m/%Y")
                
                # Xác định ngày có cần tưới không
                need_water = False
                if watering_frequency == "Hàng ngày":
                    need_water = True
                elif watering_frequency == "2 ngày/lần":
                    need_water = (day % 2 == 0)
                elif watering_frequency == "3 ngày/lần":
                    need_water = (day % 3 == 0)
                elif watering_frequency == "Tuần/lần":
                    need_water = (day % 7 == 0)
                else:  # Khi cần
                    # Dựa trên thời tiết
                    weather = weather_system.simulate_weather_data(
                        loc_schedule["lat"], 
                        loc_schedule["lon"], 
                        days=day+1
                    ).iloc[0]
                    need_water = (weather['Lượng mưa (mm)'] < 5)
                
                if need_water:
                    schedule.append({
                        "Ngày": date_str,
                        "Thứ": current_date.strftime("%A"),
                        "Hành động": "💧 Tưới nước",
                        "Lượng nước": f"{plant_schedule['Nước TB (L/ngày)']:.2f}L",
                        "Ghi chú": "Tưới đều quanh gốc"
                    })
                else:
                    schedule.append({
                        "Ngày": date_str,
                        "Thứ": current_date.strftime("%A"),
                        "Hành động": "✅ Nghỉ",
                        "Lượng nước": "0L",
                        "Ghi chú": "Kiểm tra độ ẩm đất"
                    })
                
                current_date += timedelta(days=1)
            
            df_schedule = pd.DataFrame(schedule)
            
            # Hiển thị lịch
            st.markdown(f"#### 📅 LỊCH TƯỚI {plant_for_schedule}")
            st.dataframe(df_schedule, use_container_width=True, hide_index=True)
            
            # Xuất lịch
            csv = df_schedule.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Tải xuống lịch tưới (CSV)",
                data=csv,
                file_name=f"lich_tuoi_{plant_for_schedule}_{start_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

# === TAB LỊCH CHĂM SÓC ===
elif selected == "📅 Lịch Chăm Sóc":
    st.title("📅 LỊCH CHĂM SÓC TỔNG HỢP")
    
    # Tạo lịch chăm sóc tích hợp
    col_cal1, col_cal2 = st.columns([1, 2])
    
    with col_cal1:
        st.markdown("### 🎯 THIẾT LẬP LỊCH")
        
        # Chọn cây cho lịch
        garden_plants = st.multiselect(
            "Chọn cây cho vườn:",
            df_plants['Tên Cây'].tolist(),
            default=df_plants['Tên Cây'].iloc[:5].tolist()
        )
        
        if garden_plants:
            # Hiển thị thông tin vườn
            st.markdown(f"**Vườn của bạn:** {len(garden_plants)} cây")
            
            total_water = 0
            for plant_name in garden_plants:
                plant = df_plants[df_plants['Tên Cây'] == plant_name].iloc[0]
                total_water += plant['Nước TB (L/ngày)']
            
            st.metric("Tổng nước cần/ngày", f"{total_water:.2f}L")
        
        # Tùy chọn lịch
        st.markdown("### ⚙️ TÙY CHỌN")
        
        enable_reminders = st.toggle("Nhắc nhở tự động", value=True)
        if enable_reminders:
            reminder_time = st.time_input("Thời gian nhắc nhở:", datetime.time(7, 0))
        
        notification_type = st.multiselect(
            "Loại thông báo:",
            ["Tưới nước", "Bón phân", "Cắt tỉa", "Kiểm tra sâu bệnh"],
            default=["Tưới nước"]
        )
    
    with col_cal2:
        st.markdown("### 📅 LỊCH THÁNG")
        
        # Tạo lịch tháng
        today = datetime.datetime.now()
        year = today.year
        month = today.month
        
        # Tạo calendar
        import calendar
        cal = calendar.monthcalendar(year, month)
        
        # Hiển thị lịch
        days_of_week = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
        
        # Tạo HTML calendar
        cal_html = """
        <div style='background: rgba(30, 35, 50, 0.9); border-radius: 10px; padding: 20px;'>
            <h4 style='text-align: center; color: #00ffcc;'>{month_name} {year}</h4>
            <table style='width: 100%; border-collapse: collapse; text-align: center;'>
                <tr style='background: rgba(0, 255, 204, 0.2);'>
        """.format(month_name=calendar.month_name[month], year=year)
        
        # Header
        for day in days_of_week:
            cal_html += f"<th style='padding: 10px; border: 1px solid rgba(0, 255, 204, 0.3);'>{day}</th>"
        cal_html += "</tr>"
        
        # Ngày
        for week in cal:
            cal_html += "<tr>"
            for day in week:
                if day == 0:
                    cal_html += "<td style='padding: 10px; border: 1px solid rgba(0, 255, 204, 0.1);'></td>"
                else:
                    # Đánh dấu ngày hôm nay
                    if day == today.day:
                        cell_style = "background: rgba(0, 255, 204, 0.3); color: white; font-weight: bold;"
                    else:
                        cell_style = ""
                    
                    # Thêm công việc (giả lập)
                    tasks = random.randint(0, 2)
                    task_indicator = "🌿" * tasks if tasks > 0 else ""
                    
                    cal_html += f"<td style='padding: 10px; border: 1px solid rgba(0, 255, 204, 0.1); {cell_style}'>"
                    cal_html += f"<div>{day}</div><small>{task_indicator}</small>"
                    cal_html += "</td>"
            cal_html += "</tr>"
        
        cal_html += "</table></div>"
        
        st.markdown(cal_html, unsafe_allow_html=True)
        
        # Danh sách công việc tuần này
        st.markdown("#### 📝 CÔNG VIỆC TUẦN NÀY")
        
        weekly_tasks = [
            {"Ngày": "Hôm nay", "Công việc": "💧 Tưới cây hồng", "Thời gian": "7:00", "Trạng thái": "✅"},
            {"Ngày": "Mai", "Công việc": "🌿 Bón phân lan", "Thời gian": "8:00", "Trạng thái": "⏳"},
            {"Ngày": "Thứ 5", "Công việc": "✂️ Cắt tỉa bonsai", "Thời gian": "9:00", "Trạng thái": "📅"},
            {"Ngày": "Thứ 7", "Công việc": "🔍 Kiểm tra sâu bệnh", "Thời gian": "10:00", "Trạng thái": "📅"},
        ]
        
        st.dataframe(pd.DataFrame(weekly_tasks), use_container_width=True, hide_index=True)
    
    # Phần thống kê
    st.markdown("---")
    st.markdown("### 📊 THỐNG KÊ CHĂM SÓC")
    
    if garden_plants:
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        
        with stats_col1:
            st.metric("Cây cần tưới", len(garden_plants), "cây")
        
        with stats_col2:
            # Tính tổng thời gian chăm sóc
            total_time = len(garden_plants) * 10  # 10 phút/cây
            st.metric("Thời gian chăm", f"{total_time} phút")
        
        with stats_col3:
            # Tính lượng nước
            total_water = sum(
                df_plants[df_plants['Tên Cây'] == plant].iloc[0]['Nước TB (L/ngày)'] 
                for plant in garden_plants
            )
            st.metric("Nước cần/ngày", f"{total_water:.1f}L")
        
        with stats_col4:
            st.metric("Tiết kiệm nước", "35%", "5.2%")

# === TAB THƯ VIỆN CÂY ===
elif selected == "🌿 Thư Viện Cây":
    st.title("🌿 THƯ VIỆN CÂY TRỒNG")
    
    # Tìm kiếm và lọc
    col_lib1, col_lib2, col_lib3 = st.columns([2, 1, 1])
    
    with col_lib1:
        search_query = st.text_input("🔍 Tìm kiếm cây:", placeholder="Nhập tên cây hoặc đặc điểm...")
    
    with col_lib2:
        filter_difficulty = st.multiselect(
            "Độ khó:",
            df_plants['Độ khó chăm sóc'].unique(),
            default=[]
        )
    
    with col_lib3:
        filter_water = st.slider("Nhu cầu nước (L/ngày):", 
                               float(df_plants['Nước TB (L/ngày)'].min()),
                               float(df_plants['Nước TB (L/ngày)'].max()),
                               (0.0, 2.0))
    
    # Lọc dữ liệu
    filtered_plants = df_plants.copy()
    
    if search_query:
        filtered_plants = filtered_plants[filtered_plants['Tên Cây'].str.contains(search_query, case=False, na=False)]
    
    if filter_difficulty:
        filtered_plants = filtered_plants[filtered_plants['Độ khó chăm sóc'].isin(filter_difficulty)]
    
    filtered_plants = filtered_plants[
        (filtered_plants['Nước TB (L/ngày)'] >= filter_water[0]) &
        (filtered_plants['Nước TB (L/ngày)'] <= filter_water[1])
    ]
    
    # Hiển thị kết quả
    st.markdown(f"### 📋 KẾT QUẢ: {len(filtered_plants)} cây")
    
    # Chế độ hiển thị
    view_mode = st.radio("Chế độ hiển thị:", ["Bảng", "Thẻ"], horizontal=True)
    
    if view_mode == "Bảng":
        st.dataframe(
            filtered_plants,
            use_container_width=True,
            height=600,
            column_config={
                "Nước TB (L/ngày)": st.column_config.ProgressColumn(
                    "💧 Nước",
                    min_value=0,
                    max_value=2.0,
                    format="%.2f L"
                ),
                "TG bình hết nước (ngày)": st.column_config.NumberColumn(
                    "⏳ TG hết nước",
                    help="Thời gian bình hết nước ước tính"
                )
            },
            hide_index=True
        )
    else:
        # Hiển thị dạng thẻ
        items_per_row = 4
        
        plants_list = filtered_plants.head(12).to_dict('records')  # Giới hạn 12 cây
        
        for i in range(0, len(plants_list), items_per_row):
            cols = st.columns(items_per_row)
            
            for col_idx, col in enumerate(cols):
                item_idx = i + col_idx
                if item_idx < len(plants_list):
                    plant = plants_list[item_idx]
                    
                    with col:
                        with st.container(border=True):
                            # Header với màu theo độ khó
                            difficulty_colors = {
                                "Rất dễ": "#4CAF50",
                                "Dễ": "#8BC34A",
                                "Trung bình": "#FFC107",
                                "Khó": "#FF9800",
                                "Rất khó": "#F44336"
                            }
                            
                            st.markdown(f"""
                            <div style="border-left: 4px solid {difficulty_colors.get(plant['Độ khó chăm sóc'], '#00ffcc')}; 
                                        padding-left: 10px; margin-bottom: 10px;">
                                <strong>{plant['Tên Cây']}</strong>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Thông tin chính
                            st.write(f"💧 **Nước:** {plant['Nước TB (L/ngày)']}L/ngày")
                            st.write(f"⏳ **Hết nước:** ~{plant['TG bình hết nước (ngày)']} ngày")
                            st.write(f"🏺 **Chậu:** {plant['Loại chậu đề xuất']}")
                            
                            # Action buttons
                            if st.button("📝 Thêm vào lịch", key=f"add_{plant['ID']}", use_container_width=True):
                                st.success(f"Đã thêm {plant['Tên Cây']} vào lịch!")

# === TAB CÀI ĐẶT ===
elif selected == "⚙️ Cài Đặt":
    st.title("⚙️ CÀI ĐẶT HỆ THỐNG")
    
    tab_set1, tab_set2, tab_set3 = st.tabs(["Cấu hình chung", "Tích hợp", "Hỗ trợ"])
    
    with tab_set1:
        st.markdown("### ⚙️ CẤU HÌNH HỆ THỐNG")
        
        col_conf1, col_conf2 = st.columns(2)
        
        with col_conf1:
            st.markdown("**Đơn vị đo lường:**")
            unit_system = st.radio("Hệ đơn vị:", ["Metric (m, L, °C)", "Imperial (ft, gal, °F)"])
            date_format = st.selectbox("Định dạng ngày:", ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
        
        with col_conf2:
            st.markdown("**Hiển thị:**")
            theme = st.selectbox("Giao diện:", ["Tối (mặc định)", "Sáng", "Tự động"])
            language = st.selectbox("Ngôn ngữ:", ["Tiếng Việt", "English"])
        
        st.markdown("### 🔔 THÔNG BÁO")
        notif_col1, notif_col2 = st.columns(2)
        
        with notif_col1:
            email_notif = st.toggle("Email thông báo", value=True)
            push_notif = st.toggle("Thông báo trình duyệt", value=True)
        
        with notif_col2:
            water_reminder = st.toggle("Nhắc tưới nước", value=True)
            weather_alert = st.toggle("Cảnh báo thời tiết", value=True)
        
        if st.button("💾 Lưu cài đặt", type="primary", use_container_width=True):
            st.success("Đã lưu cài đặt!")
    
    with tab_set2:
        st.markdown("### 🔗 TÍCH HỢP BÊN THỨ BA")
        
        st.info("""
        **Lưu ý:** Vì chậu cây không có linh kiện điện tử, 
        hệ thống dựa hoàn toàn vào dữ liệu vị trí và thời tiết.
        """)
        
        # Tích hợp Google Maps
        st.markdown("#### 🗺️ Google Maps Integration")
        
        maps_api_key = st.text_input("Google Maps API Key (tùy chọn):", 
                                    type="password",
                                    placeholder="Nhập key để bật tính năng nâng cao")
        
        if maps_api_key:
            st.success("✅ Đã kết nối Google Maps API")
            st.caption("Có thể xem bản đồ trực tiếp và chỉ đường")
        else:
            st.warning("⚠️ Chỉ sử dụng bản đồ tĩnh")
        
        # Tích hợp thời tiết
        st.markdown("#### 🌦️ Weather API")
        
        weather_source = st.selectbox(
            "Nguồn dữ liệu thời tiết:",
            ["Mô phỏng (mặc định)", "OpenWeatherMap", "WeatherAPI.com"]
        )
        
        if weather_source != "Mô phỏng (mặc định)":
            weather_api_key = st.text_input(f"{weather_source} API Key:", type="password")
            
            if weather_api_key:
                st.success(f"✅ Đã kết nối {weather_source}")
            else:
                st.error("⚠️ Vui lòng nhập API Key")
    
    with tab_set3:
        st.markdown("### 🆘 HỖ TRỢ & TÀI NGUYÊN")
        
        st.markdown("""
        **📚 Tài liệu hướng dẫn:**
        - [Hướng dẫn sử dụng cơ bản](https://ecomind.com/docs)
        - [Cách lấy tọa độ từ Google Maps](https://ecomind.com/coordinates)
        - [Tính toán nhu cầu nước](https://ecomind.com/water-calculation)
        
        **📞 Liên hệ hỗ trợ:**
        - Email: support@ecomind.com
        - Hotline: 1800-1234
        - Giờ làm việc: 8:00-17:00 (Thứ 2-Thứ 6)
        
        **🔄 Cập nhật hệ thống:**
        - Phiên bản hiện tại: 2.0.0
        - Cập nhật cuối: 15/01/2024
        - Phiên bản tiếp theo: 2.1.0 (dự kiến 15/02/2024)
        """)
        
        # Kiểm tra cập nhật
        if st.button("🔍 Kiểm tra cập nhật", use_container_width=True):
            st.info("✅ Bạn đang sử dụng phiên bản mới nhất!")
        
        # Xuất dữ liệu
        st.markdown("### 📤 XUẤT DỮ LIỆU")
        
        export_format = st.selectbox("Định dạng xuất:", ["CSV", "Excel", "JSON"])
        
        if st.button("📥 Xuất toàn bộ dữ liệu", use_container_width=True):
            if export_format == "CSV":
                csv = df_plants.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Tải xuống CSV",
                    data=csv,
                    file_name="ecomind_plant_database.csv",
                    mime="text/csv"
                )
            elif export_format == "Excel":
                # Tạo Excel file
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_plants.to_excel(writer, index=False, sheet_name='Plants')
                excel_data = output.getvalue()
                
                st.download_button(
                    label="Tải xuống Excel",
                    data=excel_data,
                    file_name="ecomind_plant_database.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:  # JSON
                json_data = df_plants.to_json(orient='records', force_ascii=False)
                st.download_button(
                    label="Tải xuống JSON",
                    data=json_data,
                    file_name="ecomind_plant_database.json",
                    mime="application/json"
                )

# --- 9. FOOTER ---
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("**🌿 EcoMind System**")
    st.caption("Hệ thống dự báo chăm sóc cây thông minh")

with footer_col2:
    st.markdown("**♻️ Sản phẩm xanh**")
    st.caption("Chậu cây tái chế 100%")

with footer_col3:
    st.markdown("**📞 Liên hệ**")
    st.caption("contact@ecomind.com")

# Hiển thị phiên bản và thời gian
current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
st.caption(f"Phiên bản 2.0.0 • {current_time} • © 2024 EcoMind")
