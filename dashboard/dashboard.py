import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='dark')

# Load dataset
hour_df = pd.read_csv("hour_data.csv")
day_df = pd.read_csv("day_data.csv")

# Konversi kolom tanggal
if 'dteday' in hour_df.columns:
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

if 'dteday' in day_df.columns:
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])

if "selected_section" not in st.session_state:
    st.session_state["selected_section"] = "About Dataset"

# Sidebar Menu Navigasi dengan Button
st.sidebar.image("https://raw.githubusercontent.com/DumaSitorus/Bike-Sharing-Dashboard/main/dashboard/st_logo.png")
selected_section = st.session_state.get("selected_section", "About Dataset")

if st.sidebar.button("📊 About Dataset"):
    st.session_state["selected_section"] = "About Dataset"
if st.sidebar.button("🚴 Penyewaan Sepeda Harian"):
    st.session_state["selected_section"] = "Penyewaan Sepeda Harian"
if st.sidebar.button("📈 Visualisasi & Eksplanatory Analysis"):
    st.session_state["selected_section"] = "Visualisasi & Eksplanatory Analysis"
if st.sidebar.button("🔍 Analisis Lanjutan"):
    st.session_state["selected_section"] = "Analisis Lanjutan"

selected_section = st.session_state["selected_section"]

# ===================================================
# SECTION 1: About Dataset
# ===================================================
if selected_section == "About Dataset":
    st.title("📊 About Dataset")
    st.write(
        "Dataset ini berisi data historis penyewaan sepeda dari Capital Bikeshare System di Washington D.C., USA, yang mencakup periode tahun 2011 dan 2012. Data ini mencatat jumlah penyewaan sepeda berdasarkan berbagai faktor lingkungan dan waktu."
    )
    st.header("1. Data per Jam")
    st.dataframe(hour_df.head(10))

    st.subheader("✨Statistik Deskriptif per Jam")
    st.write(hour_df.describe())

    st.header("2. Data per Hari")
    st.dataframe(day_df.head(10))

    st.subheader("✨Statistik Deskriptif per Hari")
    st.write(hour_df.describe())
    st.markdown("""
                **✨Kolom utama dalam dataset ini meliputi:**
                - instant: record index
                - dteday : tanggal
                - season : musim (1:springer, 2:summer, 3:fall, 4:winter)
                - yr : tahun (0: 2011, 1:2012)
                - mnth : bulan ( 1 to 12)
                - hr : jam (0 to 23)
                - holiday : hari libur berdasarkan jadwal libur berikut: http://dchr.dc.gov/page/holiday-schedule
                - weekday : hari dalam pekan
                - workingday : jika bukan akhir pekan dan hari libut maka bernilai 1,selainnya bernilai 0.
                - weathersit : 
                    + 1: Cerah, Sedikit awan, Berawan sebagian, Berawan sebagian
                    + 2: Kabut + Berawan, Kabut + Awan pecah, Kabut + Sedikit awan, Kabut
                    + 3: Salju Ringan, Hujan Ringan + Badai Petir + Awan tersebar, HujanRingan + Awan tersebar
                    + 4: Hujan Lebat + Es + Badai Petir + Kabut, Salju + Kabut
                - temp: Suhu yang dinormalkan dalam Celcius. Nilai dibagi menjadi 41 (maks)
                - atemp: Suhu yang dinormalkan dalam Celcius. Nilai dibagi menjadi 50 (maks)
                - hum: Kelembapan yang dinormalkan. Nilai dibagi menjadi 100 (maks)
                - windspeed: Kecepatan angin yang dinormalkan. Nilai dibagi menjadi 67 (maks)
                - casual: jumlah pengguna kasual
                - registered: jumlah pengguna terdaftar
                - cnt: jumlah total sepeda sewaan termasuk kasual dan terdaftar
    """)

# ===================================================
# SECTION 2: Penyewaan Sepeda Harian
# ===================================================
elif selected_section == "Penyewaan Sepeda Harian":
    st.title("🚴 Penyewaan Sepeda Harian")

    st.sidebar.header("Filter Tanggal")
    min_date = hour_df['dteday'].min()
    max_date = hour_df['dteday'].max()
    selected_date = st.sidebar.date_input("Pilih Tanggal", min_value=min_date, max_value=max_date, value=min_date)

    filtered_df = hour_df[hour_df['dteday'] == pd.Timestamp(selected_date)]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Penyewaan", filtered_df['cnt'].sum())
    with col2:
        st.metric("Casual Users", filtered_df['casual'].sum())
    with col3:
        st.metric("Registered Users", filtered_df['registered'].sum())

    st.subheader("📈 Penyewaan Sepeda per Jam")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=filtered_df['hr'], y=filtered_df['cnt'], marker='o', ax=ax)
    ax.set_title("Jumlah Penyewaan Sepeda per Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.set_xticks(range(0, 24))
    ax.grid("true")
    st.pyplot(fig)

# ===================================================
# SECTION 3: Visualisasi & Eksplanatory Analysis
# ===================================================
elif selected_section == "Visualisasi & Eksplanatory Analysis":
    st.title("📊 Visualisasi & Eksplanatory Analysis")

    # ANALISIS 1: Penyewaan Sepeda Berdasarkan Hari dan Jam
    st.subheader("1. Pada jam berapa dan hari apa jumlah penyewaan sepeda paling tinggi dan paling rendah?")

    # Rata-rata penyewaan per hari
    weekday_avg = day_df.groupby("weekday")["cnt"].mean().reset_index()
    weekday_labels = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 
                      4: "Thursday", 5: "Friday", 6: "Saturday"}
    weekday_avg["weekday"] = weekday_avg["weekday"].map(weekday_labels)

    # Rata-rata penyewaan per jam
    hourly_avg = hour_df.groupby("hr")["cnt"].mean().reset_index()

    # Buat figure dan subplot
    fig, axes = plt.subplots(1, 2, figsize=(15,5))

    # Grafik 1: Penyewaan sepeda per hari
    sns.barplot(ax=axes[0], x="weekday", y="cnt", data=weekday_avg, palette="magma")
    axes[0].set_title("Rata-rata Penyewaan Sepeda per Hari")
    axes[0].set_xlabel("Hari")
    axes[0].set_ylabel("Rata-rata Penyewaan Sepeda")
    axes[0].set_xticklabels(weekday_avg["weekday"], rotation=45)

    # Grafik 2: Penyewaan sepeda per jam
    sns.lineplot(ax=axes[1], x="hr", y="cnt", data=hourly_avg, marker="o", color="b")
    axes[1].set_title("Pola Penyewaan Sepeda Sepanjang Hari")
    axes[1].set_xlabel("Jam")
    axes[1].set_ylabel("Rata-rata Penyewaan Sepeda")
    axes[1].set_xticks(range(0, 24))
    axes[1].grid(True)

    plt.tight_layout()
    st.pyplot(fig)

    st.text("Insight:")
    st.markdown("""
        - Rata-rata penyewaan sepeda tertinggi terjadi pada hari **Kamis dan Jumat**.
        - Penyewaan sepeda terendah terjadi pada **hari Minggu**.
        - Jam sibuk penyewaan sepeda adalah **jam 5-6 sore** dan **jam 8 pagi**.
        - Penyewaan paling rendah terjadi **pada malam dan subuh**.
    """)

    # ANALISIS 2: Pengaruh Cuaca dan Musim terhadap Penyewaan Sepeda
    st.subheader("2. Bagaimana pengaruh cuaca dan musim terhadap jumlah penyewaan sepeda?")  

    # Rata-rata penyewaan per cuaca
    weather_avg = hour_df.groupby("weathersit")["cnt"].mean().reset_index()

    # Rata-rata penyewaan per musim
    season_avg = day_df.groupby("season")["cnt"].mean().reset_index()
    season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    season_avg["season"] = season_avg["season"].map(season_labels)

    # Buat figure dan subplot
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 5))

    # Bar Chart untuk cuaca
    sns.barplot(ax=axes[0], x="weathersit", y="cnt", data=weather_avg, palette="viridis")
    axes[0].set_title("Rata-rata Penyewaan Sepeda per Kondisi Cuaca")
    axes[0].set_xlabel("Kondisi Cuaca")
    axes[0].set_ylabel("Rata-rata Penyewaan Sepeda")

    # Bar Chart untuk musim
    sns.barplot(ax=axes[1], x="season", y="cnt", data=season_avg, palette="viridis")
    axes[1].set_title("Rata-rata Penyewaan Sepeda per Musim")
    axes[1].set_xlabel("Musim")
    axes[1].set_ylabel("Rata-rata Penyewaan Sepeda")

    plt.tight_layout()
    st.pyplot(fig)

    st.text("Insight:")
    st.markdown("""
        - Catatan untuk label Barchart Rata-rata penyewaan Sepeda per Kondisi Cuaca:
            + 1: Cerah, Sedikit awan, Berawan sebagian, Berawan sebagian
            + 2: Kabut + Berawan, Kabut + Awan pecah, Kabut + Sedikit awan, Kabut
            + 3: Salju Ringan, Hujan Ringan + Badai Petir + Awan tersebar, HujanRingan + Awan tersebar
            + 4: Hujan Lebat + Es + Badai Petir + Kabut, Salju + Kabut
        - Rata-rata jumlah penyewa sepeda terbanyak pada saat cuaca Cerah, Sedikit awan, Berawan sebagian, Berawan sebagian, dan paling sedikit pada saat cuaca Hujan Lebat + Es + Badai Petir + Kabut, Salju + Kabut. Hal ini menunjukkan bahwa cuaca merupakan faktor penting dalam penggunaan sepeda, jika cuaca buruk pengguna lebih memilih menggunakan transportasi jenis lain
        - Rata-rata jumlah penyewa sepeda terbanyak pada musim gugur diikuti dengan musim panas dan musim dingin yang tidak jauh menurun. Pada urutan terakhir yaitu penyewa paling sedikit pada musim Spring(semi). Jumlah penyewaan sepeda pada musim semi dapat ditingkatkan untuk strastegi pemasaran misalnya dengan memberikan diskon musim semi.
    """)

# ===================================================
# SECTION 4: Analisis Lanjutan
# ===================================================
elif selected_section == "Analisis Lanjutan":
    st.title("🔍 Analisis Lanjutan")
    
    st.write("Bagian ini akan menampilkan hasil analisis clustering pada dataset penyewaan sepeda.")

    st.subheader("Hasil Clustering")

    day_df_copy = day_df.copy()

    # melakukan Manual Grouping
    def categorize_temp(temp):
        if temp < 0.3:
            return 'Dingin'
        elif temp <= 0.6:
            return 'Normal'
        else:
            return 'Panas'

    def categorize_atemp(atemp):
        if atemp < 0.3:
            return 'Sejuk'
        elif atemp <= 0.6:
            return 'Hangat'
        else:
            return 'Panas'

    def categorize_hum(hum):
        if hum < 0.4:
            return 'Kering'
        elif hum <= 0.7:
            return 'Normal'
        else:
            return 'Lembap'

    def categorize_windspeed(windspeed):
        if windspeed < 0.2:
            return 'Lemah'
        elif windspeed <= 0.4:
            return 'Sedang'
        else:
            return 'Kuat'

    # kolom kategori
    day_df_copy['temp_group'] = day_df_copy['temp'].apply(categorize_temp)
    day_df_copy['atemp_group'] = day_df_copy['atemp'].apply(categorize_atemp)
    day_df_copy['hum_group'] = day_df_copy['hum'].apply(categorize_hum)
    day_df_copy['windspeed_group'] = day_df_copy['windspeed'].apply(categorize_windspeed)

    # Visualisasi
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Warna
    colors = ['#3498db', '#2ecc71', '#e74c3c']

    # temp
    temp_group = day_df_copy.groupby('temp_group')['cnt'].sum().reset_index()
    sns.barplot(x='temp_group', y='cnt', data=temp_group, palette=colors, ax=axes[0, 0])
    axes[0, 0].set_title('Distribusi Suhu (temp)')
    axes[0, 0].set_xlabel('Kategori')
    axes[0, 0].set_ylabel('Jumlah')

    # atemp
    atemp_group = day_df_copy.groupby('atemp_group')['cnt'].sum().reset_index()
    sns.barplot(x='atemp_group', y='cnt', data=atemp_group, palette=colors, ax=axes[0, 1])
    axes[0, 1].set_title('Distribusi Suhu Terasa (atemp)')
    axes[0, 1].set_xlabel('Kategori')
    axes[0, 1].set_ylabel('Jumlah')

    # hum
    hum_group = day_df_copy.groupby('hum_group')['cnt'].sum().reset_index()
    sns.barplot(x='hum_group', y='cnt', data=hum_group, palette=colors, ax=axes[1, 0])
    axes[1, 0].set_title('Distribusi Kelembaban (hum)')
    axes[1, 0].set_xlabel('Kategori')
    axes[1, 0].set_ylabel('Jumlah')

    # windspeed
    windspeed_group = day_df_copy.groupby('windspeed_group')['cnt'].sum().reset_index()
    sns.barplot(x='windspeed_group', y='cnt', data=windspeed_group, palette=colors, ax=axes[1, 1])
    axes[1, 1].set_title('Distribusi Kecepatan Angin (windspeed)')
    axes[1, 1].set_xlabel('Kategori')
    axes[1, 1].set_ylabel('Jumlah')

    plt.tight_layout()
    st.pyplot(fig)

    st.write("insight:")
    st.markdown("""
        - Pada grafik Distribusi Suhu(temp):
            + Pada suhu "Normal" memiliki frekuensi penyewaan sepeda yang paling tinggi
            + Pada Suhu "Panas" juga cukup tinggi, tetapi lebih rendah dibandingkan suhu "Normal".
            + Suhu "Dingin" memiliki frekuensi penyewaan sepeda terendah
        
        - Pada grafik Distribusi Suhu Terasa (atemp)
            + Pada suhu "Hangat" memiliki frekuensi penyewaan sepeda yang paling tinggi
            + Pada suhu "Panas" juga cukup tinggi, tetapi lebih rendah dibandingkan suhu "Hangat"
            + Pada suhu "Sejuk" memiliki frekuensi penyewaan sepeda terendah
        
        - Pada grafik Distribusi Kelembaban (hum)
            + Pada kelembaban "Normal" memiliki jumlah penyewaan sepeda paling tinggi dibandingkan kategori lainnya
            + Pada kelembaban "Lembab" juga cukup sering terjadi, tetapi lebih rendah dibandingkan suhu "Normal"
            + Pada kelembaban "Kering" memiliki frekuensi penyewaan terendah
        
        - Pada grafik Distribusi Kecepatan Angin(winspeed)
            + Pada kecepatan angin "Sedang" memiliki frekuensi tertinggi dibandingkan kategori lainnya
            + Pada kecepatan angin "Sedang" juga cukup sering terjadi, tetapi lebih rendah dibandingkan kecepatan angin "Sedang"
            + Pada kecepatan angin "Kuat" memiliki frekuensi penyewaan terendah
    """)
    
st.caption("Duma Mora Arta Sitorus | LaskarAi 2025")
