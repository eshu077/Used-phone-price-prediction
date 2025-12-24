import streamlit as st
import pandas as pd
import pickle

with open('used_phone.pkl', 'rb') as f:
    model = pickle.load(f)


df = pd.read_csv(r'C:\Users\HP\OneDrive\Desktop\Mobile Price Prediction\used_phone.csv')   

brand_model_map=df.groupby('brand')['model'].unique().to_dict(  )
brand_list=list(brand_model_map.keys())
st.title("Used Phone Price Prediction")
st.sidebar.header("Enter phone details")

selected_brand=st.sidebar.selectbox("Select Brand",brand_list)
selected_model=st.sidebar.selectbox("Select Model",brand_model_map[selected_brand])
ram=st.sidebar.selectbox("Select RAM in GB",sorted(df['ram_gb'].unique()))
storage=st.sidebar.selectbox("Select Storage in GB",sorted(df['storage_gb'].unique()))
condition=st.sidebar.selectbox("Select Condition",(df['condition'].unique()))
battery=st.sidebar.slider("Battery health (%)",50,100,80)
age=st.sidebar.slider("Age of Phone (in years)",0,5,1)
original_price=st.sidebar.number_input("Original Price (INR)",3000,100000,15000)


from sklearn.preprocessing import LabelEncoder
le_brand=LabelEncoder()
le_model=LabelEncoder() 
le_condition=LabelEncoder()

df['brand']=le_brand.fit_transform(df['brand'])
df['model']=le_model.fit_transform(df['model'])
df['condition']=le_condition.fit_transform(df['condition'])

brand_encoder=le_brand.transform([selected_brand])[0]
model_encoder=le_model.transform([selected_model])[0]
condition_encoder=le_condition.transform([condition])[0]


input_data=pd.DataFrame({
    'brand':[brand_encoder],
    'model':[model_encoder],
    'ram_gb':[ram],
    'storage_gb':[storage],
    'condition':[condition_encoder],
    "battery_health":[battery],
    "age_years":[age],
    "original_price":[original_price]
})

if st.sidebar.button("Predict"):
    predicted_price=model.predict(input_data)[0]
    st.success(f"Estimated Price of Used Phone: {int(predicted_price):,}")