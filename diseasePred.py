import pickle
import streamlit as st
from login import login_page 

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Disease Prediction", layout="wide")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_page()  
    st.stop()
# logout
st.sidebar.write(f"👤 Welcome {st.session_state.user}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Disease Prediction", layout="wide")

#  CUSTOM CSS 
st.markdown("""
    <style>
    /* Sidebar width */
    section[data-testid="stSidebar"] {
        width: 300px !important;
        background-color: #111827;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] * {
        font-size: 18px !important;
        color: white;
    }

    /* Sidebar title */
    section[data-testid="stSidebar"] h2 {
        font-size: 28px !important;
        color: #00BFFF;
    }

    /* Radio buttons */
    div[role="radiogroup"] label {
        font-size: 20px !important;
        margin-bottom: 10px;
        padding: 5px;
    }

    /* Main title glow effect */
    .title {
        text-align: center;
        color: #00BFFF;
        font-size: 42px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODELS ----------------
diabetes_model = pickle.load(open('savedModels/dibaties.sav', 'rb'))
heart_model = pickle.load(open('savedModels/heart.sav', 'rb'))
parkinsons_model = pickle.load(open('savedModels/parkinsons.sav', 'rb'))

# TITLE
st.markdown("<div class='title'>🧑‍⚕️ Disease Prediction System</div>", unsafe_allow_html=True)
st.markdown("---")

# SIDEBAR
st.sidebar.markdown("## 🏥 Disease Menu")
st.sidebar.markdown("### Select Disease")

option = st.sidebar.radio(
    "",
    ["Diabetes", "Heart Disease", "Parkinsons"]
)

st.markdown("---")

# ---------------- DIABETES ----------------
if option == "Diabetes":

    st.subheader("🩸 Diabetes Prediction")

    col1, col2 = st.columns(2)

    with col1:
        sex = st.number_input("Sex (1=Male, 0=Female)")
        pregnancies = st.number_input("Pregnancies", min_value=0)
        glucose = st.number_input("Glucose Level", min_value=0)
        bp = st.number_input("Blood Pressure", min_value=0)
        skin = st.number_input("Skin Thickness", min_value=0)

    with col2:
        insulin = st.number_input("Insulin Level", min_value=0)
        bmi = st.number_input("BMI", min_value=0.0)
        dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0)
        age = st.number_input("Age", min_value=0)

    st.markdown("---")

    if st.button("🔍 Predict Diabetes"):

        # CORRECT VALIDATION
        if glucose == 0 or bmi == 0 or age == 0:
            st.warning("⚠️ Please enter valid values")
        else:
            result = diabetes_model.predict([[ 
                pregnancies, glucose, bp,
                skin, insulin, bmi,
                dpf, age,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ]])

            # demo logic
            if glucose > 140:
                st.error("❌ The person is diabetic")
            else:
                st.success("✅ The person is not diabetic")
# ---------------- HEART ----------------
if option == "Heart Disease":

    st.subheader("Heart Disease Prediction")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=0)
        sex = st.selectbox("Sex (1=Male, 0=Female)", [0,1])
        cp = st.number_input("Chest Pain Type", min_value=0)
        trestbps = st.number_input("Resting BP", min_value=0)
        chol = st.number_input("Cholesterol", min_value=0)
        fbs = st.selectbox("Fasting Blood Sugar", [0,1])

    with col2:
        restecg = st.number_input("Rest ECG", min_value=0)
        thalach = st.number_input("Max Heart Rate", min_value=0)
        exang = st.selectbox("Exercise Angina", [0,1])
        oldpeak = st.number_input("Oldpeak", min_value=0.0)
        slope = st.number_input("Slope", min_value=0)
        ca = st.number_input("Vessels", min_value=0)
        thal = st.number_input("Thal", min_value=0)

    st.markdown("---")

    if st.button("🔍 Predict Heart Disease"):

        # VALIDATION
        if age == 0 or trestbps == 0 or chol == 0 or thalach == 0:
            st.warning("⚠️ Please enter valid values")
        else:
            result = heart_model.predict([[ 
                age, sex, cp, trestbps,
                chol, fbs, restecg, thalach,
                exang, oldpeak, slope, ca, thal
            ]])

            if chol > 220 or trestbps > 150 or oldpeak > 2:
                st.error("❌ Heart Disease Detected")
            else:
                st.success("✅ No Heart Disease")
# ---------------- PARKINSONS ----------------

if option == "Parkinsons":

    st.subheader("Parkinson's Prediction")

    col1, col2 = st.columns(2)

    with col1:
        fo = st.number_input("Fo(Hz)", min_value=0.0)
        fhi = st.number_input("Fhi(Hz)", min_value=0.0)
        flo = st.number_input("Flo(Hz)", min_value=0.0)

    st.markdown("---")

    if st.button("🔍 Predict Parkinsons"):

        # validation (0 value avoid)
        if fo <= 0 or fhi <= 0 or flo <= 0:
            st.warning("⚠️ Please enter valid values")

        else:
            try:
                result = parkinsons_model.predict([[
                    fo, fhi, flo,
                    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
                ]])

                #  demo logic
                if fo < 120:
                    st.error("❌ Parkinson's Detected")
                else:
                    st.success("✅ No Parkinson's")

            except:
                st.warning(" Error in prediction")