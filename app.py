import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from streamlit_js_eval import get_geolocation

# --- 1. CẤU HÌNH HỆ THỐNG ---
st.set_page_config(page_title="EcoMind V5 - Auto Botanical API", layout="wide", page_icon="🧬")

# TREFLE API KEY (Đây là API mở về thực vật lớn nhất thế giới)
# Bạn có thể đăng ký lấy key miễn phí tại trefle.io
TREFLE_API_KEY = "YOUR_TREFLE_TOKEN_HERE" 

# --- 2. HÀM TỰ ĐỘNG LẤY VỊ TRÍ HIỆN TẠI (GPS) ---
def get_user_location():
    loc = get_geolocation()
    if loc:
        return loc['coords']['latitude'], loc['coords']['longitude']
    return 10.8231, 106.6297 # Mặc định TP.HCM nếu không lấy được GPS

# --- 3. BỘ MÁY TỰ ĐỘNG BẮT API THỰC VẬT (AUTO-DATABASE) ---
@st.cache_data(show_spinner="Đang truy xuất thư viện thực vật toàn cầu...")
def search_plant_api(query):
    """Tự động kết nối API để lấy thông tin cây bất kỳ"""
    try:
        # Gọi API Trefle để lấy dữ liệu loài
        url = f"https://trefle.io/api/v1/plants/search?token={TREFLE_API_KEY}&q={query}"
        response = requests.get(url).json()
        if response['data']:
            plant = response['data'][0] # Lấy kết quả chính xác nhất
            return {
                "common_name": plant.get('common_name', 'Cây lạ'),
                "scientific_name": plant.get('scientific_name', 'N/A'),
                "image": plant.get('image_url', ''),
                "family": plant.get('family', 'N/A')
            }
    except:
        return None

# --- 4. HÀM LẤY THỜI TIẾT TỰ ĐỘNG ---
def get_weather_auto(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relativehumidity_2m"
    data = requests.get(url).json()
    return data['current_weather']['temperature'], data['hourly']['relativehumidity_2m'][0]

# --- 5. GIAO DIỆN CHÍNH ---
st.title("🧬 EcoMind V5: Hệ Sinh Thái Tự Động")

# Giao diện tìm kiếm cây thông minh (Bắt API ngay khi gõ)
st.subheader("🔍 Tìm kiếm & Kích hoạt Cây trồng")
search_query = st.text_input("Nhập tên cây bằng tiếng Anh (Ví dụ: Rose, Cactus, Monstera...)", "Monstera")

if search_query:
    plant_info = search_plant_api(search_query)
    if plant_info:
        col_img, col_txt = st.columns([1, 3])
        with col_img:
            if plant_info['image']:
                st.image(plant_info['image'], width=200)
        with col_txt:
            st.markdown(f"### {plant_info['common_name']}")
            st.write(f"🔬 **Tên khoa học:** {plant_info['scientific_name']}")
            st.write(f"🌿 **Họ:** {plant_info['family']}")
            
            # Giả lập logic sinh học dựa trên họ cây (Vì API thực vật thường không cho chỉ số tưới)
            if "Cactaceae" in plant_info['family']:
                water_need = 0.05
                survival = 40
            elif "Araceae" in plant_info['family']:
                water_need = 0.5
                survival = 7
            else:
                water_need = 0.3
                survival = 10

# --- 6. VỊ TRÍ & DỰ BÁO ---
st.divider()
lat, lon = get_user_location()
temp, hum = get_weather_auto(lat, lon)

st.subheader(f"📍 Tình trạng tại vị trí hiện tại ({lat:.2f}, {lon:.2f})")
c1, c2, c3 = st.columns(3)

# Logic tính toán lượng nước VIP
tank_capacity = st.sidebar.number_input("Dung tích bình (L)", 1.0, 50.0, 5.0)
current_water = st.sidebar.slider("Nước hiện tại (L)", 0.0, tank_capacity, 2.5)

# Cảnh báo dựa trên API thời tiết thực
real_usage = water_need * (1 + (temp - 25) * 0.05)
days_left = current_water / real_usage

with c1:
    st.metric("Nhiệt độ thực", f"{temp}°C")
with c2:
    st.metric("Dự báo hết nước", f"{days_left:.1f} Ngày")
with c3:
    status = "🚨 NGUY CẤP" if days_left < 2 else "✅ AN TOÀN"
    st.metric("Trạng thái", status)

# BIỂU ĐỒ ĐƠN GIẢN NHÌN LÀ HIỂU
st.markdown("### 📊 Biểu đồ tiêu thụ nước")
days = list(range(10))
water_levels = [max(0, current_water - (real_usage * d)) for d in days]

fig = go.Figure()
fig.add_trace(go.Scatter(x=days, y=water_levels, fill='tozeroy', name='Mức nước'))
fig.add_hline(y=0.5, line_dash="dot", line_color="red", annotation_text="Ngưỡng chết của cây")
fig.update_layout(xaxis_title="Ngày tới", yaxis_title="Lượng nước (Lít)")
st.plotly_chart(fig, use_container_width=True)

# LỜI KHUYÊN TỰ ĐỘNG
if temp > 32:
    st.error(f"⚠️ Cảnh báo VIP: Nhiệt độ thực tế đang rất cao ({temp}°C). Hệ thống tự động kích hoạt chế độ tiết kiệm hơi nước cho {plant_info['common_name']}.")
