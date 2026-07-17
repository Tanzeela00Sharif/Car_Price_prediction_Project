import pandas as pd
import pickle
import streamlit as st
# Page config
st.set_page_config(page_title="Car Price Predictor", page_icon="🚗", layout="centered")
# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: 
#f5f7fa;
    }
    .stButton>button {
        background-color: 
#ff4b4b;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 0.6em 2em;
        border-radius: 12px;
        border: none;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: 
#e63939;
        transform: scale(1.02);
    }
    .prediction-box {
        background-color: 
#e8f8f0;
        border-left: 6px solid 
#00c853;
        padding: 20px;
        border-radius: 10px;
        font-size: 22px;
        font-weight: bold;
        color: 
#00692e;
        margin-top: 20px;
    }
    h1 {
        color: 
#1f2937;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)
car_data = pd.read_csv('clean_car_data.csv')
model = pickle.load(open('LinearRegression.pkl', 'rb'))
st.title("🚗 Car Price Predictor")
st.markdown("##### Get an instant price estimate for your used car")
st.divider()
col1, col2 = st.columns(2)
with col1:
    name=st.selectbox("name", sorted(car_data['name'].unique()))
    year = st.number_input("Year", min_value=int(car_data['year'].min()), max_value=int(car_data['year'].max()), value=2015)
    kms_driven = st.number_input("Kilometers Driven", min_value=0, value=50000)
with col2:
    company = st.selectbox("Company", sorted(car_data['company'].unique()))
    fuel_type = st.selectbox("Fuel Type", sorted(car_data['fuel_type'].unique()))
st.write("")
if st.button("🔍 Predict Price"):
    input_df = pd.DataFrame([[name, company, year, fuel_type, kms_driven]],
                              columns=['name','company', 'year', 'fuel_type', 'kms_driven'])
    prediction = model.predict(input_df)[0]
    prediction_pkr = prediction * 2.93
    # --- Option B: fuel type icon ---
    fuel_icons = {
        'Petrol': '⛽',
        'Diesel': '🛢️',
        'LPG': '🌿'
    }
    icon = fuel_icons.get(fuel_type, '🚗')
    st.markdown(f"<h1 style='text-align:center;'>{icon}</h1>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="prediction-box">
            💰 Estimated Price: PKR{prediction:,.0f} (PKR)<br>
            </div>
    """, unsafe_allow_html=True)
