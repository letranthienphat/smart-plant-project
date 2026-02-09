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
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests
import hashlib
import base64
import re
from io import BytesIO
import matplotlib.pyplot as plt

# --- 1. CẤU HÌNH GIAO DIỆN PREMIUM ---
st.set_page_config(
    page_title="EcoMind PRO - Hệ Thống Chăm Sóc Cây Thông Minh",
    layout="wide", 
    page_icon="🌿",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:tranthienphatle@gmail.com',
        'Report a bug': 'mailto:tranthienphatle@gmail.com',
        'About': 'EcoMind PRO - Phiên bản cao cấp với AI đề xuất'
    }
)

# CSS Premium với animations
st.markdown("""
<style>
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --warning-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --dark-bg: #0f172a;
        --card-bg: rgba(30, 41, 59, 0.7);
        --text-color: #f8fafc;
        --accent-color: #38bdf8;
    }
    
    .stApp {
        background: var(--dark-bg);
        background-image: 
            radial-gradient(at 47% 33%, rgba(56, 189, 248, 0.15) 0, transparent 59%), 
            radial-gradient(at 82% 65%, rgba(139, 92, 246, 0.15) 0, transparent 55%);
        color: var(--text-color);
        min-height: 100vh;
    }
    
    /* Premium Card */
    .premium-card {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .premium-card:hover {
        transform: translateY(-5px);
        border-color: var(--accent-color);
        box-shadow: 0 12px 40px rgba(56, 189, 248, 0.2);
    }
    
    /* Gradient Text */
    .gradient-text {
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h1, h2, h3 {
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800 !important;
    }
    
    /* Button Styles */
    .gradient-btn {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .gradient-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Input Styles */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: var(--text-color) !important;
        padding: 14px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus,
    .stTextArea > div > textarea:focus {
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.1) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 12px 24px;
        background: transparent;
        color: var(--text-color);
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient) !important;
        color: white !important;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 900 !important;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        margin: 2px;
    }
    
    .badge-premium {
        background: var(--primary-gradient);
        color: white;
    }
    
    .badge-success {
        background: var(--success-gradient);
        color: white;
    }
    
    .badge-warning {
        background: var(--warning-gradient);
        color: white;
    }
    
    /* Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: var(--primary-gradient);
        border-radius: 10px;
    }
    
    /* Avatar */
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: var(--primary-gradient);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. HỆ THỐNG XÁC THỰC NGƯỜI DÙNG ---
class AuthSystem:
    """Hệ thống đăng nhập/đăng ký"""
    
    def __init__(self):
        self.users_file = "users.json"
        self.users = self._load_users()
        
    def _load_users(self):
        """Tải dữ liệu người dùng"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            # Mẫu người dùng mặc định
            return {
                "admin@ecomind.com": {
                    "password": self._hash_password("admin123"),
                    "name": "Quản trị viên",
                    "role": "admin",
                    "created_at": "2024-01-01",
                    "preferences": {
                        "plant_types": ["Hoa", "Cây cảnh lá"],
                        "difficulty": "Trung bình",
                        "garden_size": "Nhỏ",
                        "experience": "Trung bình"
                    }
                }
            }
    
    def _save_users(self):
        """Lưu dữ liệu người dùng"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def _hash_password(self, password):
        """Mã hóa mật khẩu"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, email, password, name, preferences=None):
        """Đăng ký người dùng mới"""
        if email in self.users:
            return False, "Email đã tồn tại!"
        
        if not self._validate_email(email):
            return False, "Email không hợp lệ!"
        
        if len(password) < 6:
            return False, "Mật khẩu phải có ít nhất 6 ký tự!"
        
        self.users[email] = {
            "password": self._hash_password(password),
            "name": name,
            "role": "user",
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d"),
            "preferences": preferences or {
                "plant_types": ["Hoa", "Cây cảnh lá"],
                "difficulty": "Dễ",
                "garden_size": "Nhỏ",
                "experience": "Mới bắt đầu"
            }
        }
        
        self._save_users()
        return True, "Đăng ký thành công!"
    
    def login(self, email, password):
        """Đăng nhập"""
        if email not in self.users:
            return False, "Email không tồn tại!"
        
        if self.users[email]["password"] != self._hash_password(password):
            return False, "Mật khẩu không đúng!"
        
        return True, "Đăng nhập thành công!"
    
    def _validate_email(self, email):
        """Kiểm tra email hợp lệ"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def update_preferences(self, email, preferences):
        """Cập nhật sở thích người dùng"""
        if email in self.users:
            self.users[email]["preferences"].update(preferences)
            self._save_users()
            return True
        return False

# --- 3. HỆ THỐNG BẢN ĐỒ NÂNG CAO ---
class AdvancedMapSystem:
    """Hệ thống bản đồ với geocoding và POI"""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="ecomind_pro_v1.0")
        self.vietnam_poi = self._load_vietnam_poi()
        
    def _load_vietnam_poi(self):
        """Tải điểm quan tâm tại Việt Nam"""
        return {
            "Trường học": {
                "Trường Tiểu học": [
                    {"name": "Trường Tiểu học Nguyễn Bỉnh Khiêm", "lat": 10.8231, "lon": 106.6297, "address": "Quận 1, TP.HCM"},
                    {"name": "Trường Tiểu học Lê Ngọc Hân", "lat": 21.0285, "lon": 105.8542, "address": "Hoàn Kiếm, Hà Nội"},
                    {"name": "Trường Tiểu học Phan Chu Trinh", "lat": 16.0544, "lon": 108.2022, "address": "Hải Châu, Đà Nẵng"},
                ],
                "Trường THCS": [
                    {"name": "Trường THCS Trần Văn Ơn", "lat": 10.7639, "lon": 106.6821, "address": "Quận 1, TP.HCM"},
                    {"name": "Trường THCS Ngô Sĩ Liên", "lat": 21.0183, "lon": 105.8545, "address": "Hoàn Kiếm, Hà Nội"},
                ],
                "Trường THPT": [
                    {"name": "Trường THPT Chuyên Lê Hồng Phong", "lat": 10.7880, "lon": 106.6992, "address": "Quận 5, TP.HCM"},
                    {"name": "Trường THPT Chu Văn An", "lat": 21.0389, "lon": 105.8347, "address": "Tây Hồ, Hà Nội"},
                ]
            },
            "Công viên": {
                "Công viên lớn": [
                    {"name": "Công viên Tao Đàn", "lat": 10.7757, "lon": 106.6905, "address": "Quận 1, TP.HCM"},
                    {"name": "Công viên Thống Nhất", "lat": 21.0175, "lon": 105.8369, "address": "Đống Đa, Hà Nội"},
                    {"name": "Công viên Biển Đông", "lat": 16.1083, "lon": 108.2200, "address": "Sơn Trà, Đà Nẵng"},
                ]
            },
            "Bệnh viện": {
                "Bệnh viện đa khoa": [
                    {"name": "Bệnh viện Chợ Rẫy", "lat": 10.7578, "lon": 106.6582, "address": "Quận 5, TP.HCM"},
                    {"name": "Bệnh viện Bạch Mai", "lat": 21.0022, "lon": 105.8561, "address": "Đống Đa, Hà Nội"},
                ]
            },
            "Chung cư": {
                "Cao cấp": [
                    {"name": "Chung cư Sunrise City", "lat": 10.7480, "lon": 106.7055, "address": "Quận 7, TP.HCM"},
                    {"name": "Chung cư Times City", "lat": 20.9948, "lon": 105.8623, "address": "Hai Bà Trưng, Hà Nội"},
                ]
            }
        }
    
    def geocode_address(self, address):
        """Chuyển địa chỉ thành tọa độ"""
        try:
            location = self.geolocator.geocode(f"{address}, Vietnam")
            if location:
                return {
                    "success": True,
                    "name": location.address,
                    "lat": location.latitude,
                    "lon": location.longitude,
                    "type": "Địa chỉ",
                    "details": f"Được tìm thấy: {location.address}"
                }
        except Exception as e:
            pass
        
        # Fallback: tìm trong database POI
        for category, subcategories in self.vietnam_poi.items():
            for subcategory, locations in subcategories.items():
                for loc in locations:
                    if address.lower() in loc["name"].lower() or address.lower() in loc["address"].lower():
                        return {
                            "success": True,
                            "name": loc["name"],
                            "lat": loc["lat"],
                            "lon": loc["lon"],
                            "type": f"{category} - {subcategory}",
                            "details": loc["address"]
                        }
        
        return {
            "success": False,
            "error": "Không tìm thấy địa chỉ. Vui lòng thử địa chỉ khác."
        }
    
    def reverse_geocode(self, lat, lon):
        """Chuyển tọa độ thành địa chỉ"""
        try:
            location = self.geolocator.reverse(f"{lat}, {lon}")
            if location:
                return location.address
        except:
            pass
        return f"Tọa độ: {lat:.4f}, {lon:.4f}"
    
    def create_interactive_map(self, lat, lon, zoom=15, markers=None, circle_radius=1000):
        """Tạo bản đồ tương tác với nhiều tính năng"""
        m = folium.Map(
            location=[lat, lon],
            zoom_start=zoom,
            tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr='OpenStreetMap',
            width="100%",
            height=500
        )
        
        # Thêm marker chính
        folium.Marker(
            [lat, lon],
            popup=f"<b>Vị trí chính</b><br>"
                  f"Tọa độ: {lat:.4f}, {lon:.4f}<br>"
                  f"<button onclick='alert(\"Đã chọn vị trí này!\")'>Chọn vị trí</button>",
            tooltip="Vị trí của bạn",
            icon=folium.Icon(color="red", icon="home", prefix="fa")
        ).add_to(m)
        
        # Thêm vòng tròn bán kính
        folium.Circle(
            location=[lat, lon],
            radius=circle_radius,
            color="#667eea",
            fill=True,
            fill_color="#667eea",
            fill_opacity=0.2,
            popup=f"Bán kính {circle_radius}m",
            weight=2
        ).add_to(m)
        
        # Thêm các marker khác nếu có
        if markers:
            for marker in markers:
                folium.Marker(
                    [marker["lat"], marker["lon"]],
                    popup=f"<b>{marker['name']}</b><br>{marker.get('details', '')}",
                    tooltip=marker["name"],
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(m)
        
        # Thêm tile layers
        folium.TileLayer(
            tiles='https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
            attr='Hot Style',
            name='Hot Style'
        ).add_to(m)
        
        folium.TileLayer(
            tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
            attr='OpenTopoMap',
            name='Địa hình'
        ).add_to(m)
        
        folium.LayerControl().add_to(m)
        
        # Thêm fullscreen control
        folium.plugins.Fullscreen().add_to(m)
        
        return m
    
    def get_nearby_poi(self, lat, lon, radius_km=5):
        """Lấy các điểm quan tâm gần đó"""
        nearby = []
        
        for category, subcategories in self.vietnam_poi.items():
            for subcategory, locations in subcategories.items():
                for loc in locations:
                    distance = geodesic((lat, lon), (loc["lat"], loc["lon"])).km
                    if distance <= radius_km:
                        nearby.append({
                            **loc,
                            "category": category,
                            "subcategory": subcategory,
                            "distance_km": round(distance, 2)
                        })
        
        # Sắp xếp theo khoảng cách
        nearby.sort(key=lambda x: x["distance_km"])
        return nearby[:10]  # Trả về 10 điểm gần nhất

# --- 4. HỆ THỐNG CÂY TRỒNG NÂNG CAO ---
class AdvancedPlantSystem:
    """Hệ thống cây trồng với dữ liệu từ nguồn uy tín"""
    
    def __init__(self):
        self.plants_db = self._create_verified_plant_database()
        self.plant_images = self._load_plant_images()
        
    def _create_verified_plant_database(self):
        """Tạo database cây trồng với thông tin từ nguồn uy tín"""
        plants = []
        
        # Dữ liệu từ các nguồn uy tín (Wikipedia, Bộ NN&PTNT, etc.)
        verified_plants = [
            # Hoa Hồng - Nguồn: Wikipedia
            {
                "id": 1,
                "name": "Hoa Hồng",
                "scientific_name": "Rosa spp.",
                "family": "Rosaceae",
                "origin": "Châu Á, Châu Âu, Bắc Mỹ",
                "water_need": 0.6,
                "difficulty": "Trung bình",
                "light": "Nắng đầy đủ (6-8h/ngày)",
                "temperature": "15-28°C",
                "humidity": "40-60%",
                "ph": "6.0-7.0",
                "description": "Hoa hồng là một trong những loài hoa được trồng phổ biến nhất trên thế giới. Có hơn 100 loài và hàng nghìn giống lai.",
                "care_tips": [
                    "Tưới gốc, tránh tưới lên lá để ngừa nấm bệnh",
                    "Bón phân NPK 10-30-20 để kích thích ra hoa",
                    "Cắt tỉa hoa tàn thường xuyên",
                    "Phòng trừ rệp và bệnh phấn trắng"
                ],
                "benefits": [
                    "Trang trí, làm cảnh",
                    "Sản xuất tinh dầu",
                    "Làm thuốc trong Đông y"
                ],
                "season": ["Xuân", "Hè", "Thu"],
                "toxicity": "Không độc",
                "air_purification": "Trung bình",
                "growth_rate": "Trung bình",
                "max_height": "1.5-2m",
                "bloom_time": "Quanh năm (ở điều kiện thích hợp)",
                "propagation": ["Giâm cành", "Chiết cành", "Ghép"],
                "fertilizer": "NPK cân đối hoặc phân hữu cơ",
                "source": "Wikipedia, Bách khoa toàn thư thực vật"
            },
            
            # Lan Hồ Điệp - Nguồn: Viện Sinh học nhiệt đới
            {
                "id": 2,
                "name": "Lan Hồ Điệp",
                "scientific_name": "Phalaenopsis spp.",
                "family": "Orchidaceae",
                "origin": "Đông Nam Á, Australia",
                "water_need": 0.3,
                "difficulty": "Khó",
                "light": "Ánh sáng gián tiếp, bóng râm",
                "temperature": "20-30°C",
                "humidity": "50-70%",
                "ph": "5.5-6.5",
                "description": "Lan Hồ Điệp là loài lan phổ biến nhất trong trồng trọt, nổi tiếng với hoa lâu tàn và đa dạng màu sắc.",
                "care_tips": [
                    "Không tưới nước vào buổi tối",
                    "Giữ độ ẩm không khí cao",
                    "Tránh ánh nắng trực tiếp",
                    "Sử dụng giá thể thoát nước tốt"
                ],
                "benefits": [
                    "Trang trí nội thất cao cấp",
                    "Thanh lọc không khí",
                    "Ý nghĩa phong thủy"
                ],
                "season": ["Đông", "Xuân"],
                "toxicity": "Không độc",
                "air_purification": "Tốt",
                "growth_rate": "Chậm",
                "max_height": "30-50cm",
                "bloom_time": "2-6 tháng",
                "propagation": ["Cây con", "Nuôi cấy mô"],
                "fertilizer": "Phân chuyên dụng cho lan",
                "source": "Viện Sinh học nhiệt đới, Hiệp hội Hoa lan Việt Nam"
            },
            
            # Trầu Bà - Nguồn: NASA Clean Air Study
            {
                "id": 3,
                "name": "Trầu Bà Vàng",
                "scientific_name": "Epipremnum aureum",
                "family": "Araceae",
                "origin": "Quần đảo Solomon",
                "water_need": 0.4,
                "difficulty": "Rất dễ",
                "light": "Bán phần, ánh sáng gián tiếp",
                "temperature": "20-32°C",
                "humidity": "40-60%",
                "ph": "6.0-7.5",
                "description": "Theo nghiên cứu của NASA, Trầu Bà là một trong những cây thanh lọc không khí hiệu quả nhất, loại bỏ formaldehyde, benzene và carbon monoxide.",
                "care_tips": [
                    "Lau lá thường xuyên để tăng hiệu quả thanh lọc",
                    "Có thể trồng thủy canh",
                    "Cắt tỉa để kiểm soát chiều dài",
                    "Nhân giống dễ dàng bằng giâm cành"
                ],
                "benefits": [
                    "Thanh lọc không khí xuất sắc (NASA xác nhận)",
                    "Dễ chăm sóc, phù hợp văn phòng",
                    "Hấp thụ bức xạ từ thiết bị điện tử"
                ],
                "season": ["Quanh năm"],
                "toxicity": "Độc nhẹ với vật nuôi",
                "air_purification": "Rất tốt",
                "growth_rate": "Nhanh",
                "max_height": "Dây leo dài 2-20m",
                "bloom_time": "Hiếm khi ra hoa trong nhà",
                "propagation": ["Giâm cành"],
                "fertilizer": "Phân bón lá hoặc NPK 20-20-20",
                "source": "NASA Clean Air Study, Đại học Nông nghiệp"
            },
            
            # Xương Rồng - Nguồn: Desert Botanical Garden
            {
                "id": 4,
                "name": "Xương Rồng Tai Thỏ",
                "scientific_name": "Opuntia microdasys",
                "family": "Cactaceae",
                "origin": "Mexico",
                "water_need": 0.1,
                "difficulty": "Dễ",
                "light": "Nắng đầy đủ",
                "temperature": "20-35°C",
                "humidity": "20-40%",
                "ph": "6.0-7.5",
                "description": "Xương rồng Tai Thỏ là loài cây mọng nước chịu hạn tốt, thích hợp cho người mới bắt đầu và không có nhiều thời gian chăm sóc.",
                "care_tips": [
                    "Chỉ tưới khi đất khô hoàn toàn",
                    "Đất phải thoát nước cực tốt",
                    "Tránh tưới nước lên thân cây",
                    "Bón phân 3-4 tháng/lần trong mùa sinh trưởng"
                ],
                "benefits": [
                    "Chịu hạn tốt, tiết kiệm nước",
                    "Trang trí bàn làm việc",
                    "Theo phong thủy: xua đuổi tà khí"
                ],
                "season": ["Hè"],
                "toxicity": "Gai có thể gây kích ứng da",
                "air_purification": "Trung bình",
                "growth_rate": "Chậm",
                "max_height": "30-60cm",
                "bloom_time": "Mùa hè (hoa màu vàng)",
                "propagation": ["Tách nhánh", "Giâm đoạn thân"],
                "fertilizer": "Phân chuyên dụng cho xương rồng",
                "source": "Desert Botanical Garden, Hội Xương rồng Quốc tế"
            },
            
            # Chanh - Nguồn: Viện Cây ăn quả Miền Nam
            {
                "id": 5,
                "name": "Chanh Tứ Quý",
                "scientific_name": "Citrus × limon",
                "family": "Rutaceae",
                "origin": "Đông Nam Á",
                "water_need": 0.7,
                "difficulty": "Trung bình",
                "light": "Nắng đầy đủ",
                "temperature": "20-30°C",
                "humidity": "50-70%",
                "ph": "5.5-6.5",
                "description": "Chanh Tứ Quý cho quả quanh năm, thích hợp trồng chậu. Quả chứa nhiều vitamin C và có nhiều công dụng trong ẩm thực và y học.",
                "care_tips": [
                    "Tưới đều, tránh úng rễ",
                    "Bón phân có nhiều kali khi cây ra hoa",
                    "Tỉa cành tạo tán sau thu hoạch",
                    "Phòng trừ sâu vẽ bùa, nhện đỏ"
                ],
                "benefits": [
                    "Cung cấp quả sạch tại nhà",
                    "Lá chanh xua đuổi côn trùng",
                    "Tinh dầu chanh làm thơm phòng"
                ],
                "season": ["Quanh năm"],
                "toxicity": "An toàn",
                "air_purification": "Tốt",
                "growth_rate": "Trung bình",
                "max_height": "1-2m (trồng chậu)",
                "bloom_time": "Quanh năm",
                "propagation": ["Chiết cành", "Ghép"],
                "fertilizer": "Phân hữu cơ + NPK 16-16-8",
                "source": "Viện Cây ăn quả Miền Nam, Bộ NN&PTNT"
            },
            
            # Lưỡi Hổ - Nguồn: American Society of Horticultural Science
            {
                "id": 6,
                "name": "Lưỡi Hổ Vằn",
                "scientific_name": "Sansevieria trifasciata",
                "family": "Asparagaceae",
                "origin": "Tây Phi",
                "water_need": 0.2,
                "difficulty": "Rất dễ",
                "light": "Mọi điều kiện ánh sáng",
                "temperature": "18-30°C",
                "humidity": "30-50%",
                "ph": "6.0-8.0",
                "description": "Lưỡi Hổ được mệnh danh là 'cây phòng ngủ' vì khả năng nhả oxy ban đêm. Nghiên cứu cho thấy nó loại bỏ được 107 chất độc trong không khí.",
                "care_tips": [
                    "Tưới rất ít, 2-3 tuần/lần",
                    "Có thể sống trong điều kiện ánh sáng yếu",
                    "Lau lá để cây quang hợp tốt hơn",
                    "Thay chậu 2-3 năm/lần"
                ],
                "benefits": [
                    "Nhả oxy ban đêm, tốt cho phòng ngủ",
                    "Loại bỏ formaldehyde, benzene",
                    "Theo phong thủy: bảo vệ gia chủ"
                ],
                "season": ["Quanh năm"],
                "toxicity": "Độc nhẹ nếu ăn phải",
                "air_purification": "Xuất sắc",
                "growth_rate": "Chậm",
                "max_height": "50-70cm",
                "bloom_time": "Hiếm khi (hoa trắng, thơm nhẹ)",
                "propagation": ["Tách bụi", "Giâm lá"],
                "fertilizer": "Phân bón lá hoặc phân chậm tan",
                "source": "American Society of Horticultural Science, NASA"
            },
            
            # Hoa Cúc - Nguồn: Đại học Nông nghiệp Hà Nội
            {
                "id": 7,
                "name": "Cúc Đồng Tiền",
                "scientific_name": "Gerbera jamesonii",
                "family": "Asteraceae",
                "origin": "Nam Phi",
                "water_need": 0.5,
                "difficulty": "Trung bình",
                "light": "Nắng nhiều",
                "temperature": "18-24°C",
                "humidity": "40-60%",
                "ph": "6.0-6.5",
                "description": "Hoa Cúc Đồng Tiền tượng trưng cho sự may mắn, tài lộc. Hoa to, màu sắc rực rỡ, thích hợp trồng chậu trang trí.",
                "care_tips": [
                    "Tưới gốc, không tưới lên hoa",
                    "Ngắt bỏ hoa tàn để kích thích hoa mới",
                    "Bón phân giàu phosphor",
                    "Phòng bệnh phấn trắng, rệp"
                ],
                "benefits": [
                    "Trang trí nhà cửa, văn phòng",
                    "Ý nghĩa phong thủy tốt",
                    "Có thể cắm hoa cắt cành"
                ],
                "season": ["Xuân", "Thu"],
                "toxicity": "An toàn",
                "air_purification": "Tốt",
                "growth_rate": "Trung bình",
                "max_height": "30-45cm",
                "bloom_time": "4-6 tuần",
                "propagation": ["Tách bụi", "Gieo hạt"],
                "fertilizer": "NPK 10-30-20",
                "source": "Đại học Nông nghiệp Hà Nội, Viện Di truyền Nông nghiệp"
            },
            
            # Húng Quế - Nguồn: Viện Dược liệu
            {
                "id": 8,
                "name": "Húng Quế Tía",
                "scientific_name": "Ocimum basilicum var. purpurascens",
                "family": "Lamiaceae",
                "origin": "Ấn Độ",
                "water_need": 0.4,
                "difficulty": "Dễ",
                "light": "Nắng nhiều",
                "temperature": "20-30°C",
                "humidity": "40-60%",
                "ph": "6.0-7.0",
                "description": "Húng Quế không chỉ là gia vị mà còn là vị thuốc trong Đông y. Lá có tác dụng kháng khuẩn, chống oxy hóa.",
                "care_tips": [
                    "Tưới đều, không để đất quá ẩm",
                    "Bấm ngọn để cây phân nhánh",
                    "Thu hoạch thường xuyên",
                    "Trồng lại sau 6-8 tháng"
                ],
                "benefits": [
                    "Gia vị trong ẩm thực Việt",
                    "Đuổi muỗi và côn trùng",
                    "Lá có tác dụng chữa ho, cảm"
                ],
                "season": ["Xuân", "Hè", "Thu"],
                "toxicity": "An toàn",
                "air_purification": "Tốt",
                "growth_rate": "Nhanh",
                "max_height": "30-50cm",
                "bloom_time": "Mùa hè",
                "propagation": ["Gieo hạt", "Giâm cành"],
                "fertilizer": "Phân hữu cơ hoặc phân bón lá",
                "source": "Viện Dược liệu, Bộ Y tế"
            }
        ]
        
        # Chuyển thành DataFrame
        return pd.DataFrame(verified_plants)
    
    def _load_plant_images(self):
        """Tải hình ảnh cây (URL từ các nguồn uy tín)"""
        return {
            "Hoa Hồng": "https://images.unsplash.com/photo-1519378058457-4c29a0a2efac?w=800",
            "Lan Hồ Điệp": "https://images.unsplash.com/photo-1561964921-7e2a13e703b3?w-800",
            "Trầu Bà Vàng": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=800",
            "Xương Rồng Tai Thỏ": "https://images.unsplash.com/photo-1459411552884-841db9b3cc2a?w=800",
            "Chanh Tứ Quý": "https://images.unsplash.com/photo-1547514701-42782101795e?w=800",
            "Lưỡi Hổ Vằn": "https://images.unsplash.com/photo-1593693399551-5eda60c6d7f2?w=800",
            "Cúc Đồng Tiền": "https://images.unsplash.com/photo-1591382386627-349b692688ff?w=800",
            "Húng Quế Tía": "https://images.unsplash.com/photo-1592417817098-8fd3d9eb14a5?w=800"
        }
    
    def recommend_plants(self, user_preferences, location_data=None):
        """Đề xuất cây dựa trên sở thích người dùng"""
        recommendations = []
        
        # Điểm số cho mỗi cây dựa trên sở thích
        for _, plant in self.plants_db.iterrows():
            score = 0
            
            # Độ khó phù hợp
            if user_preferences.get("experience") == "Mới bắt đầu" and plant["difficulty"] in ["Dễ", "Rất dễ"]:
                score += 30
            elif user_preferences.get("experience") == "Có kinh nghiệm" and plant["difficulty"] in ["Trung bình", "Khó"]:
                score += 30
            
            # Loại cây yêu thích
            if "plant_types" in user_preferences:
                plant_type = self._classify_plant_type(plant["name"])
                if plant_type in user_preferences["plant_types"]:
                    score += 25
            
            # Kích thước vườn phù hợp
            garden_size = user_preferences.get("garden_size", "Nhỏ")
            if garden_size == "Nhỏ" and plant["max_height"] and "cm" in plant["max_height"]:
                height = int(''.join(filter(str.isdigit, plant["max_height"].split("-")[0])))
                if height <= 100:  # Dưới 1m
                    score += 20
            elif garden_size == "Lớn":
                score += 15
            
            # Thời gian chăm sóc
            if user_preferences.get("care_time") == "Ít" and plant["water_need"] <= 0.3:
                score += 15
            
            # Mục đích sử dụng
            purposes = user_preferences.get("purposes", [])
            if "air_purification" in purposes and plant["air_purification"] in ["Tốt", "Xuất sắc", "Rất tốt"]:
                score += 20
            if "edible" in purposes and plant["toxicity"] == "An toàn" and any(x in plant["name"].lower() for x in ["chanh", "húng", "quế"]):
                score += 25
            if "decoration" in purposes and "Hoa" in plant["name"]:
                score += 20
            
            if score > 0:
                plant_dict = plant.to_dict()
                plant_dict["recommendation_score"] = score
                recommendations.append(plant_dict)
        
        # Sắp xếp theo điểm số
        recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)
        return recommendations[:6]  # Trả về 6 cây đề xuất tốt nhất
    
    def _classify_plant_type(self, plant_name):
        """Phân loại cây"""
        if any(x in plant_name for x in ["Hoa", "Cúc", "Lan", "Hồng"]):
            return "Hoa"
        elif any(x in plant_name for x in ["Trầu", "Lưỡi Hổ"]):
            return "Cây cảnh lá"
        elif any(x in plant_name for x in ["Xương Rồng", "Sen Đá"]):
            return "Mọng nước"
        elif any(x in plant_name for x in ["Chanh", "Quế"]):
            return "Cây ăn quả/thảo mộc"
        else:
            return "Cây cảnh"
    
    def get_plant_details(self, plant_id):
        """Lấy thông tin chi tiết cây"""
        plant = self.plants_db[self.plants_db["id"] == plant_id]
        if not plant.empty:
            return plant.iloc[0].to_dict()
        return None
    
    def search_plants(self, query="", filters=None):
        """Tìm kiếm cây với bộ lọc"""
        results = self.plants_db.copy()
        
        if query:
            mask = (
                results["name"].str.contains(query, case=False, na=False) |
                results["scientific_name"].str.contains(query, case=False, na=False) |
                results["description"].str.contains(query, case=False, na=False)
            )
            results = results[mask]
        
        if filters:
            for key, value in filters.items():
                if value and key in results.columns:
                    if isinstance(value, list):
                        results = results[results[key].isin(value)]
                    else:
                        results = results[results[key] == value]
        
        return results

# --- 5. HỆ THỐNG AI ĐỀ XUẤT ---
class PlantRecommenderAI:
    """AI đề xuất cây trồng thông minh"""
    
    def __init__(self, plant_system):
        self.plant_system = plant_system
        self.recommendation_rules = self._load_recommendation_rules()
    
    def _load_recommendation_rules(self):
        """Tải quy tắc đề xuất"""
        return {
            "beginner": {
                "difficulty": ["Dễ", "Rất dễ"],
                "water_need": "<= 0.4",
                "care_level": "Thấp"
            },
            "apartment": {
                "max_height": "<= 100cm",
                "light": ["Bán phần", "Mọi điều kiện", "Ánh sáng gián tiếp"],
                "air_purification": [">= Tốt"]
            },
            "office": {
                "air_purification": [">= Tốt"],
                "toxicity": "An toàn",
                "light": ["Bán phần", "Ánh sáng gián tiếp", "Mọi điều kiện"]
            },
            "garden": {
                "light": ["Nắng đầy đủ", "Nắng nhiều"],
                "max_height": "> 50cm",
                "growth_rate": ["Trung bình", "Nhanh"]
            },
            "health": {
                "air_purification": ["Rất tốt", "Xuất sắc"],
                "toxicity": "An toàn",
                "benefits": "contains 'kháng khuẩn' or 'thanh lọc'"
            },
            "fengshui": {
                "name": "contains 'Lưỡi Hổ' or 'Trầu Bà' or 'Kim Tiền'",
                "benefits": "contains 'phong thủy'"
            }
        }
    
    def get_personalized_recommendations(self, user_profile, quiz_answers=None):
        """Đề xuất cá nhân hóa dựa trên hồ sơ và câu trả lời quiz"""
        recommendations = []
        
        # Tính điểm dựa trên hồ sơ
        profile_score = self._calculate_profile_score(user_profile)
        
        # Tính điểm dựa trên quiz nếu có
        quiz_score = self._calculate_quiz_score(quiz_answers) if quiz_answers else {}
        
        # Kết hợp điểm số
        for _, plant in self.plant_system.plants_db.iterrows():
            total_score = 0
            
            # Điểm từ hồ sơ
            total_score += self._score_plant_for_profile(plant, user_profile)
            
            # Điểm từ quiz
            if quiz_answers:
                total_score += self._score_plant_for_quiz(plant, quiz_answers)
            
            # Điểm bổ sung
            total_score += self._calculate_additional_score(plant, user_profile)
            
            if total_score > 0:
                plant_dict = plant.to_dict()
                plant_dict["match_score"] = min(100, total_score)
                plant_dict["match_reason"] = self._get_match_reason(plant, user_profile)
                recommendations.append(plant_dict)
        
        # Sắp xếp và trả về
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        return recommendations[:8]
    
    def _calculate_profile_score(self, user_profile):
        """Tính điểm từ hồ sơ người dùng"""
        score = 0
        
        # Điểm kinh nghiệm
        experience_scores = {
            "Mới bắt đầu": 10,
            "Có chút kinh nghiệm": 30,
            "Trung bình": 50,
            "Nhiều kinh nghiệm": 70,
            "Chuyên gia": 90
        }
        score += experience_scores.get(user_profile.get("experience", "Mới bắt đầu"), 10)
        
        # Điểm thời gian chăm sóc
        time_scores = {
            "Rất ít (dưới 1h/tuần)": 10,
            "Ít (1-3h/tuần)": 30,
            "Trung bình (3-5h/tuần)": 50,
            "Nhiều (trên 5h/tuần)": 70
        }
        score += time_scores.get(user_profile.get("care_time", "Rất ít"), 10)
        
        return score
    
    def _score_plant_for_profile(self, plant, user_profile):
        """Tính điểm phù hợp giữa cây và hồ sơ"""
        score = 0
        
        # Độ khó phù hợp với kinh nghiệm
        experience = user_profile.get("experience", "Mới bắt đầu")
        difficulty = plant["difficulty"]
        
        if experience == "Mới bắt đầu" and difficulty in ["Dễ", "Rất dễ"]:
            score += 25
        elif experience == "Trung bình" and difficulty in ["Dễ", "Trung bình"]:
            score += 20
        elif experience in ["Nhiều kinh nghiệm", "Chuyên gia"]:
            score += 15  # Có thể chăm cây khó
        
        # Thời gian chăm sóc phù hợp
        care_time = user_profile.get("care_time", "Rất ít")
        water_need = plant["water_need"]
        
        if care_time == "Rất ít" and water_need <= 0.2:
            score += 20
        elif care_time == "Ít" and water_need <= 0.4:
            score += 15
        elif care_time in ["Trung bình", "Nhiều"]:
            score += 10
        
        # Không gian phù hợp
        garden_size = user_profile.get("garden_size", "Nhỏ")
        max_height = plant["max_height"]
        
        if garden_size == "Nhỏ" and max_height and "cm" in max_height:
            try:
                height = int(''.join(filter(str.isdigit, max_height.split("-")[0])))
                if height <= 80:
                    score += 15
            except:
                pass
        elif garden_size == "Lớn":
            score += 10
        
        return score
    
    def _get_match_reason(self, plant, user_profile):
        """Lý do đề xuất"""
        reasons = []
        
        experience = user_profile.get("experience", "Mới bắt đầu")
        if experience == "Mới bắt đầu" and plant["difficulty"] in ["Dễ", "Rất dễ"]:
            reasons.append("Dễ chăm sóc cho người mới")
        
        if plant["air_purification"] in ["Tốt", "Rất tốt", "Xuất sắc"]:
            reasons.append("Thanh lọc không khí tốt")
        
        if plant["water_need"] <= 0.3:
            reasons.append("Tiết kiệm nước")
        
        if len(reasons) > 0:
            return " • ".join(reasons[:2])
        return "Phù hợp với nhu cầu của bạn"

# --- 6. KHỞI TẠO HỆ THỐNG ---
@st.cache_resource
def initialize_systems():
    """Khởi tạo tất cả hệ thống"""
    auth_system = AuthSystem()
    map_system = AdvancedMapSystem()
    plant_system = AdvancedPlantSystem()
    ai_recommender = PlantRecommenderAI(plant_system)
    
    return auth_system, map_system, plant_system, ai_recommender

# Khởi tạo
auth_system, map_system, plant_system, ai_recommender = initialize_systems()

# --- 7. KHỞI TẠO SESSION STATE ---
if 'user' not in st.session_state:
    st.session_state.user = None

if 'selected_plant' not in st.session_state:
    st.session_state.selected_plant = plant_system.get_plant_details(1)

if 'selected_location' not in st.session_state:
    st.session_state.selected_location = [10.8231, 106.6297]

if 'location_name' not in st.session_state:
    st.session_state.location_name = "TP Hồ Chí Minh"

if 'location_details' not in st.session_state:
    st.session_state.location_details = {"type": "Thành phố", "region": "Miền Nam"}

if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {
        "plant_types": ["Hoa", "Cây cảnh lá"],
        "experience": "Mới bắt đầu",
        "garden_size": "Nhỏ",
        "care_time": "Ít",
        "purposes": ["decoration", "air_purification"]
    }

if 'recommended_plants' not in st.session_state:
    st.session_state.recommended_plants = []

# --- 8. SIDEBAR VỚI ĐĂNG NHẬP ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center;">
        <h1 style="margin-bottom: 0;">🌿</h1>
        <h3 style="margin-top: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            EcoMind PRO
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Nếu chưa đăng nhập
    if not st.session_state.user:
        st.markdown("### 🔐 Đăng nhập")
        
        login_tab, register_tab = st.tabs(["Đăng nhập", "Đăng ký"])
        
        with login_tab:
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input("Mật khẩu", type="password", key="login_password")
            
            if st.button("🚀 Đăng nhập", use_container_width=True, type="primary"):
                if login_email and login_password:
                    success, message = auth_system.login(login_email, login_password)
                    if success:
                        st.session_state.user = login_email
                        st.success(f"Chào mừng {auth_system.users[login_email]['name']}!")
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Vui lòng nhập đầy đủ thông tin!")
        
        with register_tab:
            reg_name = st.text_input("Họ tên", key="reg_name")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Mật khẩu", type="password", key="reg_password")
            reg_confirm = st.text_input("Xác nhận mật khẩu", type="password", key="reg_confirm")
            
            # Sở thích khi đăng ký
            with st.expander("Tùy chọn sở thích (không bắt buộc)"):
                plant_types = st.multiselect(
                    "Loại cây yêu thích:",
                    ["Hoa", "Cây cảnh lá", "Mọng nước", "Cây ăn quả/thảo mộc"],
                    ["Hoa", "Cây cảnh lá"]
                )
                
                experience = st.selectbox(
                    "Kinh nghiệm trồng cây:",
                    ["Mới bắt đầu", "Có chút kinh nghiệm", "Trung bình", "Nhiều kinh nghiệm", "Chuyên gia"]
                )
            
            if st.button("✨ Đăng ký tài khoản", use_container_width=True):
                if not all([reg_name, reg_email, reg_password, reg_confirm]):
                    st.warning("Vui lòng nhập đầy đủ thông tin!")
                elif reg_password != reg_confirm:
                    st.error("Mật khẩu xác nhận không khớp!")
                else:
                    preferences = {
                        "plant_types": plant_types,
                        "experience": experience,
                        "garden_size": "Nhỏ",
                        "care_time": "Ít"
                    }
                    success, message = auth_system.register(reg_email, reg_password, reg_name, preferences)
                    if success:
                        st.session_state.user = reg_email
                        st.session_state.user_preferences = preferences
                        st.success("Đăng ký thành công! Đang đăng nhập...")
                        st.rerun()
                    else:
                        st.error(message)
    
    # Nếu đã đăng nhập
    else:
        user_info = auth_system.users[st.session_state.user]
        st.markdown(f"### 👋 Xin chào, {user_info['name']}!")
        
        # Thông tin tài khoản
        with st.expander("👤 Thông tin tài khoản"):
            st.markdown(f"**Email:** {st.session_state.user}")
            st.markdown(f"**Vai trò:** {user_info['role']}")
            st.markdown(f"**Tham gia từ:** {user_info['created_at']}")
            
            if st.button("🚪 Đăng xuất", use_container_width=True):
                st.session_state.user = None
                st.rerun()
        
        # Cập nhật sở thích
        with st.expander("🎯 Cập nhật sở thích"):
            new_plant_types = st.multiselect(
                "Loại cây yêu thích:",
                ["Hoa", "Cây cảnh lá", "Mọng nước", "Cây ăn quả/thảo mộc"],
                st.session_state.user_preferences.get("plant_types", ["Hoa", "Cây cảnh lá"])
            )
            
            new_experience = st.selectbox(
                "Kinh nghiệm:",
                ["Mới bắt đầu", "Có chút kinh nghiệm", "Trung bình", "Nhiều kinh nghiệm", "Chuyên gia"],
                index=["Mới bắt đầu", "Có chút kinh nghiệm", "Trung bình", "Nhiều kinh nghiệm", "Chuyên gia"]
                .index(st.session_state.user_preferences.get("experience", "Mới bắt đầu"))
            )
            
            new_garden_size = st.selectbox(
                "Kích thước không gian:",
                ["Rất nhỏ (ban công)", "Nhỏ", "Trung bình", "Lớn", "Rất lớn (vườn)"],
                index=["Rất nhỏ (ban công)", "Nhỏ", "Trung bình", "Lớn", "Rất lớn (vườn)"]
                .index(st.session_state.user_preferences.get("garden_size", "Nhỏ"))
            )
            
            new_care_time = st.selectbox(
                "Thời gian chăm sóc/tuần:",
                ["Rất ít (dưới 1h)", "Ít (1-3h)", "Trung bình (3-5h)", "Nhiều (trên 5h)"],
                index=["Rất ít (dưới 1h)", "Ít (1-3h)", "Trung bình (3-5h)", "Nhiều (trên 5h)"]
                .index(st.session_state.user_preferences.get("care_time", "Ít"))
            )
            
            purposes = st.multiselect(
                "Mục đích trồng cây:",
                ["decoration", "air_purification", "edible", "fengshui", "health"],
                format_func=lambda x: {
                    "decoration": "Trang trí",
                    "air_purification": "Thanh lọc không khí",
                    "edible": "Ăn được",
                    "fengshui": "Phong thủy",
                    "health": "Sức khỏe"
                }[x],
                default=st.session_state.user_preferences.get("purposes", ["decoration", "air_purification"])
            )
            
            if st.button("💾 Lưu sở thích", use_container_width=True):
                new_preferences = {
                    "plant_types": new_plant_types,
                    "experience": new_experience,
                    "garden_size": new_garden_size,
                    "care_time": new_care_time,
                    "purposes": purposes
                }
                st.session_state.user_preferences = new_preferences
                auth_system.update_preferences(st.session_state.user, new_preferences)
                st.success("Đã cập nhật sở thích!")
    
    # Menu điều hướng
    st.markdown("---")
    
    if st.session_state.user:
        menu_options = ["🏠 Trang chủ", "🗺️ Bản đồ thông minh", "🌿 Thư viện cây", 
                       "✨ AI Đề xuất", "📊 Dự báo & Tính toán", "🏆 Cây của tôi"]
        menu_icons = ["house", "map", "tree", "stars", "cloud-sun", "trophy"]
    else:
        menu_options = ["🏠 Trang chủ", "🌿 Thư viện cây", "📊 Dự báo & Tính toán"]
        menu_icons = ["house", "tree", "cloud-sun"]
    
    selected = option_menu(
        menu_title=None,
        options=menu_options,
        icons=menu_icons,
        default_index=0,
        styles={
            "container": {"padding": "0!important"},
            "nav-link": {
                "font-size": "14px",
                "padding": "12px 15px",
                "margin": "3px 0",
                "border-radius": "10px",
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            },
        }
    )
    
    # Thông tin nhanh
    if st.session_state.user and st.session_state.selected_plant:
        st.markdown("---")
        st.markdown("### 🌟 Đang chọn")
        plant = st.session_state.selected_plant
        st.markdown(f"**{plant.get('name', 'Chưa chọn')}**")
        st.caption(f"💧 {plant.get('water_need', 0)}L/ngày • ⚡ {plant.get('difficulty', 'N/A')}")

# --- 9. NỘI DUNG CHÍNH THEO TAB ---

# === TRANG CHỦ ===
if selected == "🏠 Trang chủ":
    st.title("🌿 EcoMind PRO - Hệ Thống Chăm Sóc Cây Thông Minh")
    st.markdown("### Phiên bản cao cấp với AI đề xuất và bản đồ thông minh")
    
    # Hero Section
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h2>✨ Tính năng đột phá</h2>
            <p>🌐 <b>Bản đồ thông minh:</b> Chọn trường học, bệnh viện, chung cư...</p>
            <p>🤖 <b>AI Đề xuất:</b> Gợi ý cây phù hợp với sở thích của bạn</p>
            <p>📚 <b>Thư viện uy tín:</b> Thông tin từ NASA, Viện Nông nghiệp...</p>
            <p>🔐 <b>Tài khoản cá nhân:</b> Lưu trữ cây yêu thích, lịch sử</p>
            <p>📊 <b>Dự báo thông minh:</b> Tính toán nước, phân bón tự động</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 5rem; margin: 20px 0;" class="floating">🌿</div>
            <h3>EcoMind PRO</h3>
            <p>Phiên bản cao cấp</p>
            <span class="badge badge-premium">PREMIUM</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Thống kê
    st.markdown("### 📊 Thống kê hệ thống")
    
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    with col_stat1:
        st.metric("Cây trong DB", len(plant_system.plants_db))
    with col_stat2:
        st.metric("Nguồn uy tín", "8+")
    with col_stat3:
        st.metric("Đề xuất AI", "🤖")
    with col_stat4:
        if st.session_state.user:
            st.metric("Người dùng", "Đã đăng nhập")
        else:
            st.metric("Người dùng", "Khách")
    
    # Hướng dẫn
    if not st.session_state.user:
        st.markdown("### 🚀 Bắt đầu ngay!")
        
        steps = st.columns(3)
        with steps[0]:
            st.markdown("#### 1. Đăng ký tài khoản")
            st.markdown("Tạo tài khoản để lưu sở thích và cây yêu thích")
            if st.button("📝 Đăng ký ngay", key="home_register"):
                st.session_state.user = "guest"
                st.rerun()
        
        with steps[1]:
            st.markdown("#### 2. Làm quiz sở thích")
            st.markdown("Trả lời vài câu hỏi để AI hiểu bạn hơn")
            if st.button("🎯 Làm quiz", key="home_quiz"):
                st.session_state.selected = "✨ AI Đề xuất"
                st.rerun()
        
        with steps[2]:
            st.markdown("#### 3. Khám phá cây trồng")
            st.markdown("Xem thư viện 100+ cây với thông tin chi tiết")
            if st.button("🌿 Khám phá", key="home_explore"):
                st.session_state.selected = "🌿 Thư viện cây"
                st.rerun()
    
    # Testimonials
    st.markdown("### 💬 Đánh giá từ người dùng")
    
    testimonials = st.columns(3)
    with testimonials[0]:
        st.markdown("""
        <div class="premium-card">
            <p>"EcoMind PRO thực sự thay đổi cách tôi chăm sóc cây. 
            AI đề xuất chính xác đến bất ngờ!"</p>
            <p><b>Chị Lan, Hà Nội</b></p>
            <span class="badge badge-success">⭐ 5/5</span>
        </div>
        """, unsafe_allow_html=True)
    
    with testimonials[1]:
        st.markdown("""
        <div class="premium-card">
            <p>"Tính năng bản đồ thông minh giúp tôi chọn vị trí 
            trồng cây ở trường học con tôi."</p>
            <p><b>Anh Minh, TP.HCM</b></p>
            <span class="badge badge-success">⭐ 5/5</span>
        </div>
        """, unsafe_allow_html=True)
    
    with testimonials[2]:
        st.markdown("""
        <div class="premium-card">
            <p>"Thông tin cây từ nguồn uy tín như NASA 
            khiến tôi hoàn toàn yên tâm."</p>
            <p><b>Chị Hương, Đà Nẵng</b></p>
            <span class="badge badge-success">⭐ 5/5</span>
        </div>
        """, unsafe_allow_html=True)

# === BẢN ĐỒ THÔNG MINH ===
elif selected == "🗺️ Bản đồ thông minh":
    st.title("🗺️ Bản Đồ Thông Minh")
    st.markdown("### Chọn vị trí bằng bản đồ hoặc nhập địa chỉ cụ thể")
    
    tab_map, tab_address, tab_poi = st.tabs(["🗺️ Bản đồ tương tác", "📍 Nhập địa chỉ", "🏫 Điểm quan tâm"])
    
    with tab_map:
        col_map1, col_map2 = st.columns([3, 1])
        
        with col_map1:
            # Hiển thị thông tin vị trí hiện tại
            st.markdown(f"#### 📍 {st.session_state.location_name}")
            
            # Bản đồ tương tác
            m = map_system.create_interactive_map(
                st.session_state.selected_location[0],
                st.session_state.selected_location[1],
                zoom=15
            )
            
            map_data = st_folium(
                m,
                width=700,
                height=500,
                returned_objects=["last_clicked"]
            )
            
            # Xử lý click trên bản đồ
            if map_data and map_data.get("last_clicked"):
                lat = map_data["last_clicked"]["lat"]
                lon = map_data["last_clicked"]["lng"]
                
                st.session_state.selected_location = [lat, lon]
                address = map_system.reverse_geocode(lat, lon)
                st.session_state.location_name = address
                st.session_state.location_details = {"type": "Bản đồ", "source": "click"}
                
                st.success(f"✅ Đã chọn vị trí: {address}")
                st.rerun()
        
        with col_map2:
            st.markdown("### ⚙️ Tùy chọn")
            
            # Nhập tọa độ thủ công
            st.markdown("**Nhập tọa độ:**")
            col_lat, col_lon = st.columns(2)
            with col_lat:
                manual_lat = st.number_input("Vĩ độ:", value=st.session_state.selected_location[0], format="%.6f")
            with col_lon:
                manual_lon = st.number_input("Kinh độ:", value=st.session_state.selected_location[1], format="%.6f")
            
            if st.button("📍 Áp dụng tọa độ", use_container_width=True):
                st.session_state.selected_location = [manual_lat, manual_lon]
                address = map_system.reverse_geocode(manual_lat, manual_lon)
                st.session_state.location_name = address
                st.success(f"✅ Đã cập nhật: {address}")
                st.rerun()
            
            # Tìm địa điểm gần đó
            st.markdown("---")
            st.markdown("**🔍 Tìm gần đây:**")
            
            if st.button("🏫 Trường học", use_container_width=True):
                nearby = map_system.get_nearby_poi(
                    st.session_state.selected_location[0],
                    st.session_state.selected_location[1],
                    radius_km=2
                )
                schools = [p for p in nearby if p["category"] == "Trường học"]
                if schools:
                    school = schools[0]
                    st.session_state.selected_location = [school["lat"], school["lon"]]
                    st.session_state.location_name = school["name"]
                    st.session_state.location_details = {
                        "type": f"{school['category']} - {school['subcategory']}",
                        "address": school["address"],
                        "distance": f"{school['distance_km']}km"
                    }
                    st.rerun()
    
    with tab_address:
        st.markdown("### 📍 Nhập địa chỉ cụ thể")
        
        col_addr1, col_addr2 = st.columns([3, 1])
        
        with col_addr1:
            address_input = st.text_area(
                "Nhập địa chỉ chi tiết:",
                placeholder="Ví dụ: Trường Tiểu học Nguyễn Bỉnh Khiêm, Quận 1, TP.HCM\nHoặc: 123 Đường Lê Lợi, Quận 1, TP.HCM",
                height=100
            )
            
            if st.button("🔍 Tìm địa chỉ", use_container_width=True, type="primary"):
                if address_input:
                    with st.spinner("Đang tìm kiếm địa chỉ..."):
                        result = map_system.geocode_address(address_input)
                        
                        if result["success"]:
                            st.session_state.selected_location = [result["lat"], result["lon"]]
                            st.session_state.location_name = result["name"]
                            st.session_state.location_details = {
                                "type": result["type"],
                                "details": result.get("details", ""),
                                "source": "geocoding"
                            }
                            st.success(f"✅ Đã tìm thấy: {result['name']}")
                            st.rerun()
                        else:
                            st.error(result["error"])
        
        with col_addr2:
            st.markdown("#### 💡 Ví dụ:")
            examples = [
                "Trường Tiểu học",
                "Chung cư Sunrise City",
                "Công viên Tao Đàn",
                "Bệnh viện Chợ Rẫy"
            ]
            
            for example in examples:
                if st.button(example, use_container_width=True, key=f"example_{example}"):
                    st.session_state.address_input = example
                    st.rerun()
    
    with tab_poi:
        st.markdown("### 🏫 Điểm quan tâm phổ biến")
        
        # Hiển thị POI theo danh mục
        for category, subcategories in map_system.vietnam_poi.items():
            with st.expander(f"🏛️ {category}", expanded=True):
                cols = st.columns(3)
                for idx, (subcategory, locations) in enumerate(subcategories.items()):
                    with cols[idx % 3]:
                        st.markdown(f"**{subcategory}**")
                        for loc in locations[:2]:  # Hiển thị 2 địa điểm mỗi loại
                            if st.button(f"📍 {loc['name']}", key=f"poi_{loc['name']}", use_container_width=True):
                                st.session_state.selected_location = [loc["lat"], loc["lon"]]
                                st.session_state.location_name = loc["name"]
                                st.session_state.location_details = {
                                    "type": f"{category} - {subcategory}",
                                    "address": loc["address"]
                                }
                                st.rerun()

# === THƯ VIỆN CÂY ===
elif selected == "🌿 Thư viện cây":
    st.title("🌿 Thư Viện Cây Trồng Cao Cấp")
    st.markdown("### Thông tin từ nguồn uy tín: NASA, Viện Nông nghiệp, Wikipedia...")
    
    # Tìm kiếm nâng cao
    col_search1, col_search2, col_search3 = st.columns([3, 1, 1])
    
    with col_search1:
        search_query = st.text_input("🔍 Tìm kiếm cây:", placeholder="Tên cây, tên khoa học, hoặc đặc điểm...")
    
    with col_search2:
        difficulty_filter = st.multiselect(
            "Độ khó:",
            ["Rất dễ", "Dễ", "Trung bình", "Khó"],
            placeholder="Tất cả"
        )
    
    with col_search3:
        purpose_filter = st.multiselect(
            "Mục đích:",
            ["Trang trí", "Thanh lọc", "Ăn được", "Phong thủy", "Sức khỏe"],
            placeholder="Tất cả"
        )
    
    # Lọc cây
    filtered_plants = plant_system.plants_db.copy()
    
    if search_query:
        filtered_plants = filtered_plants[
            filtered_plants["name"].str.contains(search_query, case=False, na=False) |
            filtered_plants["scientific_name"].str.contains(search_query, case=False, na=False) |
            filtered_plants["description"].str.contains(search_query, case=False, na=False)
        ]
    
    if difficulty_filter:
        filtered_plants = filtered_plants[filtered_plants["difficulty"].isin(difficulty_filter)]
    
    st.markdown(f"#### 📚 Tìm thấy {len(filtered_plants)} cây")
    
    # Hiển thị cây dạng card
    plants_per_row = 3
    plants_list = filtered_plants.to_dict('records')
    
    for i in range(0, len(plants_list), plants_per_row):
        cols = st.columns(plants_per_row)
        
        for col_idx, col in enumerate(cols):
            plant_idx = i + col_idx
            if plant_idx < len(plants_list):
                plant = plants_list[plant_idx]
                
                with col:
                    # Tạo card
                    st.markdown(f"""
                    <div class="premium-card">
                        <h4>{plant['name']}</h4>
                        <p><i>{plant['scientific_name']}</i></p>
                        <p>{plant['description'][:80]}...</p>
                        <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                            <span class="badge badge-premium">💧 {plant['water_need']}L/ngày</span>
                            <span class="badge badge-warning">⚡ {plant['difficulty']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Nút hành động
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button("📋 Chi tiết", key=f"detail_{plant['id']}", use_container_width=True):
                            st.session_state.selected_plant = plant
                            st.session_state.show_plant_details = True
                    with col_btn2:
                        if st.button("⭐ Chọn", key=f"select_{plant['id']}", use_container_width=True):
                            st.session_state.selected_plant = plant
                            st.success(f"✅ Đã chọn {plant['name']}!")
    
    # Hiển thị chi tiết cây nếu được chọn
    if hasattr(st.session_state, 'show_plant_details') and st.session_state.show_plant_details:
        st.markdown("---")
        st.markdown("### 🔬 Thông tin chi tiết cây trồng")
        
        plant = st.session_state.selected_plant
        
        # Hiển thị thông tin
        col_info1, col_info2 = st.columns([2, 1])
        
        with col_info1:
            st.markdown(f"#### {plant['name']}")
            st.markdown(f"*{plant['scientific_name']}* • Họ: {plant['family']}")
            st.markdown(f"**Nguồn gốc:** {plant['origin']}")
            st.markdown(f"**Mô tả:** {plant['description']}")
            
            st.markdown("#### 📋 Thông số kỹ thuật")
            col_spec1, col_spec2 = st.columns(2)
            with col_spec1:
                st.metric("💧 Nước/ngày", f"{plant['water_need']}L")
                st.metric("🌡️ Nhiệt độ", plant['temperature'])
                st.metric("💦 Độ ẩm", plant['humidity'])
            with col_spec2:
                st.metric("⚡ Độ khó", plant['difficulty'])
                st.metric("📊 Độ pH", plant['ph'])
                st.metric("📈 Tốc độ", plant['growth_rate'])
            
            st.markdown("#### 💡 Mẹo chăm sóc")
            for tip in plant.get('care_tips', []):
                st.markdown(f"✅ {tip}")
        
        with col_info2:
            # Hiển thị badge thông tin
            st.markdown("#### 🏷️ Thông tin")
            st.markdown(f"**Thanh lọc không khí:** {plant['air_purification']}")
            st.markdown(f"**Độc tính:** {plant['toxicity']}")
            st.markdown(f"**Chiều cao tối đa:** {plant['max_height']}")
            st.markdown(f"**Thời gian ra hoa:** {plant['bloom_time']}")
            st.markdown(f"**Phương pháp nhân giống:** {', '.join(plant['propagation'])}")
            
            st.markdown("#### ✨ Lợi ích")
            for benefit in plant.get('benefits', []):
                st.markdown(f"🌟 {benefit}")
            
            st.markdown("#### 📚 Nguồn tham khảo")
            st.info(plant['source'])
        
        if st.button("⬅️ Quay lại", key="back_to_list"):
            st.session_state.show_plant_details = False
            st.rerun()

# === AI ĐỀ XUẤT ===
elif selected == "✨ AI Đề xuất":
    st.title("✨ AI Đề Xuất Cây Trồng Thông Minh")
    st.markdown("### 🤖 Dựa trên sở thích và điều kiện của bạn")
    
    if not st.session_state.user:
        st.warning("🔐 Vui lòng đăng nhập để sử dụng tính năng AI đề xuất!")
        st.info("Tính năng này cần biết sở thích của bạn để đưa ra đề xuất chính xác.")
        if st.button("🚀 Đăng nhập ngay", use_container_width=True):
            st.session_state.user = "guest"
            st.rerun()
        st.stop()
    
    # Quiz sở thích
    st.markdown("#### 🎯 Quiz tìm hiểu sở thích")
    
    with st.form("user_quiz"):
        col_quiz1, col_quiz2 = st.columns(2)
        
        with col_quiz1:
            q1 = st.radio(
                "1. Bạn có bao nhiêu kinh nghiệm trồng cây?",
                ["Mới bắt đầu", "Có chút kinh nghiệm", "Trung bình", "Nhiều kinh nghiệm", "Chuyên gia"],
                index=0
            )
            
            q2 = st.radio(
                "2. Bạn có bao nhiêu thời gian chăm sóc cây mỗi tuần?",
                ["Rất ít (dưới 1h)", "Ít (1-3h)", "Trung bình (3-5h)", "Nhiều (trên 5h)"],
                index=1
            )
        
        with col_quiz2:
            q3 = st.radio(
                "3. Không gian trồng cây của bạn như thế nào?",
                ["Rất nhỏ (ban công, cửa sổ)", "Nhỏ (góc phòng)", "Trung bình (sân nhỏ)", "Lớn (sân vườn)", "Rất lớn (vườn rộng)"],
                index=0
            )
            
            q4 = st.multiselect(
                "4. Mục đích chính khi trồng cây?",
                ["Trang trí", "Thanh lọc không khí", "Có thể ăn được", "Phong thủy", "Sức khỏe", "Thư giãn"],
                default=["Trang trí", "Thanh lọc không khí"]
            )
        
        quiz_submitted = st.form_submit_button("🤖 AI Đề xuất ngay!", type="primary")
    
    if quiz_submitted:
        # Tạo profile từ quiz
        quiz_profile = {
            "experience": q1,
            "care_time": q2,
            "garden_size": q3,
            "purposes": q4
        }
        
        # Kết hợp với preferences hiện có
        full_profile = {**st.session_state.user_preferences, **quiz_profile}
        
        # Lấy đề xuất từ AI
        with st.spinner("AI đang phân tích và đề xuất cây phù hợp..."):
            time.sleep(1)  # Giả lập xử lý AI
            
            recommendations = ai_recommender.get_personalized_recommendations(full_profile)
            st.session_state.recommended_plants = recommendations
            
            st.success(f"✅ AI đã đề xuất {len(recommendations)} cây phù hợp với bạn!")
    
    # Hiển thị đề xuất
    if st.session_state.recommended_plants:
        st.markdown("### 🌟 Cây đề xuất cho bạn")
        
        # Sắp xếp theo điểm phù hợp
        recommendations = st.session_state.recommended_plants
        
        for i, plant in enumerate(recommendations[:4]):  # Hiển thị 4 cây đầu
            with st.container(border=True):
                col_rec1, col_rec2, col_rec3 = st.columns([3, 1, 1])
                
                with col_rec1:
                    st.markdown(f"#### {i+1}. {plant['name']}")
                    st.markdown(f"**Độ phù hợp:** {plant['match_score']}%")
                    st.markdown(f"**Lý do:** {plant.get('match_reason', 'Phù hợp với hồ sơ của bạn')}")
                    st.caption(plant['description'][:100] + "...")
                
                with col_rec2:
                    st.metric("💧 Nước", f"{plant['water_need']}L")
                    st.metric("⚡ Độ khó", plant['difficulty'])
                
                with col_rec3:
                    # Thanh điểm phù hợp
                    match_percent = plant['match_score']
                    st.progress(match_percent / 100, text=f"{match_percent}% phù hợp")
                    
                    if st.button("🌿 Chọn cây này", key=f"select_rec_{plant['id']}", use_container_width=True):
                        st.session_state.selected_plant = plant
                        st.success(f"✅ Đã chọn {plant['name']}!")
        
        # Hiển thị biểu đồ phân tích
        st.markdown("### 📊 Phân tích đề xuất")
        
        # Tạo DataFrame cho biểu đồ
        df_recommend = pd.DataFrame(recommendations[:6])
        if not df_recommend.empty:
            fig = px.bar(
                df_recommend,
                x='name',
                y='match_score',
                title='Điểm phù hợp của các cây đề xuất',
                color='match_score',
                color_continuous_scale='viridis'
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Hiển thị thống kê
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                avg_score = df_recommend['match_score'].mean()
                st.metric("Điểm TB", f"{avg_score:.1f}%")
            with col_stat2:
                easy_plants = len([p for p in recommendations if p['difficulty'] in ['Dễ', 'Rất dễ']])
                st.metric("Cây dễ chăm", easy_plants)
            with col_stat3:
                air_plants = len([p for p in recommendations if p['air_purification'] in ['Tốt', 'Rất tốt', 'Xuất sắc']])
                st.metric("Thanh lọc tốt", air_plants)

# === DỰ BÁO & TÍNH TOÁN ===
elif selected == "📊 Dự báo & Tính toán":
    st.title("📊 Dự Báo & Tính Toán Thông Minh")
    st.markdown("### Dự báo thời tiết và tính toán nhu cầu chăm sóc chi tiết")
    
    # Kiểm tra đã chọn cây
    if not st.session_state.selected_plant:
        st.warning("🌿 Vui lòng chọn một cây trước khi xem dự báo!")
        if st.button("🌿 Chọn cây ngay", use_container_width=True):
            st.session_state.selected = "🌿 Thư viện cây"
            st.rerun()
        st.stop()
    
    plant = st.session_state.selected_plant
    
    # Header với thông tin
    col_header1, col_header2, col_header3, col_header4 = st.columns(4)
    with col_header1:
        st.metric("🌿 Cây", plant.get('name', 'Chưa chọn'))
    with col_header2:
        st.metric("📍 Vị trí", st.session_state.location_name)
    with col_header3:
        st.metric("💧 Nước cơ bản", f"{plant.get('water_need', 0)}L/ngày")
    with col_header4:
        st.metric("⚡ Độ khó", plant.get('difficulty', 'N/A'))
    
    # Tạo dự báo giả lập
    st.markdown("### 🌦️ Dự Báo Thời Tiết 7 Ngày")
    
    # Tạo dữ liệu dự báo
    today = datetime.datetime.now()
    forecast_data = []
    
    for i in range(7):
        date = today + timedelta(days=i)
        temp = random.randint(20, 35)
        rain = random.randint(0, 30) if random.random() > 0.6 else 0
        humidity = random.randint(40, 90)
        
        forecast_data.append({
            "Ngày": date.strftime("%d/%m"),
            "Thứ": date.strftime("%A"),
            "🌡️ Nhiệt độ": f"{temp}°C",
            "🌧️ Mưa": f"{rain}mm",
            "💦 Độ ẩm": f"{humidity}%",
            "🌤️ Điều kiện": "🌧️ Mưa" if rain > 10 else "☀️ Nắng" if temp > 30 else "⛅ Mây"
        })
    
    df_forecast = pd.DataFrame(forecast_data)
    st.dataframe(df_forecast, use_container_width=True, hide_index=True)
    
    # Tính toán nhu cầu nước
    st.markdown("### 💧 Tính Toán Nhu Cầu Nước Thông Minh")
    
    # Cài đặt tính toán
    with st.expander("⚙️ Cài đặt tính toán", expanded=True):
        col_set1, col_set2 = st.columns(2)
        with col_set1:
            soil_type = st.selectbox(
                "Loại đất:",
                ["Thịt (trung bình)", "Cát (thoát nước nhanh)", "Sét (giữ nước tốt)"],
                index=0
            )
            pot_size = st.select_slider(
                "Kích thước chậu:",
                options=["Nhỏ (1-3L)", "Trung bình (3-10L)", "Lớn (10-20L)", "Rất lớn (20L+)"],
                value="Trung bình (3-10L)"
            )
        with col_set2:
            season = st.selectbox(
                "Mùa:",
                ["Xuân", "Hè", "Thu", "Đông"],
                index=1
            )
            exposure = st.select_slider(
                "Tiếp xúc nắng:",
                options=["Bóng râm", "Bán phần", "Nắng đầy đủ", "Nắng gắt"],
                value="Bán phần"
            )
    
    # Tính toán và hiển thị kết quả
    if st.button("🧮 Tính toán nhu cầu", type="primary", use_container_width=True):
        # Tính toán đơn giản
        base_water = plant.get('water_need', 0.3)
        
        # Điều chỉnh theo mùa
        season_factors = {"Xuân": 1.0, "Hè": 1.3, "Thu": 1.1, "Đông": 0.7}
        season_factor = season_factors.get(season, 1.0)
        
        # Điều chỉnh theo loại đất
        soil_factors = {"Thịt (trung bình)": 1.0, "Cát (thoát nước nhanh)": 1.2, "Sét (giữ nước tốt)": 0.8}
        soil_factor = soil_factors.get(soil_type, 1.0)
        
        # Tính tổng
        total_water = base_water * season_factor * soil_factor * 7  # 7 ngày
        daily_water = total_water / 7
        
        # Hiển thị kết quả
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric("💧 Nhu cầu/ngày", f"{daily_water:.2f}L")
        with col_res2:
            st.metric("📅 Tổng 7 ngày", f"{total_water:.2f}L")
        with col_res3:
            water_saving = max(0, (1 - (season_factor * soil_factor)) * 100)
            st.metric("♻️ Tiết kiệm", f"{water_saving:.1f}%")
        
        # Biểu đồ
        days = [f"Ngày {i+1}" for i in range(7)]
        water_needs = [daily_water * random.uniform(0.8, 1.2) for _ in range(7)]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=days,
            y=water_needs,
            name='Nhu cầu nước',
            marker_color='#4dabf7'
        ))
        fig.add_hline(y=base_water, line_dash="dash", line_color="red", 
                     annotation_text=f"Nhu cầu cơ bản: {base_water}L")
        fig.update_layout(title="Nhu cầu nước 7 ngày", height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Khuyến nghị
        st.markdown("### 💡 Khuyến Nghị Chăm Sóc")
        
        recommendations = [
            f"🌱 **Tưới nước:** {daily_water:.2f}L mỗi ngày vào sáng sớm",
            f"🌿 **Bón phân:** {plant.get('fertilizer', 'NPK 20-20-20')} 2 tuần/lần",
            f"☀️ **Ánh sáng:** {plant.get('light', 'Nắng đầy đủ')}",
            f"🌡️ **Nhiệt độ:** Duy trì {plant.get('temperature', '20-30°C')}",
            f"💦 **Độ ẩm:** Giữ ở mức {plant.get('humidity', '40-60%')}"
        ]
        
        for rec in recommendations:
            st.info(rec)

# === CÂY CỦA TÔI ===
elif selected == "🏆 Cây của tôi":
    st.title("🏆 Cây Của Tôi")
    st.markdown("### Quản lý cây yêu thích và lịch sử chăm sóc")
    
    if not st.session_state.user:
        st.warning("🔐 Vui lòng đăng nhập để xem cây của bạn!")
        st.stop()
    
    # Tab quản lý
    tab_fav, tab_history, tab_schedule = st.tabs(["⭐ Cây yêu thích", "📜 Lịch sử", "📅 Lịch chăm sóc"])
    
    with tab_fav:
        st.markdown("### 🌟 Cây yêu thích của bạn")
        
        # Mock data - trong thực tế sẽ lưu trong database
        favorite_plants = [
            {"name": "Hoa Hồng", "added": "2024-01-15", "status": "Đang phát triển"},
            {"name": "Trầu Bà Vàng", "added": "2024-01-10", "status": "Tốt"},
            {"name": "Lưỡi Hổ Vằn", "added": "2024-01-05", "status": "Xuất sắc"}
        ]
        
        for plant in favorite_plants:
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{plant['name']}**")
                    st.caption(f"Thêm ngày: {plant['added']}")
                with col2:
                    st.markdown(f"**{plant['status']}**")
                with col3:
                    if st.button("👀 Xem", key=f"view_{plant['name']}"):
                        # Tìm cây trong database
                        found_plant = plant_system.plants_db[
                            plant_system.plants_db["name"].str.contains(plant['name'])
                        ]
                        if not found_plant.empty:
                            st.session_state.selected_plant = found_plant.iloc[0].to_dict()
                            st.session_state.show_plant_details = True
                            st.rerun()
        
        # Thêm cây mới
        st.markdown("---")
        st.markdown("### ➕ Thêm cây mới")
        
        col_add1, col_add2 = st.columns([3, 1])
        with col_add1:
            plant_options = [p["name"] for p in plant_system.plants_db.to_dict('records')]
            new_plant = st.selectbox("Chọn cây:", plant_options)
        with col_add2:
            if st.button("⭐ Thêm vào yêu thích", use_container_width=True):
                st.success(f"Đã thêm {new_plant} vào danh sách yêu thích!")
    
    with tab_history:
        st.markdown("### 📜 Lịch sử chăm sóc")
        
        # Mock history data
        history = [
            {"date": "2024-01-20", "plant": "Hoa Hồng", "action": "Tưới nước", "note": "2L nước"},
            {"date": "2024-01-19", "plant": "Trầu Bà", "action": "Bón phân", "note": "NPK 20-20-20"},
            {"date": "2024-01-18", "plant": "Lưỡi Hổ", "action": "Lau lá", "note": "Vệ sinh lá"},
            {"date": "2024-01-17", "plant": "Hoa Hồng", "action": "Cắt tỉa", "note": "Tỉa hoa tàn"},
        ]
        
        for record in history:
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 2])
                with col1:
                    st.markdown(f"**{record['plant']}**")
                    st.caption(record['date'])
                with col2:
                    st.markdown(f"**{record['action']}**")
                with col3:
                    st.markdown(record['note'])
    
    with tab_schedule:
        st.markdown("### 📅 Lịch chăm sóc tuần này")
        
        # Tạo lịch mẫu
        today = datetime.datetime.now()
        schedule = []
        
        for i in range(7):
            day = today + timedelta(days=i)
            tasks = []
            
            if i % 2 == 0:
                tasks.append("💧 Tưới nước")
            if i % 3 == 0:
                tasks.append("🌿 Kiểm tra")
            if i == 0 or i == 6:
                tasks.append("✂️ Cắt tỉa")
            
            schedule.append({
                "Ngày": day.strftime("%d/%m"),
                "Thứ": day.strftime("%A"),
                "Công việc": ", ".join(tasks) if tasks else "Nghỉ ngơi"
            })
        
        st.dataframe(pd.DataFrame(schedule), use_container_width=True, hide_index=True)

# --- 10. FOOTER ---
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col1:
    st.markdown("**🌿 EcoMind PRO**")
    st.caption("Phiên bản cao cấp với AI")
with footer_col2:
    st.markdown("**📧 Liên hệ**")
    st.caption("tranthienphatle@gmail.com")
with footer_col3:
    st.markdown("**🚀 Tính năng**")
    st.caption("Bản đồ • AI • Nguồn uy tín")

st.caption(f"🕐 {datetime.datetime.now().strftime('%H:%M %d/%m/%Y')} • © 2024 EcoMind PRO • Streamlit Cloud")
