import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Dashboard Data", layout="wide")

st.title("📊 Dashboard Analisis Data Interaktif")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("main_data.csv")

df = load_data()

# =========================
# SIDEBAR
# =========================
st.sidebar.header("⚙️ Pengaturan")

# Pilih kolom numerik
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

# Filter data
selected_column = st.sidebar.selectbox("Pilih Kolom untuk Filter", df.columns)

if df[selected_column].dtype == 'object':
    selected_value = st.sidebar.selectbox("Pilih Nilai", df[selected_column].unique())
    filtered_df = df[df[selected_column] == selected_value]
else:
    min_val = float(df[selected_column].min())
    max_val = float(df[selected_column].max())
    range_val = st.sidebar.slider("Range", min_val, max_val, (min_val, max_val))
    filtered_df = df[(df[selected_column] >= range_val[0]) & (df[selected_column] <= range_val[1])]

# =========================
# MAIN CONTENT
# =========================

tab1, tab2, tab3 = st.tabs(["📄 Data", "📊 Visualisasi", "📈 Statistik"])

# =========================
# TAB 1 - DATA
# =========================
with tab1:
    st.subheader("Preview Data")
    st.dataframe(filtered_df)

# =========================
# TAB 2 - VISUALISASI
# =========================
with tab2:
    st.subheader("Visualisasi Data")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Histogram")
        hist_col = st.selectbox("Pilih Kolom Histogram", numeric_cols)
        fig, ax = plt.subplots()
        sns.histplot(filtered_df[hist_col], kde=True, ax=ax)
        st.pyplot(fig)

    with col2:
        st.write("Bar Chart")
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()
        if cat_cols:
            bar_col = st.selectbox("Pilih Kolom Kategori", cat_cols)
            fig, ax = plt.subplots()
            filtered_df[bar_col].value_counts().plot(kind='bar', ax=ax)
            st.pyplot(fig)

    st.write("Correlation Heatmap")
    fig, ax = plt.subplots()
    sns.heatmap(filtered_df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

# =========================
# TAB 3 - STATISTIK
# =========================
with tab3:
    st.subheader("Statistik Deskriptif")
    st.write(filtered_df.describe())

    st.subheader("Missing Values")
    st.write(filtered_df.isnull().sum())

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("Dibuat dengan Streamlit 🚀")
