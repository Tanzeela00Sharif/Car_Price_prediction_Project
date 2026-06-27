import pandas as pd
import pickle
import streamlit as st

# Load your original cleaned dataset (the one used for training)
car_data = pd.read_csv('/content/clean_car_data.csv')  # or wherever it's saved

model = pickle.load(open('LinearRegression.pkl', 'rb'))

st.title("Car Price Predictor")

name = st.selectbox("Car Name", sorted(car_data['name'].unique()))
company = st.selectbox("Company", sorted(car_data['company'].unique()))
year = st.number_input("Year", min_value=int(car_data['year'].min()), max_value=int(car_data['year'].max()), value=2015)
fuel_type = st.selectbox("Fuel Type", sorted(car_data['fuel_type'].unique()))
kms_driven = st.number_input("Kilometers Driven", min_value=0, value=50000)

if st.button("Predict Price"):
    input_df = pd.DataFrame([[name, company, year, fuel_type, kms_driven]],
                              columns=['name', 'company', 'year', 'fuel_type', 'kms_driven'])
    prediction = model.predict(input_df)
    st.success(f"Predicted Price: PKR{prediction[0]:,.0f}")
