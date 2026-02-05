import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# --- 1. CẤU HÌNH HỆ THỐNG PRO ---
st.set_page_config(
    page_title="EcoMind Enterprise - Smart Plant AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed" # Thu gọn sidebar ban đầu cho thoáng
)

# Custom CSS cho giao diện Dark/Glassmorphism chuyên nghiệp
st.markdown("""
<style>
    .big-font { font-size:20px !important; font-weight: bold; }
    .stMetric { background-color: #1E1E1E; border-radius: 10px; padding: 10px; border: 1px solid #333; }
    .css-1aumxhk { background-color: #0E1117; }
    div[data-testid="stExpander"] div[role="button"] p { font-size: 1.1rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 2. KHỞI TẠO "BIG DATA" (CƠ SỞ DỮ LIỆU CÂY TRỒNG) ---
# Chúng ta tạo một DataFrame lớn để mô phỏng dữ liệu phong phú
def load_data():
    data = {
        "Tên thường gọi": ["Xương rồng Saguaro", "Cây Lưỡi Hổ", "Trầu bà Nam Mỹ", "Lan Ý", "Cây Bàng Singapore", "Dương xỉ Mỹ", "Cây Kim Tiền", "Cây Đa Búp Đỏ", "Cây Dây Nhện", "Sen đá Nâu", "Cây Hạnh Phúc", "Cây Ngọc Ngân"],
        "Tên khoa học": ["Carnegiea gigantea", "Sansevieria trifasciata", "Monstera deliciosa", "Spathiphyllum", "Ficus lyrata", "Nephrolepis exaltata", "Zamioculcas zamiifolia", "Ficus elastica", "Chlorophytum comosum", "Echeveria", "Radermachera sinica", "Aglaonema"],
        "Loại": ["Sa mạc", "Trong nhà", "Nhiệt đới", "Trong nhà", "Thân gỗ", "Ưa ẩm", "Phong thủy", "Thân gỗ", "Treo", "Sa mạc", "Thân gỗ", "Lá màu"],
        "Nhu cầu nước (L/ngày)": [0.05, 0.1, 0.8, 0.4, 0.9, 0.7, 0.2, 0.6, 0.3, 0.08, 0.65, 0.35],
        "Chịu hạn (Ngày)": [60, 45, 7, 5, 6, 3, 30, 10, 12, 40, 8, 10],
        "An toàn cho Pet": [False, False, False, False, False, True, False, False, True, True, True, False],
        "Ánh sáng": ["Trực tiếp", "Bóng râm/Vừa", "Tán xạ", "Bóng râm", "Tán xạ mạnh", "Bóng râm", "Vừa", "Tán xạ", "Tán xạ", "Trực tiếp", "Tán xạ", "Vừa"],
        "Icon": ["🌵", "🎍", "🌿", "💐", "🌳", "🍃", "💰", "🍂", "🕷️", "🪷", "🌲", "🌱"]
    }
    return pd.DataFrame(data)

df_plants = load_data()

# --- 3. SESSION STATE MANAGEMENT ---
# Đảm bảo ban đầu chưa chọn gì cả
if 'selected_plant_index' not in st.session_state:
    st.session_state.selected_plant_index = None # Chưa chọn cây nào
if 'tank_level' not in st.session_state:
    st.session_state.tank_level = 100.0

# --- 4. LOGIC AI "VIP PRO" ---
def calculate_analytics(plant_row, temp, humidity, tank_cap):
    # Logic phức tạp hơn: Tính cả áp suất hơi bão hòa (VPD - Vapor Pressure Deficit) giả lập
    base_consumption = plant_row["Nhu cầu nước (L/ngày)"]
    
    # Hệ số stress nhiệt (Heat Stress Factor)
    heat_stress = 1.0
    if temp > 30: heat_stress += (temp - 30) * 0.1
    if temp > 38: heat_stress += (temp - 38) * 0.2 # Nắng gắt tốn nước gấp bội
    
    # Hệ số độ ẩm
    humidity_factor = 1.0 + (50 - humidity) * 0.015 # Độ ẩm thấp thì tốn nước hơn
    
    real_consumption = base_consumption * heat_stress * humidity_factor
    daily_loss_pct = (real_consumption / tank_cap) * 100
    
    days_left = st.session_state.tank_level / daily_loss_pct if daily_loss_pct > 0 else 999
    
    return real_consumption, daily_loss_pct, days_left

# --- 5. GIAO DIỆN CHÍNH ---

# HEADER
col_h1, col_h2 = st.columns([1, 4])
with col_h1:
    st.title("🧬 EcoMind")
with col_h2:
    st.markdown("#### Hệ thống Quản trị Sinh thái Thực vật V3.0")
    st.caption("AI-Powered Plant Monitoring System without Sensors")

st.markdown("---")

# === TRƯỜNG HỢP 1: CHƯA CHỌN CÂY (HOME SCREEN) ===
if st.session_state.selected_plant_index is None:
    st.info("👋 Chào mừng! Vui lòng truy cập Cơ sở dữ liệu bên dưới để chọn loại cây bạn muốn giám sát.")
    
    # Bộ lọc tìm kiếm chuyên nghiệp
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search_query = st.text_input("🔍 Tìm kiếm cây (theo tên, tên khoa học...)", placeholder="Ví dụ: Monstera, Xương rồng...")
    with col_filter:
        filter_type = st.selectbox("Lọc theo loại", ["Tất cả"] + list(df_plants["Loại"].unique()))
    
    # Lọc dữ liệu
    filtered_df = df_plants.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df["Tên thường gọi"].str.contains(search_query, case=False) | filtered_df["Tên khoa học"].str.contains(search_query, case=False)]
    if filter_type != "Tất cả":
        filtered_df = filtered_df[filtered_df["Loại"] == filter_type]
    
    st.subheader(f"📚 Thư viện cây trồng ({len(filtered_df)} kết quả)")
    
    # Hiển thị dạng Grid các thẻ cây
    for i in range(0, len(filtered_df), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(filtered_df):
                row = filtered_df.iloc[i + j]
                original_index = row.name # Lưu lại index gốc để chọn
                with cols[j]:
                    with st.container(border=True):
                        st.markdown(f"## {row['Icon']}")
                        st.markdown(f"**{row['Tên thường gọi']}**")
                        st.caption(f"_{row['Tên khoa học']}_")
                        st.text(f"💧 Nhu cầu: {row['Nhu cầu nước (L/ngày)']} L/ngày")
                        
                        # Logic nút chọn
                        if st.button("📡 KẾT NỐI GIÁM SÁT", key=f"btn_{original_index}", use_container_width=True):
                            st.session_state.selected_plant_index = original_index
                            st.rerun() # Load lại trang để vào Dashboard

# === TRƯỜNG HỢP 2: ĐÃ CHỌN CÂY (DASHBOARD MODE) ===
else:
    # Lấy thông tin cây đã chọn
    plant = df_plants.iloc[st.session_state.selected_plant_index]
    
    # Nút quay lại
    if st.button("⬅️ Ngắt kết nối / Chọn cây khác"):
        st.session_state.selected_plant_index = None
        st.rerun()
    
    # --- SIDEBAR (Chỉ hiện khi đã chọn cây để chỉnh tham số môi trường) ---
    with st.sidebar:
        st.header("🎛️ Control Center")
        st.divider()
        st.write(f"Đang theo dõi: **{plant['Tên thường gọi']}**")
        
        st.subheader("⚙️ Phần cứng ảo")
        tank_cap = st.number_input("Dung tích bình chứa (Lít)", 1.0, 50.0, 5.0)
        
        st.subheader("🌤️ Môi trường giả lập")
        temp = st.slider("Nhiệt độ (°C)", 10, 50, 30)
        humidity = st.slider("Độ ẩm không khí (%)", 10, 100, 65)
        
        st.divider()
        if st.button("💧 NẠP ĐẦY NƯỚC", type="primary", use_container_width=True):
            st.session_state.tank_level = 100.0
            st.toast("Đã nạp đầy bình chứa!", icon="✅")

    # --- TÍNH TOÁN AI ---
    real_loss, loss_pct, days_remain = calculate_analytics(plant, temp, humidity, tank_cap)
    
    # --- DASHBOARD LAYOUT ---
    st.title(f"{plant['Icon']} {plant['Tên thường gọi']} - Dashboard")
    st.markdown(f"**Tên khoa học:** _{plant['Tên khoa học']}_ | **Phân loại:** {plant['Loại']}")
    
    # Cảnh báo nhanh
    if days_remain < 2:
        st.error("⚠️ CẢNH BÁO NGUY HIỂM: Nguồn nước sắp cạn kiệt! Cây sẽ bắt đầu chết sau 2 ngày nữa.")
    elif days_remain < 5:
        st.warning("⚠️ CHÚ Ý: Cần chuẩn bị bổ sung nước.")
    
    # 4 Cột chỉ số chính
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Lượng nước tiêu thụ thực tế", f"{real_loss:.2f} L/ngày", 
                  f"{((real_loss/plant['Nhu cầu nước (L/ngày)'])-1)*100:.1f}% so với chuẩn", 
                  delta_color="inverse")
    with m2:
        st.metric("Dự báo thời gian còn lại", f"{days_remain:.1f} Ngày", "Tính đến khi cạn 0%")
    with m3:
        safe_color = "normal" if plant['An toàn cho Pet'] else "off"
        safe_text = "An toàn" if plant['An toàn cho Pet'] else "Độc hại"
        st.metric("An toàn cho Thú cưng", safe_text, "Chó/Mèo", delta_color=safe_color)
    with m4:
        st.metric("Sức chịu hạn của giống", f"{plant['Chịu hạn (Ngày)']} Ngày", "Sau khi hết nước")

    # TABS CHI TIẾT
    tab_overview, tab_analytics, tab_advisor = st.tabs(["📊 Tổng quan Bình chứa", "📈 Phân tích Môi trường", "🤖 AI Cố vấn"])
    
    with tab_overview:
        c1, c2 = st.columns([1, 2])
        with c1:
            # Gauge Chart xịn xò
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = st.session_state.tank_level,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Mức nước hiện tại (%)"},
                delta = {'reference': 100, 'increasing': {'color': "green"}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#00CC96"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 20], 'color': '#FF4136'},
                        {'range': [20, 100], 'color': '#1E1E1E'}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 10}}))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white", 'family': "Arial"})
            st.plotly_chart(fig, use_container_width=True)
            
        with c2:
            st.markdown("#### Dự báo cạn kiệt theo thời gian")
            # Tạo dữ liệu giả lập tương lai
            future_days = int(days_remain) + 5
            days_x = list(range(future_days))
            water_y = [max(0, st.session_state.tank_level - (loss_pct * d)) for d in days_x]
            
            df_chart = pd.DataFrame({"Ngày tới": days_x, "Mức nước (%)": water_y})
            
            fig_area = px.area(df_chart, x="Ngày tới", y="Mức nước (%)", title="Biểu đồ suy giảm mực nước")
            fig_area.add_hline(y=0, line_dash="dot", annotation_text="Cạn kiệt", annotation_position="bottom right", line_color="red")
            st.plotly_chart(fig_area, use_container_width=True)

    with tab_analytics:
        st.subheader("Tác động môi trường đến cây trồng")
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            st.info(f"""
            **Yêu cầu ánh sáng:** {plant['Ánh sáng']}
            
            Hiện tại, với nhiệt độ **{temp}°C**, tốc độ thoát hơi nước của cây đang **{'CAO' if temp > 32 else 'BÌNH THƯỜNG'}**.
            """)
        with col_a2:
            # Biểu đồ radar so sánh đặc tính cây
            categories = ['Nhu cầu nước', 'Chịu nhiệt', 'Chịu hạn', 'Thẩm mỹ', 'Lọc không khí']
            # Giả lập chỉ số (Randomize nhẹ cho demo)
            r_vals = [
                min(10, plant['Nhu cầu nước (L/ngày)']*10), 
                8 if temp > 35 and plant['Loại'] == 'Sa mạc' else 5,
                min(10, plant['Chịu hạn (Ngày)']/5),
                8, 7
            ]
            
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=r_vals,
                theta=categories,
                fill='toself',
                name=plant['Tên thường gọi']
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                showlegend=False,
                title="Biểu đồ năng lực sinh học của cây"
            )
            st.plotly_chart(fig_radar, use_container_width=True)

    with tab_advisor:
        st.markdown("### 🤖 Trợ lý AI Sinh thái")
        with st.chat_message("assistant"):
            st.write(f"Xin chào! Tôi đang phân tích dữ liệu cho cây **{plant['Tên thường gọi']}**...")
            advice = []
            if temp > 35:
                advice.append(f"- 🌡️ **Cảnh báo nhiệt:** {temp}°C là quá nóng. Hãy di chuyển cây vào bóng râm ngay lập tức để giảm 30% lượng nước tiêu thụ.")
            if humidity < 40 and plant['Loại'] in ['Ưa ẩm', 'Nhiệt đới']:
                advice.append("- 💧 **Độ ẩm thấp:** Cây này ưa ẩm. Bạn nên phun sương lên lá 2 lần/ngày.")
            if days_remain < 3:
                advice.append(f"- 🚨 **Khẩn cấp:** Chỉ còn nước cho {days_remain:.1f} ngày. Lên lịch châm nước ngay.")
            
            if not advice:
                st.write("Môi trường hiện tại rất lý tưởng. Cây đang phát triển tốt!")
            else:
                for item in advice:
                    st.markdown(item)
            
            st.caption(f"Dữ liệu tham chiếu từ: {plant['Tên khoa học']} Database.")
