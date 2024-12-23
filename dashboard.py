import pandas as pd
import plotly.express as px
import streamlit as st

# Load Data dengan st.cache_data untuk caching
@st.cache_data
def load_data():
    df = pd.read_csv('day.csv')
    columns_to_keep = ['dteday', 'yr', 'mnth', 'season', 'cnt']
    df = df[columns_to_keep]
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['year'] = df['dteday'].dt.year
    return df

df_bersih = load_data()

# Summarize data by year, month, and season
monthly_rentals = df_bersih.groupby(['year', 'mnth'])['cnt'].sum().reset_index()
seasonal_rentals = df_bersih.groupby(['year', 'season'])['cnt'].sum().reset_index()

# Replace numeric values in 'mnth' and 'season' with descriptive text
monthly_rentals['mnth'] = monthly_rentals['mnth'].replace({
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
})

seasonal_rentals['season'] = seasonal_rentals['season'].replace({
    1: 'spring', 2: 'summer', 3: 'fall', 4: 'winter'
})

# Streamlit App
st.title("Interactive Bike Rentals Analysis (2011 and 2012)")

# Sidebar for navigation
st.sidebar.header("Navigasi")
selected_year = st.sidebar.selectbox('Select Year', [2011, 2012])

# Filter data based on selected year
filtered_monthly_rentals = monthly_rentals[monthly_rentals['year'] == selected_year]
filtered_seasonal_rentals = seasonal_rentals[seasonal_rentals['year'] == selected_year]

# Monthly Rentals Plot using Plotly
st.header(f"Monthly Rentals for {selected_year}")
fig1 = px.bar(filtered_monthly_rentals, x='mnth', y='cnt', color='mnth', title=f'Monthly Bike Rentals in {selected_year}')
fig1.update_layout(xaxis_title='Month', yaxis_title='Number of Rentals', xaxis={'categoryorder':'category ascending'})
st.plotly_chart(fig1)

# Penjelasan dinamis tentang Monthly Rentals
st.subheader("Penjelasan tentang Monthly Rentals")

# Selectbox to choose between highest and lowest rentals
selected_month = st.selectbox('Select Month', filtered_monthly_rentals['mnth'].unique())
month_data = filtered_monthly_rentals[filtered_monthly_rentals['mnth'] == selected_month]
highest_rentals = month_data['cnt'].max()
lowest_rentals = month_data['cnt'].min()

st.write(f"Pada bulan {selected_month} di tahun {selected_year}:")
st.write(f"- Tertinggi: {month_data.loc[month_data['cnt'] == highest_rentals, 'cnt'].values[0]:,.0f} penyewaan.")
st.write(f"- Terendah: {month_data.loc[month_data['cnt'] == lowest_rentals, 'cnt'].values[0]:,.0f} penyewaan.")

# Seasonal Rentals Plot using Plotly
st.header(f"Seasonal Rentals for {selected_year}")
fig2 = px.bar(filtered_seasonal_rentals, x='season', y='cnt', color='season', title=f'Seasonal Bike Rentals in {selected_year}')
fig2.update_layout(xaxis_title='Season', yaxis_title='Number of Rentals')
st.plotly_chart(fig2)

# Penjelasan dinamis tentang Seasonal Rentals
st.subheader("Penjelasan tentang Seasonal Rentals")

# Radio button to choose between highest and lowest season
selected_season = st.radio('Select Season', filtered_seasonal_rentals['season'].unique())
season_data = filtered_seasonal_rentals[filtered_seasonal_rentals['season'] == selected_season]
highest_season_rentals = season_data['cnt'].max()
lowest_season_rentals = season_data['cnt'].min()

st.write(f"Pada musim {selected_season} di tahun {selected_year}:")
st.write(f"- Tertinggi: {season_data.loc[season_data['cnt'] == highest_season_rentals, 'cnt'].values[0]:,.0f} penyewaan.")
st.write(f"- Terendah: {season_data.loc[season_data['cnt'] == lowest_season_rentals, 'cnt'].values[0]:,.0f} penyewaan.")

# Kesimpulan
st.subheader("Kesimpulan")
st.write("""
Penyewaan sepeda cenderung tinggi di musim gugur dan di bulan dengan cuaca yang lebih hangat seperti Juni atau September. 
Penyewaan paling sedikit terjadi di bulan Januari (musim dingin), yang mungkin disebabkan oleh kondisi cuaca yang kurang mendukung aktivitas luar ruangan.
""")