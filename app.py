import pandas as pd
import pickle
import streamlit as st

# Page config
st.set_page_config(page_title="Car Price Predictor", page_icon="🚗", layout="centered")

# ----------------------------------------------------------------------
# Custom CSS — hero banner + form styling, tuned for dark theme
# ----------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Hide Streamlit's default header bar so the hero banner isn't clipped under it */
    header[data-testid="stHeader"] {
        background: transparent;
        height: 0rem;
    }
    div[data-testid="stToolbar"] {
        visibility: hidden;
    }

    /* Force consistent dark background across the whole app */
    [data-testid="stAppViewContainer"], .stApp {
        background-color: #0e1117;
    }

    /* Remove default top padding, add just enough so hero isn't clipped */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* ---------- HERO BANNER ---------- */
    .hero {
        background: linear-gradient(135deg, #0a0e27 0%, #161b3d 100%);
        border-radius: 14px;
        padding: 2.2rem 2rem;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .hero-title {
        font-size: 1.9rem;
        font-weight: 800;
        line-height: 1.3;
        margin: 0;
        color: #f5f5f5;
    }
    .hero-title .accent {
        color: #f5a623;
    }
    .hero-subtitle {
        font-size: 0.8rem;
        font-weight: 400;
        color: #c8c9d6;
        margin-top: 0.6rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* ---------- SECTION TITLE ---------- */
    .form-title-wrap {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .form-title {
        font-weight: 700;
        font-size: 1.25rem;
        letter-spacing: 1px;
        border-bottom: 2px solid #f5a623;
        padding-bottom: 0.4rem;
        color: #f5f5f5;
    }

    /* ---------- LABELS — light text for dark background ---------- */
    label, .stSelectbox label, .stNumberInput label {
        font-weight: 700 !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        color: #b8bac4 !important;
    }

    /* ---------- BUTTON ---------- */
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        font-size: 16px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 0.7em 2em;
        border-radius: 8px;
        border: none;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #e63939;
        transform: scale(1.02);
    }

    /* ---------- RESULT BOX ---------- */
    .prediction-box {
        background-color: #10281c;
        border-left: 6px solid #00c853;
        padding: 20px;
        border-radius: 10px;
        font-size: 22px;
        font-weight: bold;
        color: #4dffa0;
        margin-top: 20px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Hero banner — single clear headline as requested
# ----------------------------------------------------------------------
st.markdown("""
    <div class="hero">
        <div class="hero-title">MOST-RELIABLE <span class="accent">USED CAR PRICE</span> PREDICTOR</div>
        <div class="hero-subtitle">🚗 Get an instant, data-driven price estimate</div>
    </div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Your original logic — untouched
# ----------------------------------------------------------------------
car_data = pd.read_csv('clean_car_data.csv')
model = pickle.load(open('LinearRegression.pkl', 'rb'))

st.markdown("""<div class="form-title-wrap"><span class="form-title">PREDICT YOUR CAR PRICE</span></div>""",
            unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    name = st.selectbox("Name", sorted(car_data['name'].unique()))
    year = st.number_input("Year", min_value=int(car_data['year'].min()), max_value=int(car_data['year'].max()), value=2015)
    kms_driven = st.number_input("Kilometers Driven", min_value=0, value=50000)
with col2:
    company = st.selectbox("Company", sorted(car_data['company'].unique()))
    fuel_type = st.selectbox("Fuel Type", sorted(car_data['fuel_type'].unique()))

st.write("")

if st.button("🔍 Predict Price"):
    input_df = pd.DataFrame([[name, company, year, fuel_type, kms_driven]],
                              columns=['name', 'company', 'year', 'fuel_type', 'kms_driven'])
    prediction = model.predict(input_df)[0]
    prediction_pkr = prediction * 2.93

    # --- fuel type icon ---
    fuel_icons = {
        'Petrol': '⛽',
        'Diesel': '🛢️',
        'LPG': '🌿'
    }
    icon = fuel_icons.get(fuel_type, '🚗')

    st.markdown(f"<h1 style='text-align:center;'>{icon}</h1>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="prediction-box">
            💰 Estimated Price: PKR {prediction:,.0f} (PKR)
        </div>
    """, unsafe_allow_html=True)
