import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Judul Dashboard
st.title("Analisis Penyewaan Sepeda")

# Memuat data
hour_data = pd.read_csv(r'C:\Data Sicience\Submission\data\hour.csv')
day_data = pd.read_csv(r'C:\Data Sicience\Submission\data\day.csv')

# Pilihan untuk memilih analisis per jam atau per hari
data_option = st.selectbox('Pilih Analisis Berdasarkan', ['Per Jam', 'Per Hari'])

if data_option == 'Per Jam':
    fig, ax = plt.subplots()
    sns.boxplot(x='season', y='cnt', data=hour_data, ax=ax)
    ax.set_title('Penyewaan Sepeda per Jam berdasarkan Musim')
    st.pyplot(fig)
    
elif data_option == 'Per Hari':
    fig, ax = plt.subplots()
    sns.boxplot(x='season', y='cnt', data=day_data, ax=ax)
    ax.set_title('Penyewaan Sepeda per Hari berdasarkan Musim')
    st.pyplot(fig)