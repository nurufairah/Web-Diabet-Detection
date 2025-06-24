import streamlit as st
import pandas as pd
import joblib

model = joblib.load("model/rfc_diabet_model.pkl")

st.title("Input Manual Data Pasien")

with st.form("input_form"):
    gender = st.selectbox("Gender", ["Female", "Male"])
    age = st.number_input("Umur", min_value=1, max_value=120, step=1)
    urea = st.number_input("Rasio Urea", min_value=0.0, step=0.01)
    cr = st.number_input("Rasio Kreatinin", min_value=0.0, step=0.01)
    hba1c = st.number_input("Rasio HbA1c", min_value=0.0, step=0.01)
    chol = st.number_input("Rasio Kolesterol", min_value=0.0, step=0.01)
    tg = st.number_input("Rasio Trigliserida", min_value=0.0, step=0.01)
    hdl = st.number_input("Rasio HDL", min_value=0.0, step=0.01)
    ldl = st.number_input("Rasio LDL", min_value=0.0, step=0.01)
    vldl = st.number_input("Rasio VLDL", min_value=0.0, step=0.01)
    bmi = st.number_input("Rasio BMI", min_value=0.0, step=0.01)

    submitted = st.form_submit_button("Prediksi")

if submitted:
    gender_encoded = 1 if gender == "Male" else 0
    input_data = pd.DataFrame([{
        "Gender": gender_encoded,
        "AGE": age,
        "Urea": urea,
        "Cr": cr,
        "HbA1c": hba1c,
        "Chol": chol,
        "TG": tg,
        "HDL": hdl,
        "LDL": ldl,
        "VLDL": vldl,
        "BMI": bmi
    }])

    prediction = model.predict(input_data)[0]

    st.subheader("Hasil Prediksi:")
    if prediction == 1:
        st.error("Model memprediksi pasien diabetes.")
    else:
        st.success("Model memprediksi pasien tidak diabetes.")
