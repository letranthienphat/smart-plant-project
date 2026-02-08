import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import wikipedia
import random
import time

# --- 1. CẤU HÌNH HỆ THỐNG VIP ---
st.set_page_config(page_title="EcoMind OS - Knowledge Graph", layout="wide", page_icon="🧠")
wikipedia.set_lang("vi") # Cài đặt Wikipedia tiếng Việt

# CSS Giao diện Glassmorphism (Kính mờ)
st.markdown("""
<style>
    .stApp { background-color: #0f172a; color: #e2e8f0; }
    .stDataFrame { border: 1px solid #38bdf8; border-radius: 8px; }
    div[data-testid="stMetricValue"] { color: #38bdf8 !important; font-weight: bold; }
    h1, h2, h3 { color: #38bdf8 !important; }
    .wiki-card { background: rgba(30, 41, 59, 0.7); padding: 20px; border-radius: 15px; border-left: 5px solid #38bdf8; margin-bottom: 15px; }
    .advice-box { background: rgba(20, 83, 45, 0.4); padding: 15px; border-radius: 10px; border: 1px solid #22c55e; color: #86efac; }
</style>
""", unsafe_allow_html=True)

# --- 2. HÀM TẠO DỮ LIỆU CÂY (SIMULATED DB) ---
@st.cache_data
def generate_db():
    names = ["Hoa Hồng", "Lan Hồ Điệp", "Xương Rồng", "Sen Đá", "Trầu Bà", "Dương Xỉ", "Cây Bàng Singapore", "Cây Kim Tiền", "Cây Lưỡi Hổ", "Cây Phát Tài"]
    data = []
    for i, name in enumerate(names):
        # Tạo đặc tính sinh học riêng
        is_desert = name in ["Xương Rồng", "Sen Đá", "Cây Lưỡi Hổ"]
        water_need = 0.1 if is_desert else 0.5
        light = "Nắng gắt" if is_desert else "Bóng râm/Tán xạ"
        
        data.append({
            "ID": i+1,
            "Tên Cây": name,
            "Tên Khoa Học": f"Species {i+1}",
            "Nước (L/ngày)": water_need,
            "Ánh Sáng": light,
            "Loại": "Sa mạc" if is_desert else "Nhiệt đới"
        })
    return pd.DataFrame(data)

df = generate_db()

# --- 3. HÀM TRÍ TUỆ NHÂN TẠO (AI FUNCTIONS) ---

@st.cache_data(show_spinner="Đang đọc dữ liệu từ Wikipedia & Google...")
def get_wiki_data(query):
    """Hàm lấy dữ liệu thực tế từ Wikipedia"""
    try:
        # 1. Lấy tóm tắt ngắn (Summary)
        summary = wikipedia.summary(query, sentences=3)
        
        # 2. Lấy trang chi tiết (Detail)
        page = wikipedia.page(query)
        full_url = page.url
        content = page.content[:1500] + "..." # Lấy 1500 ký tự đầu
        
        return {
            "found": True,
            "summary": summary,
            "content": content,
            "url": full_url,
            "images": page.images[0] if page.images else "https://via.placeholder.com/400"
        }
    except:
        return {"found": False}

def smart_advice(plant_row, current_temp, current_hum):
    """Hàm đưa ra lời khuyên thay đổi theo từng loại cây"""
    advices = []
    
    # 1. Phân tích theo Loại cây
    if plant_row["Loại"] == "Sa mạc":
        if current_hum > 70:
            advices.append("⚠️ **Cảnh báo độ ẩm:** Cây này ghét ẩm ướt! Độ ẩm hiện tại quá cao, ngưng tưới nước ngay lập tức kẻo thối rễ.")
        if current_temp < 15:
            advices.append("❄️ **Cảnh báo lạnh:** Cây sa mạc chịu lạnh kém. Hãy mang vào nhà.")
        base_advice = "Đây là dòng cây chịu hạn cực tốt. Chỉ tưới khi đất khô trắng."
        
    else: # Cây nhiệt đới
        if current_temp > 35:
            advices.append("🔥 **Cảnh báo nhiệt:** Trời quá nóng! Hãy phun sương lên lá để hạ nhiệt.")
        if current_hum < 50:
            advices.append("💧 **Thiếu ẩm:** Không khí quá khô. Cây này cần độ ẩm cao, hãy đặt cạnh chậu nước.")
        base_advice = "Dòng cây này ưa ẩm, giữ đất luôn hơi ẩm nhẹ."

    return base_advice, advices

# --- 4. GIAO DIỆN CHÍNH ---
with st.sidebar:
    st.title("🧠 EcoMind AI")
    selected = option_menu(
        menu_title=None,
        options=["Tra Cứu Thông Minh", "Giám Sát Vườn", "Cấu Hình"],
        icons=["search", "flower1", "gear"],
        default_index=0,
    )

# === TAB 1: TRA CỨU THÔNG MINH (WIKIPEDIA + GOOGLE) ===
if selected == "Tra Cứu Thông Minh":
    st.title("🔍 TRA CỨU BÁCH KHOA TOÀN THƯ")
    
    col_search, col_res = st.columns([1, 2])
    
    with col_search:
        st.subheader("Chọn cây cần tìm")
        # Người dùng có thể chọn từ list hoặc gõ tên bất kỳ
        search_input = st.selectbox("Danh sách cây phổ biến:", df["Tên Cây"])
        custom_search = st.text_input("Hoặc gõ tên cây khác:", "")
        
        query = custom_search if custom_search else search_input
        
        if st.button("🚀 Kích hoạt AI Tìm kiếm", type="primary"):
            st.session_state.search_query = query

    with col_res:
        if 'search_query' in st.session_state:
            q = st.session_state.search_query
            st.info(f"Đang kết nối vệ tinh dữ liệu cho: **{q}**...")
            
            # Gọi hàm lấy dữ liệu thật
            data = get_wiki_data(q)
            
            if data["found"]:
                # HIỂN THỊ KẾT QUẢ VIP PRO
                st.markdown(f"## 🌿 Kết quả cho: {q}")
                
                # 1. Phần tóm tắt ngắn (Smart Summary)
                st.markdown("### ⚡ Tóm tắt nhanh (AI Summary)")
                st.success(data["summary"])
                
                # 2. Phần chi tiết (Google/Wiki Detail)
                st.markdown("### 📖 Dữ liệu chi tiết (Wikipedia)")
                with st.expander("Xem toàn bộ nội dung nghiên cứu", expanded=True):
                    c_img, c_text = st.columns([1, 2])
                    with c_img:
                        st.image(data["images"], caption="Hình ảnh trích xuất từ nguồn dữ liệu", use_container_width=True)
                        st.markdown(f"[🔗 Đọc bài gốc trên Wikipedia]({data['url']})")
                    with c_text:
                        st.write(data["content"])
            else:
                st.warning(f"Không tìm thấy dữ liệu chính xác cho '{q}'. Vui lòng thử tên tiếng Anh hoặc tên khoa học.")

# === TAB 2: GIÁM SÁT VƯỜN (DYNAMIC ADVICE) ===
elif selected == "Giám Sát Vườn":
    st.title("🏡 GIÁM SÁT & LỜI KHUYÊN CHUYÊN GIA")
    
    # Giả lập môi trường
    c1, c2, c3 = st.columns(3)
    temp = c1.slider("Nhiệt độ môi trường (°C)", 10, 45, 36)
    hum = c2.slider("Độ ẩm không khí (%)", 10, 100, 80)
    
    # Chọn cây để nhận lời khuyên
    target_plant_name = c3.selectbox("Chọn cây để phân tích:", df["Tên Cây"])
    target_plant = df[df["Tên Cây"] == target_plant_name].iloc[0]
    
    st.divider()
    
    # TÍNH TOÁN LỜI KHUYÊN ĐỘNG
    base_msg, warnings = smart_advice(target_plant, temp, hum)
    
    # Hiển thị giao diện phân tích
    col_info, col_advice = st.columns([1, 2])
    
    with col_info:
        st.markdown(f"### Hồ sơ: {target_plant['Tên Cây']}")
        st.info(f"Phân loại: **{target_plant['Loại']}**")
        st.write(f"💧 Nhu cầu nước: {target_plant['Nước (L/ngày)']} L")
        st.write(f"☀️ Ánh sáng: {target_plant['Ánh Sáng']}")
    
    with col_advice:
        st.markdown("### 🤖 Bác sĩ AI chẩn đoán:")
        
        # 1. Lời khuyên cốt lõi (Theo loại cây)
        st.markdown(f"<div class='advice-box'>💡 <b>Nguyên tắc vàng:</b> {base_msg}</div>", unsafe_allow_html=True)
        
        # 2. Cảnh báo động (Dựa trên thời tiết thực)
        if warnings:
            for w in warnings:
                st.error(w)
        else:
            st.success("✅ Môi trường hiện tại RẤT LÝ TƯỞNG cho loài cây này phát triển.")

# === TAB 3: CẤU HÌNH ===
elif selected == "Cấu Hình":
    st.title("⚙️ CẤU HÌNH HỆ THỐNG")
    st.write("Phiên bản: EcoMind v9.0 Knowledge Edition")
    st.checkbox("Tự động dịch sang Tiếng Việt (Auto-Translate)", value=True)
    st.checkbox("Chế độ tiết kiệm băng thông", value=False)
