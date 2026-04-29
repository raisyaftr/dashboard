import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ========================
# LOAD DATA
# ========================
@st.cache_data
def load_data():
    df = pd.read_csv('main_data.csv')
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['year'] = df['dteday'].dt.year
    df['month'] = df['dteday'].dt.month
    return df

df = load_data()

# ========================
# TITLE
# ========================
st.title("🚲 Dashboard Analisis Penyewaan Sepeda")
st.write("""
Dashboard ini dibuat untuk menjawab:
1. Pengaruh suhu terhadap penyewaan sepeda tahun 2011
2. Perbandingan penyewaan tahun 2011 vs 2012
""")

# ========================
# FILTER INTERAKTIF
# ========================
st.sidebar.header("🔍 Filter Data")

selected_year = st.sidebar.multiselect(
    "Pilih Tahun",
    options=df['year'].unique(),
    default=df['year'].unique()
)

selected_month = st.sidebar.slider(
    "Pilih Rentang Bulan",
    1, 12, (1, 12)
)

filtered_df = df[
    (df['year'].isin(selected_year)) &
    (df['month'] >= selected_month[0]) &
    (df['month'] <= selected_month[1])
]

# ========================
# VISUALISASI 1
# ========================
st.subheader("📈 Pengaruh Suhu terhadap Penyewaan (2011)")

df_2011 = df[df['year'] == 2011]

monthly_temp_rent = df_2011.groupby('month').agg({
    'temp': 'mean',
    'cnt': 'sum'
}).reset_index()

fig1, ax1 = plt.subplots()

sns.lineplot(
    data=monthly_temp_rent,
    x='month',
    y='cnt',
    marker='o',
    label='Total Penyewaan',
    ax=ax1
)

sns.lineplot(
    data=monthly_temp_rent,
    x='month',
    y='temp',
    marker='o',
    label='Suhu',
    ax=ax1
)

ax1.set_title("Suhu vs Penyewaan Sepeda (2011)")
ax1.set_xlabel("Bulan")
ax1.set_ylabel("Nilai")

st.pyplot(fig1)

st.write("""
Insight:
- Saat suhu meningkat (pertengahan tahun), jumlah penyewaan juga meningkat
- Hubungan positif terlihat jelas
""")

# ========================
# VISUALISASI 2
# ========================
st.subheader("📊 Perbandingan Penyewaan 2011 vs 2012")

yearly_rent = df.groupby('year')['cnt'].sum().reset_index()

fig2, ax2 = plt.subplots()

sns.barplot(
    data=yearly_rent,
    x='year',
    y='cnt',
    ax=ax2
)

ax2.set_title("Total Penyewaan per Tahun")

st.pyplot(fig2)

st.write("""
Insight:
- Tahun 2012 memiliki total penyewaan lebih tinggi dibanding 2011
- Menunjukkan adanya pertumbuhan bisnis
""")

# ========================
# FITUR INTERAKTIF
# ========================
st.subheader("🔎 Eksplorasi Data Interaktif")

st.write("Data berdasarkan filter yang dipilih:")

st.dataframe(filtered_df)

# Tambahan visual interaktif
st.write("Distribusi Penyewaan Berdasarkan Bulan")

fig3, ax3 = plt.subplots()

sns.lineplot(
    data=filtered_df.groupby('month')['cnt'].sum().reset_index(),
    x='month',
    y='cnt',
    marker='o',
    ax=ax3
)

st.pyplot(fig3)
