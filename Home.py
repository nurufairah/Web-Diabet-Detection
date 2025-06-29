import streamlit as st
import pandas as pd
import plotly.express as px # Import untuk visualisasi data

# --- Konfigurasi Halaman Streamlit (Harus di bagian paling atas script) ---
st.set_page_config(
    page_title="Aplikasi Deteksi Diabetes", # Judul yang muncul di tab browser diubah
    layout="wide", # Menggunakan layout lebar untuk tampilan tabel yang lebih baik
    initial_sidebar_state="expanded" # Sidebar akan terbuka secara default
)

# --- Bagian Header dan Deskripsi Utama ---
st.title("Selamat Datang di Aplikasi Deteksi Diabetes") # Judul utama diubah
st.write("""
Aplikasi ini menggunakan Machine Learning untuk **mendeteksi** risiko penyakit diabetes berdasarkan input manual
ataupun dari file CSV.

Silakan gunakan menu di sebelah kiri untuk memilih metode input yang kamu inginkan.
""")
st.caption("Catatan: Hasil **deteksi** ini bersifat informatif dan bukan pengganti diagnosis medis.") # Teks diubah

st.markdown("---")

# --- Penjelasan Atribut Input ---
st.subheader("Penjelasan Atribut Input")
st.markdown("""
- **Gender**: Jenis kelamin pasien. Pilih *Male* (laki-laki) atau *Female* (perempuan).
- **Umur**: Umur pasien dalam satuan tahun.
- **Rasio Urea**: Rasio urea dalam darah.
- **Rasio Kreatinin (Cr)**: Rasio kreatinin dalam darah.
- **Rasio HbA1c**: Hemoglobin terglikasi (penanda kadar gula darah rata-rata dalam 2-3 bulan terakhir).
- **Rasio Kolesterol**: Kolesterol total dalam darah.
- **Rasio Trigliserida (TG)**: Trigliserida dalam darah.
- **Rasio HDL**: Kolesterol HDL (kolesterol baik).
- **Rasio LDL**: Kolesterol LDL (kolesterol jahat).
- **Rasio VLDL**: Kolesterol VLDL (very-low-density lipoprotein) dalam darah.
- **Rasio BMI**: Indeks massa tubuh (Body Mass Index).
""")

st.markdown("---")

# --- Memuat dan Menampilkan Data Hasil Deteksi ---
st.subheader("Tabel Hasil Deteksi Diabetes dari Model") # Sub-judul diubah
st.write("Berikut adalah data hasil **deteksi** yang telah diproses oleh model machine learning:") # Teks diubah

# Path default untuk file hasil deteksi
# PASTIKAN FILE INI BERADA DI DIREKTORI YANG SAMA DENGAN FILE home.py
prediction_file_csv = "hasil_prediksi_diabetes.csv" # Nama file tetap sama agar tidak perlu ganti nama file Anda
prediction_file_xlsx = "hasil_prediksi_diabetes.xlsx" # Nama file tetap sama

hasil_predeksi = None # Inisialisasi variabel untuk menampung DataFrame

try:
    # Coba baca file CSV terlebih dahulu
    hasil_predeksi = pd.read_csv(prediction_file_csv)
    st.info(f"Data hasil **deteksi** berhasil dimuat dari '{prediction_file_csv}'.") # Teks diubah
except FileNotFoundError:
    try:
        # Jika CSV tidak ada, coba baca file Excel
        hasil_predeksi = pd.read_excel(prediction_file_xlsx)
        st.info(f"Data hasil **deteksi** berhasil dimuat dari '{prediction_file_xlsx}'.") # Teks diubah
    except FileNotFoundError:
        st.error("File 'hasil_prediksi_diabetes.csv' atau 'hasil_prediksi_diabetes.xlsx' tidak ditemukan di direktori aplikasi. Harap pastikan salah satu file tersebut ada untuk menampilkan hasil **deteksi**.") # Teks diubah
        st.stop() # Hentikan eksekusi Streamlit jika file tidak ditemukan
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat file Excel '{prediction_file_xlsx}': {e}")
        st.stop()
except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat file CSV '{prediction_file_csv}': {e}")
    st.stop()

# Menampilkan dataframe hasil deteksi
if hasil_predeksi is not None:
    st.dataframe(hasil_predeksi, use_container_width=True) # Tabel akan mengisi lebar kontainer

# --- Analisis Atribut Berisiko ---
if hasil_predeksi is not None: # Pastikan hasil_predeksi berhasil dimuat sebelum analisis
    st.markdown("---")
    st.subheader("Analisis Atribut Berisiko Tinggi Terhadap Diabetes")
    st.write("Berdasarkan data yang **dideteksi** oleh model, berikut adalah beberapa insight terkait atribut yang memiliki keterkaitan paling kuat dengan status diabetes:") # Teks diubah

    # --- Fungsi Pembantu untuk Analisis Numerik ---
    def analyze_numeric_attribute(df, attribute_name, display_name, unit=''):
        st.markdown(f"#### Analisis {display_name}")
        if attribute_name in df.columns and 'y_pred' in df.columns:
            attr_diabetes = df[df['y_pred'] == 1][attribute_name]
            attr_non_diabetes = df[df['y_pred'] == 0][attribute_name]

            st.write(f"Rata-rata {display_name} pasien yang **dideteksi** diabetes: **{attr_diabetes.mean():.2f}{unit}**") # Teks diubah
            st.write(f"Rata-rata {display_name} pasien yang **dideteksi** non-diabetes: **{attr_non_diabetes.mean():.2f}{unit}**") # Teks diubah

            if attr_diabetes.mean() > attr_non_diabetes.mean():
                st.markdown(f"**Kesimpulan**: Pasien dengan nilai **{display_name} yang lebih tinggi** cenderung memiliki risiko lebih tinggi untuk **dideteksi** menderita diabetes.") # Teks diubah
            elif attr_diabetes.mean() < attr_non_diabetes.mean():
                st.markdown(f"**Kesimpulan**: Pasien dengan nilai **{display_name} yang lebih rendah** cenderung memiliki risiko lebih tinggi untuk **dideteksi** menderita diabetes.") # Teks diubah
            else:
                st.markdown(f"**Kesimpulan**: Dalam konteks data ini, nilai {display_name} tidak menunjukkan perbedaan rata-rata yang signifikan antara kelompok diabetes dan non-diabetes (**deteksi**).") # Teks diubah
        else:
            st.warning(f"Kolom '{attribute_name}' atau 'y_pred' tidak ditemukan untuk analisis {display_name}.")

    # --- Analisis Gender ---
    st.markdown("#### Analisis Gender")
    # Asumsi: 0 = Female (Perempuan), 1 = Male (Laki-laki)
    # Sesuaikan mapping ini jika encoding Anda berbeda!
    gender_mapping = {0: 'Perempuan', 1: 'Laki-laki'}
    
    # Membuat salinan agar tidak mengubah DataFrame asli jika tidak diinginkan
    df_analysis = hasil_predeksi.copy()
    
    # Pastikan kolom 'Gender' ada sebelum mapping
    if 'Gender' in df_analysis.columns:
        df_analysis['Gender_Label'] = df_analysis['Gender'].map(gender_mapping)

        # Hitung jumlah pasien diabetes (y_pred=1) per gender
        gender_diabetes_counts = df_analysis.groupby('Gender_Label')['y_pred'].sum().reset_index()
        # Hitung total individu per gender
        gender_total_counts = df_analysis.groupby('Gender_Label').size().reset_index(name='Total')
        
        # Gabungkan kedua DataFrame
        gender_analysis_df = pd.merge(gender_diabetes_counts, gender_total_counts, on='Gender_Label')
        
        # Hitung persentase diabetes per gender
        gender_analysis_df['Persentase Diabetes'] = (gender_analysis_df['y_pred'] / gender_analysis_df['Total'] * 100).round(2)

        st.write("Jumlah kasus diabetes (**deteksi**) dan persentasenya berdasarkan Gender:") # Teks diubah
        st.dataframe(gender_analysis_df.rename(columns={'y_pred': 'Jumlah Pasien Diabetes (**Deteksi**)'})) # Teks diubah

        if not gender_analysis_df.empty:
            # Temukan gender dengan persentase diabetes tertinggi
            most_affected_gender = gender_analysis_df.loc[gender_analysis_df['Persentase Diabetes'].idxmax()]
            st.markdown(f"**Kesimpulan**: Dari data yang **dideteksi**, **{most_affected_gender['Gender_Label']}** menunjukkan persentase kasus diabetes (**deteksi**) yang paling tinggi, yaitu **{most_affected_gender['Persentase Diabetes']}%** dari total individu dengan gender tersebut dalam dataset ini.") # Teks diubah
    else:
        st.warning("Kolom 'Gender' tidak ditemukan dalam data hasil **deteksi** untuk analisis gender.") # Teks diubah

    # --- Analisis Atribut Numerik Lainnya ---
    analyze_numeric_attribute(df_analysis, 'AGE', 'Usia', ' tahun')
    analyze_numeric_attribute(df_analysis, 'Urea', 'Rasio Urea')
    analyze_numeric_attribute(df_analysis, 'Cr', 'Rasio Kreatinin (Cr)')
    analyze_numeric_attribute(df_analysis, 'HbA1c', 'Rasio HbA1c')
    analyze_numeric_attribute(df_analysis, 'Chol', 'Rasio Kolesterol')
    analyze_numeric_attribute(df_analysis, 'TG', 'Rasio Trigliserida (TG)')
    analyze_numeric_attribute(df_analysis, 'HDL', 'Rasio HDL')
    analyze_numeric_attribute(df_analysis, 'LDL', 'Rasio LDL')
    analyze_numeric_attribute(df_analysis, 'VLDL', 'Rasio VLDL')
    analyze_numeric_attribute(df_analysis, 'BMI', 'Rasio BMI')


    # --- Bagian Visualisasi (Opsional) ---
    st.markdown("#### Visualisasi Distribusi Atribut")
    st.write("Anda dapat melihat distribusi atribut utama berdasarkan status diabetes yang **dideteksi**:") # Teks diubah

    # Fungsi Pembantu untuk Visualisasi Numerik
    def plot_numeric_distribution(df, attribute_name, display_name, plot_type='box'):
        if attribute_name in df.columns and 'y_pred' in df.columns:
            if st.checkbox(f"Tampilkan Visualisasi Distribusi {display_name} Berdasarkan **Deteksi** ({plot_type.capitalize()})", key=f"plot_{attribute_name}_{plot_type}"): # Teks diubah
                if plot_type == 'box':
                    fig = px.box(df, x='y_pred', y=attribute_name,
                                 title=f'Distribusi {display_name} berdasarkan Status Diabetes (**Deteksi**)', # Teks diubah
                                 labels={'y_pred': 'Status Diabetes (0=Non, 1=Diabetes)', attribute_name: display_name},
                                 color='y_pred',
                                 color_discrete_map={0: 'blue', 1: 'red'})
                elif plot_type == 'histogram':
                    fig = px.histogram(df, x=attribute_name, color='y_pred',
                                       title=f'Distribusi {display_name} berdasarkan Status Diabetes (**Deteksi**)', # Teks diubah
                                       labels={'y_pred': 'Status Diabetes (0=Non, 1=Diabetes)', attribute_name: display_name},
                                       barmode='overlay', # Untuk menumpuk bar
                                       histnorm='probability density', # Untuk melihat distribusi relatif
                                       color_discrete_map={0: 'blue', 1: 'red'})
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"Tidak dapat membuat visualisasi {display_name} karena kolom yang dibutuhkan tidak ada.")

    # Panggilan untuk Visualisasi Atribut Numerik
    plot_numeric_distribution(df_analysis, 'AGE', 'Usia', 'histogram')
    plot_numeric_distribution(df_analysis, 'Urea', 'Rasio Urea', 'box')
    plot_numeric_distribution(df_analysis, 'Cr', 'Rasio Kreatinin (Cr)', 'box')
    plot_numeric_distribution(df_analysis, 'HbA1c', 'Rasio HbA1c', 'box')
    plot_numeric_distribution(df_analysis, 'Chol', 'Rasio Kolesterol', 'box')
    plot_numeric_distribution(df_analysis, 'TG', 'Rasio Trigliserida (TG)', 'box')
    plot_numeric_distribution(df_analysis, 'HDL', 'Rasio HDL', 'box')
    plot_numeric_distribution(df_analysis, 'LDL', 'Rasio LDL', 'box')
    plot_numeric_distribution(df_analysis, 'VLDL', 'Rasio VLDL', 'box')
    plot_numeric_distribution(df_analysis, 'BMI', 'Rasio BMI', 'box')