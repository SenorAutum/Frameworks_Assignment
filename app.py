import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Page Config
st.set_page_config(page_title="COVID Analysis", layout="wide")

st.title("🦠 CORD-19 Research Analysis")
st.markdown("Exploring COVID-19 Research Papers interactively.")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv('cleaned_metadata.csv')

try:
    df = load_data()
except FileNotFoundError:
    st.error("Data file not found. Please run analysis.py first.")
    st.stop()

# Sidebar
st.sidebar.header("Filters")
min_year = int(df['publish_year'].min())
max_year = int(df['publish_year'].max())
selected_year = st.sidebar.slider("Filter by Year", min_year, max_year, max_year)

data = df[df['publish_year'] <= selected_year]

# Layout: KPI Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Papers", len(data))
col2.metric("Journals", data['journal'].nunique())
col3.metric("Latest Paper", int(data['publish_year'].max()))

# Layout: Charts
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Papers per Year")
    fig1, ax1 = plt.subplots()
    data['publish_year'].value_counts().sort_index().plot(kind='bar', ax=ax1)
    st.pyplot(fig1)

with col_right:
    st.subheader("Top Journals")
    fig2, ax2 = plt.subplots()
    data['journal'].value_counts().head(5).plot(kind='barh', ax=ax2, color='orange')
    st.pyplot(fig2)

st.subheader("Word Cloud of Titles")
if st.checkbox("Show Word Cloud"):
    text = " ".join(title for title in data['title'].astype(str))
    wordcloud = WordCloud(width=800, height=300, background_color='white').generate(text)
    st.image(wordcloud.to_array())

st.dataframe(data.head(50))