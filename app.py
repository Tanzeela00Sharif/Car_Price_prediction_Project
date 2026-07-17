import pandas as pd
import pickle
import streamlit as st

# Page config
st.set_page_config(page_title="Car Price Predictor", page_icon="🚗", layout="centered")

# ----------------------------------------------------------------------
# Custom CSS — hero banner + form styling (design language from reference)
# ----------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .main {
        background-color: #f5f7fa;
    }

    /* Remove default top padding so hero banner sits flush at the top */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 2rem;
    }

    /* ---------- HERO BANNER ---------- */
    .hero {
        background: linear-gradient(135deg, #0a0e27 0%, #161b3d 100%);
        border-radius: 0 0 18px 18px;
        padding: 2.8rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        color: white;
        text-align: center;
    }
    .hero-eyebrow {
        color: #f5a623;
        font-weight: 600;
        font-size: 0.9rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.2;
        margin: 0;
    }
    .hero-title .accent {
        color: #f5a623;
    }
    .hero-subtitle {
        font-size: 0.85rem;
        font-weight: 400;
        opacity: 0.75;
        margin-top: 0.5rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* ---------- SECTION TITLE ---------- */
    .form-title-wrap {
        text-align: center;
        margin-bottom: 1.3rem;
    }
    .form-title {
        font-weight: 700;
        font-size: 1.3rem;
        letter-spacing: 1px;
        border-bottom: 2px solid #0a0e27;
        padding-bottom: 0.4rem;
        color: #1f2937;
    }

    /* ---------- LABELS ---------- */
    label, .stSelectbox label, .stNumberInput label {
        font-weight: 700 !important;
        font-size: 0.78rem !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        color: #1a1a2e !important;
    }

    /* ---------- BUTTON (kept your red accent, just refined) ---------- */
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

    /* ---------- RESULT BOX (kept your green success style, refined) ---------- */
    .prediction-box {
        background-color: #e8f8f0;
        border-left: 6px solid #00c853;
        padding: 20px;
        border-radius: 10px;
        font-size: 22px;
        font-weight: bold;
        color: #00692e;
        margin-top: 20px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Hero banner markup (replaces the plain st.title)
# ----------------------------------------------------------------------
st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">Sell Your Car At A Best Price</div>
        <div class="hero-title">MOST-RELIABLE <span class="accent">PRICE</span></div>
        <div class="hero-subtitle">🚗 Predictor</div>
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
