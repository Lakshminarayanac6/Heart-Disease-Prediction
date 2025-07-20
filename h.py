import streamlit as st
import numpy as np
import pickle
import json
import os
import time

# -------- Configuration --------
USER_DB = "users.json"
MODEL_PATH = "C:\\Users\\vadap\\OneDrive\\Desktop\\heart\\heart_disease_model.sav"
BACKGROUND_IMAGE_URL = "https://png.pngtree.com/png-vector/20220808/ourlarge/pngtree-man-silhouette-healthy-heart-connected-dots-low-poly-wireframe-png-image_5759856.png"

# -------- User Handling --------
def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

# -------- Session Init --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# -------- Background and CSS --------
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url('{BACKGROUND_IMAGE_URL}');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}
    .top-left {{
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 9999;
        background: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
    }}
    .title-bar {{
        background-color: #111;
        color: #007BFF;
        font-size: 30px;
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 30px;
        font-weight: bold;
    }}
    .glass-card {{
        background: rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        backdrop-filter: blur(8px);
    }}
    .input-title {{
        font-weight: 700;
        margin: 10px 0 4px;
        color: #007BFF;
    }}
    .auth-title {{
        color: #007BFF;
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 15px;
    }}
    .result-box {{
        padding: 20px;
        font-weight: bold;
        font-size: 20px;
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
    }}
    .success {{
        background-color: #28a745dd;
        color: white;
    }}
    .error {{
        background-color: #dc3545dd;
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)

# -------- Login / Signup UI --------
def auth_ui():
    with st.container():
        with st.form("auth_form"):
            st.markdown('<div class="auth-title">🔐 Login / Sign Up</div>', unsafe_allow_html=True)
            tab = st.radio("Select Option", ["Login", "Sign Up"], horizontal=True)
            if tab == "Login":
                st.markdown('<div class="input-title">👤 Username</div>', unsafe_allow_html=True)
                username = st.text_input("", key="login_username")
                st.markdown('<div class="input-title">🔑 Password</div>', unsafe_allow_html=True)
                password = st.text_input("", type="password", key="login_password")
                if st.form_submit_button("Login"):
                    users = load_users()
                    if username in users and users[username] == password:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success(f"✅ Welcome, {username}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password.")
            else:
                st.markdown('<div class="input-title">👤 New Username</div>', unsafe_allow_html=True)
                new_username = st.text_input("", key="signup_username")
                st.markdown('<div class="input-title">🔐 New Password</div>', unsafe_allow_html=True)
                new_password = st.text_input("", type="password", key="signup_password")
                st.markdown('<div class="input-title">🔁 Confirm Password</div>', unsafe_allow_html=True)
                confirm_password = st.text_input("", type="password", key="signup_confirm")
                if st.form_submit_button("Sign Up"):
                    users = load_users()
                    if not new_username or not new_password:
                        st.warning("⚠ Fields cannot be empty.")
                    elif new_username in users:
                        st.error("❌ Username already exists.")
                    elif new_password != confirm_password:
                        st.warning("⚠ Passwords do not match.")
                    else:
                        users[new_username] = new_password
                        save_users(users)
                        st.success("🎉 Account created! Please log in.")

# -------- Show Login Overlay if Not Logged In --------
if not st.session_state.logged_in:
    with st.container():
        st.markdown('<div class="top-left">', unsafe_allow_html=True)
        auth_ui()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# -------- Load Model --------
@st.cache_resource
def load_model():
    return pickle.load(open(MODEL_PATH, 'rb'))

model = load_model()

# -------- App Title --------
st.markdown('<div class="title-bar">AI-Powered Heart Disease Prediction</div>', unsafe_allow_html=True)
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

# -------- Input Fields --------
st.markdown('<div class="input-title">Age:</div>', unsafe_allow_html=True)
age = st.number_input("", min_value=1, max_value=120, step=1, key="age")

st.markdown('<div class="input-title">Sex:</div>', unsafe_allow_html=True)
sex = st.radio("", options=[0, 1], format_func=lambda x: "Male" if x == 1 else "Female", key="sex")

st.markdown('<div class="input-title">Chest Pain Type:</div>', unsafe_allow_html=True)
cp = st.selectbox("", [0, 1, 2, 3], format_func=lambda x: ["Typical Angina", "Atypical Angina", "Non-anginal", "Asymptomatic"][x], key="cp")

st.markdown('<div class="input-title">Resting Blood Pressure (mm Hg):</div>', unsafe_allow_html=True)
trestbps = st.number_input("", min_value=80, max_value=200, step=1, key="trestbps")

st.markdown('<div class="input-title">Serum Cholesterol (mg/dL):</div>', unsafe_allow_html=True)
chol = st.number_input("", min_value=100, max_value=600, step=1, key="chol")

st.markdown('<div class="input-title">Fasting Blood Sugar > 120 mg/dL:</div>', unsafe_allow_html=True)
fbs = st.radio("", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No", key="fbs")

st.markdown('<div class="input-title">Resting ECG Results:</div>', unsafe_allow_html=True)
restecg = st.selectbox("", [0, 1, 2], key="restecg")

st.markdown('<div class="input-title">Maximum Heart Rate Achieved:</div>', unsafe_allow_html=True)
thalach = st.number_input("", min_value=60, max_value=250, step=1, key="thalach")

st.markdown('<div class="input-title">Exercise Induced Angina:</div>', unsafe_allow_html=True)
exang = st.radio("", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No", key="exang")

st.markdown('<div class="input-title">ST Depression Induced by Exercise:</div>', unsafe_allow_html=True)
oldpeak = st.number_input("", min_value=0.0, max_value=6.2, step=0.1, key="oldpeak")

st.markdown('<div class="input-title">Slope of the Peak Exercise ST Segment:</div>', unsafe_allow_html=True)
slope = st.selectbox("", [0, 1, 2], key="slope")

st.markdown('<div class="input-title">Number of Major Vessels (0–4):</div>', unsafe_allow_html=True)
ca = st.selectbox("", [0, 1, 2, 3, 4], key="ca")

st.markdown('<div class="input-title">Thalassemia Type:</div>', unsafe_allow_html=True)
thal = st.selectbox("", [0, 1, 2, 3], key="thal")

st.markdown('</div>', unsafe_allow_html=True)

# -------- Prediction Button --------
if st.button("✅ Predict", key="predict"):
    with st.spinner("AI is analyzing your data..."):
        time.sleep(2)
        user_input = np.array([[age, sex, cp, trestbps, chol, fbs, restecg,
                                thalach, exang, oldpeak, slope, ca, thal]])
        prediction = model.predict(user_input)

        if prediction[0] == 1:
            st.markdown('<div class="result-box error">⚠ High Risk of Heart Disease!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-box success">✅ No Heart Disease Detected!</div>', unsafe_allow_html=True)
