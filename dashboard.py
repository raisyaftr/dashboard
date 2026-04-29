import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Dashboard Bike Sharing", layout="wide")

st.title("🚲 Dashboard Analisis Penyewaan Sepeda")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("main.csv")

df = load_data()

# =========================
# SIDEBAR (INTERAKTIF)
# =========================
st.sidebar.header("⚙️ Filter Data")

selected_year = st.sidebar.selectbox(
    "Pilih Tahun",
    options=[0, 1],
    format_func=lambda x: "2011" if x == 0 else "2012"
)

filtered_df = df[df['yr'] == selected_year]

# =========================
# METRICS
# =========================
col1, col2 = st.columns(2)
col1.metric("Total Data", len(filtered_df))
col2.metric("Total Penyewaan", int(filtered_df['cnt'].sum()))

st.markdown("---")

# =========================
# PERTANYAAN 1
# =========================
st.subheader("🌡️ Pengaruh Suhu terhadap Penyewaan (2011)")

# Filter khusus 2011

df_2011 = df[df['yr'] == 0]

agg_q1 = df_2011.groupby('mnth').agg({
    'temp': 'mean',
    'cnt': 'sum'
}).reset_index()

fig, ax1 = plt.subplots()

ax1.plot(agg_q1['mnth'], agg_q1['cnt'], marker='o')
ax1.set_ylabel('Total Penyewaan')
ax1.set_xlabel('Bulan')

ax2 = ax1.twinx()
ax2.plot(agg_q1['mnth'], agg_q1['temp'], linestyle='--')
ax2.set_ylabel('Rata-rata Suhu')

st.pyplot(fig)

st.info("Kenaikan suhu di pertengahan tahun diikuti peningkatan jumlah penyewaan sepeda.")

# =========================
# PERTANYAAN 2
# =========================
st.subheader("📈 Perbandingan Penyewaan 2011 vs 2012")

agg_q2 = df.groupby('yr')['cnt'].sum().reset_index()
agg_q2['yr'] = agg_q2['yr'].map({0: '2011', 1: '2012'})

fig2, ax = plt.subplots()
ax.bar(agg_q2['yr'], agg_q2['cnt'])
ax.set_ylabel("Total Penyewaan")

st.pyplot(fig2)

st.info("Terjadi peningkatan signifikan jumlah penyewaan dari 2011 ke 2012.")

# =========================
# DATA PREVIEW
# =========================
st.subheader("📄 Data Preview")
st.dataframe(filtered_df, use_container_width=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("Dashboard sesuai pertanyaan bisnis ✔️")
