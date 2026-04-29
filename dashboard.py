import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

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
Dashboard ini menjawab:
1. Pengaruh suhu terhadap penyewaan (2011)
2. Tren pertumbuhan 2011 ke 2012
""")

# ========================
# FILTER INTERAKTIF
# ========================
st.sidebar.header("Filter Data")

year_filter = st.sidebar.multiselect(
    "Pilih Tahun",
    options=sorted(df['year'].unique()),
    default=sorted(df['year'].unique())
)

month_filter = st.sidebar.slider(
    "Rentang Bulan",
    1, 12, (1,12)
)

filtered_df = df[(df['year'].isin(year_filter)) &
                 (df['month'] >= month_filter[0]) &
                 (df['month'] <= month_filter[1])]

# ========================
# PERTANYAAN 1
# ========================
st.subheader("📈 Pengaruh Suhu terhadap Penyewaan (2011)")

df_2011 = df[df['year'] == 2011]

monthly_data = df_2011.groupby('month').agg({
    'temp': 'mean',
    'cnt': 'sum'
}).reset_index()

fig1, ax1 = plt.subplots()

sns.lineplot(data=monthly_data, x='month', y='cnt', marker='o', label='Total Rentals', ax=ax1)
sns.lineplot(data=monthly_data, x='month', y='temp', marker='o', label='Avg Temp', ax=ax1)

ax1.set_title("Tren Suhu dan Penyewaan (2011)")
st.pyplot(fig1)

st.write("""
Suhu meningkat di pertengahan tahun diikuti peningkatan penyewaan.
Menunjukkan hubungan positif antara suhu dan jumlah rental.
""")

# ========================
# PERTANYAAN 2
# ========================
st.subheader("📊 Tren Pertumbuhan 2011 vs 2012")

yearly = df.groupby('year')['cnt'].sum().reset_index()

fig2, ax2 = plt.subplots()
sns.barplot(data=yearly, x='year', y='cnt', ax=ax2)
ax2.set_title("Total Penyewaan per Tahun")
st.pyplot(fig2)

monthly = df.groupby(['year','month'])['cnt'].sum().reset_index()

fig3, ax3 = plt.subplots()
sns.lineplot(data=monthly, x='month', y='cnt', hue='year', marker='o', ax=ax3)
ax3.set_title("Tren Bulanan")
st.pyplot(fig3)

st.write("""
Tahun 2012 menunjukkan peningkatan signifikan dan konsisten dibanding 2011.
""")

# ========================
# ANALISIS FAKTOR
# ========================
st.subheader("🔥 Faktor yang Mempengaruhi")

corr = df[['temp','atemp','hum','windspeed','cnt']].corr()

fig4, ax4 = plt.subplots()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax4)
st.pyplot(fig4)

st.write("""
Suhu memiliki pengaruh paling kuat terhadap penyewaan.
""")

# ========================
# FITUR INTERAKTIF
# ========================
st.subheader("🎮 Eksplorasi Interaktif")

feature = st.selectbox(
    "Pilih faktor",
    ['temp','atemp','hum','windspeed']
)

fig5, ax5 = plt.subplots()
sns.scatterplot(data=filtered_df, x=feature, y='cnt', ax=ax5)
sns.regplot(data=filtered_df, x=feature, y='cnt', scatter=False, color='red', ax=ax5)

st.pyplot(fig5)

st.write("Gunakan filter di sidebar untuk eksplorasi data.")

# ========================
# DATA
# ========================
st.subheader("📄 Data")
st.dataframe(filtered_df)
