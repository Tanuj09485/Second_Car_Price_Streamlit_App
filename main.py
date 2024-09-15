import numpy as np
import pandas as pd
import streamlit as st
from joblib import load

# Custom CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize the session state with an empty prediction
if 'pred' not in st.session_state:
    st.session_state['pred'] = None

# Function to load the model
@st.cache_resource(show_spinner="Loading Model...")
def load_model():
    pipe = load('dump_model/model.joblib')
    return pipe

# Creating a function to make prediction
def make_prediction(pipe):
    make = st.session_state['make']
    fuel = st.session_state['fuel']
    kms_driven = st.session_state['kms_driven']
    model = st.session_state['model']
    year = st.session_state['year']

    columns = ['kms_driven', 'fuel_type', 'year_of_manufacture', 'brand', 'model']
    X_pred = pd.DataFrame([[kms_driven, fuel, year, make, model]], columns=columns)

    pred = pipe.predict(X_pred)
    pred = round(pred[0], 2)
    st.session_state['pred'] = pred

# Dictionary to map car makes to models
car_dict = {
    'Maruti Suzuki': ["Wagon R", "Alto", "Baleno", "Swift DZire", "Swift", "S-Presso", "Ciaz"],
    'Hyundai': ["Grand i10", "Elite i20", "Creta", "Verna", "Santro", "Eon"],
    'Honda': ["City", "Jazz", "Amaze", "BR-V", "WR-V", "Brio"],
    'Ford': ["EcoSport", "Endeavour", "Figo", "Aspire"],
    'Toyota': ["Corolla", "Innova", "Fortuner", "Urban", "Etios", "Camry"],
    'Tata': ["Harrier", "Tiago", "Nexon EV", "Nexon", "Safari", "Hexa"],
    'Renault': ["Kwid", "Duster", "Triber"],
    'Mahindra': ["XUV500", "TUV300", "Alturas", "Thar", "Bolero", "Scorpio", "XUV300"],
    'Mercedes': ["CLA 200", "E-Class", "C-Class", "GLE 250"],
    'Audi': ["A3", "A4", "A6", "Q3", "Q7"],
    'Volkswagen': ["Polo", "Vento", "Tiguan", "Ameo"],
    'BMW': ["X1", "X5", "3 Series", "5 Series", "7 Series"],
    'Skoda': ["Kodiaq", "Rapid", "Octavia", "Superb"],
    'Kia': ["Sonet", "Seltos"],
    'MG': ["Astor", "Hector", "Gloster"],
    'Jeep': ["Compass", "Wrangler"],
    'Nissan': ["Terrano", "Magnite"]
}

# Main app function
if __name__ == "__main__":
    # Load custom CSS
    local_css("styles.css")

    # Page title
    st.markdown("<h1 style='text-align: center;'>🚗 CarValuX</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: red;'>Get an estimated price for your car with just a few inputs</p>", unsafe_allow_html=True)

    # Load model
    pipe = load_model()

    # Main container layout
    with st.container():
        # First row for inputs
        st.markdown("<h3 style='text-align: center;'>Enter Car Details</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            make = st.selectbox("🚘 Select Make", options=list(car_dict.keys()), key='make')

            # Dynamically update the model options based on the selected make
            models_for_make = car_dict.get(make, [])
            model = st.selectbox("🚗 Select Model", options=models_for_make, key='model')

        with col2:
            st.selectbox("⛽ Fuel Type", options=['Petrol', 'Diesel', 'CNG'], key='fuel')
            st.selectbox("🛠 Year of Manufacturing", options=[2022, 2021, 2020, 2019, 2018, 2017, 2016,
                                                              2015, 2014, 2013, 2012, 2011,
                                                              2010, 2009, 2008, 2007, 2006, 2005], key='year')

        with col3:
            st.number_input("📏 Kms Driven", min_value=1000, value=20000, step=1000, key='kms_driven')
            name = st.text_input("Your Name",'Name',key='name')

    # Centered button
    button_col = st.columns([3, 2, 3])[1]
    with button_col:
        if st.button("💸 Check Value", type="primary"):
            make_prediction(pipe)

    # Result
    if st.session_state['pred'] is not None:
        st.success(f"Hi {name}, I hope you having a good day!")
        st.success(f" 🎯 The estimated car price is {st.session_state['pred']}₹", icon="💰")


