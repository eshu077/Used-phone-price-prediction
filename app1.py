import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="PhoneValuate AI | High-Contrast Pro",
    page_icon="📱",
    layout="wide"
)

# ---------------- ULTRA-CLEAR CSS (ZERO FADING) ----------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

    /* Sabse pehle default fading hatane ke liye */
    * {
        font-family: 'Poppins', sans-serif !important;
        opacity: 1 !important; /* Force visibility on everything */
    }

    .stApp {
        background-color: #0A0B10; /* Solid Deep Black-Blue */
        color: #FFFFFF;
    }

    /* Top Bar & Header removal */
    header {visibility: hidden;}
    .block-container {padding-top: 1rem !important;}

    /* Sidebar - Pure Solid Look (No Transparency) */
    [data-testid="stSidebar"] {
        background-color: #12141d !important;
        border-right: 2px solid #1E2130;
    }

    /* Crystal Clear Headers & Labels */
    h1, h2, h3, h4 {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    label {
        color: #00D2FF !important; /* Vibrant Neon Blue for Labels */
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        margin-bottom: 10px !important;
    }

    /* Input Field Clarity (Pure White Text) */
    input, .stSelectbox div[data-baseweb="select"] {
        background-color: #1E2130 !important;
        color: #FFFFFF !important;
        border: 1px solid #333 !important;
        font-weight: 600 !important;
    }

    /* Device Configuration Title Style */
    .config-title {
        color: #00FF88 !important; /* Neon Green for Sidebar Title */
        font-size: 1.4rem;
        font-weight: 800;
        border-bottom: 2px solid #00FF88;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }

    /* Summary Card Styling */
    .details-card {
        background: #161B22;
        padding: 30px;
        border-radius: 20px;
        border-left: 8px solid #00D2FF;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .details-card p {
        color: #FFFFFF !important;
        font-size: 1.2rem !important;
        margin-bottom: 15px !important;
    }

    /* Result Box - The Star Element */
    .result-container {
        background: linear-gradient(135deg, #00D2FF 0%, #3A7BD5 100%);
        padding: 40px;
        border-radius: 30px;
        text-align: center;
        box-shadow: 0 0 40px rgba(0, 210, 255, 0.3);
    }
    .result-container h1 {
        font-size: 4.5rem !important;
        margin: 10px 0 !important;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }

    /* Button - Ultra Bold */
    div.stButton > button {
        background: #00FF88 !important;
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 1.3rem !important;
        border-radius: 15px;
        padding: 20px;
        border: none;
        box-shadow: 0 5px 15px rgba(0, 255, 136, 0.4);
    }

    /* Footer - High Visibility Glow */
    .footer-text {
        text-align: center;
        padding: 30px;
        font-weight: 600;
        font-size: 1.1rem;
        color: #FFFFFF !important;
        border-top: 1px solid #333;
        margin-top: 50px;
    }
    .footer-text span {
        color: #00FF88 !important; /* Glow your name */
        font-weight: 800;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- CORE LOGIC ----------------
@st.cache_data
def load_data():
    try:
        return pd.read_csv(r'C:\Users\HP\OneDrive\Desktop\Mobile Price Prediction\used_phone.csv')
    except:
        return None

df = load_data()

# Load Model
try:
    with open('used_phone.pkl', 'rb') as f:
        model = pickle.load(f)
except:
    st.error("Missing .pkl file!")

if df is not None:
    le_brand = LabelEncoder()
    le_model = LabelEncoder()
    le_condition = LabelEncoder()
    df['brand'] = le_brand.fit_transform(df['brand'])
    df['model'] = le_model.fit_transform(df['model'])
    df['condition'] = le_condition.fit_transform(df['condition'])

    # --- MAIN HEADER ---
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem;'>📱 PHONE<span style='color: #00D2FF;'>VALUATE</span> PRO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #888;'>Premium AI Engine for Used Smartphone Valuation</p>", unsafe_allow_html=True)

    # --- SIDEBAR (CRYSTAL CLEAR SPECS) ---
    st.sidebar.markdown('<p class="config-title">🛠 DEVICE SPECS</p>', unsafe_allow_html=True)
    
    brand_name = st.sidebar.selectbox("BRANDS", sorted(le_brand.classes_))
    
    # Model filter logic
    brand_id = le_brand.transform([brand_name])[0]
    m_list = sorted(le_model.inverse_transform(df[df['brand'] == brand_id]['model'].unique()))
    model_name = st.sidebar.selectbox("MODEL NAME", m_list)
    
    st.sidebar.markdown("---")
    ram = st.sidebar.select_slider("RAM (GB)", options=sorted(df['ram_gb'].unique()), value=8)
    storage = st.sidebar.select_slider("STORAGE (GB)", options=sorted(df['storage_gb'].unique()), value=128)
    condition_val = st.sidebar.selectbox("OVERALL CONDITION", le_condition.classes_)
    
    st.sidebar.markdown("---")
    battery = st.sidebar.slider("BATTERY HEALTH (%)", 50, 100, 85)
    age = st.sidebar.number_input("AGE (IN YEARS)", 0, 10, 1)
    orig_price = st.sidebar.number_input("ORIGINAL PRICE (₹)", 5000, 200000, 25000)

    # --- MAIN BODY ---
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("<h3>📋 PHONE REPORT</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="details-card">
            <p><b>📱 DEVICE:</b> {brand_name} {model_name}</p>
            <p><b>💾 SPECS:</b> {ram}GB RAM | {storage}GB ROM</p>
            <p><b>✨ STATUS:</b> {condition_val} Condition</p>
            <p><b>🔋 POWER:</b> {battery}% Battery Life</p>
            <p><b>⏳ USAGE:</b> {age} Year(s) Used</p>
            <p style="color: #00D2FF; font-size: 1.4rem !important; border-top: 1px solid #333; padding-top:15px;">
                <b>💰 BOUGHT AT:</b> ₹{orig_price:,}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("<h3>📊 AI VALUATION</h3>", unsafe_allow_html=True)
        st.write("") 
        if st.button("PREDICT BEST PRICE"):
            with st.spinner('Calculating value...'):
                time.sleep(1)
                
                # Input Preparation
                b_enc = le_brand.transform([brand_name])[0]
                m_enc = le_model.transform([model_name])[0]
                c_enc = le_condition.transform([condition_val])[0]

                features = pd.DataFrame({
                    'brand': [b_enc], 'model': [m_enc], 'ram_gb': [ram],
                    'storage_gb': [storage], 'condition': [c_enc],
                    'battery_health': [battery], 'age_years': [age],
                    'original_price': [orig_price]
                })

                price = model.predict(features)[0]
                # Price Logic
                final_price = max(1000, min(price, orig_price * 0.9))

                st.markdown(f"""
                    <div class="result-container">
                        <p style="font-weight: 800; letter-spacing: 2px;">MARKET ESTIMATE</p>
                        <h1>₹ {int(final_price):,}</h1>
                        <p style="opacity: 0.8;">Retained Value: {round((final_price/orig_price)*100, 1)}%</p>
                    </div>
                """, unsafe_allow_html=True)
                st.balloons()

    # --- FOOTER ---
    st.markdown(f"""
        <div class="footer-text">
            DEVELOPED BY <span>ESHU SHARMA</span> | ML POWERED PRICE ENGINE
        </div>
    """, unsafe_allow_html=True)

else:
    st.error("Error: CSV File not found or path incorrect.")