import streamlit as st
import numpy as np
import pickle
import time

# Load the saved model
@st.cache_resource
def load_model():
    model_filename = "C:\\Users\\vadap\\OneDrive\\Desktop\\heart\\heart_disease_model.sav"
    loaded_model = pickle.load(open(model_filename, 'rb'))
    return loaded_model

model = load_model()

# Custom CSS for a Modern Design
st.markdown("""
    <style>
        @keyframes slide {
            from { transform: translateX(-100%); }
            to { transform: translateX(0); }
        }
        .title-bar {
            background-color: black;
            color: white;
            font-size: 30px;
            font-weight: bold;
            text-align: center;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0px 6px 14px rgba(255, 255, 255, 0.2);
            animation: slide 1s ease-out;
            letter-spacing: 1px;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0px 8px 20px rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            margin-bottom: 20px;
        }
        .input-title {
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        .result-box {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .success {
            background-color: rgba(40, 167, 69, 0.85);
            color: white;
        }
        .error {
            background-color: rgba(220, 53, 69, 0.85);
            color: white;
        }
        .stButton>button {
            background-color: #28a745 !important;
            color: white !important;
            font-size: 18px !important;
            font-weight: bold !important;
            padding: 10px 20px !important;
            border-radius: 8px !important;
            box-shadow: 0px 4px 10px rgba(0, 255, 0, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

# Header with Sliding Black Bar
st.markdown('<div class="title-bar">AI-Powered Heart Disease Prediction</div>', unsafe_allow_html=True)

# Input Form with Separate Spacing
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown('<div class="input-title">Age:</div>', unsafe_allow_html=True)
age = st.number_input("", min_value=1, max_value=120, step=1, key="age_key")

st.markdown('<div class="input-title">Sex:</div>', unsafe_allow_html=True)
sex = st.radio("", options=[0, 1], format_func=lambda x: "Male" if x == 1 else "Female", key="sex_key")

st.markdown('<div class="input-title">Chest Pain Type:</div>', unsafe_allow_html=True)
cp = st.selectbox("", [0, 1, 2, 3], format_func=lambda x: ["Typical Angina", "Atypical Angina", "Non-anginal", "Asymptomatic"][x], key="cp_key")

st.markdown('<div class="input-title">Resting Blood Pressure (mm Hg):</div>', unsafe_allow_html=True)
trestbps = st.number_input("", min_value=80, max_value=200, step=1, key="trestbps_key")

st.markdown('<div class="input-title">Serum Cholesterol (mg/dL):</div>', unsafe_allow_html=True)
chol = st.number_input("", min_value=100, max_value=600, step=1, key="chol_key")

st.markdown('<div class="input-title">Fasting Blood Sugar > 120 mg/dL:</div>', unsafe_allow_html=True)
fbs = st.radio("", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No", key="fbs_key")

st.markdown('<div class="input-title">Resting ECG Results:</div>', unsafe_allow_html=True)
restecg = st.selectbox("", [0, 1, 2], key="restecg_key")

st.markdown('<div class="input-title">Maximum Heart Rate Achieved:</div>', unsafe_allow_html=True)
thalach = st.number_input("", min_value=60, max_value=250, step=1, key="thalach_key")

st.markdown('<div class="input-title">Exercise Induced Angina:</div>', unsafe_allow_html=True)
exang = st.radio("", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No", key="exang_key")

st.markdown('<div class="input-title">ST Depression Induced by Exercise:</div>', unsafe_allow_html=True)
oldpeak = st.number_input("", min_value=0.0, max_value=6.2, step=0.1, key="oldpeak_key")

st.markdown('<div class="input-title">Slope of the Peak Exercise ST Segment:</div>', unsafe_allow_html=True)
slope = st.selectbox("", [0, 1, 2], key="slope_key")

st.markdown('<div class="input-title">Number of Major Vessels (0-4):</div>', unsafe_allow_html=True)
ca = st.selectbox("", [0, 1, 2, 3, 4], key="ca_key")

st.markdown('<div class="input-title">Thalassemia Type:</div>', unsafe_allow_html=True)
thal = st.selectbox("", [0, 1, 2, 3], key="thal_key")

st.markdown('</div>', unsafe_allow_html=True)

# Space for Better Layout
st.markdown("<br><br>", unsafe_allow_html=True)

# Predict Button
predict_btn = st.button("✅ Predict")

if predict_btn:
    with st.spinner("AI is analyzing your data..."):
        time.sleep(2)  # Simulated AI Processing
        user_input = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
        prediction = model.predict(user_input)

        # Display Results
        st.markdown("<br>", unsafe_allow_html=True)
        if prediction[0] == 1:
            st.markdown('<div class="result-box error">⚠️High Risk of Heart Disease!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-box success">✅No Heart Disease Detected!</div>', unsafe_allow_html=True)
