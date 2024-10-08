# -*- coding: utf-8 -*-
"""notebook.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1OaZaWK7vQsuLyyifyJXD_lz_RPm7I8y-

# Proyek Analisis Data : Bike Sharing
- **Nama:** Azzah Nabila Herdy
- **Email:** azzah8872@gmail.com/m246b4kx0778@bangkit.academy
- **ID Dicoding:** azzah2304

## Menentukan Pertanyaan Bisnis

- Paling banyak sepeda disewa pada jam berapa dalam sehari?
- Hari apa yang menunjukkan jumlah penyewaan sepeda tertinggi dalam seminggu?
- Apakah ada perbedaan besar dalam penyewaan sepeda antara weekday dan weekend?

## Import Semua Packages/Library yang Digunakan
"""

pip install numpy pandas scipy matplotlib seaborn jupyter

"""## Data Wrangling

### Gathering Data
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Tabel hari
day_df = pd.read_csv("https://raw.githubusercontent.com/Azzah2323/projek/refs/heads/main/data/day.csv")
day_df.head()

# Tabel jam
hour_df = pd.read_csv("https://raw.githubusercontent.com/Azzah2323/projek/refs/heads/main/data/hour.csv")
hour_df.head()

combined_df = pd.merge(hour_df, day_df, on=['dteday', 'season', 'yr', 'mnth', 'weekday', 'holiday', 'workingday', 'weathersit'], suffixes=('_hour', '_day'))

print("\nStatistical summary of the combined dataset:")
print(combined_df.describe())

combined_df['weekend'] = combined_df['weekday'].apply(lambda x: 1 if x == 0 or x == 6 else 0)

"""**Insight:**
- Membuat empat tabel dari sebuah dataset yang diperoleh dari repository
- Ada dua dataset yaitu day dan hour
- Tahap ini yaitu membuat tabel yaitu guna mengumpulkan dan mempersiapkan data sebelum dilakukan analisis lebih lanjut.
- Mendapatkan data lengkap yang akan memudahkan untuk langkah analisis berikutnya

### Assessing Data
"""

# Menilai data day
day_df.info()
day_df.isna().sum()
print("Jumlah duplikasi: ", day_df.duplicated().sum())
day_df.describe()

print(day_df[['season', 'weathersit', 'holiday', 'workingday']].nunique())
print(day_df[['season', 'weathersit', 'holiday', 'workingday']].drop_duplicates())

day_df.isna().sum()

# Menilai data hour
hour_df.info()
hour_df.isna().sum()
print("Jumlah duplikasi: ", hour_df.duplicated().sum())
hour_df.describe()

print(hour_df[['temp', 'hum', 'windspeed']].describe())

hour_df.isna().sum()

"""**Insight:**
- Menilai data yang telah diperoleh dari proses data wrangling
- Terdapat format data yang tidak sesuai, hal ini harus diperbaiki agar sesuai dengan ketentuan
- Penilaian dilakukan untuk mengetahui apakah ada data yang tidak sesuai. Terdapat pengecekan duplikasi, missing value, tipe data dan pengecekan kesalahan input data
- Penggunaan file CSV yang digunakan pada dataset dan URL eksternal yang digunakan untuk mempermudah memperoleh data yang lebih besar dan terstruktur

### Cleaning Data
"""

# Membersihkan data day
# Mengubah tipe data dteday

day_df['dteday'] = pd.to_datetime(day_df['dteday'], format='%Y-%m-%d', errors='coerce')

print(day_df.dtypes)

# Membersihkan data hour
# Mengubah tipe data dteday

hour_df['dteday'] = pd.to_datetime(hour_df['dteday'], format='%Y-%m-%d', errors='coerce')

print(hour_df.dtypes)

combined_df = pd.merge(hour_df, day_df, on=['dteday', 'season', 'yr', 'mnth', 'weekday', 'holiday', 'workingday', 'weathersit'], suffixes=('_hour', '_day'))

combined_df['weekend'] = combined_df['weekday'].apply(lambda x: 1 if x == 0 or x == 6 else 0)

"""**Insight:**
- Setelah data di assessment tahap selanjutnya yaitu data cleaning dimana pada tahap ini data diperiksa apakan ada kesalahan input data dan sebagainya
- Tidak ada duplikasi yang terjadi pada data diatas
- Terdapat format data yang tidak sesuai, hal ini harus diperbaiki agar sesuai dengan ketentuan

## Exploratory Data Analysis (EDA)

### Explore data day
"""

day_df.describe(include="all")

hour_df.describe(include="all")

hourly_rentals = combined_df.groupby('hr')['cnt_hour'].mean()

# Penyewa terbanyak
max_rentals_hour = hourly_rentals.idxmax()
print("Hour with the most bike rentals: ", max_rentals_hour)

# Penyewa dalam seminggu
weekday_rentals = combined_df.groupby('weekday')['cnt_hour'].mean()

# Display the result
print("\nAverage bike rentals by day of the week:")
print(weekday_rentals)

# Hari terbanya penyewa dalam seminggu
max_rentals_day = weekday_rentals.idxmax()
weekday_names = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
print(f"Hari dengan penyewaan sepeda tertinggi: {weekday_names[max_rentals_day]}")

weekend_rentals = combined_df.groupby('weekend')['cnt_hour'].mean()
print("\nRata-rata penyewaan sepeda:")
print(f"Rata-rata penyewaan pada hari kerja: {weekend_rentals[0]}")
print(f"Rata-rata penyewaan pada akhir pekan: {weekend_rentals[1]}")

"""Eksplorasi data all"""

all_df = pd.merge(left=day_df, right=hour_df, how='inner', left_on='dteday', right_on='dteday')
all_df.head()

"""**Insight:**
- Memahami struktur data yang terdapat pada masing-masing tabel, karena setiap tabel memiliki struktur dan karakteristik yang berbeda
- Mendapatkan gambaran distribusi nilai setiap kolom dengan melakukan statistik describe
- Mengdistribusikan variabel kategori untuk menganalisis tabel berdasarkan kategori

## Visualization & Explanatory Analysis

### Pertanyaan 1: Paling banyak sepeda disewa pada jam berapa dalam sehari?
"""

hourly_rentals = combined_df.groupby('hr')['cnt_hour'].mean()

# Visualisasi penyewaan sepeda berdasarkan jam dalam sehari
plt.figure(figsize=(10, 6))
plt.plot(hourly_rentals.index, hourly_rentals.values, marker='o', linestyle='-', color='purple', label='Penyewaan per Jam')
plt.title('Penyewaan Sepeda Berdasarkan Jam dalam Sehari', fontsize=14)
plt.xlabel('Jam dalam Sehari (0-23)', fontsize=12)
plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
plt.xticks(ticks=range(0, 24), labels=[str(i) for i in range(0, 24)])
plt.grid(True)
plt.legend()

# Tampilkan visualisasi
plt.show()

# Menemukan jam dengan penyewaan tertinggi
max_hour = hourly_rentals.idxmax()
max_hour_rentals = hourly_rentals.max()

print(f"Jam dengan penyewaan tertinggi adalah jam {max_hour} dengan total {max_hour_rentals} penyewaan.")

"""### Pertanyaan 2: Paling banyak sepeda disewa perhari dalam seminggu?"""

weekday_rentals = all_df.groupby('weekday_y')['cnt_y'].sum()
plt.figure(figsize=(10, 6))
plt.plot(weekday_rentals.index, weekday_rentals.values, marker='o', linestyle='-', color='b', label='Penyewaan per Hari')
plt.title('Penyewaan Sepeda Berdasarkan Hari dalam Seminggu', fontsize=14)
plt.xlabel('Hari dalam Seminggu (0 = Minggu, 6 = Sabtu)', fontsize=12)
plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
plt.xticks(ticks=range(7), labels=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
plt.grid(True)
plt.legend()
plt.show()

"""### Pertanyaan 3: - Apakah ada perbedaan besar dalam penyewaan sepeda antara weekday dan weekend?"""

weekday_vs_weekend = all_df.groupby('workingday_y')['cnt_y'].sum()
plt.figure(figsize=(10, 6))
plt.bar(['Weekend', 'Weekday'], weekday_vs_weekend.values, color=['orange', 'green'])
plt.title('Penyewaan Sepeda: Weekday vs Weekend', fontsize=14)
plt.xlabel('Jenis Hari', fontsize=12)
plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
plt.grid(True)

"""**Insight:**
- Setelah dilakukan visualisasi menjadi legih mudah melihat dan menjawab pertanyaan
- Mengidentifikasi jumlah penyewaan sepeda dalam sehari
- Mengidentifikasikan sepeda yang disewa perhari dalam seminggu
- Mengidentifikasikan perbedaan sewa antara weekdays dan weekend

## Conclusion

#Conclusion pertanyaan 1
Jumlah sepeda paling banyak diewa yaitu pada jam 17.00 . hal ini menunjukkan puncak penyewaan sepeda yang kemungkinan besar terkait dengan kegiatan harian seperti pulang sekolah maupun bekerja, ataupun untuk olahraga sore

#Conclusion pertanyaan 2
 Berdasarkan analisis jumlah penyewaan sepeda per hari dalam seminggu, hari dengan jumlah penyewaan sepeda tertinggi adalah hari Jumat. Hal ini mungkin menunjukkan bahwa pada hari Jumat dan Sabtu, banyak orang menggunakan sepeda untuk aktivitas akhir pekan, baik untuk perjalanan ke tempat kerja atau rekreasi.

 # Conclusion pertanyaan 3
Hasil analisis menunjukkan bahwa jumlah penyewaan sepeda cenderung lebih tinggi pada weekend dibandingkan dengan weekdays. Ini dapat dijelaskan oleh meningkatnya aktivitas rekreasi di kalangan masyarakat pada saat akhir pekan, di mana banyak orang memanfaatkan waktu luang mereka untuk berolahraga, bersantai, atau berkumpul dengan teman-teman.
"""

all_df.to_csv("all_data.csv", index=False)