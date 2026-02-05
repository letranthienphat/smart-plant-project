import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime

# --- 1. CẤU HÌNH HỆ THỐNG ---
st.set_page_config(
    page_title="EcoMind Ultimate - Location Based",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Tối giản & Hiện đại
st.markdown("""
<style>
    .stMetric { background-color: #f0f2f6; border-radius: 10px; padding: 10px; border-left: 5px solid #00CC96; }
    div[data-testid="stExpander"] div[role="button"] p { font-size: 1.1rem; font-weight: bold; }
    .css-1d391kg { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)

# --- 2. DỮ LIỆU CÂY TRỒNG (DATABASE) ---
def load_plant_data():
    return pd.DataFrame({
        "Tên": ["Xương rồng", "Lưỡi Hổ", "Trầu bà", "Lan Ý", "Bàng Singapore", "Dương xỉ", "Sen đá", "Kim Tiền"],
        "Nước (L/ngày)": [0.05, 0.1, 0.6, 0.4, 0.9, 0.7, 0.08, 0.2],
        "Chịu hạn (Ngày)": [60, 45, 7, 5, 6, 3, 40, 30],
        "Nhiệt độ lý tưởng": [30, 28, 25, 24, 27, 22, 25, 26],
        "Icon": ["🌵", "🎍", "🌿", "💐", "🌳", "🍃", "🪷", "💰"]
    })

df_plants = load_plant_data()

# --- 3. DỮ LIỆU ĐỊA LÝ (GEOLOCATION DATABASE) ---
# Tọa độ các thành phố lớn để gọi API
CITIES = {
    "Hồ Chí Minh": {"lat": 10.8231, "lon": 106.6297},
    "Hà Nội": {"lat": 21.0285, "lon": 105.8542},
    "Đà Nẵng": {"lat": 16.0544, "lon": 108.2022},
    "Cần Thơ": {"lat": 10.0452, "lon": 105.7469},
    "Hải Phòng": {"lat": 20.8449, "lon": 106.6881},
    "Đà Lạt": {"lat": 11.9404, "lon": 108.4583},
    "Nha Trang": {"lat": 12.2388, "lon": 109.1967},
    "Sapa": {"lat": 22.3364, "lon": 103.8438}
}

# --- 4. HÀM GỌI API THỜI TIẾT (OPEN-METEO - MIỄN PHÍ) ---
@st.cache_data(ttl=3600) # Cache dữ liệu 1 tiếng để web chạy nhanh
def get_real_weather(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relativehumidity_2m,rain"
        response = requests.get(url)
        data = response.json()
        
        current = data['current_weather']
        # Lấy độ ẩm giờ hiện tại (API này trả về mảng theo giờ)
        current_hour = datetime.now().hour
        humidity = data['hourly']['relativehumidity_2m'][current_hour]
        rain_chance = data['hourly']['rain'][current_hour]
        
        return {
            "temp": current['temperature'],
            "wind": current['windspeed'],
            "humidity": humidity,
            "rain": rain_chance,
            "is_day": current['is_day']
        }
    except:
        # Fallback nếu mất mạng
        return {"temp": 30, "wind": 5, "humidity": 70, "rain": 0, "is_day": 1}

# --- 5. LOGIC DỰ BÁO ---
def calculate_status(plant_row, weather_data, tank_cap, current_level):
    temp = weather_data['temp']
    hum = weather_data['humidity']
    
    # Công thức thoát hơi nước dựa trên dữ liệu thực
    base_usage = plant_row["Nước (L/ngày)"]
    evaporation_factor = 1.0 + ((temp - 25) * 0.05) - ((hum - 50) * 0.01)
    
    real_usage = base_usage * max(0.5, evaporation_factor)
    daily_pct_loss = (real_usage / tank_cap) * 100
    
    days_left = current_level / daily_pct_loss if daily_pct_loss > 0 else 999
    return real_usage, daily_pct_loss, days_left

# --- 6. GIAO DIỆN ---
st.title("🌍 EcoMind Geo-Spatial")
st.caption("Dự báo thông minh dựa trên vị trí thực tế")

# --- BƯỚC 1: CHỌN VỊ TRÍ (QUAN TRỌNG NHẤT) ---
with st.container():
    col_city, col_plant = st.columns([1, 1])
    with col_city:
        selected_city = st.selectbox("📍 Chọn vị trí của bạn:", list(CITIES.keys()))
    with col_plant:
        selected_plant_name = st.selectbox("🌱 Chọn loại cây:", df_plants["Tên"])

# Xử lý dữ liệu
coords = CITIES[selected_city]
plant_info = df_plants[df_plants["Tên"] == selected_plant_name].iloc[0]

# Gọi API Thời tiết
with st.spinner(f"Đang kết nối vệ tinh lấy dữ liệu tại {selected_city}..."):
    weather = get_real_weather(coords['lat'], coords['lon'])

# --- BƯỚC 2: HIỂN THỊ THỜI TIẾT THỰC (ĐƠN GIẢN DỄ HIỂU) ---
st.markdown("### 🌤️ Thời tiết hiện tại")
w1, w2, w3, w4 = st.columns(4)
with w1:
    st.metric("Nhiệt độ", f"{weather['temp']}°C", "Thực tế ngoài trời")
with w2:
    st.metric("Độ ẩm", f"{weather['humidity']}%", "Ảnh hưởng tưới tiêu")
with w3:
    st.metric("Mưa", f"{weather['rain']} mm", "Lượng mưa giờ này")
with w4:
    day_status = "Ban ngày ☀️" if weather['is_day'] else "Ban đêm 🌙"
    st.metric("Thời gian", day_status)

st.markdown("---")

# --- BƯỚC 3: CẤU HÌNH BÌNH CHỨA & KẾT QUẢ ---
# Sidebar cho cấu hình phụ
with st.sidebar:
    st.header("⚙️ Thiết lập bình chứa")
    tank_cap = st.slider("Dung tích bình (Lít)", 1.0, 20.0, 5.0)
    current_water_pct = st.slider("Lượng nước hiện có (%)", 0, 100, 80)
    st.info("Kéo thanh trượt để mô phỏng mức nước hiện tại.")

# Tính toán
usage, loss_pct, days_left = calculate_status(plant_info, weather, tank_cap, current_water_pct)

# --- BƯỚC 4: BIỂU ĐỒ ĐƠN GIẢN (THEO YÊU CẦU) ---

# LAYOUT CHÍNH
col_main_1, col_main_2 = st.columns([2, 1])

with col_main_1:
    st.subheader(f"📊 Dự báo cho {plant_info['Icon']} {plant_info['Tên']}")
    
    # 1. Biểu đồ đường ĐƠN GIẢN (Line Chart)
    # Dự báo mực nước giảm dần trong 7 ngày tới
    future_days = 10
    levels = []
    current = current_water_pct
    for _ in range(future_days):
        levels.append(max(0, current))
        current -= loss_pct
    
    chart_data = pd.DataFrame({
        "Ngày": [f"Ngày {i}" for i in range(future_days)],
        "Mức nước (%)": levels
    })
    
    # Vẽ biểu đồ vùng đơn giản, dễ hiểu
    fig = px.area(chart_data, x="Ngày", y="Mức nước (%)", 
                  title="Biểu đồ cạn nước theo thời gian (Dựa trên thời tiết thực)",
                  color_discrete_sequence=["#00CC96"])
    
    # Thêm đường giới hạn đỏ
    fig.add_hline(y=10, line_dash="dot", line_color="red", annotation_text="Nguy hiểm (10%)")
    fig.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

with col_main_2:
    st.subheader("Tiến độ sử dụng")
    
    # 2. Biểu đồ Donut ĐƠN GIẢN (Thay thế Gauge phức tạp)
    fig_donut = go.Figure(data=[go.Pie(
        labels=['Nước còn lại', 'Đã dùng'], 
        values=[current_water_pct, 100-current_water_pct], 
        hole=.7,
        marker_colors=['#00CC96', '#EEF0F4'],
        sort=False
    )])
    fig_donut.update_layout(
        showlegend=False, 
        annotations=[dict(text=f"{days_left:.1f} Ngày", x=0.5, y=0.5, font_size=20, showarrow=False)],
        margin=dict(t=20, b=20, l=20, r=20),
        height=250
    )
    st.plotly_chart(fig_donut, use_container_width=True)
    
    # Hiển thị text ngắn gọn
    if days_left > 7:
        st.success("✅ Trạng thái: Ổn định")
    elif days_left > 3:
        st.warning("⚠️ Trạng thái: Cần chú ý")
    else:
        st.error("🚨 Trạng thái: CẤP CỨU")

# --- BƯỚC 5: LỜI KHUYÊN AI (Dựa trên vị trí) ---
st.markdown("### 🤖 Lời khuyên từ chuyên gia AI")

advice_box = st.container(border=True)
with advice_box:
    # Logic so sánh khí hậu
    temp_diff = weather['temp'] - plant_info['Nhiệt độ lý tưởng']
    
    st.write(f"**Phân tích tại {selected_city}:**")
    
    # Lời khuyên 1: Nhiệt độ
    if temp_diff > 5:
        st.markdown(f"🔥 **Nắng nóng:** Nhiệt độ tại {selected_city} đang nóng hơn {temp_diff:.1f}°C so với mức cây thích. **Hành động:** Dời cây vào bóng râm ngay.")
    elif temp_diff < -5:
        st.markdown(f"❄️ **Trời lạnh:** Nhiệt độ thấp. Cây sẽ 'ngủ đông', tưới ít nước lại để tránh thối rễ.")
    else:
        st.markdown(f"✅ **Nhiệt độ:** Rất lý tưởng cho cây phát triển.")

    # Lời khuyên 2: Mưa
    if weather['rain'] > 0 and weather['is_day']:
        st.markdown(f"🌧️ **Đang mưa:** Tận dụng nước mưa tự nhiên nếu cây ở ngoài trời. Hệ thống sẽ tự động hoãn thông báo tưới.")
    
    # Lời khuyên 3: Vị trí
    if selected_city == "Đà Lạt" and plant_info['Tên'] == "Xương rồng":
        st.markdown("⚠️ **Lưu ý địa phương:** Đà Lạt có độ ẩm cao và sương mù, Xương rồng rất dễ bị úng. Hãy đảm bảo đất thoát nước cực tốt.")
    elif selected_city == "Hồ Chí Minh" and plant_info['Tên'] == "Dương xỉ":
        st.markdown("💡 **Mẹo:** Sài Gòn khá nóng, hãy phun sương cho Dương xỉ 2 lần/ngày.")
