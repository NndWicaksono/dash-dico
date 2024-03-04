import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# URL file CSV di GitHub
url = 'https://raw.githubusercontent.com/NndWicaksono/Submission/main/Dashboard/main_data.csv'

# Membaca file CSV dari URL
main_df = pd.read_csv(url)

# Menambahkan Judul
st.title('Dashboard Bike Sharing :bike:')

# Menambahkan Subheader
st.subheader('selamat datang di dashboard')

# Mendeskripsikan kategori
season_names = {1: 'springer', 2: 'summer', 3: 'fall', 4: 'winter'}
main_df['season'] = main_df['season'].map(season_names)

# Membuat Sidebar Rentang Waktu
datetime_columns = ['dteday']
main_df.sort_values(by='dteday', inplace=True)
main_df.reset_index(inplace=True)
 
for column in datetime_columns:
    main_df[column] = pd.to_datetime(main_df[column])

min_date = main_df['dteday'].min()
max_date = main_df['dteday'].max()
 
with st.sidebar:  
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filtered_data = main_df[(main_df['dteday'] >= start_date) & (main_df['dteday'] <= end_date)]

# Membuat Sidebar Selected Data
with st.sidebar:
    # Menggunakan selectbox untuk memilih jenis data
    selected_data = st.selectbox(
        label='Pilih data yang dibutuhkan',
        options=['casual', 'registered', 'cnt']
    )
    st.write('Selected data:', selected_data)

# Membuat tab
tab1, tab2= st.tabs(["Deskripsi Statistik", "Pola Runtun Waktu"])

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        # Metric 1 total
        total_sharing = filtered_data[selected_data].sum()
        st.metric("Total Peminjam {}".format(selected_data), value="{:,.0f}".format(total_sharing))
    with col2:
        # Metric 2 Mean
        mean_sharing = filtered_data[selected_data].mean()
        st.metric("Rata-Rata Peminjam {}/Hari".format(selected_data), value="{:,.0f}".format(mean_sharing))
    with col3:
        # Metric 3 Standar Deviasi
        std_sharing = filtered_data[selected_data].std()
        st.metric("Standar Deviasi Peminjam {}".format(selected_data), value="{:,.0f}".format(std_sharing))


with tab2:
    # Menampilkan line plot Peminjaman Sepeda berdasar waktu
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_title("Line Plot Peminjam {} dari {} hingga {}".format(selected_data, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')), loc="center", fontsize=50)
    ax.plot(
        filtered_data['dteday'],
        filtered_data[selected_data],
        marker='o', 
        linewidth=2,
        color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
 
    st.pyplot(fig)