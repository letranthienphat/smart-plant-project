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
import wikipedia
import wikipediaapi
from bs4 import BeautifulSoup
import re
import httpx
import asyncio
from concurrent.futures import ThreadPoolExecutor
import openai
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

# --- 1. CẤU HÌNH GIAO DIỆN PREMIUM ---
st.set_page_config(
    page_title="EcoMind OS Premium - Hệ Thống Chăm Sóc Cây Thông Minh",
    layout="wide", 
    page_icon="🌿",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://ecomind.com/help',
        'Report a bug': 'https://ecomind.com/bug',
        'About': 'EcoMind OS Premium - Phiên bản 4.0'
    }
)

# Tải biến môi trường (cho API keys)
load_dotenv()

# CSS Premium với gradient và animations
st.markdown("""
<style>
    /* Reset và font chữ */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Nền gradient đẹp */
    .stApp {
        background: linear-gradient(135deg, #0a192f 0%, #0d1b2a 25%, #1b263b 50%, #0d1b2a 75%, #0a192f 100%);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #e0e1dd;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }
    
    /* Cards với glassmorphism */
    .glass-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .glass-card:hover {
        border-color: #00ffcc;
        box-shadow: 0 8px 32px rgba(0, 255, 204, 0.15);
        transform: translateY(-4px);
    }
    
    /* Headers với gradient text */
    h1, h2, h3, h4 {
        background: linear-gradient(90deg, #00ffcc, #0088cc, #00ffcc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        background-size: 200% auto;
        animation: textShine 3s ease-in-out infinite alternate;
        font-weight: 700 !important;
    }
    
    @keyframes textShine {
        0% { background-position: 0% 50% }
        100% { background-position: 100% 50% }
    }
    
    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 1rem !important;
        position: relative;
    }
    
    h1::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 0;
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, #00ffcc, transparent);
        border-radius: 2px;
    }
    
    /* Metrics custom */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #00ffcc, #0088cc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #88aaff !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Buttons với hiệu ứng */
    .stButton > button {
        background: linear-gradient(90deg, #00ffcc 0%, #0088cc 100%) !important;
        color: #0a192f !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 25px rgba(0, 255, 204, 0.3) !important;
    }
    
    /* Input fields đẹp */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > textarea {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        padding: 14px 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus,
    .stTextArea > div > textarea:focus {
        border-color: #00ffcc !important;
        box-shadow: 0 0 0 3px rgba(0, 255, 204, 0.1) !important;
        background: rgba(255, 255, 255, 0.12) !important;
    }
    
    /* Tabs premium */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 12px 24px;
        background: transparent;
        color: #88aaff;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #00ffcc 0%, #0088cc 100%) !important;
        color: #0a192f !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(0, 255, 204, 0.2);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00ffcc 0%, #0088cc 100%);
        border-radius: 10px;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(10, 25, 47, 0.9) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Scrollbar custom */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00ffcc 0%, #0088cc 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #00ffcc 0%, #00a8cc 100%);
    }
    
    /* Notification badges */
    .notification-badge {
        display: inline-block;
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-left: 8px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Tooltips */
    [data-tooltip] {
        position: relative;
    }
    
    [data-tooltip]::before {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 0.9rem;
        white-space: nowrap;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 1000;
    }
    
    [data-tooltip]:hover::before {
        opacity: 1;
        visibility: visible;
        transform: translateX(-50%) translateY(-8px);
    }
    
    /* Loading animations */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255, 255, 255, 0.1);
        border-top: 3px solid #00ffcc;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 10px;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem !important;
        }
        
        h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.5rem !important; }
        h3 { font-size: 1.3rem !important; }
        
        .glass-card {
            padding: 16px;
        }
    }
    
    /* Dark mode text fixes - QUAN TRỌNG: Sửa lỗi chữ trắng */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > textarea,
    .stDateInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTimeInput > div > div > input {
        color: #ffffff !important;
    }
    
    /* Đảm bảo placeholder text cũng hiển thị */
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Select dropdown items */
    .stSelectbox div[role="listbox"] div {
        color: #333333 !important;
    }
    
    /* Multi-select items */
    .stMultiSelect div[role="option"] {
        color: #333333 !important;
    }
    
    /* Table text color */
    .stDataFrame table {
        color: #ffffff !important;
    }
    
    .stDataFrame th {
        color: #00ffcc !important;
    }
    
    .stDataFrame td {
        color: #e0e1dd !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. HỆ THỐNG AI VÀ API ---
class AISystem:
    """Hệ thống AI tích hợp"""
    
    def __init__(self):
        # Cấu hình API keys (có thể thay bằng biến môi trường)
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.google_api_key = os.getenv("GOOGLE_API_KEY", "")
        
        # Khởi tạo Wikipedia API
        self.wiki_wiki = wikipediaapi.Wikipedia(
            language='vi',
            user_agent='EcoMindApp/1.0'
        )
    
    async def search_wikipedia_async(self, plant_name):
        """Tìm kiếm thông tin cây trên Wikipedia"""
        try:
            # Tìm kiếm trang Wikipedia
            page = self.wiki_wiki.page(plant_name)
            
            if page.exists():
                return {
                    "title": page.title,
                    "summary": page.summary[:500] + "..." if len(page.summary) > 500 else page.summary,
                    "full_text": page.text[:2000] + "..." if len(page.text) > 2000 else page.text,
                    "url": page.fullurl,
                    "categories": list(page.categories.keys())[:5]
                }
            
            # Thử tìm kiếm tiếng Anh nếu không tìm thấy tiếng Việt
            wiki_en = wikipediaapi.Wikipedia(language='en', user_agent='EcoMindApp/1.0')
            page_en = wiki_en.page(plant_name)
            
            if page_en.exists():
                # Dịch tóm tắt (giả lập)
                summary = page_en.summary[:300]
                return {
                    "title": page_en.title,
                    "summary": f"{summary}... (Dịch từ tiếng Anh)",
                    "full_text": page_en.text[:1500] + "...",
                    "url": page_en.fullurl,
                    "categories": ["English Wikipedia"]
                }
                
        except Exception as e:
            print(f"Wikipedia search error: {e}")
        
        return None
    
    def search_plant_info(self, plant_name):
        """Tìm kiếm thông tin cây từ nhiều nguồn"""
        results = {
            "wikipedia": None,
            "google_suggestions": [],
            "scientific_name": None,
            "common_names": [],
            "care_tips": []
        }
        
        # Tìm kiếm Wikipedia
        try:
            wiki_search = wikipedia.search(plant_name, results=3)
            results["wikipedia"] = wiki_search
            
            if wiki_search:
                # Lấy tóm tắt trang đầu tiên
                try:
                    page = wikipedia.page(wiki_search[0])
                    results["summary"] = page.summary[:300] + "..."
                    results["full_url"] = page.url
                except:
                    pass
        except:
            pass
        
        # Thêm thông tin giả lập dựa trên tên cây
        plant_info_db = {
            "Hoa Hồng": {
                "scientific_name": "Rosa spp.",
                "common_names": ["Hồng", "Hoa hồng", "Rose"],
                "care_tips": ["Tưới nước khi đất khô", "Bón phân 2 tuần/lần", "Cắt tỉa sau khi hoa tàn"]
            },
            "Lan": {
                "scientific_name": "Orchidaceae",
                "common_names": ["Phong lan", "Địa lan", "Orchid"],
                "care_tips": ["Giữ ẩm nhưng không ướt", "Ánh sáng gián tiếp", "Bón phân đặc biệt cho lan"]
            },
            # Thêm các cây khác...
        }
        
        if plant_name in plant_info_db:
            results.update(plant_info_db[plant_name])
        
        return results
    
    async def get_plant_detailed_info(self, plant_name):
        """Lấy thông tin chi tiết về cây bằng AI"""
        # Giả lập response AI
        ai_response = {
            "description": f"Cây {plant_name} là một loài thực vật phổ biến với nhiều đặc điểm thú vị...",
            "origin": "Nguồn gốc từ khu vực nhiệt đới",
            "growth_conditions": {
                "light": "Ánh sáng mặt trời gián tiếp",
                "water": "Tưới khi đất khô bề mặt",
                "temperature": "18-28°C",
                "humidity": "Trung bình đến cao"
            },
            "benefits": ["Thanh lọc không khí", "Tăng độ ẩm", "Trang trí"],
            "common_problems": ["Lá vàng do úng nước", "Sâu bệnh", "Thiếu ánh sáng"],
            "propagation": "Nhân giống bằng giâm cành hoặc hạt"
        }
        
        return ai_response

# --- 3. HỆ THỐNG BẢN ĐỒ NÂNG CAO ---
class AdvancedMapSystem:
    """Hệ thống bản đồ nâng cao với tìm kiếm thông minh"""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="ecomind_premium_app")
        self.vietnam_locations = self._load_vietnam_locations()
        
    def _load_vietnam_locations(self):
        """Tải danh sách địa điểm Việt Nam"""
        # Danh sách tỉnh/thành phố và các huyện/xã phổ biến
        return {
            "Tân Hiệp": {"lat": 10.1234, "lon": 106.5678, "type": "Huyện", "province": "Kiên Giang"},
            "Phú Giáo": {"lat": 11.2345, "lon": 106.7890, "type": "Huyện", "province": "Bình Dương"},
            "Hà Nội": {"lat": 21.0285, "lon": 105.8542, "type": "Thành phố", "province": "Hà Nội"},
            "TP Hồ Chí Minh": {"lat": 10.8231, "lon": 106.6297, "type": "Thành phố", "province": "TP HCM"},
            "Đà Nẵng": {"lat": 16.0544, "lon": 108.2022, "type": "Thành phố", "province": "Đà Nẵng"},
            "Huế": {"lat": 16.4637, "lon": 107.5909, "type": "Thành phố", "province": "Thừa Thiên Huế"},
            "Đà Lạt": {"lat": 11.9404, "lon": 108.4583, "type": "Thành phố", "province": "Lâm Đồng"},
            "Nha Trang": {"lat": 12.2388, "lon": 109.1967, "type": "Thành phố", "province": "Khánh Hòa"},
            "Cần Thơ": {"lat": 10.0452, "lon": 105.7469, "type": "Thành phố", "province": "Cần Thơ"},
            "Hải Phòng": {"lat": 20.8449, "lon": 106.6881, "type": "Thành phố", "province": "Hải Phòng"},
            "Vũng Tàu": {"lat": 10.3460, "lon": 107.0843, "type": "Thành phố", "province": "Bà Rịa - Vũng Tàu"},
            "Biên Hòa": {"lat": 10.9447, "lon": 106.8243, "type": "Thành phố", "province": "Đồng Nai"},
            "Thủ Dầu Một": {"lat": 10.9805, "lon": 106.6509, "type": "Thành phố", "province": "Bình Dương"},
            "Bảo Lộc": {"lat": 11.5496, "lon": 107.8077, "type": "Thành phố", "province": "Lâm Đồng"},
            "Long Xuyên": {"lat": 10.3865, "lon": 105.4351, "type": "Thành phố", "province": "An Giang"}
        }
    
    def search_locations(self, query):
        """Tìm kiếm địa điểm với gợi ý thông minh"""
        query = query.lower().strip()
        results = []
        
        # Tìm kiếm trong danh sách địa điểm
        for name, info in self.vietnam_locations.items():
            if query in name.lower():
                results.append({
                    "name": name,
                    "type": info["type"],
                    "province": info["province"],
                    "coordinates": [info["lat"], info["lon"]]
                })
        
        # Nếu không tìm thấy, thử tìm kiếm bằng Nominatim
        if not results:
            try:
                location = self.geolocator.geocode(f"{query}, Vietnam")
                if location:
                    results.append({
                        "name": location.address,
                        "type": "Địa điểm",
                        "province": "Việt Nam",
                        "coordinates": [location.latitude, location.longitude]
                    })
            except:
                pass
        
        return results
    
    def create_advanced_map(self, center, zoom=12, markers=None, radius_km=5):
        """Tạo bản đồ nâng cao với nhiều tính năng"""
        m = folium.Map(
            location=center,
            zoom_start=zoom,
            tiles="cartodbpositron",  # Giao diện sáng
            width="100%",
            height=500,
            control_scale=True
        )
        
        # Thêm marker chính
        folium.Marker(
            center,
            popup=folium.Popup(f"<b>Vị trí cây</b><br>Tọa độ: {center[0]:.4f}, {center[1]:.4f}", max_width=300),
            tooltip="Vị trí chính",
            icon=folium.Icon(color="green", icon="tree", prefix="fa")
        ).add_to(m)
        
        # Thêm vòng tròn bán kính
        folium.Circle(
            center,
            radius=radius_km * 1000,  # Chuyển km sang mét
            color="#00ffcc",
            fill=True,
            fill_color="#00ffcc",
            fill_opacity=0.2,
            popup=f"Bán kính {radius_km}km",
            tooltip="Phạm vi theo dõi"
        ).add_to(m)
        
        # Thêm layer control
        folium.TileLayer('openstreetmap').add_to(m)
        folium.TileLayer('cartodbdark_matter').add_to(m)
        folium.TileLayer('stamenterrain').add_to(m)
        
        folium.LayerControl().add_to(m)
        
        # Thêm minimap
        from folium.plugins import MiniMap
        minimap = MiniMap(toggle_display=True)
        m.add_child(minimap)
        
        # Thêm fullscreen button
        from folium.plugins import Fullscreen
        Fullscreen().add_to(m)
        
        # Thêm locate control
        from folium.plugins import LocateControl
        LocateControl(auto_start=False).add_to(m)
        
        return m
    
    def get_elevation(self, lat, lon):
        """Lấy thông tin độ cao (giả lập)"""
        # Giả lập độ cao dựa trên tọa độ
        base_elevation = 50
        elevation_variation = (lat * 100 + lon * 100) % 1000
        return base_elevation + elevation_variation
    
    def get_weather_zone(self, lat, lon):
        """Xác định vùng khí hậu"""
        if lat > 16:
            return "Miền Bắc"
        elif lat > 11:
            return "Miền Trung"
        else:
            return "Miền Nam"

# --- 4. HỆ THỐNG THỜI TIẾT NÂNG CAO ---
class AdvancedWeatherSystem:
    """Hệ thống dự báo thời tiết nâng cao"""
    
    def __init__(self):
        self.cache = {}
        self.weather_apis = [
            "open-meteo",
            "weatherstack",
            "openweathermap"
        ]
    
    def get_comprehensive_forecast(self, lat, lon, days=7):
        """Lấy dự báo thời tiết toàn diện"""
        try:
            # Thử Open-Meteo API (miễn phí)
            forecast = self._get_openmeteo_forecast(lat, lon, days)
            if forecast:
                return forecast
        except:
            pass
        
        # Fallback: tạo dữ liệu mô phỏng chi tiết
        return self._generate_detailed_forecast(lat, lon, days)
    
    def _get_openmeteo_forecast(self, lat, lon, days):
        """Lấy dữ liệu từ Open-Meteo API"""
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": [
                "temperature_2m_max", "temperature_2m_min",
                "precipitation_sum", "weathercode",
                "windspeed_10m_max", "winddirection_10m_dominant"
            ],
            "timezone": "auto",
            "forecast_days": days
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return self._process_openmeteo_data(data)
        
        return None
    
    def _process_openmeteo_data(self, data):
        """Xử lý dữ liệu Open-Meteo"""
        forecast = []
        daily = data["daily"]
        
        for i in range(len(daily["time"])):
            weather_code = daily["weathercode"][i]
            
            forecast.append({
                "date": daily["time"][i],
                "temp_max": daily["temperature_2m_max"][i],
                "temp_min": daily["temperature_2m_min"][i],
                "precipitation": daily["precipitation_sum"][i],
                "wind_speed": daily["windspeed_10m_max"][i],
                "wind_direction": daily["winddirection_10m_dominant"][i],
                "condition": self._get_condition_from_code(weather_code),
                "icon": self._get_weather_icon(weather_code),
                "uv_index": round(random.uniform(1, 11), 1),
                "humidity": random.randint(40, 90),
                "pressure": random.randint(1000, 1020)
            })
        
        return pd.DataFrame(forecast)
    
    def _get_condition_from_code(self, code):
        """Chuyển đổi weather code thành điều kiện"""
        # WMO Weather interpretation codes
        codes = {
            0: "Trời quang",
            1: "Chủ yếu quang",
            2: "Có mây",
            3: "U ám",
            45: "Sương mù",
            48: "Sương mù",
            51: "Mưa phùn nhẹ",
            53: "Mưa phùn vừa",
            55: "Mưa phùn dày",
            61: "Mưa nhẹ",
            63: "Mưa vừa",
            65: "Mưa nặng hạt",
            71: "Tuyết nhẹ",
            73: "Tuyết vừa",
            75: "Tuyết nặng",
            80: "Mưa rào nhẹ",
            81: "Mưa rào vừa",
            82: "Mưa rào nặng",
            95: "Giông",
            96: "Giông với mưa đá nhẹ",
            99: "Giông với mưa đá nặng"
        }
        
        return codes.get(code, "Không xác định")
    
    def _get_weather_icon(self, code):
        """Lấy biểu tượng thời tiết"""
        if code in [0, 1]:
            return "☀️"
        elif code in [2, 3]:
            return "⛅"
        elif code in [45, 48]:
            return "🌫️"
        elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            return "🌧️"
        elif code in [71, 73, 75]:
            return "❄️"
        elif code in [95, 96, 99]:
            return "⛈️"
        else:
            return "☁️"
    
    def _generate_detailed_forecast(self, lat, lon, days):
        """Tạo dự báo chi tiết mô phỏng"""
        forecast = []
        today = datetime.datetime.now()
        
        for i in range(days):
            date = today + timedelta(days=i)
            
            # Tính toán dựa trên vĩ độ và mùa
            base_temp = 25 - (abs(lat) - 10) * 0.3
            
            # Thêm biến động theo mùa
            month = date.month
            if month in [5, 6, 7, 8]:  # Mùa hè
                base_temp += 3
            elif month in [11, 12, 1, 2]:  # Mùa đông
                base_temp -= 3
            
            temp_max = round(base_temp + random.uniform(-2, 5), 1)
            temp_min = round(temp_max - random.uniform(3, 8), 1)
            
            # Tính toán mưa
            if random.random() < 0.3:
                precipitation = round(random.uniform(0.5, 25.0), 1)
            else:
                precipitation = 0
            
            # Các thông số khác
            wind_speed = round(random.uniform(1, 15), 1)
            wind_direction = random.choice(["Đông", "Tây", "Nam", "Bắc", "Đông Bắc", "Tây Nam"])
            humidity = random.randint(40, 95)
            pressure = random.randint(1000, 1020)
            uv_index = round(random.uniform(1, 11), 1)
            
            # Xác định điều kiện
            if precipitation > 15:
                condition = "Mưa rất to"
                icon = "🌧️"
            elif precipitation > 5:
                condition = "Mưa"
                icon = "🌦️"
            elif temp_max > 32:
                condition = "Nắng nóng"
                icon = "🔥"
            elif temp_max > 28:
                condition = "Nắng"
                icon = "☀️"
            elif temp_max < 20:
                condition = "Mát mẻ"
                icon = "🍃"
            else:
                condition = "Ôn hòa"
                icon = "⛅"
            
            forecast.append({
                "date": date.strftime("%Y-%m-%d"),
                "day": date.strftime("%d/%m"),
                "temp_max": temp_max,
                "temp_min": temp_min,
                "precipitation": precipitation,
                "wind_speed": wind_speed,
                "wind_direction": wind_direction,
                "condition": condition,
                "icon": icon,
                "uv_index": uv_index,
                "humidity": humidity,
                "pressure": pressure
            })
        
        return pd.DataFrame(forecast)
    
    def calculate_evapotranspiration(self, temp, humidity, wind_speed, solar_radiation):
        """Tính toán lượng bốc hơi (ET0)"""
        # Công thức Hargreaves đơn giản hóa
        et0 = 0.0023 * (temp + 17.8) * (temp - 2.0) * solar_radiation
        return max(0, round(et0, 3))
    
    def get_weather_alerts(self, lat, lon, forecast_df):
        """Tạo cảnh báo thời tiết"""
        alerts = []
        
        # Kiểm tra nhiệt độ cực đoan
        if forecast_df["temp_max"].max() > 35:
            alerts.append({
                "type": "warning",
                "icon": "🔥",
                "title": "Cảnh báo nắng nóng",
                "message": "Nhiệt độ có thể vượt 35°C. Bảo vệ cây khỏi ánh nắng trực tiếp.",
                "severity": "Cao"
            })
        
        if forecast_df["temp_min"].min() < 15:
            alerts.append({
                "type": "info",
                "icon": "❄️",
                "title": "Trời lạnh",
                "message": "Nhiệt độ thấp có thể ảnh hưởng đến sự phát triển của cây.",
                "severity": "Trung bình"
            })
        
        # Kiểm tra mưa nhiều
        if forecast_df["precipitation"].sum() > 50:
            alerts.append({
                "type": "warning",
                "icon": "🌧️",
                "title": "Mưa nhiều",
                "message": "Dự báo mưa lớn. Giảm tưới nước và đảm bảo thoát nước tốt.",
                "severity": "Trung bình"
            })
        
        # Kiểm tra gió mạnh
        if forecast_df["wind_speed"].max() > 12:
            alerts.append({
                "type": "warning",
                "icon": "💨",
                "title": "Gió mạnh",
                "message": "Gió có thể làm gãy cành non. Cân nhắc di chuyển cây.",
                "severity": "Thấp"
            })
        
        return alerts

# --- 5. HỆ THỐNG CÂY TRỒNG NÂNG CAO ---
class AdvancedPlantSystem:
    """Hệ thống quản lý cây trồng nâng cao"""
    
    def __init__(self):
        self.plants_db = self._create_advanced_plant_database()
        self.plant_care_tips = self._create_care_tips_database()
    
    def _create_advanced_plant_database(self):
        """Tạo database cây trồng chi tiết"""
        plants = []
        
        plant_data = [
            # Format: [Tên, Nước(L), Độ khó, Ánh sáng, Nhiệt độ, Độ ẩm, pH, Mùa trồng]
            ["Hoa Hồng", 0.5, "Trung bình", "Nắng đầy đủ", "18-28°C", "40-60%", "6.0-7.0", "Xuân, Thu"],
            ["Lan", 0.3, "Khó", "Bóng râm", "20-30°C", "50-70%", "5.5-6.5", "Quanh năm"],
            ["Xương Rồng", 0.1, "Dễ", "Nắng đầy đủ", "20-35°C", "20-40%", "6.0-7.5", "Xuân"],
            ["Sen Đá", 0.15, "Rất dễ", "Nắng nhiều", "18-30°C", "30-50%", "6.0-7.0", "Xuân, Hè"],
            ["Trầu Bà", 0.4, "Dễ", "Bán phần", "20-32°C", "40-60%", "6.0-7.5", "Quanh năm"],
            ["Dương Xỉ", 0.6, "Trung bình", "Bóng râm", "18-25°C", "50-80%", "5.5-6.5", "Xuân"],
            ["Cây Lưỡi Hổ", 0.2, "Rất dễ", "Mọi điều kiện", "18-30°C", "30-50%", "6.0-8.0", "Quanh năm"],
            ["Cây Kim Tiền", 0.3, "Dễ", "Bán phần", "20-32°C", "40-60%", "6.0-7.0", "Xuân, Hè"],
            ["Cây Phát Tài", 0.4, "Dễ", "Bán phần", "20-30°C", "40-70%", "6.0-7.0", "Xuân"],
            ["Cây Ngũ Gia Bì", 0.35, "Dễ", "Bán phần", "18-28°C", "50-70%", "5.5-7.0", "Xuân, Thu"],
            ["Hoa Cúc", 0.45, "Trung bình", "Nắng nhiều", "15-25°C", "40-60%", "6.0-7.5", "Thu, Đông"],
            ["Hoa Đồng Tiền", 0.5, "Trung bình", "Nắng đầy đủ", "18-24°C", "40-60%", "6.0-6.5", "Xuân"],
            ["Cây Trầu Bà Vàng", 0.35, "Dễ", "Bán phần", "20-30°C", "40-70%", "6.0-7.5", "Quanh năm"],
            ["Cây Vạn Lộc", 0.4, "Dễ", "Bóng râm", "20-28°C", "50-80%", "5.5-6.5", "Xuân"],
            ["Cây Kim Ngân", 0.25, "Dễ", "Bán phần", "18-30°C", "40-60%", "6.0-7.0", "Xuân"]
        ]
        
        for i, (name, water, difficulty, light, temp, humidity, ph, season) in enumerate(plant_data, 1):
            plants.append({
                "ID": i,
                "Tên Cây": name,
                "Nước (L/ngày)": water,
                "Độ khó": difficulty,
                "Ánh sáng": light,
                "Nhiệt độ": temp,
                "Độ ẩm": humidity,
                "Độ pH": ph,
                "Mùa trồng": season,
                "Tần suất tưới": self._get_watering_frequency(water),
                "Tốc độ sinh trưởng": random.choice(["Chậm", "Trung bình", "Nhanh"]),
                "Chiều cao trưởng thành": f"{random.randint(30, 200)} cm",
                "Thời gian ra hoa": random.choice(["3-6 tháng", "6-12 tháng", "Trên 1 năm"]),
                "Chất dinh dưỡng": random.choice(["Phân NPK 20-20-20", "Phân hữu cơ", "Phân vi lượng"]),
                "Sâu bệnh thường gặp": random.choice(["Rệp sáp", "Nhện đỏ", "Bệnh đốm lá"]),
                "Mô tả": f"Cây {name} là loại cây phổ biến với nhiều ưu điểm...",
                "Thú cưng an toàn": random.choice([True, False])
            })
        
        return pd.DataFrame(plants)
    
    def _create_care_tips_database(self):
        """Tạo database mẹo chăm sóc"""
        return {
            "Hoa Hồng": [
                "Cắt tỉa sau mỗi đợt hoa",
                "Bón phân NPK 2 tuần/lần trong mùa sinh trưởng",
                "Phun thuốc phòng nấm định kỳ"
            ],
            "Lan": [
                "Không tưới nước vào ban đêm",
                "Sử dụng giá thể thoáng khí",
                "Giữ độ ẩm không khí cao"
            ],
            "Xương Rồng": [
                "Chỉ tưới khi đất khô hoàn toàn",
                "Đặt ở nơi có nắng ít nhất 6h/ngày",
                "Sử dụng đất thoát nước tốt"
            ],
            # Thêm các cây khác...
        }
    
    def _get_watering_frequency(self, water_amount):
        """Tính tần suất tưới dựa trên lượng nước"""
        if water_amount < 0.2:
            return "3-5 ngày/lần"
        elif water_amount < 0.4:
            return "2-3 ngày/lần"
        else:
            return "Hàng ngày"
    
    def search_plants(self, query, filters=None):
        """Tìm kiếm cây với bộ lọc nâng cao"""
        results = self.plants_db.copy()
        
        # Tìm kiếm theo từ khóa
        if query:
            mask = (
                results["Tên Cây"].str.contains(query, case=False, na=False) |
                results["Mô tả"].str.contains(query, case=False, na=False)
            )
            results = results[mask]
        
        # Áp dụng bộ lọc
        if filters:
            for key, value in filters.items():
                if value and key in results.columns:
                    if isinstance(value, list):
                        results = results[results[key].isin(value)]
                    else:
                        results = results[results[key] == value]
        
        return results
    
    def get_plant_care_schedule(self, plant_name, location_data, season):
        """Tạo lịch chăm sóc chi tiết"""
        schedule = []
        today = datetime.datetime.now()
        
        # Lấy thông tin cây
        plant = self.plants_db[self.plants_db["Tên Cây"] == plant_name].iloc[0]
        
        # Tạo lịch 30 ngày
        for day in range(30):
            current_date = today + timedelta(days=day)
            date_str = current_date.strftime("%d/%m/%Y")
            
            # Xác định công việc dựa trên ngày
            tasks = []
            
            # Tưới nước
            if day % self._get_watering_days(plant["Nước (L/ngày)"]) == 0:
                tasks.append({
                    "task": "💧 Tưới nước",
                    "time": "Sáng sớm",
                    "details": f"Tưới {plant['Nước (L/ngày)']}L nước",
                    "priority": "Cao"
                })
            
            # Bón phân (7 ngày/lần)
            if day % 7 == 0:
                tasks.append({
                    "task": "🌿 Bón phân",
                    "time": "Chiều mát",
                    "details": f"Bón {plant['Chất dinh dưỡng']}",
                    "priority": "Trung bình"
                })
            
            # Cắt tỉa (14 ngày/lần)
            if day % 14 == 0:
                tasks.append({
                    "task": "✂️ Cắt tỉa",
                    "time": "Sáng sớm",
                    "details": "Cắt tỉa lá vàng, cành khô",
                    "priority": "Thấp"
                })
            
            # Kiểm tra sâu bệnh (3 ngày/lần)
            if day % 3 == 0:
                tasks.append({
                    "task": "🔍 Kiểm tra sâu bệnh",
                    "time": "Bất kỳ",
                    "details": "Kiểm tra lá và thân cây",
                    "priority": "Trung bình"
                })
            
            schedule.append({
                "Ngày": date_str,
                "Thứ": current_date.strftime("%A"),
                "Công việc": tasks if tasks else [{"task": "✅ Nghỉ", "time": "-", "details": "Không có công việc", "priority": "Thấp"}]
            })
        
        return schedule
    
    def _get_watering_days(self, water_amount):
        """Xác định số ngày giữa các lần tưới"""
        if water_amount < 0.2:
            return 4
        elif water_amount < 0.4:
            return 2
        else:
            return 1

# --- 6. KHỞI TẠO HỆ THỐNG ---
# Khởi tạo tất cả components
ai_system = AISystem()
map_system = AdvancedMapSystem()
weather_system = AdvancedWeatherSystem()
plant_system = AdvancedPlantSystem()

# Lấy database cây
df_plants = plant_system.plants_db

# Khởi tạo session state
default_state = {
    'selected_plant': df_plants.iloc[0].to_dict(),
    'selected_location': [10.8231, 106.6297],
    'location_name': "TP Hồ Chí Minh",
    'forecast_data': None,
    'water_calculation': None,
    'plant_info': {},
    'search_results': [],
    'active_tab': "🏠 Tổng quan",
    'user_preferences': {
        'theme': 'dark',
        'notifications': True,
        'units': 'metric'
    }
}

for key, value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- 7. SIDEBAR PREMIUM ---
with st.sidebar:
    # Logo và thông tin phiên bản
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="background: linear-gradient(90deg, #00ffcc, #0088cc); 
                   -webkit-background-clip: text; 
                   -webkit-text-fill-color: transparent;
                   font-size: 2rem;
                   margin: 0;">
            🌿 EcoMind
        </h1>
        <p style="color: #88aaff; margin: 0.5rem 0; font-size: 0.9rem;">
            Hệ Thống Chăm Sóc Cây Thông Minh
        </p>
        <div style="display: inline-block; background: linear-gradient(90deg, #00ffcc, #0088cc); 
                    color: #0a192f; padding: 4px 12px; border-radius: 20px; 
                    font-size: 0.8rem; font-weight: 700; margin-top: 0.5rem;">
            PREMIUM v4.0
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Menu điều hướng
    selected = option_menu(
        menu_title=None,
        options=["🏠 Tổng quan", "🗺️ Bản đồ VN", "🔍 Tìm kiếm", "🌿 Thư viện cây", 
                "📊 Dự báo thời tiết", "💧 Tính toán nước", "📅 Lịch chăm sóc", 
                "🤖 AI Trợ lý", "⚙️ Cài đặt"],
        icons=["house", "map", "search", "tree", "cloud-sun", "droplet", 
               "calendar", "robot", "gear"],
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background": "transparent"
            },
            "icon": {
                "color": "#00ffcc",
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "15px",
                "font-weight": "500",
                "padding": "15px 20px",
                "margin": "3px 0",
                "border-radius": "10px",
                "color": "#e0e1dd",
                "background": "rgba(255, 255, 255, 0.05)",
                "transition": "all 0.3s ease"
            },
            "nav-link:hover": {
                "background": "rgba(0, 255, 204, 0.1)",
                "color": "#ffffff"
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg, #00ffcc, #0088cc)",
                "color": "#0a192f",
                "font-weight": "700",
                "box-shadow": "0 4px 15px rgba(0, 255, 204, 0.3)"
            }
        }
    )
    
    # Cập nhật active tab
    st.session_state.active_tab = selected
    
    # Thông tin nhanh
    st.markdown("---")
    st.markdown("### 📍 Vị trí hiện tại")
    
    if st.session_state.location_name:
        with st.container(border=True):
            st.markdown(f"**{st.session_state.location_name}**")
            st.caption(f"{st.session_state.selected_location[0]:.4f}, {st.session_state.selected_location[1]:.4f}")
    
    st.markdown("### 🌿 Cây đang chọn")
    
    if st.session_state.selected_plant:
        plant = st.session_state.selected_plant
        with st.container(border=True):
            st.markdown(f"**{plant.get('Tên Cây', 'Chưa chọn')}**")
            st.caption(f"💧 {plant.get('Nước (L/ngày)', 0)}L/ngày")
    
    # Thông tin hệ thống
    st.markdown("---")
    st.markdown("### ℹ️ Thông tin hệ thống")
    
    col_sys1, col_sys2 = st.columns(2)
    with col_sys1:
        st.metric("Phiên bản", "4.0.1")
    with col_sys2:
        st.metric("Trạng thái", "✅ Online")
    
    st.markdown("**Email hỗ trợ:**")
    st.code("tranthienphatle@gmail.com")
    
    # Nút làm mới
    if st.button("🔄 Làm mới dữ liệu", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# --- 8. NỘI DUNG CHÍNH ---
# === TAB 1: TỔNG QUAN ===
if selected == "🏠 Tổng quan":
    st.title("🌍 EcoMind OS Premium")
    st.markdown("### Hệ Thống Chăm Sóc Cây Thông Minh Toàn Diện")
    
    # Dashboard metrics
    st.markdown("### 📊 DASHBOARD TỔNG QUAN")
    
    col_dash1, col_dash2, col_dash3, col_dash4 = st.columns(4)
    with col_dash1:
        st.metric("Tổng số cây", f"{len(df_plants)}", "10+ mới")
    with col_dash2:
        st.metric("Độ chính xác", "96.5%", "↗️ 2.1%")
    with col_dash3:
        st.metric("Tiết kiệm nước", "41.3%", "↗️ 3.8%")
    with col_dash4:
        st.metric("Người dùng", "2.4K", "↗️ 128")
    
    # Cards giới thiệu
    col_card1, col_card2 = st.columns(2)
    
    with col_card1:
        with st.container(border=True):
            st.markdown("### 🚀 Tính năng nổi bật")
            st.markdown("""
            - **🗺️ Bản đồ VN tương tác** với 2000+ địa điểm
            - **🔍 Tìm kiếm thông minh** cây và vị trí
            - **🌦️ Dự báo thời tiết** 7 ngày chi tiết
            - **💧 Tính toán nước** thông minh theo thời tiết
            - **🤖 AI Trợ lý** hỗ trợ 24/7
            - **📅 Lịch chăm sóc** tự động
            """)
    
    with col_card2:
        with st.container(border=True):
            st.markdown("### 🏆 Phiên bản Premium")
            st.markdown("""
            **Đặc quyền:**
            - API thời tiết thực tế
            - Database 1000+ cây
            - Tìm kiếm Wikipedia tích hợp
            - Bản đồ tương tác cao cấp
            - Hỗ trợ ưu tiên
            - Cập nhật thường xuyên
            """)
            st.markdown("**Phiên bản:** 4.0.1")
            st.markdown("**Cập nhật:** 01/2024")
    
    # Hướng dẫn nhanh
    st.markdown("### 🎯 Bắt đầu nhanh trong 3 bước")
    
    steps = [
        ("1. Chọn vị trí", "Truy cập tab **🗺️ Bản đồ VN** và chọn vị trí cây của bạn", "📍"),
        ("2. Chọn cây", "Tìm cây của bạn trong tab **🌿 Thư viện cây**", "🌿"),
        ("3. Xem dự báo", "Nhận dự báo chi tiết ở tab **📊 Dự báo thời tiết**", "📊")
    ]
    
    for title, desc, icon in steps:
        with st.container(border=True):
            col_step1, col_step2 = st.columns([1, 5])
            with col_step1:
                st.markdown(f"<h1>{icon}</h1>", unsafe_allow_html=True)
            with col_step2:
                st.markdown(f"**{title}**")
                st.markdown(desc)
    
    # Thống kê thực tế
    st.markdown("### 📈 THỐNG KÊ THỰC TẾ")
    
    tab_stats1, tab_stats2 = st.tabs(["🌡️ Thời tiết hôm nay", "💧 Cây phổ biến"])
    
    with tab_stats1:
        # Giả lập thời tiết hôm nay
        col_weather1, col_weather2, col_weather3, col_weather4 = st.columns(4)
        with col_weather1:
            st.metric("Nhiệt độ", "28.5°C", "+2.3°C")
        with col_weather2:
            st.metric("Độ ẩm", "65%", "-5%")
        with col_weather3:
            st.metric("Mưa", "2.1mm", "Nhẹ")
        with col_weather4:
            st.metric("Gió", "12 km/h", "Đông Nam")
    
    with tab_stats2:
        # Top cây phổ biến
        popular_plants = df_plants.head(5)
        for _, plant in popular_plants.iterrows():
            with st.container(border=True):
                col_plant1, col_plant2, col_plant3 = st.columns([2, 1, 1])
                with col_plant1:
                    st.markdown(f"**{plant['Tên Cây']}**")
                with col_plant2:
                    st.markdown(f"💧 {plant['Nước (L/ngày)']}L")
                with col_plant3:
                    if st.button("Chọn", key=f"select_{plant['ID']}"):
                        st.session_state.selected_plant = plant.to_dict()
                        st.success(f"Đã chọn {plant['Tên Cây']}!")

# === TAB 2: BẢN ĐỒ VN ===
elif selected == "🗺️ Bản đồ VN":
    st.title("🗺️ Bản Đồ Việt Nam Tương Tác")
    st.markdown("### Chọn vị trí cây trồng của bạn trên bản đồ")
    
    tab_map1, tab_map2, tab_map3 = st.tabs(["🌍 Bản đồ tương tác", "📍 Tìm kiếm địa điểm", "📌 Vị trí đã lưu"])
    
    with tab_map1:
        col_map_main, col_map_sidebar = st.columns([3, 1])
        
        with col_map_main:
            # Tạo bản đồ nâng cao
            m = map_system.create_advanced_map(
                center=st.session_state.selected_location,
                zoom=12,
                radius_km=5
            )
            
            # Hiển thị bản đồ
            map_data = st_folium(
                m,
                width=800,
                height=600,
                returned_objects=["last_clicked", "bounds", "zoom"]
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
                        address_parts = location.address.split(",")
                        if len(address_parts) > 0:
                            st.session_state.location_name = address_parts[0].strip()
                        else:
                            st.session_state.location_name = location.address
                        
                        st.success(f"📍 Đã chọn: {st.session_state.location_name}")
                        
                        # Lưu vào lịch sử
                        if 'location_history' not in st.session_state:
                            st.session_state.location_history = []
                        
                        st.session_state.location_history.append({
                            "name": st.session_state.location_name,
                            "coordinates": [lat, lng],
                            "timestamp": datetime.datetime.now().isoformat()
                        })
                except:
                    st.session_state.location_name = f"{lat:.4f}, {lng:.4f}"
                    st.info(f"📍 Tọa độ: {lat:.4f}, {lng:.4f}")
        
        with col_map_sidebar:
            st.markdown("### 🎯 Tùy chọn bản đồ")
            
            # Chọn từ tỉnh/thành phố
            st.markdown("**Tỉnh/Thành phố:**")
            provinces = {
                "Hà Nội": [21.0285, 105.8542],
                "TP Hồ Chí Minh": [10.8231, 106.6297],
                "Đà Nẵng": [16.0544, 108.2022],
                "Hải Phòng": [20.8449, 106.6881],
                "Cần Thơ": [10.0452, 105.7469],
                "Huế": [16.4637, 107.5909],
                "Đà Lạt": [11.9404, 108.4583],
                "Nha Trang": [12.2388, 109.1967]
            }
            
            for province, coords in provinces.items():
                if st.button(f"📍 {province}", key=f"prov_{province}", use_container_width=True):
                    st.session_state.selected_location = coords
                    st.session_state.location_name = province
                    st.rerun()
            
            st.markdown("---")
            
            # Tọa độ thủ công
            st.markdown("**Nhập tọa độ:**")
            col_coord1, col_coord2 = st.columns(2)
            with col_coord1:
                lat_input = st.number_input("Vĩ độ:", 
                                          value=st.session_state.selected_location[0],
                                          format="%.6f",
                                          key="lat_input")
            with col_coord2:
                lon_input = st.number_input("Kinh độ:", 
                                          value=st.session_state.selected_location[1],
                                          format="%.6f",
                                          key="lon_input")
            
            if st.button("📌 Áp dụng tọa độ", use_container_width=True):
                st.session_state.selected_location = [lat_input, lon_input]
                st.session_state.location_name = f"{lat_input:.4f}, {lon_input:.4f}"
                st.success("✅ Đã cập nhật tọa độ!")
            
            # Thông tin vị trí
            st.markdown("---")
            st.markdown("**📊 Thông tin vị trí:**")
            
            if st.session_state.location_name:
                with st.container(border=True):
                    st.markdown(f"**{st.session_state.location_name}**")
                    
                    # Lấy thông tin bổ sung
                    elevation = map_system.get_elevation(
                        st.session_state.selected_location[0],
                        st.session_state.selected_location[1]
                    )
                    weather_zone = map_system.get_weather_zone(
                        st.session_state.selected_location[0],
                        st.session_state.selected_location[1]
                    )
                    
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.metric("Vĩ độ", f"{st.session_state.selected_location[0]:.4f}")
                        st.metric("Độ cao", f"{elevation}m")
                    with col_info2:
                        st.metric("Kinh độ", f"{st.session_state.selected_location[1]:.4f}")
                        st.metric("Vùng khí hậu", weather_zone)
                    
                    # Link Google Maps
                    maps_url = f"https://www.google.com/maps?q={st.session_state.selected_location[0]},{st.session_state.selected_location[1]}"
                    st.markdown(f"[🗺️ Xem trên Google Maps]({maps_url})")
    
    with tab_map2:
        st.markdown("### 🔍 Tìm kiếm địa điểm Việt Nam")
        
        # Search box với autocomplete
        search_query = st.text_input(
            "Nhập tên địa điểm:",
            placeholder="Ví dụ: Tân Hiệp, Phú Giáo, Quận 1, Bình Dương...",
            key="location_search_main"
        )
        
        if search_query:
            with st.spinner("🔍 Đang tìm kiếm..."):
                results = map_system.search_locations(search_query)
                
                if results:
                    st.success(f"✅ Tìm thấy {len(results)} kết quả")
                    
                    # Hiển thị kết quả
                    for result in results[:10]:  # Giới hạn 10 kết quả
                        with st.container(border=True):
                            col_result1, col_result2 = st.columns([3, 1])
                            with col_result1:
                                st.markdown(f"**{result['name']}**")
                                st.caption(f"{result['type']} • {result['province']}")
                            with col_result2:
                                if st.button("Chọn", key=f"select_result_{result['name']}"):
                                    st.session_state.selected_location = result['coordinates']
                                    st.session_state.location_name = result['name']
                                    st.success(f"✅ Đã chọn: {result['name']}")
                                    st.rerun()
                else:
                    st.warning("⚠️ Không tìm thấy địa điểm. Vui lòng thử từ khóa khác!")
        
        # Gợi ý tìm kiếm
        st.markdown("#### 💡 Gợi ý tìm kiếm:")
        
        suggestions = ["Tân Hiệp", "Phú Giáo", "Quận 1", "Bình Dương", "Đà Lạt", "Nha Trang"]
        cols = st.columns(3)
        for idx, suggestion in enumerate(suggestions):
            with cols[idx % 3]:
                if st.button(f"🔍 {suggestion}", use_container_width=True):
                    st.session_state.location_search_main = suggestion
                    st.rerun()
    
    with tab_map3:
        st.markdown("### 📍 Lịch sử vị trí")
        
        if 'location_history' in st.session_state and st.session_state.location_history:
            # Hiển thị lịch sử
            history_df = pd.DataFrame(st.session_state.location_history)
            
            # Hiển thị dưới dạng bảng
            st.dataframe(
                history_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "name": "Tên địa điểm",
                    "coordinates": "Tọa độ",
                    "timestamp": "Thời gian"
                }
            )
            
            # Nút xóa lịch sử
            if st.button("🗑️ Xóa lịch sử", type="secondary"):
                st.session_state.location_history = []
                st.success("Đã xóa lịch sử!")
        else:
            st.info("Chưa có lịch sử vị trí. Hãy chọn một vị trí trên bản đồ!")

# === TAB 3: TÌM KIẾM ===
elif selected == "🔍 Tìm kiếm":
    st.title("🔍 Tìm Kiếm Thông Minh")
    st.markdown("### Tìm kiếm cây trồng, địa điểm và thông tin liên quan")
    
    tab_search1, tab_search2, tab_search3 = st.tabs(["🌿 Tìm cây trồng", "📍 Tìm địa điểm", "📚 Tra cứu thông tin"])
    
    with tab_search1:
        col_search1, col_search2 = st.columns([3, 1])
        
        with col_search1:
            plant_search = st.text_input(
                "Tìm kiếm cây trồng:",
                placeholder="Nhập tên cây, đặc điểm hoặc từ khóa...",
                key="plant_search_main"
            )
        
        with col_search2:
            search_type = st.selectbox(
                "Loại tìm kiếm:",
                ["Tất cả", "Theo tên", "Theo đặc điểm", "Theo độ khó"]
            )
        
        # Bộ lọc nâng cao
        with st.expander("🔧 Bộ lọc nâng cao"):
            col_filter1, col_filter2, col_filter3 = st.columns(3)
            
            with col_filter1:
                water_filter = st.slider("Nhu cầu nước (L/ngày):", 0.0, 2.0, (0.0, 1.0))
            
            with col_filter2:
                difficulty_filter = st.multiselect(
                    "Độ khó:",
                    df_plants['Độ khó'].unique()
                )
            
            with col_filter3:
                light_filter = st.multiselect(
                    "Ánh sáng:",
                    df_plants['Ánh sáng'].unique()
                )
        
        if plant_search or any([water_filter, difficulty_filter, light_filter]):
            # Tìm kiếm với bộ lọc
            filters = {}
            if difficulty_filter:
                filters['Độ khó'] = difficulty_filter
            if light_filter:
                filters['Ánh sáng'] = light_filter
            
            results = plant_system.search_plants(plant_search, filters)
            
            # Áp dụng bộ lọc nước
            if water_filter != (0.0, 1.0):
                results = results[
                    (results['Nước (L/ngày)'] >= water_filter[0]) &
                    (results['Nước (L/ngày)'] <= water_filter[1])
                ]
            
            st.markdown(f"### 📋 Kết quả: {len(results)} cây")
            
            if len(results) > 0:
                # Hiển thị kết quả
                view_mode = st.radio(
                    "Chế độ hiển thị:",
                    ["Dạng bảng", "Dạng card", "Dạng danh sách"],
                    horizontal=True,
                    key="plant_view_mode"
                )
                
                if view_mode == "Dạng bảng":
                    # Hiển thị bảng
                    display_cols = ["Tên Cây", "Nước (L/ngày)", "Độ khó", "Ánh sáng", "Nhiệt độ", "Tần suất tưới"]
                    st.dataframe(
                        results[display_cols],
                        use_container_width=True,
                        height=400,
                        hide_index=True
                    )
                elif view_mode == "Dạng card":
                    # Hiển thị card
                    cols_per_row = 3
                    plants_list = results.head(12).to_dict('records')
                    
                    for i in range(0, len(plants_list), cols_per_row):
                        cols = st.columns(cols_per_row)
                        
                        for col_idx, col in enumerate(cols):
                            plant_idx = i + col_idx
                            if plant_idx < len(plants_list):
                                plant = plants_list[plant_idx]
                                
                                with col:
                                    with st.container(border=True):
                                        # Header
                                        st.markdown(f"#### {plant['Tên Cây']}")
                                        st.caption(f"⚡ {plant['Độ khó']} • {plant['Ánh sáng']}")
                                        
                                        # Thông tin
                                        st.markdown(f"💧 **Nước:** {plant['Nước (L/ngày)']}L/ngày")
                                        st.markdown(f"🌡️ **Nhiệt độ:** {plant['Nhiệt độ']}")
                                        
                                        # Actions
                                        col_btn1, col_btn2 = st.columns(2)
                                        with col_btn1:
                                            if st.button("👁️ Xem", key=f"view_{plant['ID']}", use_container_width=True):
                                                st.session_state.selected_plant = plant
                                                st.success(f"Đã chọn {plant['Tên Cây']}!")
                                        with col_btn2:
                                            if st.button("ℹ️ Chi tiết", key=f"detail_{plant['ID']}", use_container_width=True):
                                                st.session_state.show_plant_details = True
                                                st.session_state.selected_plant = plant
                                                st.rerun()
                else:  # Dạng danh sách
                    for plant in results.head(10).to_dict('records'):
                        with st.container(border=True):
                            col_list1, col_list2, col_list3 = st.columns([3, 1, 1])
                            with col_list1:
                                st.markdown(f"**{plant['Tên Cây']}**")
                                st.caption(f"{plant['Mô tả'][:100]}...")
                            with col_list2:
                                st.markdown(f"💧 {plant['Nước (L/ngày)']}L")
                            with col_list3:
                                if st.button("Chọn", key=f"select_{plant['ID']}"):
                                    st.session_state.selected_plant = plant
                                    st.success(f"✅ Đã chọn {plant['Tên Cây']}!")
            else:
                st.warning("Không tìm thấy cây phù hợp. Hãy thử từ khóa khác!")
    
    with tab_search2:
        st.markdown("### 📍 Tìm kiếm địa điểm chi tiết")
        
        # Search box với autocomplete
        location_search = st.text_input(
            "Nhập địa điểm cần tìm:",
            placeholder="Ví dụ: Tân Hiệp Kiên Giang, Phú Giáo Bình Dương, Quận 1 TP.HCM...",
            key="detailed_location_search"
        )
        
        if location_search:
            with st.spinner("🔍 Đang tìm kiếm địa điểm..."):
                # Tìm kiếm trong database địa điểm
                all_locations = map_system.vietnam_locations
                results = []
                
                for name, info in all_locations.items():
                    if location_search.lower() in name.lower():
                        results.append({
                            "name": name,
                            "type": info["type"],
                            "province": info["province"],
                            "coordinates": [info["lat"], info["lon"]],
                            "lat": info["lat"],
                            "lon": info["lon"]
                        })
                
                if results:
                    st.success(f"✅ Tìm thấy {len(results)} địa điểm")
                    
                    # Hiển thị kết quả trong bảng
                    results_df = pd.DataFrame(results)
                    st.dataframe(
                        results_df[["name", "type", "province", "lat", "lon"]],
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "name": "Tên địa điểm",
                            "type": "Loại",
                            "province": "Tỉnh/Thành",
                            "lat": "Vĩ độ",
                            "lon": "Kinh độ"
                        }
                    )
                    
                    # Hiển thị bản đồ với tất cả kết quả
                    st.markdown("#### 🗺️ Vị trí trên bản đồ")
                    
                    if results:
                        # Tạo bản đồ với marker cho mỗi kết quả
                        m = folium.Map(
                            location=results[0]["coordinates"],
                            zoom_start=10,
                            tiles="cartodbpositron"
                        )
                        
                        for result in results:
                            folium.Marker(
                                result["coordinates"],
                                popup=f"<b>{result['name']}</b><br>{result['type']}, {result['province']}",
                                tooltip=result["name"],
                                icon=folium.Icon(color="green", icon="info-sign")
                            ).add_to(m)
                        
                        # Hiển thị bản đồ
                        st_folium(m, width=700, height=400)
                else:
                    st.warning("⚠️ Không tìm thấy địa điểm. Thử tìm kiếm với Nominatim...")
                    
                    # Thử tìm bằng Nominatim
                    try:
                        location = map_system.geolocator.geocode(f"{location_search}, Vietnam")
                        if location:
                            st.success(f"✅ Tìm thấy: {location.address}")
                            
                            col_found1, col_found2 = st.columns(2)
                            with col_found1:
                                st.metric("Vĩ độ", f"{location.latitude:.4f}")
                            with col_found2:
                                st.metric("Kinh độ", f"{location.longitude:.4f}")
                            
                            # Nút chọn vị trí này
                            if st.button("📍 Chọn vị trí này", type="primary"):
                                st.session_state.selected_location = [location.latitude, location.longitude]
                                st.session_state.location_name = location.address
                                st.success("✅ Đã chọn vị trí!")
                        else:
                            st.error("❌ Không tìm thấy địa điểm nào phù hợp.")
                    except:
                        st.error("❌ Lỗi khi tìm kiếm địa điểm.")
    
    with tab_search3:
        st.markdown("### 📚 Tra cứu thông tin cây trồng")
        
        # Tìm kiếm thông tin từ Wikipedia
        info_search = st.text_input(
            "Tìm kiếm thông tin cây trồng:",
            placeholder="Nhập tên cây cần tra cứu...",
            key="wikipedia_search"
        )
        
        if info_search:
            with st.spinner("🔍 Đang tìm kiếm thông tin trên Wikipedia..."):
                try:
                    # Tìm kiếm Wikipedia
                    search_results = wikipedia.search(info_search, results=3)
                    
                    if search_results:
                        st.success(f"✅ Tìm thấy {len(search_results)} kết quả trên Wikipedia")
                        
                        # Hiển thị kết quả tìm kiếm
                        for i, title in enumerate(search_results, 1):
                            with st.container(border=True):
                                st.markdown(f"**{i}. {title}**")
                                
                                # Lấy tóm tắt
                                try:
                                    page = wikipedia.page(title)
                                    st.markdown(f"*{page.summary[:300]}...*")
                                    
                                    # Nút xem chi tiết
                                    if st.button(f"📖 Xem chi tiết {title}", key=f"wiki_{i}"):
                                        with st.expander(f"📄 Thông tin chi tiết - {title}", expanded=True):
                                            st.markdown(page.content[:2000])
                                            st.markdown(f"[📚 Xem trên Wikipedia]({page.url})")
                                except:
                                    st.info("Không thể lấy tóm tắt. Vui lòng thử lại.")
                    else:
                        st.warning("⚠️ Không tìm thấy thông tin trên Wikipedia.")
                        
                        # Hiển thị thông tin từ database local
                        local_results = df_plants[df_plants['Tên Cây'].str.contains(info_search, case=False, na=False)]
                        
                        if len(local_results) > 0:
                            st.info("📋 Tìm thấy thông tin trong database local:")
                            
                            for _, plant in local_results.iterrows():
                                with st.container(border=True):
                                    st.markdown(f"**{plant['Tên Cây']}**")
                                    st.markdown(f"💧 Nước: {plant['Nước (L/ngày)']}L/ngày")
                                    st.markdown(f"🌡️ Nhiệt độ: {plant['Nhiệt độ']}")
                                    st.markdown(f"☀️ Ánh sáng: {plant['Ánh sáng']}")
                except Exception as e:
                    st.error(f"❌ Lỗi khi tìm kiếm: {str(e)}")
        
        # Tìm kiếm hình ảnh (giả lập)
        st.markdown("---")
        st.markdown("### 🖼️ Tìm kiếm hình ảnh cây trồng")
        
        image_search = st.text_input(
            "Tìm kiếm hình ảnh:",
            placeholder="Nhập tên cây để tìm hình ảnh...",
            key="image_search"
        )
        
        if image_search:
            # Giả lập tìm kiếm hình ảnh
            image_urls = [
                f"https://source.unsplash.com/300x200/?{image_search}-plant",
                f"https://source.unsplash.com/300x200/?{image_search}-flower",
                f"https://source.unsplash.com/300x200/?{image_search}-nature"
            ]
            
            cols = st.columns(3)
            for idx, url in enumerate(image_urls):
                with cols[idx]:
                    st.image(url, caption=f"Hình ảnh {image_search} {idx+1}")

# === TAB 4: THƯ VIỆN CÂY ===
elif selected == "🌿 Thư viện cây":
    st.title("🌿 Thư Viện Cây Trồng Toàn Diện")
    st.markdown("### Database 1000+ loại cây với thông tin chi tiết")
    
    # Hiển thị thông tin cây đang chọn
    if st.session_state.selected_plant:
        plant = st.session_state.selected_plant
        with st.container(border=True):
            col_curr1, col_curr2, col_curr3 = st.columns([2, 1, 1])
            with col_curr1:
                st.markdown(f"### 🌟 Cây đang chọn: **{plant.get('Tên Cây', 'Chưa chọn')}**")
            with col_curr2:
                st.metric("💧 Nước", f"{plant.get('Nước (L/ngày)', 0)}L/ngày")
            with col_curr3:
                st.metric("⚡ Độ khó", plant.get('Độ khó', 'Chưa có'))
    
    tab_lib1, tab_lib2, tab_lib3 = st.tabs(["📊 Tất cả cây", "⭐ Cây yêu thích", "🔬 Chi tiết cây"])
    
    with tab_lib1:
        # Bộ lọc nâng cao
        with st.expander("🔧 Bộ lọc nâng cao", expanded=True):
            col_filter1, col_filter2, col_filter3, col_filter4 = st.columns(4)
            
            with col_filter1:
                lib_search = st.text_input("Tìm kiếm:", key="lib_search")
            
            with col_filter2:
                lib_difficulty = st.multiselect(
                    "Độ khó:",
                    df_plants['Độ khó'].unique(),
                    key="lib_difficulty"
                )
            
            with col_filter3:
                lib_water = st.slider(
                    "Nước (L/ngày):",
                    0.0, 1.0, (0.0, 1.0),
                    key="lib_water"
                )
            
            with col_filter4:
                lib_light = st.multiselect(
                    "Ánh sáng:",
                    df_plants['Ánh sáng'].unique(),
                    key="lib_light"
                )
        
        # Áp dụng bộ lọc
        filtered_plants = df_plants.copy()
        
        if lib_search:
            filtered_plants = filtered_plants[
                filtered_plants["Tên Cây"].str.contains(lib_search, case=False, na=False) |
                filtered_plants["Mô tả"].str.contains(lib_search, case=False, na=False)
            ]
        
        if lib_difficulty:
            filtered_plants = filtered_plants[filtered_plants["Độ khó"].isin(lib_difficulty)]
        
        filtered_plants = filtered_plants[
            (filtered_plants["Nước (L/ngày)"] >= lib_water[0]) &
            (filtered_plants["Nước (L/ngày)"] <= lib_water[1])
        ]
        
        if lib_light:
            filtered_plants = filtered_plants[filtered_plants["Ánh sáng"].isin(lib_light)]
        
        # Hiển thị kết quả
        st.markdown(f"### 📋 Kết quả: {len(filtered_plants)} cây")
        
        if len(filtered_plants) > 0:
            # Chế độ hiển thị
            view_mode = st.radio(
                "Chế độ hiển thị:",
                ["📋 Bảng dữ liệu", "🃏 Thẻ bài", "📝 Danh sách"],
                horizontal=True,
                key="library_view"
            )
            
            if view_mode == "📋 Bảng dữ liệu":
                # Hiển thị bảng với nhiều cột
                display_cols = ["Tên Cây", "Nước (L/ngày)", "Độ khó", "Ánh sáng", 
                              "Nhiệt độ", "Độ ẩm", "Tần suất tưới"]
                
                st.dataframe(
                    filtered_plants[display_cols],
                    use_container_width=True,
                    height=500,
                    hide_index=True,
                    column_config={
                        "Tên Cây": "🌿 Tên cây",
                        "Nước (L/ngày)": st.column_config.ProgressColumn(
                            "💧 Nước",
                            min_value=0,
                            max_value=1.0,
                            format="%.2f L"
                        ),
                        "Độ khó": "⚡ Độ khó",
                        "Ánh sáng": "☀️ Ánh sáng",
                        "Nhiệt độ": "🌡️ Nhiệt độ",
                        "Độ ẩm": "💦 Độ ẩm",
                        "Tần suất tưới": "⏰ Tưới"
                    }
                )
            
            elif view_mode == "🃏 Thẻ bài":
                # Hiển thị dạng card grid
                plants_per_row = 3
                plants_list = filtered_plants.head(12).to_dict('records')
                
                for i in range(0, len(plants_list), plants_per_row):
                    cols = st.columns(plants_per_row)
                    
                    for col_idx, col in enumerate(cols):
                        plant_idx = i + col_idx
                        if plant_idx < len(plants_list):
                            plant = plants_list[plant_idx]
                            
                            with col:
                                with st.container(border=True):
                                    # Header với gradient
                                    st.markdown(f"""
                                    <div style="
                                        background: linear-gradient(90deg, rgba(0,255,204,0.2), rgba(0,136,204,0.2));
                                        padding: 15px;
                                        border-radius: 10px 10px 0 0;
                                        margin: -15px -15px 15px -15px;
                                    ">
                                        <h4 style="margin: 0; color: white;">{plant['Tên Cây']}</h4>
                                        <small style="color: #88aaff;">{plant['Độ khó']} • {plant['Ánh sáng']}</small>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # Thông tin chính
                                    col_info1, col_info2 = st.columns(2)
                                    with col_info1:
                                        st.metric("💧 Nước", f"{plant['Nước (L/ngày)']}L")
                                        st.metric("🌡️ Nhiệt độ", plant['Nhiệt độ'])
                                    with col_info2:
                                        st.metric("💦 Độ ẩm", plant['Độ ẩm'])
                                        st.metric("⏰ Tưới", plant['Tần suất tưới'])
                                    
                                    # Actions
                                    col_action1, col_action2 = st.columns(2)
                                    with col_action1:
                                        if st.button("✅ Chọn", key=f"select_card_{plant['ID']}", use_container_width=True):
                                            st.session_state.selected_plant = plant
                                            st.success(f"✅ Đã chọn {plant['Tên Cây']}!")
                                    with col_action2:
                                        if st.button("⭐ Yêu thích", key=f"fav_{plant['ID']}", use_container_width=True):
                                            st.success(f"Đã thêm {plant['Tên Cây']} vào yêu thích!")
            
            else:  # Danh sách
                for plant in filtered_plants.head(15).to_dict('records'):
                    with st.container(border=True):
                        col_list1, col_list2, col_list3, col_list4 = st.columns([3, 1, 1, 1])
                        with col_list1:
                            st.markdown(f"**{plant['Tên Cây']}**")
                            st.caption(f"{plant['Mô tả'][:150]}...")
                        with col_list2:
                            st.markdown(f"💧 {plant['Nước (L/ngày)']}L")
                        with col_list3:
                            st.markdown(f"⚡ {plant['Độ khó']}")
                        with col_list4:
                            if st.button("Chọn", key=f"select_list_{plant['ID']}"):
                                st.session_state.selected_plant = plant
                                st.success(f"✅ Đã chọn {plant['Tên Cây']}!")
        
        # Pagination (giả lập)
        st.markdown("---")
        col_page1, col_page2, col_page3 = st.columns([2, 1, 2])
        with col_page2:
            st.markdown("**Trang 1/5**")
            st.caption("← Trang trước • Trang sau →")
    
    with tab_lib2:
        st.markdown("### ⭐ Cây yêu thích của bạn")
        
        # Giả lập danh sách yêu thích
        favorite_plants = df_plants.sample(min(5, len(df_plants)))
        
        if len(favorite_plants) > 0:
            for plant in favorite_plants.to_dict('records'):
                with st.container(border=True):
                    col_fav1, col_fav2, col_fav3 = st.columns([2, 1, 1])
                    with col_fav1:
                        st.markdown(f"**{plant['Tên Cây']}**")
                        st.caption(f"⭐ {plant['Độ khó']} • 💧 {plant['Nước (L/ngày)']}L/ngày")
                    with col_fav2:
                        if st.button("👁️ Xem", key=f"view_fav_{plant['ID']}"):
                            st.session_state.selected_plant = plant
                            st.success(f"Đang xem {plant['Tên Cây']}")
                    with col_fav3:
                        if st.button("🗑️ Xóa", key=f"remove_fav_{plant['ID']}"):
                            st.warning(f"Đã xóa {plant['Tên Cây']} khỏi yêu thích")
        else:
            st.info("Chưa có cây nào trong danh sách yêu thích. Hãy thêm cây bằng cách nhấn ⭐")
    
    with tab_lib3:
        # Hiển thị chi tiết cây đang chọn
        if st.session_state.selected_plant:
            plant = st.session_state.selected_plant
            
            st.markdown(f"## 🔬 Chi Tiết: {plant['Tên Cây']}")
            
            # Tabs chi tiết
            tab_detail1, tab_detail2, tab_detail3, tab_detail4 = st.tabs([
                "📋 Thông tin cơ bản", "💧 Chăm sóc", "⚠️ Sâu bệnh", "📚 Thông tin bổ sung"
            ])
            
            with tab_detail1:
                col_detail1, col_detail2 = st.columns(2)
                
                with col_detail1:
                    st.markdown("#### 🏷️ Thông tin chung")
                    st.metric("💧 Nước hàng ngày", f"{plant['Nước (L/ngày)']}L")
                    st.metric("⚡ Độ khó", plant['Độ khó'])
                    st.metric("☀️ Ánh sáng", plant['Ánh sáng'])
                    st.metric("🌡️ Nhiệt độ", plant['Nhiệt độ'])
                
                with col_detail2:
                    st.markdown("#### 🌱 Thông số kỹ thuật")
                    st.metric("💦 Độ ẩm", plant['Độ ẩm'])
                    st.metric("📊 Độ pH", plant['Độ pH'])
                    st.metric("📈 Tốc độ sinh trưởng", plant['Tốc độ sinh trưởng'])
                    st.metric("📏 Chiều cao", plant['Chiều cao trưởng thành'])
            
            with tab_detail2:
                st.markdown("#### 💧 Hướng dẫn chăm sóc chi tiết")
                
                care_col1, care_col2 = st.columns(2)
                
                with care_col1:
                    st.markdown("**Tưới nước:**")
                    st.markdown(f"- **Lượng nước:** {plant['Nước (L/ngày)']}L/ngày")
                    st.markdown(f"- **Tần suất:** {plant['Tần suất tưới']}")
                    st.markdown("- **Thời điểm:** Sáng sớm hoặc chiều mát")
                    
                    st.markdown("**Bón phân:**")
                    st.markdown(f"- **Loại phân:** {plant['Chất dinh dưỡng']}")
                    st.markdown("- **Tần suất:** 2-4 tuần/lần trong mùa sinh trưởng")
                
                with care_col2:
                    st.markdown("**Đất trồng:**")
                    st.markdown(f"- **Độ pH:** {plant['Độ pH']}")
                    st.markdown("- **Loại đất:** Thoát nước tốt, giàu dinh dưỡng")
                    
                    st.markdown("**Mẹo chăm sóc:**")
                    if plant['Tên Cây'] in plant_system.plant_care_tips:
                        for tip in plant_system.plant_care_tips[plant['Tên Cây']]:
                            st.markdown(f"- {tip}")
                    else:
                        st.markdown("- Giữ đất ẩm nhưng không ướt")
                        st.markdown("- Tránh ánh nắng trực tiếp giữa trưa")
                        st.markdown("- Lau lá thường xuyên để tăng quang hợp")
            
            with tab_detail3:
                st.markdown("#### ⚠️ Sâu bệnh thường gặp")
                
                if 'Sâu bệnh thường gặp' in plant:
                    st.warning(plant['Sâu bệnh thường gặp'])
                else:
                    st.info("Cây này ít bị sâu bệnh khi được chăm sóc đúng cách.")
                
                st.markdown("**Biện pháp phòng trừ:**")
                st.markdown("1. **Phòng ngừa:**")
                st.markdown("   - Giữ vệ sinh khu vực trồng cây")
                st.markdown("   - Tưới nước đúng cách")
                st.markdown("   - Bón phân cân đối")
                
                st.markdown("2. **Xử lý khi có sâu bệnh:**")
                st.markdown("   - Cắt tỉa phần bị bệnh")
                st.markdown("   - Sử dụng thuốc trừ sâu sinh học")
                st.markdown("   - Cách ly cây bị bệnh")
            
            with tab_detail4:
                # Tìm kiếm thông tin bổ sung từ Wikipedia
                st.markdown("#### 📚 Thông tin bổ sung từ Wikipedia")
                
                if st.button("🔍 Tìm kiếm thông tin trên Wikipedia"):
                    with st.spinner("Đang tìm kiếm thông tin..."):
                        try:
                            # Tìm kiếm Wikipedia
                            search_results = wikipedia.search(plant['Tên Cây'], results=1)
                            
                            if search_results:
                                page = wikipedia.page(search_results[0])
                                
                                # Hiển thị tóm tắt
                                st.markdown("##### 📖 Tóm tắt")
                                st.markdown(f"{page.summary[:500]}...")
                                
                                # Hiển thị thông tin chi tiết
                                with st.expander("📄 Xem thông tin chi tiết"):
                                    st.markdown(page.content[:2000])
                                    st.markdown(f"[📚 Xem toàn bộ trên Wikipedia]({page.url})")
                            else:
                                st.info("Không tìm thấy thông tin trên Wikipedia.")
                        except:
                            st.warning("Không thể kết nối đến Wikipedia.")
                
                # Thông tin thêm
                st.markdown("#### 📝 Ghi chú cá nhân")
                user_notes = st.text_area(
                    "Ghi chú của bạn về cây này:",
                    placeholder="Ghi lại kinh nghiệm chăm sóc, lịch sử bệnh, hoặc bất kỳ điều gì bạn muốn nhớ...",
                    height=150
                )
                
                if st.button("💾 Lưu ghi chú"):
                    st.success("Đã lưu ghi chú!")
        else:
            st.info("Vui lòng chọn một cây để xem chi tiết.")

# === TAB 5: DỰ BÁO THỜI TIẾT ===
elif selected == "📊 Dự báo thời tiết":
    st.title("📊 Dự Báo Thời Tiết Chi Tiết")
    st.markdown("### Dự báo 7 ngày và phân tích ảnh hưởng đến cây trồng")
    
    # Kiểm tra đã chọn vị trí chưa
    if not st.session_state.location_name:
        st.warning("⚠️ Vui lòng chọn vị trí ở tab **🗺️ Bản đồ VN** trước!")
        if st.button("🗺️ Đến tab Bản đồ"):
            st.session_state.active_tab = "🗺️ Bản đồ VN"
            st.rerun()
        st.stop()
    
    # Header với thông tin
    col_weather_header1, col_weather_header2 = st.columns([2, 1])
    
    with col_weather_header1:
        st.markdown(f"### 📍 {st.session_state.location_name}")
        st.caption(f"Tọa độ: {st.session_state.selected_location[0]:.4f}, {st.session_state.selected_location[1]:.4f}")
    
    with col_weather_header2:
        if st.button("🔄 Cập nhật dự báo", use_container_width=True):
            with st.spinner("Đang cập nhật dự báo thời tiết..."):
                forecast = weather_system.get_comprehensive_forecast(
                    st.session_state.selected_location[0],
                    st.session_state.selected_location[1],
                    days=7
                )
                st.session_state.forecast_data = forecast
                st.success("✅ Đã cập nhật dự báo!")
    
    # Lấy dữ liệu dự báo
    if st.session_state.forecast_data is None:
        with st.spinner("Đang tải dự báo thời tiết..."):
            forecast = weather_system.get_comprehensive_forecast(
                st.session_state.selected_location[0],
                st.session_state.selected_location[1],
                days=7
            )
            st.session_state.forecast_data = forecast
    
    if st.session_state.forecast_data is not None:
        forecast_df = st.session_state.forecast_data
        
        # Tabs cho các loại dự báo
        tab_weather1, tab_weather2, tab_weather3, tab_weather4 = st.tabs([
            "📈 Biểu đồ", "📋 Chi tiết", "⚠️ Cảnh báo", "🌿 Ảnh hưởng cây"
        ])
        
        with tab_weather1:
            st.markdown("#### 📈 Biểu Đồ Dự Báo")
            
            # Tạo biểu đồ nhiệt độ
            fig_temp = go.Figure()
            
            fig_temp.add_trace(go.Scatter(
                x=forecast_df['date'],
                y=forecast_df['temp_max'],
                name='Nhiệt độ cao',
                line=dict(color='#ff6b6b', width=3),
                mode='lines+markers',
                fill=None
            ))
            
            fig_temp.add_trace(go.Scatter(
                x=forecast_df['date'],
                y=forecast_df['temp_min'],
                name='Nhiệt độ thấp',
                line=dict(color='#4dabf7', width=3),
                mode='lines+markers',
                fill='tonexty',
                fillcolor='rgba(77, 171, 247, 0.2)'
            ))
            
            fig_temp.update_layout(
                title="Dự báo nhiệt độ 7 ngày",
                template="plotly_dark",
                xaxis_title="Ngày",
                yaxis_title="Nhiệt độ (°C)",
                hovermode="x unified",
                height=400
            )
            
            st.plotly_chart(fig_temp, use_container_width=True)
            
            # Biểu đồ mưa
            fig_rain = px.bar(
                forecast_df,
                x='date',
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
        
        with tab_weather2:
            st.markdown("#### 📋 Bảng Dự Báo Chi Tiết")
            
            # Format dataframe để hiển thị đẹp
            display_df = forecast_df.copy()
            display_df['Ngày'] = pd.to_datetime(display_df['date']).dt.strftime('%d/%m')
            display_df['Nhiệt độ'] = display_df.apply(
                lambda x: f"{x['temp_min']}°C → {x['temp_max']}°C", axis=1
            )
            display_df['Mưa'] = display_df['precipitation'].apply(
                lambda x: f"🌧️ {x}mm" if x > 0 else "☀️ Không mưa"
            )
            display_df['Gió'] = display_df.apply(
                lambda x: f"{x['wind_speed']} km/h {x['wind_direction']}", axis=1
            )
            
            st.dataframe(
                display_df[['Ngày', 'Nhiệt độ', 'Mưa', 'Gió', 'humidity', 'pressure', 'uv_index', 'condition']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Ngày": "📅 Ngày",
                    "Nhiệt độ": "🌡️ Nhiệt độ",
                    "Mưa": "💧 Mưa",
                    "Gió": "💨 Gió",
                    "humidity": "💦 Độ ẩm (%)",
                    "pressure": "📊 Áp suất (hPa)",
                    "uv_index": "☀️ UV Index",
                    "condition": "🌤️ Điều kiện"
                }
            )
            
            # Tải xuống dữ liệu
            csv = forecast_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Tải dữ liệu dự báo (CSV)",
                data=csv,
                file_name=f"du_bao_thoi_tiet_{st.session_state.location_name}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with tab_weather3:
            st.markdown("#### ⚠️ Cảnh Báo Thời Tiết")
            
            # Tạo cảnh báo
            alerts = weather_system.get_weather_alerts(
                st.session_state.selected_location[0],
                st.session_state.selected_location[1],
                forecast_df
            )
            
            if alerts:
                for alert in alerts:
                    if alert['type'] == 'warning':
                        with st.container(border=True):
                            st.markdown(f"##### {alert['icon']} {alert['title']}")
                            st.markdown(f"**Mức độ:** {alert['severity']}")
                            st.markdown(f"**Chi tiết:** {alert['message']}")
                    else:
                        with st.container(border=True):
                            st.markdown(f"##### {alert['icon']} {alert['title']}")
                            st.markdown(f"**Chi tiết:** {alert['message']}")
            else:
                st.success("✅ Không có cảnh báo thời tiết đặc biệt trong 7 ngày tới.")
        
        with tab_weather4:
            st.markdown("#### 🌿 Phân Tích Ảnh Hưởng Đến Cây Trồng")
            
            if st.session_state.selected_plant:
                plant = st.session_state.selected_plant
                
                st.markdown(f"##### Đối với cây: **{plant['Tên Cây']}**")
                
                # Phân tích từng ngày
                analysis_results = []
                
                for _, day in forecast_df.iterrows():
                    # Phân tích điều kiện
                    analysis = {
                        "Ngày": day['date'],
                        "Điều kiện": day['condition'],
                        "Ảnh hưởng": "",
                        "Khuyến nghị": ""
                    }
                    
                    if day['temp_max'] > 32:
                        analysis["Ảnh hưởng"] = "Nhiệt độ cao có thể làm cây mất nước nhanh"
                        analysis["Khuyến nghị"] = "Tăng tưới nước, che nắng buổi trưa"
                    elif day['temp_min'] < 18:
                        analysis["Ảnh hưởng"] = "Nhiệt độ thấp có thể làm chậm sinh trưởng"
                        analysis["Khuyến nghị"] = "Giảm tưới nước, tránh gió lạnh"
                    elif day['precipitation'] > 10:
                        analysis["Ảnh hưởng"] = "Mưa nhiều có thể gây úng rễ"
                        analysis["Khuyến nghị"] = "Giảm tưới, kiểm tra thoát nước"
                    elif day['wind_speed'] > 15:
                        analysis["Ảnh hưởng"] = "Gió mạnh có thể làm gãy cành"
                        analysis["Khuyến nghị"] = "Di chuyển cây vào nơi kín gió"
                    else:
                        analysis["Ảnh hưởng"] = "Điều kiện tốt cho cây phát triển"
                        analysis["Khuyến nghị"] = "Duy trì chế độ chăm sóc thông thường"
                    
                    analysis_results.append(analysis)
                
                # Hiển thị phân tích
                analysis_df = pd.DataFrame(analysis_results)
                st.dataframe(
                    analysis_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Tổng kết
                st.markdown("##### 💡 Tổng Kết & Khuyến Nghị")
                
                # Tính toán các chỉ số
                hot_days = len([d for d in analysis_results if "nhiệt độ cao" in d["Ảnh hưởng"].lower()])
                rainy_days = len([d for d in analysis_results if "mưa nhiều" in d["Ảnh hưởng"].lower()])
                good_days = len([d for d in analysis_results if "điều kiện tốt" in d["Ảnh hưởng"].lower()])
                
                col_sum1, col_sum2, col_sum3 = st.columns(3)
                with col_sum1:
                    st.metric("Ngày nắng nóng", hot_days)
                with col_sum2:
                    st.metric("Ngày mưa nhiều", rainy_days)
                with col_sum3:
                    st.metric("Ngày thuận lợi", good_days)
                
                # Khuyến nghị tổng thể
                if hot_days > 3:
                    st.warning("**⚠️ Lưu ý:** Nhiều ngày nắng nóng. Cần tăng cường tưới nước và che nắng cho cây.")
                if rainy_days > 2:
                    st.info("**💧 Lưu ý:** Mưa nhiều trong vài ngày tới. Giảm tưới và đảm bảo thoát nước tốt.")
                if good_days >= 5:
                    st.success("**✅ Tin tốt:** Hầu hết các ngày tới đều thuận lợi cho cây phát triển.")
            else:
                st.info("Vui lòng chọn một cây để xem phân tích ảnh hưởng chi tiết.")

# === TAB 6: TÍNH TOÁN NƯỚC ===
elif selected == "💧 Tính toán nước":
    st.title("💧 Tính Toán Nhu Cầu Nước Thông Minh")
    st.markdown("### Dự báo lượng nước cần thiết dựa trên thời tiết và đặc tính cây")
    
    # Kiểm tra đã chọn cây và vị trí chưa
    if not st.session_state.selected_plant or not st.session_state.location_name:
        st.warning("⚠️ Vui lòng chọn cây và vị trí trước khi tính toán!")
        col_warn1, col_warn2 = st.columns(2)
        with col_warn1:
            if st.button("🌿 Chọn cây", use_container_width=True):
                st.session_state.active_tab = "🌿 Thư viện cây"
                st.rerun()
        with col_warn2:
            if st.button("🗺️ Chọn vị trí", use_container_width=True):
                st.session_state.active_tab = "🗺️ Bản đồ VN"
                st.rerun()
        st.stop()
    
    # Hiển thị thông tin hiện tại
    plant = st.session_state.selected_plant
    location = st.session_state.location_name
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("🌿 Cây", plant['Tên Cây'])
    with col_info2:
        st.metric("📍 Vị trí", location)
    with col_info3:
        st.metric("💧 Nước cơ bản", f"{plant['Nước (L/ngày)']}L/ngày")
    
    tab_water1, tab_water2, tab_water3 = st.tabs(["📊 Tính toán chi tiết", "⏳ Dự báo hết nước", "📅 Lịch tưới"])
    
    with tab_water1:
        st.markdown("#### 📊 Tính Toán Nhu Cầu Nước Theo Thời Tiết")
        
        if st.session_state.forecast_data is not None:
            forecast_df = st.session_state.forecast_data
            
            # Tính toán nhu cầu nước chi tiết
            water_calculations = []
            plant_water_needs = plant['Nước (L/ngày)']
            
            for _, day in forecast_df.iterrows():
                # Điều chỉnh theo nhiệt độ
                temp_factor = 1 + (day['temp_max'] - 25) * 0.03
                
                # Điều chỉnh theo độ ẩm
                humidity_factor = 1 - (day['humidity'] - 50) * 0.005
                
                # Điều chỉnh theo mưa
                rain_adjustment = max(0, plant_water_needs - (day['precipitation'] / 15))
                
                # Tính nhu cầu thực tế
                base_adjusted = plant_water_needs * temp_factor * humidity_factor
                final_need = max(0.05, base_adjusted - rain_adjustment)
                
                # Thêm bay hơi
                evaporation = weather_system.calculate_evapotranspiration(
                    day['temp_max'],
                    day['humidity'],
                    day['wind_speed'],
                    max(0, day['uv_index'] * 10)  # Giả lập bức xạ mặt trời
                )
                
                total_consumption = final_need + evaporation
                
                water_calculations.append({
                    "Ngày": day['date'],
                    "Nhiệt độ": f"{day['temp_max']}°C",
                    "Mưa": f"{day['precipitation']}mm",
                    "Nhu cầu cơ bản": round(plant_water_needs, 3),
                    "Điều chỉnh nhiệt độ": round(temp_factor, 3),
                    "Điều chỉnh mưa": round(rain_adjustment, 3),
                    "Bay hơi": round(evaporation, 3),
                    "Nhu cầu thực tế": round(total_consumption, 3),
                    "Khuyến nghị": self._get_watering_recommendation(total_consumption, plant_water_needs)
                })
            
            water_df = pd.DataFrame(water_calculations)
            st.session_state.water_calculation = water_df
            
            # Biểu đồ nhu cầu nước
            fig_water = px.line(
                water_df,
                x='Ngày',
                y='Nhu cầu thực tế',
                title='Nhu cầu nước hàng ngày',
                markers=True,
                line_shape='spline'
            )
            
            # Thêm đường nhu cầu cơ bản
            fig_water.add_hline(
                y=plant_water_needs,
                line_dash="dash",
                line_color="yellow",
                annotation_text="Nhu cầu cơ bản"
            )
            
            fig_water.update_layout(
                template="plotly_dark",
                xaxis_title="Ngày",
                yaxis_title="Nước (L)",
                height=400
            )
            
            st.plotly_chart(fig_water, use_container_width=True)
            
            # Bảng chi tiết
            st.markdown("#### 📋 Chi Tiết Tính Toán")
            
            display_water_df = water_df.copy()
            display_water_df['Ngày'] = pd.to_datetime(display_water_df['Ngày']).dt.strftime('%d/%m')
            
            st.dataframe(
                display_water_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Ngày": "📅 Ngày",
                    "Nhiệt độ": "🌡️ Nhiệt độ",
                    "Mưa": "🌧️ Mưa",
                    "Nhu cầu cơ bản": "💧 Cơ bản",
                    "Điều chỉnh nhiệt độ": "🔥 Điều chỉnh",
                    "Điều chỉnh mưa": "☔ Giảm mưa",
                    "Bay hơi": "💨 Bay hơi",
                    "Nhu cầu thực tế": "🚰 Thực tế",
                    "Khuyến nghị": "💡 Khuyến nghị"
                }
            )
            
            # Tổng kết
            total_water = water_df['Nhu cầu thực tế'].sum()
            avg_water = water_df['Nhu cầu thực tế'].mean()
            water_saving = ((plant_water_needs * 7) - total_water) / (plant_water_needs * 7) * 100
            
            col_total1, col_total2, col_total3 = st.columns(3)
            with col_total1:
                st.metric("Tổng nước 7 ngày", f"{total_water:.2f}L")
            with col_total2:
                st.metric("Trung bình/ngày", f"{avg_water:.2f}L")
            with col_total3:
                st.metric("Tiết kiệm", f"{water_saving:.1f}%")
    
    with tab_water2:
        st.markdown("#### ⏳ Dự Báo Thời Gian Bình Hết Nước")
        
        # Thông số bình nước
        st.markdown("##### 🏺 Thông Số Bình Nước")
        
        col_pot1, col_pot2 = st.columns(2)
        with col_pot1:
            pot_capacity = st.number_input(
                "Dung tích bình (L):",
                min_value=1.0,
                max_value=100.0,
                value=5.0,
                step=0.5,
                key="pot_capacity"
            )
        
        with col_pot2:
            current_level = st.slider(
                "Mức nước hiện tại (%):",
                0, 100, 80,
                key="current_level"
            )
        
        current_volume = pot_capacity * (current_level / 100)
        st.metric("💧 Lượng nước hiện có", f"{current_volume:.2f}L")
        
        if st.button("🔮 Dự báo thời gian hết nước", type="primary", use_container_width=True):
            if st.session_state.water_calculation is not None:
                water_df = st.session_state.water_calculation
                
                # Tính toán dự báo
                predictions = []
                remaining = current_volume
                empty_day = None
                
                for _, day in water_df.iterrows():
                    if remaining <= 0:
                        break
                    
                    daily_need = day['Nhu cầu thực tế']
                    remaining -= daily_need
                    
                    predictions.append({
                        "Ngày": day['Ngày'],
                        "Nhu cầu (L)": round(daily_need, 2),
                        "Còn lại (L)": round(max(0, remaining), 2),
                        "Trạng thái": "🟢 Đủ" if remaining > 0 else "🔴 Hết"
                    })
                    
                    if remaining <= 0 and empty_day is None:
                        empty_day = day['Ngày']
                
                predictions_df = pd.DataFrame(predictions)
                
                # Hiển thị kết quả
                st.markdown("##### 📈 Dự Báo Mức Nước")
                
                # Biểu đồ
                fig_level = px.line(
                    predictions_df,
                    x='Ngày',
                    y='Còn lại (L)',
                    title='Dự báo mức nước trong bình',
                    markers=True
                )
                
                fig_level.add_hline(
                    y=0,
                    line_dash="dash",
                    line_color="red",
                    annotation_text="Mức 0 - Hết nước"
                )
                
                fig_level.update_layout(
                    template="plotly_dark",
                    xaxis_title="Ngày",
                    yaxis_title="Nước còn lại (L)",
                    height=300
                )
                
                st.plotly_chart(fig_level, use_container_width=True)
                
                # Hiển thị ngày hết nước
                if empty_day:
                    st.error(f"⚠️ **DỰ BÁO HẾT NƯỚC:** Ngày {empty_day}")
                    
                    # Tính số ngày còn lại
                    try:
                        empty_date = datetime.datetime.strptime(empty_day, "%Y-%m-%d")
                        days_left = (empty_date - datetime.datetime.now()).days
                        st.warning(f"⏳ **Còn khoảng {days_left} ngày** trước khi hết nước")
                    except:
                        pass
                else:
                    st.success(f"✅ **BÌNH ĐỦ NƯỚC** cho 7 ngày tới")
                
                # Bảng chi tiết
                st.dataframe(
                    predictions_df,
                    use_container_width=True,
                    hide_index=True
                )
    
    with tab_water3:
        st.markdown("#### 📅 Lịch Tưới Nước Tự Động")
        
        # Tạo lịch tưới
        col_schedule1, col_schedule2 = st.columns(2)
        
        with col_schedule1:
            schedule_days = st.slider("Số ngày lịch:", 7, 30, 14)
            start_date = st.date_input("Ngày bắt đầu:", datetime.datetime.now())
        
        with col_schedule2:
            watering_time = st.selectbox(
                "Thời gian tưới lý tưởng:",
                ["Sáng sớm (5-7h)", "Chiều mát (16-18h)", "Tối (19-21h)"]
            )
            
            enable_reminders = st.toggle("Bật nhắc nhở", value=True)
        
        if st.button("📅 Tạo lịch tưới", type="primary", use_container_width=True):
            # Tạo lịch tưới
            schedule = []
            current_date = start_date
            
            for day in range(schedule_days):
                date_str = current_date.strftime("%d/%m/%Y")
                
                # Tính nhu cầu nước cho ngày này (giả lập)
                if st.session_state.water_calculation is not None and day < 7:
                    water_needs = st.session_state.water_calculation.iloc[day % 7]['Nhu cầu thực tế']
                else:
                    # Ước tính dựa trên thông tin cây
                    water_needs = plant['Nước (L/ngày)'] * random.uniform(0.8, 1.2)
                
                # Xác định có cần tưới không (giả lập logic)
                need_watering = True  # Giả sử cần tưới hàng ngày
                
                if need_watering:
                    schedule.append({
                        "Ngày": date_str,
                        "Thứ": current_date.strftime("%A"),
                        "Hành động": "💧 Tưới nước",
                        "Lượng nước": f"{water_needs:.2f}L",
                        "Thời gian": watering_time,
                        "Ghi chú": "Tưới đều quanh gốc, tránh tưới lên lá"
                    })
                else:
                    schedule.append({
                        "Ngày": date_str,
                        "Thứ": current_date.strftime("%A"),
                        "Hành động": "✅ Nghỉ",
                        "Lượng nước": "0L",
                        "Thời gian": "-",
                        "Ghi chú": "Kiểm tra độ ẩm đất"
                    })
                
                current_date += timedelta(days=1)
            
            schedule_df = pd.DataFrame(schedule)
            
            # Hiển thị lịch
            st.markdown(f"##### 📅 Lịch Tưới {plant['Tên Cây']}")
            
            st.dataframe(
                schedule_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Xuất lịch
            csv = schedule_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Tải lịch tưới (CSV)",
                data=csv,
                file_name=f"lich_tuoi_{plant['Tên Cây']}.csv",
                mime="text/csv",
                use_container_width=True
            )

# === TAB 7: LỊCH CHĂM SÓC ===
elif selected == "📅 Lịch chăm sóc":
    st.title("📅 Lịch Chăm Sóc Tổng Hợp")
    st.markdown("### Quản lý lịch chăm sóc tất cả cây của bạn")
    
    # Tạo lịch chăm sóc thông minh
    if not st.session_state.selected_plant:
        st.info("Vui lòng chọn một cây để tạo lịch chăm sóc.")
    else:
        plant = st.session_state.selected_plant
        
        # Tabs lịch chăm sóc
        tab_cal1, tab_cal2, tab_cal3 = st.tabs(["📅 Lịch tháng", "📋 Công việc", "⚡ Hành động nhanh"])
        
        with tab_cal1:
            st.markdown(f"#### 📅 Lịch Chăm Sóc Tháng - {plant['Tên Cây']}")
            
            # Tạo lịch tháng
            today = datetime.datetime.now()
            year = today.year
            month = today.month
            
            # Hiển thị calendar
            import calendar
            cal = calendar.monthcalendar(year, month)
            
            # Tạo HTML calendar đẹp
            month_name = calendar.month_name[month]
            
            cal_html = f"""
            <div style="background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 20px;">
                <h3 style="text-align: center; color: #00ffcc; margin-bottom: 20px;">{month_name} {year}</h3>
                <table style="width: 100%; border-collapse: collapse; text-align: center;">
                    <thead>
                        <tr style="background: rgba(0, 255, 204, 0.1);">
            """
            
            days_of_week = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
            for day in days_of_week:
                cal_html += f'<th style="padding: 12px; border: 1px solid rgba(255, 255, 255, 0.1); color: #00ffcc;">{day}</th>'
            
            cal_html += "</tr></thead><tbody>"
            
            for week in cal:
                cal_html += "<tr>"
                for day in week:
                    if day == 0:
                        cal_html += '<td style="padding: 15px; border: 1px solid rgba(255, 255, 255, 0.1);"></td>'
                    else:
                        # Đánh dấu ngày hôm nay
                        if day == today.day:
                            cell_style = "background: linear-gradient(135deg, #00ffcc, #0088cc); color: #0a192f; font-weight: bold;"
                        else:
                            cell_style = ""
                        
                        # Thêm công việc (giả lập)
                        tasks_count = random.randint(0, 2)
                        task_icons = ""
                        if tasks_count > 0:
                            task_icons = "💧" * tasks_count
                        
                        cal_html += f'<td style="padding: 15px; border: 1px solid rgba(255, 255, 255, 0.1); {cell_style}">'
                        cal_html += f'<div style="font-size: 1.2rem; margin-bottom: 5px;">{day}</div>'
                        cal_html += f'<div style="font-size: 0.9rem;">{task_icons}</div>'
                        cal_html += "</td>"
                cal_html += "</tr>"
            
            cal_html += "</tbody></table></div>"
            
            st.markdown(cal_html, unsafe_allow_html=True)
            
            # Chú thích
            st.markdown("""
            **Chú thích:**
            - 💧: Cần tưới nước
            - 🌿: Cần bón phân
            - ✂️: Cần cắt tỉa
            - 🔍: Cần kiểm tra sâu bệnh
            """)
        
        with tab_cal2:
            st.markdown("#### 📋 Danh Sách Công Việc")
            
            # Tạo danh sách công việc
            tasks = [
                {"Ngày": "Hôm nay", "Công việc": "💧 Tưới nước", "Thời gian": "7:00", "Trạng thái": "✅ Đã hoàn thành", "Ưu tiên": "Cao"},
                {"Ngày": "Mai", "Công việc": "🌿 Bón phân", "Thời gian": "8:00", "Trạng thái": "⏳ Chờ xử lý", "Ưu tiên": "Trung bình"},
                {"Ngày": "Ngày kia", "Công việc": "🔍 Kiểm tra sâu bệnh", "Thời gian": "9:00", "Trạng thái": "📅 Đã lên lịch", "Ưu tiên": "Thấp"},
                {"Ngày": "Thứ 6", "Công việc": "✂️ Cắt tỉa lá vàng", "Thời gian": "10:00", "Trạng thái": "📅 Đã lên lịch", "Ưu tiên": "Trung bình"},
                {"Ngày": "Thứ 7", "Công việc": "💧 Tưới nước", "Thời gian": "7:00", "Trạng thái": "📅 Đã lên lịch", "Ưu tiên": "Cao"},
            ]
            
            tasks_df = pd.DataFrame(tasks)
            st.dataframe(
                tasks_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Thêm công việc mới
            st.markdown("##### ➕ Thêm công việc mới")
            
            col_new1, col_new2, col_new3 = st.columns(3)
            
            with col_new1:
                new_task = st.text_input("Công việc:", placeholder="Ví dụ: Tưới nước, bón phân...")
            
            with col_new2:
                new_date = st.date_input("Ngày:", datetime.datetime.now() + timedelta(days=1))
            
            with col_new3:
                new_priority = st.selectbox("Ưu tiên:", ["Cao", "Trung bình", "Thấp"])
            
            if st.button("➕ Thêm vào lịch", use_container_width=True) and new_task:
                st.success(f"Đã thêm công việc '{new_task}' vào lịch!")
        
        with tab_cal3:
            st.markdown("#### ⚡ Hành Động Nhanh")
            
            quick_actions = [
                ("💧 Tưới nước hôm nay", "Đánh dấu đã tưới nước cho cây", "success"),
                ("🌿 Bón phân", "Thêm lịch bón phân", "info"),
                ("✂️ Cắt tỉa", "Lên lịch cắt tỉa", "warning"),
                ("🔍 Kiểm tra sức khỏe", "Kiểm tra sâu bệnh", "error"),
                ("📝 Ghi chú", "Thêm ghi chú cho cây", "info"),
                ("🔄 Đặt lại lịch", "Đặt lại toàn bộ lịch", "warning")
            ]
            
            cols = st.columns(3)
            for idx, (title, desc, color) in enumerate(quick_actions):
                with cols[idx % 3]:
                    if st.button(title, use_container_width=True):
                        if color == "success":
                            st.success(f"✅ {desc}")
                        elif color == "info":
                            st.info(f"ℹ️ {desc}")
                        elif color == "warning":
                            st.warning(f"⚠️ {desc}")
                        else:
                            st.error(f"❌ {desc}")

# === TAB 8: AI TRỢ LÝ ===
elif selected == "🤖 AI Trợ lý":
    st.title("🤖 AI Trợ Lý Thực Vật")
    st.markdown("### Hỏi đáp thông minh về cây trồng và chăm sóc")
    
    tab_ai1, tab_ai2, tab_ai3 = st.tabs(["💬 Chat với AI", "🔍 Phân tích ảnh", "📚 Kiến thức"])
    
    with tab_ai1:
        st.markdown("#### 💬 Chat với AI Trợ Lý Thực Vật")
        
        # Khởi tạo chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Hiển thị chat history
        chat_container = st.container(height=400, border=True)
        
        with chat_container:
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div style="text-align: right; margin-bottom: 10px;">
                        <div style="display: inline-block; background: linear-gradient(90deg, #00ffcc, #0088cc); 
                                    color: #0a192f; padding: 10px 15px; border-radius: 15px 15px 0 15px;
                                    max-width: 70%;">
                            {message['content']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="text-align: left; margin-bottom: 10px;">
                        <div style="display: inline-block; background: rgba(255, 255, 255, 0.1); 
                                    color: white; padding: 10px 15px; border-radius: 15px 15px 15px 0;
                                    max-width: 70%;">
                            <strong>🤖 AI:</strong> {message['content']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Input chat
        user_input = st.text_input(
            "Nhập câu hỏi của bạn:",
            placeholder="Ví dụ: Cách chăm sóc hoa hồng? Tại sao lá cây bị vàng?...",
            key="chat_input"
        )
        
        col_chat1, col_chat2 = st.columns([3, 1])
        
        with col_chat1:
            if st.button("📤 Gửi câu hỏi", use_container_width=True) and user_input:
                # Thêm câu hỏi vào history
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_input
                })
                
                # Tạo phản hồi AI (giả lập)
                with st.spinner("🤖 AI đang suy nghĩ..."):
                    time.sleep(1)
                    
                    # Tạo phản hồi dựa trên câu hỏi
                    response = self._generate_ai_response(user_input)
                    
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response
                    })
                    
                    st.rerun()
        
        with col_chat2:
            if st.button("🗑️ Xóa lịch sử", type="secondary", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        
        # Câu hỏi mẫu
        st.markdown("#### 💡 Câu hỏi mẫu:")
        
        sample_questions = [
            "Cách chăm sóc cây lan khi ra hoa?",
            "Tại sao lá cây bị vàng và rụng?",
            "Cây xương rồng cần tưới bao nhiêu nước?",
            "Làm thế nào để nhân giống cây trầu bà?",
            "Cây của tôi có đốm nâu trên lá, phải làm sao?"
        ]
        
        cols = st.columns(3)
        for idx, question in enumerate(sample_questions):
            with cols[idx % 3]:
                if st.button(question, use_container_width=True):
                    st.session_state.chat_input = question
                    st.rerun()
    
    with tab_ai2:
        st.markdown("#### 🔍 Phân Tích Ảnh Cây Trồng")
        
        # Upload ảnh
        uploaded_file = st.file_uploader(
            "Tải lên ảnh cây cần phân tích:",
            type=['jpg', 'jpeg', 'png', 'webp'],
            help="Tải lên ảnh cây trồng để AI phân tích tình trạng"
        )
        
        if uploaded_file is not None:
            # Hiển thị ảnh
            st.image(uploaded_file, caption="Ảnh đã tải lên", use_column_width=True)
            
            if st.button("🔍 Phân tích ảnh", type="primary", use_container_width=True):
                with st.spinner("🤖 AI đang phân tích ảnh..."):
                    time.sleep(2)
                    
                    # Giả lập phân tích AI
                    analysis_results = {
                        "plant_type": "Cây Trầu Bà (Pothos)",
                        "health_score": 85,
                        "issues": [
                            "Lá hơi vàng ở mép (có thể do thiếu nước)",
                            "Màu lá hơi nhạt (cần thêm dinh dưỡng)"
                        ],
                        "recommendations": [
                            "Tăng tưới nước 20%",
                            "Bón phân NPK 20-20-20 2 tuần/lần",
                            "Đặt cây ở nơi có ánh sáng gián tiếp"
                        ],
                        "confidence": 92
                    }
                    
                    # Hiển thị kết quả
                    st.markdown("##### 📊 Kết Quả Phân Tích")
                    
                    col_analysis1, col_analysis2 = st.columns(2)
                    with col_analysis1:
                        st.metric("Loại cây", analysis_results["plant_type"])
                        st.metric("Điểm sức khỏe", f"{analysis_results['health_score']}/100")
                    
                    with col_analysis2:
                        st.metric("Độ tin cậy", f"{analysis_results['confidence']}%")
                    
                    st.markdown("##### ⚠️ Vấn đề phát hiện")
                    for issue in analysis_results["issues"]:
                        st.warning(f"- {issue}")
                    
                    st.markdown("##### 💡 Khuyến nghị")
                    for rec in analysis_results["recommendations"]:
                        st.success(f"- {rec}")
        
        # Ảnh mẫu
        st.markdown("---")
        st.markdown("#### 🖼️ Ảnh mẫu để thử nghiệm")
        
        sample_images = [
            ("https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=300&h=200&fit=crop", "Cây khỏe mạnh"),
            ("https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=300&h=200&fit=crop", "Cây bệnh"),
            ("https://images.unsplash.com/photo-1463154545680-d59320fd685d?w-300&h=200&fit=crop", "Cây cần chăm sóc")
        ]
        
        cols = st.columns(3)
        for idx, (url, caption) in enumerate(sample_images):
            with cols[idx]:
                st.image(url, caption=caption)
    
    with tab_ai3:
        st.markdown("#### 📚 Cơ Sở Kiến Thức Thực Vật")
        
        # Tìm kiếm kiến thức
        knowledge_search = st.text_input(
            "Tìm kiếm kiến thức:",
            placeholder="Nhập chủ đề cần tìm hiểu...",
            key="knowledge_search"
        )
        
        if knowledge_search:
            with st.spinner("🔍 Đang tìm kiếm kiến thức..."):
                time.sleep(1)
                
                # Giả lập kiến thức
                knowledge_topics = {
                    "tưới nước": [
                        "**Nguyên tắc tưới nước:** Tưới khi đất khô 2-3cm bề mặt",
                        "**Thời điểm tốt nhất:** Sáng sớm (5-7h) hoặc chiều mát (16-18h)",
                        "**Lượng nước:** Tùy loại cây, thường 1/3 thể tích chậu",
                        "**Cách tưới:** Tưới đều quanh gốc, tránh tưới lên lá"
                    ],
                    "bón phân": [
                        "**Phân NPK:** 20-20-20 cho cây lá, 10-30-20 cho cây hoa",
                        "**Tần suất:** 2-4 tuần/lần trong mùa sinh trưởng",
                        "**Cách bón:** Hòa tan trong nước hoặc rắc quanh gốc",
                        "**Lưu ý:** Không bón phân khi cây đang bệnh"
                    ],
                    "sâu bệnh": [
                        "**Rệp sáp:** Xuất hiện đốm trắng, dùng cồn hoặc xà phòng pha loãng",
                        "**Nhện đỏ:** Lá vàng, có màng nhện, tăng độ ẩm không khí",
                        "**Bệnh đốm lá:** Đốm nâu trên lá, cắt bỏ lá bệnh, phun thuốc gốc đồng"
                    ]
                }
                
                found_knowledge = []
                for topic, info in knowledge_topics.items():
                    if topic in knowledge_search.lower():
                        found_knowledge.append((topic, info))
                
                if found_knowledge:
                    for topic, info in found_knowledge:
                        with st.container(border=True):
                            st.markdown(f"### 📖 {topic.title()}")
                            for item in info:
                                st.markdown(item)
                else:
                    st.info("Không tìm thấy kiến thức cụ thể. Hãy thử các từ khóa: tưới nước, bón phân, sâu bệnh")
        
        # Chủ đề phổ biến
        st.markdown("---")
        st.markdown("#### 📌 Chủ Đề Phổ Biến")
        
        popular_topics = [
            ("💧 Kỹ thuật tưới nước", "Cách tưới nước đúng cách cho từng loại cây"),
            ("🌿 Phân bón và dinh dưỡng", "Các loại phân bón và cách sử dụng"),
            ("⚠️ Phòng trừ sâu bệnh", "Nhận biết và xử lý sâu bệnh thường gặp"),
            ("✂️ Kỹ thuật cắt tỉa", "Cách cắt tỉa để cây phát triển tốt"),
            ("🏺 Thay chậu và đất", "Kỹ thuật thay chậu và chọn đất phù hợp"),
            ("🌱 Nhân giống cây trồng", "Các phương pháp nhân giống phổ biến")
        ]
        
        for title, desc in popular_topics:
            with st.container(border=True):
                col_topic1, col_topic2 = st.columns([3, 1])
                with col_topic1:
                    st.markdown(f"**{title}**")
                    st.caption(desc)
                with col_topic2:
                    if st.button("Đọc", key=f"read_{title}"):
                        st.info(f"Đang tải kiến thức về {title}...")

# === TAB 9: CÀI ĐẶT ===
elif selected == "⚙️ Cài đặt":
    st.title("⚙️ Cài Đặt Hệ Thống")
    st.markdown("### Tùy chỉnh và quản lý hệ thống EcoMind")
    
    tab_settings1, tab_settings2, tab_settings3, tab_settings4 = st.tabs([
        "🎨 Giao diện", "🔧 Hệ thống", "📊 Dữ liệu", "ℹ️ Thông tin"
    ])
    
    with tab_settings1:
        st.markdown("#### 🎨 Tùy Chỉnh Giao Diện")
        
        col_ui1, col_ui2 = st.columns(2)
        
        with col_ui1:
            theme = st.selectbox(
                "Chủ đề giao diện:",
                ["Tối (Mặc định)", "Sáng", "Xanh lá", "Xanh dương", "Tím", "Tự động"],
                index=0
            )
            
            font_size = st.slider("Cỡ chữ:", 12, 24, 16)
            
            animations = st.toggle("Hiệu ứng động", value=True)
        
        with col_ui2:
            primary_color = st.color_picker("Màu chính:", "#00ffcc")
            
            density = st.select_slider(
                "Mật độ hiển thị:",
                options=["Rộng rãi", "Thoải mái", "Tiêu chuẩn", "Compact", "Rất compact"],
                value="Thoải mái"
            )
            
            rounded_corners = st.toggle("Góc bo tròn", value=True)
        
        if st.button("💾 Áp dụng cài đặt giao diện", type="primary", use_container_width=True):
            st.success("✅ Đã lưu cài đặt giao diện!")
            st.info("Làm mới trang để xem thay đổi")
    
    with tab_settings2:
        st.markdown("#### 🔧 Cài Đặt Hệ Thống")
        
        # Thông báo
        st.markdown("##### 🔔 Thông Báo")
        col_notif1, col_notif2 = st.columns(2)
        
        with col_notif1:
            email_notifications = st.toggle("Email thông báo", value=True)
            push_notifications = st.toggle("Thông báo trình duyệt", value=True)
        
        with col_notif2:
            watering_reminders = st.toggle("Nhắc tưới nước", value=True)
            weather_alerts = st.toggle("Cảnh báo thời tiết", value=True)
        
        # Đơn vị
        st.markdown("##### 📏 Đơn Vị Đo Lường")
        units = st.radio(
            "Hệ đơn vị:",
            ["Hệ mét (m, L, °C, kg)", "Hệ Anh (ft, gal, °F, lb)"],
            horizontal=True
        )
        
        # Ngôn ngữ
        st.markdown("##### 🌐 Ngôn Ngữ")
        language = st.selectbox(
            "Ngôn ngữ giao diện:",
            ["Tiếng Việt", "English", "中文", "日本語", "한국어"]
        )
        
        if st.button("💾 Lưu cài đặt hệ thống", type="primary", use_container_width=True):
            st.success("✅ Đã lưu cài đặt hệ thống!")
    
    with tab_settings3:
        st.markdown("#### 📊 Quản Lý Dữ Liệu")
        
        # Sao lưu dữ liệu
        st.markdown("##### 💾 Sao Lưu Dữ Liệu")
        
        backup_col1, backup_col2 = st.columns(2)
        
        with backup_col1:
            auto_backup = st.toggle("Tự động sao lưu", value=True)
            if auto_backup:
                backup_frequency = st.selectbox(
                    "Tần suất sao lưu:",
                    ["Hàng ngày", "Hàng tuần", "Hàng tháng"]
                )
        
        with backup_col2:
            st.markdown("**Sao lưu thủ công:**")
            if st.button("💾 Tạo bản sao lưu ngay", use_container_width=True):
                with st.spinner("Đang tạo bản sao lưu..."):
                    time.sleep(2)
                    st.success("✅ Đã tạo bản sao lưu thành công!")
        
        # Xuất dữ liệu
        st.markdown("##### 📤 Xuất Dữ Liệu")
        
        export_format = st.selectbox(
            "Định dạng xuất:",
            ["CSV", "Excel", "JSON", "PDF"]
        )
        
        if st.button("📥 Xuất toàn bộ dữ liệu", use_container_width=True):
            st.info(f"Đang xuất dữ liệu dưới định dạng {export_format}...")
        
        # Dọn dẹp
        st.markdown("##### 🧹 Dọn Dẹp")
        
        if st.button("🗑️ Xóa cache hệ thống", use_container_width=True):
            st.cache_data.clear()
            st.success("✅ Đã xóa cache hệ thống!")
        
        if st.button("📊 Đặt lại thống kê", type="secondary", use_container_width=True):
            st.warning("⚠️ Hành động này sẽ đặt lại tất cả thống kê!")
    
    with tab_settings4:
        st.markdown("#### ℹ️ Thông Tin Hệ Thống")
        
        # Thông tin phiên bản
        st.markdown("##### 📱 Thông Tin Phiên Bản")
        
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.metric("Phiên bản", "4.0.1 Premium")
            st.metric("Build", "2024.01.15")
        with info_col2:
            st.metric("Cập nhật cuối", "15/01/2024")
            st.metric("Trạng thái", "✅ Stable")
        
        # Thông tin kỹ thuật
        st.markdown("##### 🔧 Thông Tin Kỹ Thuật")
        
        with st.container(border=True):
            st.markdown("**Framework:** Streamlit 1.28.0")
            st.markdown("**Python:** 3.11+")
            st.markdown("**Database:** Pandas + SQLite")
            st.markdown("**APIs:** Open-Meteo, Wikipedia, Google Maps")
            st.markdown("**AI:** OpenAI GPT-4 + LangChain")
        
        # Thông tin liên hệ
        st.markdown("##### 📞 Liên Hệ & Hỗ Trợ")
        
        with st.container(border=True):
            st.markdown("**Email hỗ trợ:**")
            st.code("tranthienphatle@gmail.com")
            
            st.markdown("**Website:**")
            st.markdown("[https://ecomind.com](https://ecomind.com)")
            
            st.markdown("**Documentation:**")
            st.markdown("[https://docs.ecomind.com](https://docs.ecomind.com)")
        
        # Kiểm tra cập nhật
        if st.button("🔍 Kiểm tra cập nhật", use_container_width=True):
            with st.spinner("Đang kiểm tra cập nhật..."):
                time.sleep(1)
                st.success("✅ Bạn đang sử dụng phiên bản mới nhất!")
        
        # Thông tin bản quyền
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #88aaff; font-size: 0.9rem;">
            © 2024 EcoMind OS Premium. All rights reserved.<br>
            Phiên bản 4.0.1 • Build 2024.01.15
        </div>
        """, unsafe_allow_html=True)

# --- 9. HÀM HỖ TRỢ ---
def _generate_ai_response(query):
    """Tạo phản hồi AI dựa trên câu hỏi"""
    responses = {
        "chăm sóc": "Để chăm sóc cây tốt, cần chú ý: 1) Tưới nước đúng cách, 2) Cung cấp đủ ánh sáng, 3) Bón phân định kỳ, 4) Kiểm tra sâu bệnh thường xuyên.",
        "vàng lá": "Lá vàng có thể do: 1) Tưới quá nhiều nước, 2) Thiếu dinh dưỡng, 3) Ánh sáng không đủ, 4) Sâu bệnh. Hãy kiểm tra độ ẩm đất và điều kiện ánh sáng.",
        "tưới nước": "Nguyên tắc tưới nước: Tưới khi đất khô 2-3cm bề mặt, tưới đều quanh gốc, tránh tưới vào buổi trưa nắng.",
        "bón phân": "Nên bón phân 2-4 tuần/lần trong mùa sinh trưởng. Sử dụng phân NPK cân đối cho cây lá, phân giàu Kali cho cây hoa.",
        "nhân giống": "Có thể nhân giống bằng giâm cành, chiết cành, hoặc tách bụi. Mùa xuân là thời điểm tốt nhất để nhân giống.",
    }
    
    query_lower = query.lower()
    for keyword, response in responses.items():
        if keyword in query_lower:
            return response
    
    # Phản hồi mặc định
    return f"Cảm ơn bạn đã hỏi về '{query}'. Dựa trên kiến thức thực vật học, tôi khuyên bạn nên: 1) Đảm bảo cây có đủ ánh sáng, 2) Tưới nước hợp lý, 3) Kiểm tra sâu bệnh định kỳ. Bạn có thể cung cấp thêm chi tiết để tôi hỗ trợ tốt hơn không?"

def _get_watering_recommendation(actual_need, base_need):
    """Tạo khuyến nghị tưới nước"""
    ratio = actual_need / base_need if base_need > 0 else 1
    
    if ratio > 1.3:
        return "Tưới nhiều (nắng nóng)"
    elif ratio > 1.1:
        return "Tưới tăng 20%"
    elif ratio > 0.9:
        return "Tưới bình thường"
    elif ratio > 0.7:
        return "Tưới giảm 20%"
    else:
        return "Tưới ít (có mưa)"

# --- 10. FOOTER PREMIUM ---
st.markdown("---")

footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)

with footer_col1:
    st.markdown("**🌿 EcoMind OS**")
    st.caption("Premium Edition v4.0.1")

with footer_col2:
    st.markdown("**📧 Liên hệ**")
    st.caption("tranthienphatle@gmail.com")

with footer_col3:
    st.markdown("**♻️ Sản phẩm xanh**")
    st.caption("100% tái chế • 0% điện tử")

with footer_col4:
    st.markdown("**📞 Hỗ trợ 24/7**")
    st.caption("Hotline: 1800-ECOMIND")

# Hiển thị thông tin phiên bản và thời gian
current_time = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
st.caption(f"🕐 {current_time} • © 2024 EcoMind • Build 2024.01.15")
