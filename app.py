import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time

# --- 1. ตั้งค่าหน้าเว็บ ---
st.set_page_config(
    page_title="NEON CITY : Lost & Found",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS ขั้นสูง (Glassmorphism & Animated Background) ---
st.markdown("""
<style>
    /* นำเข้าฟอนต์ Kanit */
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600;800&display=swap');

    * {
        font-family: 'Kanit', sans-serif !important;
    }

    /* พื้นหลังแบบเคลื่อนไหว (Aurora Gradient) */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #4a148c, #880e4f);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* หัวข้อใหญ่ Neon */
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        background: -webkit-linear-gradient(#00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 30px rgba(0, 198, 255, 0.5);
        margin-bottom: 10px;
    }
    
    .hero-subtitle {
        text-align: center;
        color: #e0e0e0;
        font-size: 1.2rem;
        margin-bottom: 40px;
        text-shadow: 0px 0px 10px rgba(255,255,255,0.3);
    }

    /* การ์ดกระจก (Glassmorphism) */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.3s ease-in-out;
    }

    .glass-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 15px 40px 0 rgba(31, 38, 135, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }

    /* สไตล์ปุ่ม */
    div.stButton > button {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 50px;
        font-weight: bold;
        transition: 0.3s;
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.5);
        width: 100%;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%);
        box-shadow: 0 0 25px rgba(0, 198, 255, 0.8);
        transform: scale(1.02);
    }

    /* ปรับแต่ง Input Fields */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #00c6ff !important;
        box-shadow: 0 0 10px rgba(0, 198, 255, 0.5) !important;
    }

    /* Badge สถานะ */
    .badge {
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 10px;
    }
    .badge-lost {
        background: rgba(255, 7, 58, 0.2);
        color: #ff073a;
        border: 1px solid #ff073a;
        box-shadow: 0 0 10px #ff073a;
    }
    .badge-found {
        background: rgba(57, 255, 20, 0.2);
        color: #39ff14;
        border: 1px solid #39ff14;
        box-shadow: 0 0 10px #39ff14;
    }

</style>
""", unsafe_allow_html=True)

# --- 3. ระบบจัดการข้อมูล (CSV) ---
DATA_FILE = 'data.csv'

def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=['Type', 'Item', 'Place', 'Desc', 'Contact', 'Time'])
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# --- 4. ส่วนแสดงผลหน้าเว็บ ---

# Header
st.markdown('<div class="hero-title">NEON LOST & FOUND</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">ศูนย์กลางแจ้งของหายและเก็บได้ ดีไซน์สำหรับโลกอนาคต</div>', unsafe_allow_html=True)

df = load_data()

# Dashboard Summary (เพิ่มลูกเล่นตัวเลข)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <h3 style="margin:0; color:#ff073a;">🔥 ของหาย (Lost)</h3>
        <h1 style="margin:0; font-size:3rem;">{len(df[df['Type']=='Lost'])}</h1>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <h3 style="margin:0; color:#39ff14;">🍀 เก็บได้ (Found)</h3>
        <h1 style="margin:0; font-size:3rem;">{len(df[df['Type']=='Found'])}</h1>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <h3 style="margin:0; color:#00c6ff;">💎 ทั้งหมด</h3>
        <h1 style="margin:0; font-size:3rem;">{len(df)}</h1>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# Layout หลัก
col_form, col_feed = st.columns([1, 2])

# --- ฝั่งซ้าย: ฟอร์มแจ้งข้อมูล ---
with col_form:
    st.markdown("### 📝 แจ้งข้อมูลใหม่")
    with st.container(): # ใช้ container เพื่อให้ CSS จับกลุ่มได้
        with st.form("main_form", clear_on_submit=True):
            type_option = st.selectbox("สถานะ", ["🔴 ของหาย (Lost)", "🟢 เก็บได้ (Found)"])
            item_name = st.text_input("สิ่งของ", placeholder="เช่น กุญแจรถ, กระเป๋าตังค์")
            place = st.text_input("สถานที่", placeholder="เช่น หน้าตึก 1, โรงอาหาร")
            desc = st.text_area("รายละเอียด", placeholder="สี, ลักษณะเด่น, แบรนด์...")
            contact = st.text_input("ติดต่อกลับ", placeholder="Line ID หรือ เบอร์โทร")
            
            submit = st.form_submit_button("ส่งข้อมูลเข้าสู่ระบบ")
            
            if submit:
                if item_name and contact:
                    new_type = 'Lost' if 'หาย' in type_option else 'Found'
                    new_entry = pd.DataFrame([{
                        'Type': new_type,
                        'Item': item_name,
                        'Place': place,
                        'Desc': desc,
                        'Contact': contact,
                        'Time': datetime.now().strftime("%d/%m/%Y %H:%M")
                    }])
                    df = pd.concat([df, new_entry], ignore_index=True)
                    save_data(df)
                    st.toast('บันทึกข้อมูลสำเร็จ!', icon='🎉')
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("กรุณากรอกชื่อสิ่งของและช่องทางติดต่อ")

# --- ฝั่งขวา: Feed รายการ ---
with col_feed:
    st.markdown("### 📡 รายการล่าสุด (Real-time Feed)")
    
    # Filter
    filter_val = st.radio("ตัวกรอง:", ["ทั้งหมด", "เฉพาะของหาย", "เฉพาะเก็บได้"], horizontal=True)
    
    show_df = df.copy()
    if filter_val == "เฉพาะของหาย":
        show_df = show_df[show_df['Type']=='Lost']
    elif filter_val == "เฉพาะเก็บได้":
        show_df = show_df[show_df['Type']=='Found']
    
    # แสดงผล (กลับลำดับเอาล่าสุดขึ้นก่อน)
    if not show_df.empty:
        for i, row in show_df.iloc[::-1].iterrows():
            
            # กำหนดสีและไอคอนตามประเภท
            if row['Type'] == 'Lost':
                badge_html = '<span class="badge badge-lost">LOST / ตามหา</span>'
                icon = "🔴"
            else:
                badge_html = '<span class="badge badge-found">FOUND / เก็บได้</span>'
                icon = "🟢"
                
            # HTML Card Structure
            st.markdown(f"""
            <div class="glass-card">
                <div style="display:flex; justify-content:space-between; align-items:start;">
                    <div>
                        {badge_html}
                        <h2 style="margin: 10px 0; color:white;">{icon} {row['Item']}</h2>
                        <p style="color:#ddd; margin:0;"><i class="fas fa-map-marker-alt"></i> 📍 <b>สถานที่:</b> {row['Place']}</p>
                        <p style="color:#bbb; margin-top:5px;">{row['Desc']}</p>
                    </div>
                    <div style="text-align:right;">
                         <div style="font-size:0.8rem; color:#888;">{row['Time']}</div>
                    </div>
                </div>
                <hr style="border-color: rgba(255,255,255,0.1);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:#00c6ff; font-weight:bold;">📞 {row['Contact']}</span>
                    <button style="background:rgba(255,255,255,0.1); border:1px solid #fff; color:#fff; border-radius:5px; cursor:pointer;">Contact</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("ยังไม่มีรายการแจ้งเข้ามาในขณะนี้")
