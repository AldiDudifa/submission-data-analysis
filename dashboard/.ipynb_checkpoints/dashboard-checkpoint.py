import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_sum_registered_rider_df(df):
    sum_registered_rider_df = day_df.groupby("month").registered_rider.sum().sort_values(ascending=False).reset_index()
    return sum_registered_rider_df

def create_sum_casual_rider_df(df):
    sum_casual_rider_df = day_df.groupby("month").casual_rider.sum().sort_values(ascending=False).reset_index()
    return sum_casual_rider_df

def create_season_rider_df(df):
    season_rider_df = day_df.groupby("season").total_rider.sum().sort_values(ascending=False).reset_index()
    return season_rider_df

# Dataframe
day_df = pd.read_csv("day_clean.csv")

#Date column should be datetime type
date_column = ["date"]
day_df.sort_values(by="date", inplace=True)
day_df.reset_index(inplace=True)
for column in date_column:
    day_df[column] = pd.to_datetime(day_df[column])

#Filter components
min_date = day_df["date"].min()
max_date = day_df["date"].max()

with st.sidebar:
    # Adding logo
    st.image("logo.png")

    # Retrieve start_date & end_date from date_input
    start_date, end_date = st.date_input(
        label='Range of Time', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["date"] >= str(start_date)) &
                (day_df["date"] <= str(end_date))]

sum_registered_rider_df = create_sum_registered_rider_df(main_df)
sum_casual_rider_df = create_sum_casual_rider_df(main_df)
season_rider_df = create_season_rider_df(main_df)

# Create dashboard
st.header("Bike Share Dashboard :sparkles:")

st.subheader("Bike Sharing Data")
st.dataframe(day_df)

#
st.subheader("Perbedaan antara pengendara langganan (registered) dengan pengendara biasa (casual) dalam mempengaruhi total penyewaan sepeda setiap bulan")
monthly_rider = pd.merge(
    left = sum_registered_rider_df,
    right = sum_casual_rider_df,
    how="left",
    left_on="month",
    right_on="month"
)

monthly_rider_type = monthly_rider.melt(id_vars="month", var_name="rider_type", value_name="total_rider")
plt.figure(figsize=(15, 6))
sns.barplot(data=monthly_rider_type, x="month", y="total_rider", hue="rider_type")
plt.ylabel(None)
plt.xlabel(None)
plt.title("Perbendaan Pengendara Langganan (Registered) dan Pengendara Biasa (Casual)")
st.pyplot(plt)

#Jumlah penyewaan sepeda berdasarkan musim
st.subheader("Dampak musim (springer, summer, fall, winter) mempengaruhi total penyewaan sepeda")

plt.figure(figsize=(15, 6))
sns.barplot(data=season_rider_df, x="season", y="total_rider", hue="total_rider")
plt.ylabel(None)
plt.xlabel(None)
plt.title("Jumlah Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(plt)

#
st.subheader("Performa penyewaan sepeda setiap bulan")
fig, ax = plt.subplots(figsize=(20,5))
sns.pointplot(data=day_df, x="month", y="total_rider", errorbar=None, ax=ax)
ax.set(title="Performa Penyewaan Sepeda Setiap Bulan")
ax.set_ylabel("Total Rider")
ax.set_xlabel("Month")
st.pyplot(fig)
