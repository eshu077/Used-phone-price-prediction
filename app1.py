import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
import time
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="PhoneValuate AI | High-Contrast Pro",
    page_icon="📱",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
* { font-family: 'Poppins', sans-serif !important; opacity: 1 !important; }
.stApp { background-color: #0A0B10; color: #FFFFFF; }
header {visibility: hidden;}
.block-container {padding-top: 1rem !important;}
[data-testid="stSidebar"] { background-color: #12141d !important; }
h1,h2,h3,h4,label,p { color: #FFFFFF !important; }
div.stButton > button {
    background: #00FF88 !important;
    color: #000 !important;
    font-weight: 800 !important;
    font-size: 1.2rem !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("used_phone.csv")

@st.cache_resource
def load_model():
    with open("used_phone.pkl", "rb") as f:
        return pickle.load(f)

try:
    df = load_data()
    model = load_model()
except Exception as e:
    st.error("❌ Failed to load data/model")
    st.stop()

# ---------------- ENCODERS ----------------
le_brand = LabelEncoder()
le_model = LabelEncoder()
le_condition = LabelEncoder()

df["brand"] = le_brand.fit_transform(df["brand"])
df["model"] = le_model.fit_transform(df["model"])
df["condition"] = le_condition.fit_transform(df["condition"])

# ---------------- UI ----------------
st.markdown("<h1 style='text-align:center'>📱 PHONEVALUATE <span style='color:#00D2FF'>AI</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>Used Smartphone Price Predictor</p>", unsafe_allow_html=True)

st.sidebar.header("📋 Device Details")

brand = st.sidebar.selectbox("Brand", le_brand.classes_)
brand_id = le_brand.transform([brand])[0]

models = sorted(
    le_model.inverse_transform(df[df["brand"] == brand_id]["model"].unique())
)
model_name = st.sidebar.selectbox("Model", models)

ram = st.sidebar.select_slider("RAM (GB)", sorted(df["ram_gb"].unique()), value=8)
storage = st.sidebar.select_slider("Storage (GB)", sorted(df["storage_gb"].unique()), value=128)
condition = st.sidebar.selectbox("Condition", le_condition.classes_)
battery = st.sidebar.slider("Battery Health (%)", 50, 100, 85)
age = st.sidebar.number_input("Age (Years)", 0, 10, 1)
orig_price = st.sidebar.number_input("Original Price (₹)", 5000, 200000, 25000)

# ---------------- PREDICTION ----------------
if st.button("💰 Predict Price"):
    with st.spinner("Predicting..."):
        time.sleep(1)

        features = pd.DataFrame({
            "brand": [le_brand.transform([brand])[0]],
            "model": [le_model.transform([model_name])[0]],
            "ram_gb": [ram],
            "storage_gb": [storage],
            "condition": [le_condition.transform([condition])[0]],
            "battery_health": [battery],
            "age_years": [age],
            "original_price": [orig_price]
        })

        price = model.predict(features)[0]
        price = max(1000, min(price, orig_price * 0.9))

        st.success(f"💸 Estimated Resale Price: ₹ {int(price):,}")

st.markdown("""
<hr>
<p style='text-align:center'>
Developed by <b style='color:#00FF88'>ESHU SHARMA</b>
</p>
""", unsafe_allow_html=True)
