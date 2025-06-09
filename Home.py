import streamlit as st

st.title("Selamat Datang di Web Prediksi Diabetes")
st.write("""
Aplikasi ini menggunakan Machine Learning untuk memprediksi risiko penyakit diabetes berdasarkan input manual 
ataupun dari file CSV.

Silakan gunakan menu di sebelah kiri untuk memilih metode input yang kamu inginkan.
""")
st.caption("Catatan: Hasil prediksi ini bersifat informatif dan bukan pengganti diagnosis medis.")

st.markdown("---")
st.subheader("Penjelasan Input")
st.markdown("""
    - **Gender**: Jenis kelamin pasien. Pilih *Male* (laki-laki) atau *Female* (perempuan).
    - **Umur**: Umur pasien dalam satuan tahun.
    - **Rasio Urea**: Rasio urea dalam darah.
    - **Rasio Kreatinin (Cr)**: Rasio kreatinin dalam darah.
    - **Rasio HbA1c**: Hemoglobin terglikasi.
    - **Rasio Kolesterol**: Kolesterol total dalam darah.
    - **Rasio Trigliserida (TG)**: Trigliserida dalam darah.
    - **Rasio HDL**: Kolesterol HDL (kolesterol baik).
    - **Rasio LDL**: Kolesterol LDL (kolesterol jahat).
    - **Rasio VLDL**: Kolesterol VLDL dalam darah.
    - **Rasio BMI**: Indeks massa tubuh.""")