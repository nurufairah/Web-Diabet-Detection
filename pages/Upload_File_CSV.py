import streamlit as st
import pandas as pd
import joblib

model = joblib.load("model/rfc_diabet_model.pkl")

st.title("Upload File CSV")

uploaded_file = st.file_uploader(
    "Upload file CSV dengan kolom: gender, age, urea, cr, hba1c, chol, tg, hdl, ldl, vldl, bmi", 
    type=["csv"]
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, sep=";")

        rename_dict = {
            'gender': 'Gender',
            'age': 'AGE',
            'urea': 'Urea',
            'cr': 'Cr',
            'hba1c': 'HbA1c',
            'chol': 'Chol',
            'tg': 'TG',
            'hdl': 'HDL',
            'ldl': 'LDL',
            'vldl': 'VLDL',
            'bmi': 'BMI',
            'class': 'CLASS'
        }

        df.columns = [col.strip().lower() for col in df.columns]
        df.rename(columns=rename_dict, inplace=True)

        gender_asli = df['Gender'].copy()
        df_for_model = df.copy()

        if 'Gender' in df_for_model.columns and df_for_model['Gender'].dtype == 'object':
            df_for_model['Gender'] = df_for_model['Gender'].apply(lambda x: 1 if str(x).strip().lower() == 'male' else 0)

        if 'CLASS' in df_for_model.columns:
            df_for_model.drop(columns=['CLASS'], inplace=True)

        required_features = ['Gender', 'AGE', 'Urea', 'Cr', 'HbA1c', 'Chol', 'TG', 'HDL', 'LDL', 'VLDL', 'BMI']
        missing_cols = [col for col in required_features if col not in df_for_model.columns]

        if missing_cols:
            st.error(f"File CSV kamu kekurangan kolom: {missing_cols}")
        else:
            predictions = model.predict(df_for_model[required_features])
            probs = model.predict_proba(df_for_model[required_features])[:, 1]

            df['Gender'] = gender_asli
            df['Prediksi'] = ["Diabetes" if p == 1 else "Tidak diabetes" for p in predictions]
            df['Probabilitas Risiko (%)'] = [round(prob * 100, 2) for prob in probs]

            st.success("Hasil Prediksi:")
            st.dataframe(df)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses file: {e}")
