import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def get_best_performing_day(df):
    best_performing_day_df = day_df.sort_values(by="cnt", ascending=False).reset_index()
    return best_performing_day_df

def create_yearly_rental_df(df):
    yearly_rental_df = df.groupby(by="yr").agg({
    "casual": "sum",
    "registered": "sum",
    "cnt": "sum"
    }).reset_index()

    return yearly_rental_df

def create_monthly_rental_df(df, year):
    monthly_rental_df = df[df.yr == year].groupby(by="mnth").agg({
    "casual": "sum",
    "registered": "sum",
    "cnt": "sum"
    }).reset_index()

    return monthly_rental_df

def create_workingday_hourly_df(df):
    workingday_hourly_df = df.groupby(by=["workingday", "hr"]).agg({
    "cnt": "mean"
    }).reset_index()

    return workingday_hourly_df

def get_users_percentage(df):
    total_count = df["cnt"].sum()
    total_casual = df["casual"].sum()
    total_registered = df["registered"].sum()

    casual_percentage = (total_casual/total_count) * 100
    registered_percentage = (total_registered/total_count) * 100

    return casual_percentage, registered_percentage

def create_season_df(df):
    season_df = df.groupby(by="season").agg({
    "cnt": "sum"
    }).reset_index()

    return season_df

def create_weekday_df(df):
    weekday_df = df.groupby(by="weekday").agg({
    "cnt": "mean"
    }).reset_index()

    return weekday_df

def create_workingday_df(df):
    workingday_df = df.groupby(by="workingday").agg({
    "cnt": "sum"
    }).reset_index()

    return workingday_df

def create_weathersit_df(df):
    weathersit_df = day_df.groupby(by="weathersit").agg({
    "cnt": "mean"
    }).reset_index()

    return weathersit_df

day_df = pd.read_csv("dashboard/main_day.csv")
hour_df = pd.read_csv("dashboard/main_hour.csv")

st.markdown("# Proyek Analisis Data: Bike Sharing Dataset :bike:")

best_performing_day = get_best_performing_day(day_df)
yearly_rental_df = create_yearly_rental_df(day_df)
monthly_rental_2011_df = create_monthly_rental_df(day_df, 0)
monthly_rental_2012_df = create_monthly_rental_df(day_df, 1)
workingday_hourly_df = create_workingday_hourly_df(hour_df)
users_percentage = get_users_percentage(day_df)
season_df = create_season_df(day_df)
weekday_df = create_weekday_df(day_df)
workingday_df = create_workingday_df(day_df)
weathersit_df = create_weathersit_df(day_df)

tab1, tab2, tab3 = st.tabs(["Business Performance", "Users Comparison", "Clustering"])

with tab1:
    st.markdown("## Business Performance")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### :sparkles: Best Performing Day :sparkles:")
        st.metric(label=str(best_performing_day["dteday"].iloc[0]), value=best_performing_day["cnt"].iloc[0])

    with col2:
        st.markdown("#### :thumbsdown: Worst Performing Day :thumbsdown:")
        st.metric(label=str(best_performing_day["dteday"].iloc[-1]), value=best_performing_day["cnt"].iloc[-1])


    fig, ax = plt.subplots(figsize=(4, 3))
    sns.barplot(data=yearly_rental_df, x="yr", y="cnt", color="#2c4773", ax=ax)

    ax.set_title("Performa Rental Sepeda per-Tahun", fontsize=8, fontweight="bold", fontfamily="sans-serif", color="#363535", pad=20)
    ax.set_xlabel("Tahun")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["2011", "2012"])
    ax.set_ylabel("Jumlah rental (juta)")
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x="mnth", y="cnt", data=monthly_rental_2011_df, marker="o", color="#2c4773")
    ax.set_title("Jumlah Rental Sepeda per Bulan (2011)", fontsize=12, fontweight="bold", fontfamily="sans-serif", color="#363535", pad=20)
    ax.set_xlabel("Month")
    ax.set_ylabel("Jumlah Rental")
    ax.set_xticks(ticks=monthly_rental_2011_df["mnth"], labels=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], rotation=45)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x="mnth", y="cnt", data=monthly_rental_2012_df, marker="o", color="#2c4773")
    ax.set_title("Jumlah Rental Sepeda per Bulan (2012)", fontsize=12, fontweight="bold", fontfamily="sans-serif", color="#363535", pad=20)
    ax.set_xlabel("Month")
    ax.set_ylabel("Jumlah Rental")
    ax.set_xticks(ticks=monthly_rental_2012_df["mnth"], labels=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], rotation=45)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(20, 6))
    sns.lineplot(data=workingday_hourly_df[workingday_hourly_df.workingday == 0], x="hr", y="cnt", marker="o", label="Non-Working Day", color="#a6c4de")
    sns.lineplot(data=workingday_hourly_df[workingday_hourly_df.workingday == 1], x="hr", y="cnt", marker="o", label="Working Day", color="#2c4773")
    ax.set_title("Rata-Rata Rental Sepeda per Jam pada Working Day dan Non-Working Day", fontsize=25, fontweight="bold", fontfamily="sans-serif", color="#363535", pad=20)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-Rata Rental")
    ax.set_xticks(ticks=workingday_hourly_df["hr"])
    st.pyplot(fig)

with tab2:
    st.markdown("## Users Comparison")
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.set_title("Perbandingan Casual dan Registered Users", fontsize=10, fontweight="bold", fontfamily="sans-serif", color="#363535")
    ax.pie(
        x=users_percentage,
        labels=("Casual", "Registered"),
        colors=("#a6c4de", "#2c4773"),
        autopct="%1.1f%%",
        explode=(0.1, 0)
    )
    st.pyplot(fig)

with tab3:
    st.markdown("## Clustering")
    
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(40, 20))
    sns.barplot(data=season_df, x="season", y="cnt", ax=ax[0], hue="season", legend=False,  palette=["#a6c4de", "#a6c4de", "#2c4773", "#a6c4de"])
    ax[0].set_title("Jumlah Rental Sepeda Berdasarkan Musim", fontsize=40, fontweight="bold", fontfamily="sans-serif", color="#363535", pad=20)
    ax[0].set_xlabel("Musim", size=40)
    ax[0].set_xticks(ticks=season_df["season"] - 1, labels=["Spring", "Summer", "Fall", "Winter"], fontsize=35)
    ax[0].set_ylabel("Jumlah Rental (juta)", size=40)
    ax[0].tick_params(axis='y', labelsize=35)

    sns.barplot(data=weekday_df, x="weekday", y="cnt", ax=ax[1], hue="weekday", legend=False, palette=["#a6c4de", "#a6c4de", "#a6c4de", "#a6c4de", "#a6c4de", "#2c4773", "#a6c4de"])
    ax[1].set_title("Jumlah Rental Sepeda Berdasarkan Weekday", fontsize=40, fontweight="bold", fontfamily="sans-serif", color="#363535", pad=20)
    ax[1].set_xlabel("Hari", size=40)
    ax[1].set_xticks(ticks=weekday_df["weekday"], labels=["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], rotation=45, fontsize=35)
    ax[1].set_ylabel("Rata-Rata Rental per Hari", size=40)
    ax[1].tick_params(axis='y', labelsize=35)
    st.pyplot(fig)

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(40, 20))
    sns.barplot(data=workingday_df, x="workingday", y="cnt", ax=ax[0], hue="workingday", legend=False,  palette=["#a6c4de", "#2c4773"])
    ax[0].set_title("Jumlah Rental Sepeda Berdasarkan Working Day", fontsize=35, fontweight="bold", fontfamily="sans-serif", color="#363535", pad=20)
    ax[0].set_xlabel("Hari", size=40)
    ax[0].set_xticks(ticks=workingday_df["workingday"], labels=["Non-Working Day", "Working Day"], fontsize=35)
    ax[0].set_ylabel("Jumlah Rental (juta)", size=40)
    ax[0].tick_params(axis='y', labelsize=35)

    sns.barplot(data=weathersit_df, x="weathersit", y="cnt", ax=ax[1], hue="weathersit", legend=False,  palette=["#2c4773", "#a6c4de", "#a6c4de"])
    ax[1].set_title("Jumlah Rental Sepeda Berdasarkan Weather Situation", fontsize=35, fontweight="bold", fontfamily="sans-serif", color="#363535", pad=20)
    ax[1].set_xlabel("Kondisi Cuaca", size=40)
    ax[1].set_xticks(ticks=weathersit_df["weathersit"] - 1, labels=["Clear", "Mist", "Rain"], fontsize=35)
    ax[1].set_ylabel("Rata-Rata Rental per Hari", size=40)
    ax[1].tick_params(axis='y', labelsize=35)
    st.pyplot(fig)