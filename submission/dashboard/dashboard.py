import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Memuat dataset
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Menggabungkan tabel day_df dan hour_df
day_hour_df = pd.merge(
    left=hour_df,
    right=day_df,
    how="outer",
    on="dteday",  # Menggabungkan berdasarkan kolom 'dteday'
    suffixes=('_hour', '_day')
)

day_hour_df['workingday'] = day_df['workingday']

# Cuaca dan Musim
# Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Dicoding Bike Sharing Dataset')
st.subheader("Pengaruh Cuaca terhadap Pengguna Kasual dan Terdaftar di Berbagai Musim")

weather_season_grouped = day_df.groupby(by=["season", "weathersit"]).agg({
    "casual": "mean",
    "registered": "mean"
}).reset_index()

season_mapping = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"}
weather_season_grouped['season'] = weather_season_grouped['season'].map(season_mapping)

# Pengaruh Cuaca pada Pengguna Kasual 
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="season", y="casual", hue="weathersit", data=weather_season_grouped, palette="Blues_d", ax=ax, saturation=0.8)
ax.set_title("Pengaruh Cuaca Terhadap Pengguna Sepeda Kasual di Berbagai Musim")
ax.set_ylabel("Rata-Rata Pengguna Kasual")
ax.set_xlabel("Musim")
plt.legend(title="Kondisi Cuaca")
st.pyplot(fig)

# Insight tentang Pengguna Kasual
st.write("""
**Insight Pengguna Kasual:**

- **Musim Panas** dan **Musim Gugur** menunjukkan jumlah pengguna kasual tertinggi, terutama ketika cuaca baik (kondisi cuaca = 1: Cerah, Sedikit Awan). Ini mengindikasikan bahwa pengguna kasual lebih mungkin menyewa sepeda saat cuaca mendukung, terutama di musim yang lebih hangat.
- Di **Musim Dingin**, jumlah pengguna kasual menurun drastis. Ketika cuaca buruk (kondisi cuaca = 3: Hujan ringan, Salju ringan), penggunaan sepeda oleh pengguna kasual sangat sedikit. Ini menunjukkan bahwa cuaca dingin dan buruk sangat mempengaruhi keputusan pengguna kasual untuk menggunakan sepeda.
- Secara keseluruhan, pengguna kasual sangat sensitif terhadap perubahan cuaca dan musim, lebih cenderung menyewa sepeda di musim panas dan gugur, dengan penurunan tajam di musim dingin dan kondisi cuaca buruk.
""")

# Pengaruh Cuaca pada Pengguna Terdaftar
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="season", y="registered", hue="weathersit", data=weather_season_grouped, palette="Greens_d")
ax.set_title("Pengaruh Cuaca Terhadap Pengguna Sepeda Terdaftar di Berbagai Musim")
ax.set_ylabel("Rata-Rata Pengguna Terdaftar")
ax.set_xlabel("Musim")
plt.legend(title="Kondisi Cuaca")
st.pyplot(fig)

# Insight tentang Pengguna Terdaftar
st.write("""
**Insight Pengguna Terdaftar:**

- Pengguna terdaftar menunjukkan pola yang lebih stabil dibandingkan dengan pengguna kasual, tetapi tetap terdapat penurunan jumlah penyewaan di **Musim Dingin** dan saat cuaca buruk. Namun, penurunan ini tidak se-drastis pengguna kasual.
- Pengguna terdaftar lebih mungkin untuk terus menggunakan layanan sepeda bahkan saat kondisi cuaca tidak ideal, terutama di **Musim Panas** dan **Musim Gugur**. Hal ini menunjukkan bahwa pengguna terdaftar mungkin menggunakan sepeda untuk perjalanan rutin seperti bekerja atau kegiatan sehari-hari, yang membuat mereka lebih konsisten.
- Walaupun jumlah penyewaan menurun pada cuaca buruk, pengguna terdaftar masih lebih aktif dibandingkan pengguna kasual, menunjukkan bahwa mereka mungkin memiliki motivasi yang lebih kuat (misalnya, komitmen berlangganan, transportasi harian).
""")

# Mengganti nilai workingday dari 0 dan 1 menjadi label yang lebih deskriptif
day_df['workingday'] = day_df['workingday'].map({1: "Hari Kerja", 0: "Bukan Hari Kerja"})

workingday_grouped = day_df.groupby(by="workingday").agg({
    "casual": "mean",
    "registered": "mean"
}).reset_index()

# Plotting
plt.figure(figsize=(12, 6))

# Subplot untuk hari kerja vs bukan hari kerja
plt.subplot(1, 2, 1)
sns.barplot(x="workingday", y="casual", data=workingday_grouped, color="blue", label="Casual")
sns.barplot(x="workingday", y="registered", data=workingday_grouped, color="green", alpha=0.6, label="Registered")
plt.title("Penggunaan Sepeda pada Hari Kerja vs Bukan Hari Kerja")
plt.xlabel("Jenis Hari")
plt.ylabel("Rata-rata Pengguna Sepeda")
plt.legend()


plt.tight_layout()

st.pyplot(plt)

# Insight 
st.write("""
**Insight Penggunaan Sepeda pada Hari Kerja vs Bukan Hari Kerja:**

- **Pengguna Kasual**: Lebih banyak menggunakan sepeda pada hari bukan kerja (akhir pekan) dibandingkan dengan hari kerja. Ini menunjukkan bahwa pengguna kasual cenderung menggunakan sepeda untuk rekreasi atau kegiatan santai selama akhir pekan.
- **Pengguna Terdaftar**: Lebih aktif pada hari kerja, menunjukkan bahwa mereka lebih sering menggunakan sepeda untuk keperluan transportasi harian seperti pergi bekerja atau kegiatan rutin.
""")

# Mengganti nilai holiday dari 0 dan 1 menjadi label yang lebih deskriptif
day_df['holiday'] = day_df['holiday'].map({1: "Hari Libur", 0: "Bukan Hari Libur"})


holiday_grouped = day_df.groupby(by="holiday").agg({
    "casual": "mean",
    "registered": "mean"
}).reset_index()

# Plotting
plt.figure(figsize=(12, 6))

# Subplot untuk hari libur vs bukan hari libur
plt.subplot(1, 2, 2)
sns.barplot(x="holiday", y="casual", data=holiday_grouped, color="blue", label="Casual")
sns.barplot(x="holiday", y="registered", data=holiday_grouped, color="green", alpha=0.6, label="Registered")
plt.title("Penggunaan Sepeda pada Hari Libur vs Bukan Hari Libur")
plt.xlabel("Jenis Hari")
plt.ylabel("Rata-rata Pengguna Sepeda")
plt.legend()


plt.tight_layout()

st.pyplot(plt)

# Insight 
st.write("""
**Insight Penggunaan Sepeda pada Hari Libur vs Bukan Hari Libur:**

- **Pengguna Kasual**: Jelas lebih banyak pengguna kasual yang menyewa sepeda pada hari libur, menunjukkan bahwa pengguna kasual memanfaatkan hari libur untuk aktivitas rekreasi.
- **Pengguna Terdaftar**: Tidak ada perubahan signifikan antara hari libur dan bukan hari libur untuk pengguna terdaftar, yang menunjukkan pola penggunaan yang lebih stabil.
""")

# Menghitung Recency: Jumlah hari sejak terakhir kali menyewa sepeda
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
reference_date = day_df['dteday'].max()  # Mengambil tanggal terakhir di dataset
day_df['recency'] = (reference_date - day_df['dteday']).dt.days

# RFM
rfm_data = day_df.groupby(['workingday']).agg({
    'recency': 'min',  # Mengambil nilai recency terendah
    'casual': 'sum',   # Total pengguna kasual sebagai Frequency
    'registered': 'sum'  # Total pengguna terdaftar sebagai Frequency
}).reset_index()

# Menambahkan kolom Monetary: Total jumlah pengguna sebagai representasi monetari
rfm_data['monetary_casual'] = day_df.groupby('workingday')['casual'].sum().values
rfm_data['monetary_registered'] = day_df.groupby('workingday')['registered'].sum().values

# Visualisasi seperti yang diinginkan
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

# Barplot berdasarkan Recency
sns.barplot(y="recency", x="workingday", data=rfm_data.sort_values(by="recency", ascending=True), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis='x', labelsize=15)

# Barplot berdasarkan Frequency (Pengguna Kasual)
sns.barplot(y="casual", x="workingday", data=rfm_data.sort_values(by="casual", ascending=False), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency (Casual Users)", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)

# Barplot berdasarkan Monetary (Pengguna Terdaftar)
sns.barplot(y="registered", x="workingday", data=rfm_data.sort_values(by="registered", ascending=False), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary (Registered Users)", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15)

plt.suptitle("Penggunaan Terbaik Berdasarkan Parameter RFM (hari kerja)", fontsize=20)
st.pyplot(fig)

st.write("""
### Insight dari Analisis RFM:

- **Recency (Penggunaan Terbaru)**: 
  Hari bukan kerja cenderung memiliki recency yang lebih tinggi, yang berarti pengguna sepeda (terutama pengguna kasual) cenderung tidak aktif di hari kerja dibandingkan pada hari libur atau akhir pekan. Pengguna terdaftar lebih konsisten dalam menggunakan sepeda di hari kerja, dengan frekuensi penggunaan yang lebih stabil meskipun cuaca atau kondisi tertentu berubah.
  
- **Frequency (Frekuensi Pengguna Kasual)**: 
  Pengguna kasual lebih sering menggunakan sepeda pada hari bukan kerja (akhir pekan), yang menunjukkan pola penggunaan yang terkait dengan aktivitas rekreasi. Pengguna kasual cenderung menyewa sepeda lebih banyak pada akhir pekan untuk bersenang-senang atau jalan-jalan.
  
- **Monetary (Pengguna Terdaftar)**: 
  Pengguna terdaftar lebih sering menggunakan sepeda pada hari kerja. Ini menunjukkan bahwa sepeda digunakan oleh pengguna terdaftar sebagai sarana transportasi sehari-hari, misalnya untuk pergi bekerja atau beraktivitas rutin.
""")

# Kesimpulan
st.write("""
### Conclusion:

#### Bagaimana Pengaruh Cuaca terhadap Jumlah Pengguna Sepeda Kasual dan Terdaftar di Berbagai Musim?

- **Pengguna Kasual**: Pengguna kasual lebih sensitif terhadap cuaca dan musim. Jumlah pengguna kasual meningkat secara signifikan pada cuaca yang cerah dan kondisi baik, terutama di Musim Panas dan Musim Gugur. Sebaliknya, pada Musim Dingin dan saat cuaca buruk (misalnya, hujan atau salju ringan), pengguna kasual berkurang drastis.

- **Pengguna Terdaftar**: Pengguna terdaftar lebih stabil dalam penggunaan sepeda sepanjang tahun. Meskipun cuaca buruk dan musim dingin mempengaruhi mereka, pengurangan jumlah pengguna tidak se-drastis pengguna kasual. Pengguna terdaftar lebih mungkin menggunakan sepeda untuk keperluan transportasi harian seperti bekerja, sehingga mereka tidak terlalu terpengaruh oleh cuaca dibandingkan pengguna kasual.

- **Kesimpulan Utama**: Cuaca baik dan musim hangat (Musim Panas dan Musim Gugur) mendorong lebih banyak penggunaan sepeda, terutama oleh pengguna kasual. Musim Dingin dan cuaca buruk berdampak signifikan pada penurunan jumlah pengguna kasual, sementara pengguna terdaftar lebih cenderung tetap aktif meskipun dengan sedikit penurunan.

#### Apakah Terdapat Pola Penggunaan Sepeda yang Signifikan antara Hari Kerja dan Hari Libur?

- **Pengguna Kasual**: Pengguna kasual lebih aktif pada hari bukan kerja (akhir pekan) dan hari libur. Hal ini menunjukkan bahwa pengguna kasual menggunakan sepeda terutama untuk aktivitas rekreasi dan santai, yang biasanya dilakukan pada waktu luang.

- **Pengguna Terdaftar**: Pengguna terdaftar lebih aktif pada hari kerja dibandingkan hari libur atau akhir pekan. Ini menunjukkan bahwa sepeda lebih sering digunakan sebagai alat transportasi untuk keperluan harian, seperti pergi bekerja atau kegiatan rutin lainnya. Perbedaan antara hari kerja dan hari libur tidak signifikan bagi mereka.

- **Kesimpulan Utama**: Pengguna kasual lebih aktif di akhir pekan dan hari libur, yang menunjukkan bahwa penggunaan sepeda oleh mereka lebih terkait dengan rekreasi. Pengguna terdaftar lebih sering menggunakan sepeda di hari kerja, yang menunjukkan bahwa mereka menggunakan sepeda sebagai alat transportasi harian.
""")

#streamlit run dashboard.py
