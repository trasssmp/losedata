import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- ตั้งค่าหน้าเว็บ ---
st.set_page_config(
    page_title="Neon Lost & Found",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS : ตกแต่งธีม Neon & Glowing ---
st.markdown("""
<style>
    /* Import Font: Kanit */
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Kanit', sans-serif;
    }

    /* พื้นหลัง Dark Mode */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 20%, #1a1a2e 0%, #000000 80%);
    }

    /* หัวข้อ Neon Glowing */
    .neon-title {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        color: #fff;
        text-transform: uppercase;
        margin-bottom: 30px;
        text-shadow: 
            0 0 5px #fff,
            0 0 10px #fff,
            0 0 20px #00f3ff,
            0 0 40px #00f3ff,
            0 0 80px #00f3ff;
        animation: flicker 2s infinite alternate;
    }

    /* Animation การกระพริบ */
    @keyframes flicker {
        0%, 18%, 22%, 25%, 53%, 57%, 100% {
            text-shadow: 
            0 0 4px #fff,
            0 0 11px #fff,
            0 0 19px #00f3ff,
            0 0 40px #00f3ff,
            0 0 80px #00f3ff;
        }
        20%, 24%, 55% {       
            text-shadow: none;
        }
    }

    /* การ์ดแสดงผล */
    .item-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .item-card:hover {
        transform: translateY(-5px);
    }

    /* เส้นขอบเรืองแสงตามสถานะ */
    .border-lost {
        border-left: 5px solid #ff073a; /* Neon Red */
        box-shadow: -5px 0 15px rgba(255, 7, 58, 0.3);
    }

    .border-found {
        border-left: 5px solid #39ff14; /* Neon Green */
        box-shadow: -5px 0 15px rgba(57, 255, 20, 0.3);
    }

    .card-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: white;
        margin-bottom: 10px;
    }

    .card-text {
        color: #e0e0e0;
        font-size: 1rem;
        margin-bottom: 5px;
    }

    .card-footer {
        font-size: 0.8rem;
        color: #888;
        text-align: right;
        margin-top: 10px;
    }

    /* ปรับแต่ง Input ของ Streamlit */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: rgba(255,255,255,0.05);
        color: #fff;
        border: 1px solid #00f3ff;
        border-radius: 8px;
    }
    
    /* ปุ่มกด */
    .stButton > button {
        width: 100%;
        background-color: transparent;
        color: #00f3ff;
        border: 2px solid #00f3ff;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #00f3ff;
        color: #000;
        box-shadow: 0 0 20px #00f3ff;
    }

</style>
""", unsafe_allow_html=True)

# --- ส่วนจัดการข้อมูล (CSV) ---
DATA_FILE = 'lost_found_data.csv'

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # สร้าง DataFrame ว่างถ้ายังไม่มีไฟล์
        return pd.DataFrame(columns=['Type', 'ItemName', 'Location', 'Description', 'Contact', 'Timestamp'])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# --- ส่วนแสดงผลหลัก ---
st.markdown('<div class="neon-title">NEON LOST & FOUND</div>', unsafe_allow_html=True)

# โหลดข้อมูล
df = load_data()

# แบ่งหน้าจอเป็น 2 คอลัมน์ (ซ้าย: ฟอร์ม, ขวา: รายการ)
col1, col2 = st.columns([1, 2])

# --- คอลัมน์ซ้าย: ฟอร์มแจ้งของ ---
with col1:
    st.markdown("### 📝 แจ้งรายการใหม่")
    
    with st.form("entry_form", clear_on_submit=True):
        report_type = st.radio("ประเภท", ["ของหาย (Lost)", "เก็บได้ (Found)"], horizontal=True)
        item_name = st.text_input("ชื่อสิ่งของ", placeholder="เช่น iPhone 13, กระเป๋าตังค์")
        location = st.text_input("สถานที่", placeholder="เช่น ตึก 5, โรงอาหาร")
        description = st.text_area("รายละเอียด", placeholder="สี, จุดสังเกต...")
        contact = st.text_input("ช่องทางติดต่อ", placeholder="เบอร์โทร หรือ Line ID")
        
        submitted = st.form_submit_button("🚀 ประกาศทันที")
        
        if submitted:
            if item_name and contact:
                new_data = {
                    'Type': 'Lost' if 'หาย' in report_type else 'Found',
                    'ItemName': item_name,
                    'Location': location,
                    'Description': description,
                    'Contact': contact,
                    'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                # ใช้ pd.concat แทน append (ตาม version ใหม่ของ pandas)
                new_df = pd.DataFrame([new_data])
                df = pd.concat([df, new_df], ignore_index=True)
                save_data(df)
                st.success("บันทึกข้อมูลสำเร็จ! ข้อมูลจะปรากฏทางขวามือ")
                st.rerun() # รีเฟรชหน้าเพื่อแสดงข้อมูลใหม่
            else:
                st.error("กรุณากรอก 'ชื่อสิ่งของ' และ 'ช่องทางติดต่อ'")

# --- คอลัมน์ขวา: แสดงรายการ (Feed) ---
with col2:
    st.markdown("### 📡 รายการล่าสุด")
    
    # ตัวกรอง (Filter)
    filter_option = st.selectbox("แสดงรายการ:", ["ทั้งหมด", "เฉพาะของหาย", "เฉพาะที่เก็บได้"])
    
    # กรองข้อมูล
    display_df = df.copy()
    if filter_option == "เฉพาะของหาย":
        display_df = display_df[display_df['Type'] == 'Lost']
    elif filter_option == "เฉพาะที่เก็บได้":
        display_df = display_df[display_df['Type'] == 'Found']
    
    # เรียงลำดับจากใหม่ไปเก่า
    if not display_df.empty:
        display_df = display_df.iloc[::-1]

        for index, row in display_df.iterrows():
            # กำหนด Class สีตามประเภท
            css_class = "border-lost" if row['Type'] == 'Lost' else "border-found"
            status_text = "LOST / ตามหา" if row['Type'] == 'Lost' else "FOUND / เก็บได้"
            status_color = "#ff073a" if row['Type'] == 'Lost' else "#39ff14"
            
            # สร้างการ์ด HTML
            html_card = f"""
            <div class="item-card {css_class}">
                <div style="color: {status_color}; font-weight: bold; letter-spacing: 2px; margin-bottom:5px;">
                    {status_text}
                </div>
                <div class="card-header">{row['ItemName']}</div>
                <div class="card-text">📍 <b>สถานที่:</b> {row['Location']}</div>
                <div class="card-text">📝 <b>รายละเอียด:</b> {row['Description']}</div>
                <div class="card-text" style="color: #00f3ff; margin-top: 10px;">
                    📞 <b>ติดต่อ:</b> {row['Contact']}
                </div>
                <div class="card-footer">🕒 {row['Timestamp']}</div>
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)
    else:
        st.info("ยังไม่มีรายการแจ้งเข้ามา")
