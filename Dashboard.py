import streamlit as st
import pandas as pd
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(page_title="Zara Sales Dashboard", layout="wide")

# Some helper funstions
@st.cache_data
def load_data():
    data = pd.read_csv("Zara_sales_dataset_preprocessed.v1.csv")
    data['DATE'] = pd.to_datetime(data['DATE'])
    data['NET_SUBSCRIBERS'] = data['SUBSCRIBERS_GAINED'] - data['SUBSCRIBERS_LOST']
    return data

df = pd.read_csv("Zara_sales_dataset_preprocessed.v1.csv")

# sidebar
st.sidebar.header('Zara Dashboard')

# countries filter
st.sidebar.header("Global Filters")
all_countries = sorted(df['Origin'].unique().tolist())
selected_countries = st.sidebar.multiselect(
    "Select Countries of Origin", 
    options=all_countries, 
    default=all_countries
)

if not selected_countries:
    selected_countries = all_countries
    st.sidebar.info("Showing all countries by default.")

filtered_df = df[df['Origin'].isin(selected_countries)]


st.sidebar.markdown('''
---
''')

# Matrics
# average revenue
avg_rev = filtered_df['revenue'].mean()
total_sold = filtered_df['Sales Volume'].sum()

# season with highest activity
seasonal_revenue = filtered_df.groupby('Season')['revenue'].sum()
best_season = seasonal_revenue.idxmax()

# most sold term
top_term = filtered_df['Terms'].mode()[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg Revenue", f"${avg_rev/1e3:.1f}K")
col2.metric("Total Units Sold", f"{total_sold:,}")
col3.metric("Top Category", top_term.title())
col4.metric("Best Season", best_season)

st.divider()

# set the whole thing in dark mode
plt.rcParams.update({
    "axes.facecolor": (0, 0, 0, 0),
    "figure.facecolor": (0, 0, 0, 0),
    "axes.edgecolor": "white",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "#ffffff22",
    "text.color": "white"
})
#Distribution Analysis
st.subheader("Revenue Distributions Analysis")
dist_rev_container = st.container()

with dist_rev_container:
    col_dist1, col_dist2 = st.columns(2)
    chart_size = (6, 4)
    
    with col_dist1:
        fig1, ax1 = plt.subplots(figsize=(5, 4))
        sns.kdeplot(data=filtered_df, x='Price', fill=True, color='#3498db', ax=ax1)
        plt.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.15)
        fig1.patch.set_alpha(0)
        ax1.set_facecolor((0, 0, 0, 0))
        st.pyplot(fig1, clear_figure=True) 
    
st.divider()

st.subheader("Price Distributions Analysis")
dist_price_container = st.container()
with dist_price_container:
    with col_dist2:
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        sns.kdeplot(data=filtered_df, x='revenue', fill=True, color='#e74c3c', ax=ax2)
        plt.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.15)
        fig2.patch.set_alpha(0)
        ax2.set_facecolor((0, 0, 0, 0))
        ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{x/1e6:.1f}M"))
        st.pyplot(fig2, clear_figure=True)

st.divider()

# Seasonal Analysis

seas_container = st.container()

with seas_container:
    st.subheader("Seasonal Performance")
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        st.write("Avg Revenue per Season")
        fig3, ax3 = plt.subplots()
        sns.barplot(data=filtered_df, x='Season', y='revenue', palette='viridis', ax=ax3)
        st.pyplot(fig3)
    
    with col_s2:
        st.write("Sales Count per Season")
        fig4, ax4 = plt.subplots()
        sns.countplot(data=filtered_df, x='Season', palette='magma', ax=ax4)
        st.pyplot(fig4)

st.divider()

# Category and Material Analysis
cat_mat_container = st.container()

with cat_mat_container:
    st.subheader("Category & Material Analysis")
    
    tab1, tab2 = st.tabs(["By Product Terms", "By Material"])
    
    with tab1:
        fig5, ax5 = plt.subplots(figsize=(10, 5))
        sns.barplot(data=filtered_df, x='Terms', y='revenue', ax=ax5)
        st.pyplot(fig5)
    
    with tab2:
        fig6, ax6 = plt.subplots(figsize=(10, 5))
        sns.countplot(data=filtered_df, x='Material', order=filtered_df['Material'].value_counts().index, ax=ax6)
        plt.xticks(rotation=45)
        st.pyplot(fig6)
