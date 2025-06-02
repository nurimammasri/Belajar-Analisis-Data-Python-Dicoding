import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np # Jika diperlukan untuk beberapa operasi

# Set style seaborn untuk plot yang lebih menarik
sns.set(style='darkgrid')

# --- Fungsi Pemuatan dan Pemfilteran Data ---
@st.cache_data
def load_data():
    day_df = pd.read_csv("https://raw.githubusercontent.com/nurimammasri/Belajar-Analisis-Data-Python-Dicoding/refs/heads/main/dashboard/dashboard_main_data_day.csv")
    hour_df = pd.read_csv("https://raw.githubusercontent.com/nurimammasri/Belajar-Analisis-Data-Python-Dicoding/refs/heads/main/dashboard/dashboard_main_data_hour.csv")
    
    # Pastikan kolom tanggal berformat datetime
    day_df['date'] = pd.to_datetime(day_df['date'])
    hour_df['date'] = pd.to_datetime(hour_df['date'])
    
    # Pastikan kolom kategorikal memiliki tipe 'category' jika belum
    categorical_cols_day = ['season', 'year', 'month', 'weekday', 'workingday', 'weather_condition', 'holiday']
    for col in categorical_cols_day:
        if col in day_df.columns:
            day_df[col] = day_df[col].astype('category')
            
    categorical_cols_hour = ['season', 'year', 'month', 'hour', 'weekday', 'workingday', 'weather_condition', 'holiday']
    for col in categorical_cols_hour:
        if col in hour_df.columns:
            hour_df[col] = hour_df[col].astype('category')
            
    return day_df, hour_df

# Fungsi untuk memfilter data berdasarkan input sidebar
def filter_data(df, start_date, end_date, seasons_filter, weather_filter):
    filtered_df = df[
        (df['date'] >= pd.to_datetime(start_date)) &
        (df['date'] <= pd.to_datetime(end_date))
    ]
    if seasons_filter: # Jika ada filter musim yang dipilih
        filtered_df = filtered_df[filtered_df['season'].isin(seasons_filter)]
    if weather_filter: # Jika ada filter kondisi cuaca yang dipilih
        filtered_df = filtered_df[filtered_df['weather_condition'].isin(weather_filter)]
    return filtered_df

# --- Load Data ---
day_df_orig, hour_df_orig = load_data()

# Urutan kategorikal untuk plot
season_order = ['Spring', 'Summer', 'Fall', 'Winter']
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weather_order = ['Clear/Cloudy', 'Mist/Cloudy', 'Light Snow/Rain', 'Heavy Rain/Fog']


# --- Sidebar untuk Filter ---
st.sidebar.header("Filter Data:")

# Filter Tanggal
min_date = day_df_orig['date'].min()
max_date = day_df_orig['date'].max()
start_date = st.sidebar.date_input("Tanggal Mulai", min_value=min_date, max_value=max_date, value=min_date)
end_date = st.sidebar.date_input("Tanggal Akhir", min_value=min_date, max_value=max_date, value=max_date)

# Filter Musim
all_seasons = day_df_orig['season'].unique().tolist()
seasons_filter = st.sidebar.multiselect("Pilih Musim", options=all_seasons, default=all_seasons)

# Filter Kondisi Cuaca
all_weather = day_df_orig['weather_condition'].dropna().unique().tolist() #dropna untuk handle NaN jika ada
weather_filter = st.sidebar.multiselect("Pilih Kondisi Cuaca", options=all_weather, default=all_weather)


# --- Terapkan Filter ke Dataframe ---
day_df_filtered = filter_data(day_df_orig.copy(), start_date, end_date, seasons_filter, weather_filter)
hour_df_filtered = filter_data(hour_df_orig.copy(), start_date, end_date, seasons_filter, weather_filter) # Filter juga data jam-an

# --- Judul Dashboard ---
st.title("Dashboard Analisis Data Penyewaan Sepeda (Bike Sharing)")
st.markdown(f"Data dari {start_date.strftime('%d %B %Y')} hingga {end_date.strftime('%d %B %Y')}")
if seasons_filter != all_seasons or weather_filter != all_weather:
    st.markdown(f"Dengan filter Musim: {', '.join(seasons_filter)} dan Kondisi Cuaca: {', '.join(weather_filter)}")


# --- Metrik Utama ---
st.header("Metrik Utama (Berdasarkan Filter Harian)")
if not day_df_filtered.empty:
    total_rentals_filtered = day_df_filtered['total_rentals'].sum()
    total_casual_filtered = day_df_filtered['casual'].sum()
    total_registered_filtered = day_df_filtered['registered'].sum()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Penyewaan", f"{total_rentals_filtered:,}")
    with col2:
        st.metric("Total Pengguna Casual", f"{total_casual_filtered:,}")
    with col3:
        st.metric("Total Pengguna Registered", f"{total_registered_filtered:,}")
else:
    st.warning("Tidak ada data untuk filter yang dipilih pada data harian.")


# --- Visualisasi Data (Meniru Analisis dari Notebook) ---
st.header("Visualisasi Data")

# Pertanyaan 1: Pengaruh Musim
st.subheader("1. Total Penyewaan Sepeda Berdasarkan Musim dan Tahun")
if not day_df_filtered.empty:
    seasonal_rentals_dashboard = day_df_filtered.groupby(by=["season", "year"], observed=True)["total_rentals"].sum().reset_index()
    seasonal_rentals_dashboard['season'] = pd.Categorical(seasonal_rentals_dashboard['season'], categories=season_order, ordered=True)
    seasonal_rentals_dashboard = seasonal_rentals_dashboard.sort_values('season')
    
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=seasonal_rentals_dashboard,
        x="season",
        y="total_rentals",
        hue="year",
        palette="viridis",
        ax=ax1
    )
    ax1.set_title("Total Penyewaan Sepeda Berdasarkan Musim dan Tahun")
    ax1.set_xlabel("Musim")
    ax1.set_ylabel("Total Penyewaan Sepeda")
    ax1.legend(title="Tahun")
    ax1.grid(True, axis='y', linestyle='--')
    st.pyplot(fig1)
    st.markdown("""
    **Insight Pertanyaan 1:**
    - Peningkatan umum penyewaan dari tahun 2011 ke 2012 di semua musim.
    - Musim Gugur (Fall) menunjukkan jumlah penyewaan tertinggi, diikuti Musim Panas dan Dingin. Musim Semi terendah.
    - Musim memiliki pengaruh signifikan, dengan tren peningkatan penggunaan dari 2011 ke 2012.
    """)
else:
    st.warning("Tidak ada data untuk visualisasi Pengaruh Musim berdasarkan filter yang dipilih.")

# Pertanyaan 2: Pola Penyewaan per Jam (Hari Kerja vs Non-Hari Kerja)
st.subheader("2. Pola Penyewaan Sepeda Rata-Rata per Jam")
if not hour_df_filtered.empty:
    hourly_pattern_dashboard = hour_df_filtered.groupby(by=["workingday", "hour"], observed=True)["total_rentals"].mean().reset_index()
    
    fig2, ax2 = plt.subplots(figsize=(12, 7))
    sns.lineplot(
        data=hourly_pattern_dashboard,
        x="hour",
        y="total_rentals",
        hue="workingday",
        marker="o",
        palette={"Working Day": "blue", "Non-Working Day": "red"},
        ax=ax2
    )
    ax2.set_title("Pola Penyewaan Sepeda Rata-Rata per Jam Berdasarkan Tipe Hari")
    ax2.set_xlabel("Jam dalam Sehari")
    ax2.set_ylabel("Rata-Rata Jumlah Penyewaan Sepeda")
    ax2.set_xticks(range(0, 24))
    ax2.legend(title="Tipe Hari")
    ax2.grid(True, linestyle='--')
    st.pyplot(fig2)
    st.markdown("""
    **Insight Pertanyaan 2:**
    - **Hari Kerja:** Dua puncak (pagi jam 7-9, sore jam 17-19) khas pola komuter.
    - **Non-Hari Kerja:** Pola lebih merata dengan puncak siang-sore (jam 10-17) untuk rekreasi.
    """)
else:
    st.warning("Tidak ada data untuk visualisasi Pola Penyewaan per Jam berdasarkan filter yang dipilih.")

# Pertanyaan 3: Pengaruh Kondisi Cuaca
st.subheader("3. Total Penyewaan Sepeda Berdasarkan Kondisi Cuaca dan Tahun")
if not day_df_filtered.empty:
    weather_rentals_dashboard = day_df_filtered.groupby(by=["weather_condition", "year"], observed=True)["total_rentals"].sum().reset_index()
    existing_weather_dashboard = day_df_filtered['weather_condition'].unique().tolist()
    weather_order_filtered_dashboard = [cond for cond in weather_order if cond in existing_weather_dashboard]
    weather_rentals_dashboard['weather_condition'] = pd.Categorical(weather_rentals_dashboard['weather_condition'], categories=weather_order_filtered_dashboard, ordered=True)
    weather_rentals_dashboard = weather_rentals_dashboard.sort_values('weather_condition')
    
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=weather_rentals_dashboard,
        x="weather_condition",
        y="total_rentals",
        hue="year",
        palette="coolwarm",
        ax=ax3
    )
    ax3.set_title("Total Penyewaan Sepeda Berdasarkan Kondisi Cuaca dan Tahun")
    ax3.set_xlabel("Kondisi Cuaca")
    ax3.set_ylabel("Total Penyewaan Sepeda")
    ax3.legend(title="Tahun")
    ax3.grid(True, axis='y', linestyle='--')
    st.pyplot(fig3)
    st.markdown("""
    **Insight Pertanyaan 3:**
    - Cuaca 'Cerah/Berawan' memiliki penyewaan tertinggi.
    - Penyewaan menurun pada 'Berkabut/Berawan' dan sangat rendah pada 'Salju Ringan/Hujan Ringan'.
    - Peningkatan tahunan terlihat di berbagai kondisi cuaca.
    """)
else:
    st.warning("Tidak ada data untuk visualisasi Pengaruh Kondisi Cuaca berdasarkan filter yang dipilih.")

# Pertanyaan Tambahan 4: Tren Penyewaan Bulanan
st.subheader("4. Tren Penyewaan Sepeda Bulanan (2011-2012)")
if not day_df_filtered.empty:
    monthly_trends_dashboard = day_df_filtered.copy()
    monthly_trends_dashboard['year_month_dt'] = monthly_trends_dashboard['date'].dt.to_period('M')
    monthly_agg_dashboard = monthly_trends_dashboard.groupby('year_month_dt', observed=True).agg(
        total_casual=('casual', 'sum'),
        total_registered=('registered', 'sum'),
        total_all_rentals=('total_rentals', 'sum')
    ).reset_index()
    monthly_agg_dashboard['year_month_str'] = monthly_agg_dashboard['year_month_dt'].astype(str)
    
    fig4, ax4 = plt.subplots(figsize=(15, 7))
    sns.lineplot(data=monthly_agg_dashboard, x='year_month_str', y='total_all_rentals', marker='o', label='Total Penyewaan', color='purple', ax=ax4)
    sns.lineplot(data=monthly_agg_dashboard, x='year_month_str', y='total_casual', marker='x', label='Pengguna Casual', color='orange', ax=ax4)
    sns.lineplot(data=monthly_agg_dashboard, x='year_month_str', y='total_registered', marker='s', label='Pengguna Registered', color='green', ax=ax4)
    ax4.set_title('Tren Penyewaan Sepeda Bulanan (2011-2012)')
    ax4.set_xlabel('Tahun-Bulan')
    ax4.set_ylabel('Jumlah Penyewaan')
    ax4.tick_params(axis='x', rotation=45)
    ax4.legend(title='Tipe Pengguna/Total')
    ax4.grid(True, linestyle='--')
    st.pyplot(fig4)
    st.markdown("""
    **Insight Pertanyaan Tambahan 4:**
    - Tren peningkatan penyewaan dari 2011 ke 2012.
    - Pola musiman bulanan jelas (puncak di pertengahan tahun, penurunan di awal/akhir).
    - Pengguna terdaftar mendominasi, pertumbuhannya juga lebih dominan.
    """)
else:
    st.warning("Tidak ada data untuk visualisasi Tren Penyewaan Bulanan berdasarkan filter yang dipilih.")


# Pertanyaan Tambahan 5: Distribusi Harian per Hari dalam Seminggu
st.subheader("5. Distribusi Penyewaan Harian berdasarkan Hari dalam Seminggu")
if not day_df_filtered.empty:
    day_df_viz5 = day_df_filtered.copy()
    day_df_viz5['weekday'] = pd.Categorical(day_df_viz5['weekday'], categories=day_order, ordered=True)
    
    fig5, axes5 = plt.subplots(1, 3, figsize=(18, 6))
    sns.boxplot(data=day_df_viz5, x='weekday', y='total_rentals', palette='pastel', ax=axes5[0])
    axes5[0].set_title('Distribusi Total Penyewaan per Hari')
    axes5[0].set_xlabel('Hari')
    axes5[0].set_ylabel('Total Penyewaan Harian')
    axes5[0].tick_params(axis='x', rotation=45)

    sns.boxplot(data=day_df_viz5, x='weekday', y='casual', palette='pastel', ax=axes5[1])
    axes5[1].set_title('Distribusi Pengguna Casual per Hari')
    axes5[1].set_xlabel('Hari')
    axes5[1].set_ylabel('Penyewaan Casual Harian')
    axes5[1].tick_params(axis='x', rotation=45)

    sns.boxplot(data=day_df_viz5, x='weekday', y='registered', palette='pastel', ax=axes5[2])
    axes5[2].set_title('Distribusi Pengguna Registered per Hari')
    axes5[2].set_xlabel('Hari')
    axes5[2].set_ylabel('Penyewaan Registered Harian')
    axes5[2].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    st.pyplot(fig5)
    st.markdown("""
    **Insight Pertanyaan Tambahan 5:**
    - Akhir pekan (Sabtu, Minggu) memiliki median total penyewaan harian lebih tinggi.
    - Penyewaan pengguna casual lebih tinggi dan bervariasi di akhir pekan.
    - Pengguna terdaftar lebih stabil di hari kerja.
    """)
else:
    st.warning("Tidak ada data untuk visualisasi Distribusi Harian per Hari berdasarkan filter yang dipilih.")


# Pertanyaan Tambahan 6: Dampak Variabel Cuaca Kontinu
st.subheader("6. Dampak Variabel Cuaca Kontinu terhadap Total Penyewaan Harian")
if not day_df_filtered.empty:
    numerical_cols_weather_dashboard = ['temperature', 'feeling_temperature', 'humidity', 'windspeed', 'casual', 'registered', 'total_rentals']
    correlation_matrix_dashboard = day_df_filtered[numerical_cols_weather_dashboard].corr()
    
    fig6_1, ax6_1 = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix_dashboard, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, ax=ax6_1)
    ax6_1.set_title('Heatmap Korelasi Variabel Numerik (Termasuk Cuaca)')
    st.pyplot(fig6_1)

    fig6_2, axes6_2 = plt.subplots(2, 2, figsize=(15, 12))
    fig6_2.suptitle('Hubungan Variabel Cuaca Kontinu dengan Total Penyewaan Harian', fontsize=16)
    weather_vars_scatter = ['temperature', 'feeling_temperature', 'humidity', 'windspeed']
    titles_scatter = ['Suhu vs. Total Penyewaan', 'Suhu Dirasakan vs. Total Penyewaan', 'Kelembapan vs. Total Penyewaan', 'Kecepatan Angin vs. Total Penyewaan']
    xlabels_scatter = ['Suhu Ternormalisasi', 'Suhu Dirasakan Ternormalisasi', 'Kelembapan Ternormalisasi', 'Kecepatan Angin Ternormalisasi']

    for i, var in enumerate(weather_vars_scatter):
        ax_row, ax_col = i // 2, i % 2
        sns.scatterplot(ax=axes6_2[ax_row, ax_col], data=day_df_filtered, x=var, y='total_rentals', alpha=0.5)
        sns.regplot(ax=axes6_2[ax_row, ax_col], data=day_df_filtered, x=var, y='total_rentals', scatter=False, color='red')
        axes6_2[ax_row, ax_col].set_title(titles_scatter[i])
        axes6_2[ax_row, ax_col].set_xlabel(xlabels_scatter[i])
        axes6_2[ax_row, ax_col].set_ylabel('Total Penyewaan Harian')
        axes6_2[ax_row, ax_col].grid(True, linestyle='--')
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    st.pyplot(fig6_2)
    st.markdown("""
    **Insight Pertanyaan Tambahan 6:**
    - Suhu (aktual & dirasakan) berkorelasi positif kuat dengan `total_rentals`.
    - Kelembapan berkorelasi negatif lemah, kecepatan angin berkorelasi negatif sedang.
    """)
else:
    st.warning("Tidak ada data untuk visualisasi Dampak Variabel Cuaca Kontinu berdasarkan filter yang dipilih.")


# Pertanyaan Tambahan 7: Interaksi Pola Jam, Musim, Tipe Hari
st.subheader("7. Pola Penyewaan per Jam Berdasarkan Musim dan Tipe Hari")
if not hour_df_filtered.empty:
    hourly_seasonal_pattern_dashboard = hour_df_filtered.groupby(by=["season", "workingday", "hour"], observed=True)["total_rentals"].mean().reset_index()
    hourly_seasonal_pattern_dashboard['season'] = pd.Categorical(hourly_seasonal_pattern_dashboard['season'], categories=season_order, ordered=True)
    hourly_seasonal_pattern_dashboard = hourly_seasonal_pattern_dashboard.sort_values(['season', 'workingday', 'hour'])
    
    g = sns.FacetGrid(hourly_seasonal_pattern_dashboard, col="season", hue="workingday", col_wrap=2, height=5, aspect=1.5, palette={"Working Day": "blue", "Non-Working Day": "red"})
    g.map(sns.lineplot, "hour", "total_rentals", marker="o")
    g.set_axis_labels("Jam dalam Sehari", "Rata-Rata Jumlah Penyewaan")
    g.set_titles("Musim: {col_name}")
    g.add_legend(title="Tipe Hari")
    g.fig.suptitle("Pola Penyewaan Sepeda per Jam Berdasarkan Musim dan Tipe Hari", y=1.03)
    plt.tight_layout()
    st.pyplot(g)
    st.markdown("""
    **Insight Pertanyaan Tambahan 7:**
    - Pola komuter (hari kerja) dan rekreasi (non-hari kerja) tetap ada, namun intensitas dan durasi puncaknya dimodifikasi oleh musim.
    """)
else:
    st.warning("Tidak ada data untuk visualisasi Interaksi Pola Jam, Musim, Tipe Hari berdasarkan filter yang dipilih.")


# Analisis Tambahan: Proporsi Pengguna Casual vs. Registered Berdasarkan Musim
st.subheader("Analisis Tambahan: Proporsi Pengguna Casual vs. Registered berdasarkan Musim")
if not day_df_filtered.empty:
    seasonal_user_type_dashboard = day_df_filtered.groupby(by=["season"], observed=True)[['casual', 'registered']].sum().reset_index()
    seasonal_user_type_melted_dashboard = seasonal_user_type_dashboard.melt(id_vars=['season'], value_vars=['casual', 'registered'], var_name='user_type', value_name='total_rentals_sum') # ganti nama kolom agar tidak konflik
    seasonal_user_type_melted_dashboard['season'] = pd.Categorical(seasonal_user_type_melted_dashboard['season'], categories=season_order, ordered=True)
    seasonal_user_type_melted_dashboard = seasonal_user_type_melted_dashboard.sort_values('season')
    
    fig_add1, ax_add1 = plt.subplots(figsize=(12, 7))
    sns.barplot(data=seasonal_user_type_melted_dashboard, x='season', y='total_rentals_sum', hue='user_type', palette={'casual': 'orange', 'registered': 'green'}, ax=ax_add1)
    ax_add1.set_title('Jumlah Pengguna Casual vs. Registered berdasarkan Musim')
    ax_add1.set_xlabel('Musim')
    ax_add1.set_ylabel('Total Penyewaan')
    ax_add1.tick_params(axis='x', rotation=0)
    ax_add1.legend(title='Tipe Pengguna')
    ax_add1.grid(axis='y', linestyle='--')
    st.pyplot(fig_add1)
    st.markdown("""
    **Insight:** Pengguna terdaftar mendominasi di semua musim. Pengguna casual meningkat proporsional di musim hangat.
    """)
else:
    st.warning("Tidak ada data untuk visualisasi Proporsi Pengguna berdasarkan filter yang dipilih.")

# Analisis Lanjutan : Clustering Penggunaan Bulanan Berdasarkan Total Penyewaan
st.subheader("Analisis Lanjutan: Clustering Penggunaan Bulanan Berdasarkan Total Penyewaan")
if not day_df_filtered.empty:
    monthly_total_rentals_df_dashboard = day_df_filtered.copy()
    monthly_total_rentals_df_dashboard['year_month_dt'] = monthly_total_rentals_df_dashboard['date'].dt.to_period('M')
    monthly_aggregated_totals_dashboard = monthly_total_rentals_df_dashboard.groupby('year_month_dt', observed=True)['total_rentals'].sum().reset_index()
    monthly_aggregated_totals_dashboard['year_month_str'] = monthly_aggregated_totals_dashboard['year_month_dt'].astype(str)

    # Ambil ambang batas dari notebook Anda atau tentukan di sini
    low_usage_threshold_dash = 100000  # Sesuaikan
    medium_usage_threshold_dash = 200000 # Sesuaikan

    def assign_total_rental_cluster_dash(total_rentals_val):
        if total_rentals_val <= low_usage_threshold_dash:
            return 'Rendah'
        elif total_rentals_val <= medium_usage_threshold_dash:
            return 'Sedang'
        else:
            return 'Tinggi'

    monthly_aggregated_totals_dashboard['usage_cluster'] = monthly_aggregated_totals_dashboard['total_rentals'].apply(assign_total_rental_cluster_dash)
    cluster_order_viz_dash = ['Rendah', 'Sedang', 'Tinggi']
    monthly_aggregated_totals_dashboard['usage_cluster'] = pd.Categorical(monthly_aggregated_totals_dashboard['usage_cluster'], categories=cluster_order_viz_dash, ordered=True)

    fig_cluster, ax_cluster = plt.subplots(figsize=(15, 7))
    sns.barplot(
        data=monthly_aggregated_totals_dashboard,
        x='year_month_str',
        y='total_rentals',
        hue='usage_cluster',
        palette={'Rendah': 'lightblue', 'Sedang': 'orange', 'Tinggi': 'salmon'},
        dodge=False,
        ax=ax_cluster
    )
    ax_cluster.set_title('Total Penyewaan Sepeda Bulanan dengan Clustering Penggunaan')
    ax_cluster.set_xlabel('Tahun-Bulan')
    ax_cluster.set_ylabel('Total Penyewaan Sepeda')
    ax_cluster.tick_params(axis='x', rotation=45)
    ax_cluster.legend(title='Cluster Penggunaan')
    ax_cluster.grid(True, axis='y', linestyle='--')
    st.pyplot(fig_cluster)
    
    st.subheader("Ringkasan Bulan per Cluster Penggunaan (Total Rentals)")
    for cluster_name_val_dash in cluster_order_viz_dash:
        months_in_cluster_dash = monthly_aggregated_totals_dashboard[monthly_aggregated_totals_dashboard['usage_cluster'] == cluster_name_val_dash]['year_month_str'].tolist()
        if months_in_cluster_dash:
            st.markdown(f"**Cluster {cluster_name_val_dash}:** {', '.join(months_in_cluster_dash)}")
        else:
            st.markdown(f"**Cluster {cluster_name_val_dash}:** Tidak ada bulan dalam cluster ini untuk filter yang dipilih.")
    st.markdown("""
    **Insight Clustering:** Mengelompokkan bulan ke dalam kategori 'Rendah', 'Sedang', dan 'Tinggi' berdasarkan total penyewaan, membantu perencanaan operasional.
    """)
else:
    st.warning("Tidak ada data untuk visualisasi Clustering berdasarkan filter yang dipilih.")


# --- Kesimpulan dari Notebook ---
st.header("Kesimpulan Umum dari Analisis")
st.markdown("""
- **Pengaruh Musim:** Musim sangat mempengaruhi perilaku penyewaan sepeda. Jumlah penyewaan tertinggi terjadi pada Musim Gugur (Fall) dan Musim Panas (Summer), sementara Musim Semi (Spring) mencatat jumlah terendah. Ada peningkatan umum penyewaan dari tahun 2011 ke 2012.
- **Pola Hari Kerja vs. Libur:** Terdapat perbedaan pola penyewaan yang jelas. Hari kerja menunjukkan dua puncak (pagi & sore) yang berkaitan dengan jam komuter. Non-hari kerja menunjukkan pola rekreasi.
- **Dampak Kondisi Cuaca:** Kondisi cuaca adalah faktor penting. Cuaca cerah/berawan menghasilkan penyewaan tertinggi; cuaca buruk menurunkannya drastis.
- **Tren Bulanan:** Tren penyewaan bulanan menunjukkan pertumbuhan dari 2011 ke 2012 dan pola musiman yang jelas. Pengguna terdaftar mendominasi.
- **Distribusi Harian per Hari:** Akhir pekan memiliki median total & casual yang lebih tinggi. Hari kerja menunjukkan penyewaan pengguna terdaftar yang lebih stabil.
- **Dampak Cuaca Kontinu:** Suhu berkorelasi positif kuat; kecepatan angin negatif sedang; kelembapan negatif lemah.
- **Interaksi Pola Jam, Musim, Tipe Hari:** Pola dasar komuter dan rekreasi per jam dimodifikasi oleh kondisi musiman.
- **Clustering Penggunaan Bulanan:** Efektif mengelompokkan bulan berdasarkan volume penggunaan, berguna untuk perencanaan.
""")

st.caption("Dashboard dibuat berdasarkan analisis dari notebook Jupyter.")