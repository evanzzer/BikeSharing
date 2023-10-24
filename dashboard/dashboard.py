import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Initialization
# Since it's already clean data, import original data
day_df = pd.read_csv('../data/day.csv')
hour_df = pd.read_csv('../data/hour.csv')

# Preparing Data
season_day_df = day_df.groupby("season").agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum',
}).reset_index().sort_values("season", ascending=False)
season_day_df.season.replace(1, "Spring", inplace=True)
season_day_df.season.replace(2, "Summer", inplace=True)
season_day_df.season.replace(3, "Autumn", inplace=True)
season_day_df.season.replace(4, "Winter", inplace=True)

season_hour_df = hour_df.groupby(["season", "hr"]).agg({
    'casual': 'mean',
    'registered': 'mean',
}).reset_index().sort_values(["season", "hr"])
season_hour_df.season.replace(1, "Spring", inplace=True)
season_hour_df.season.replace(2, "Summer", inplace=True)
season_hour_df.season.replace(3, "Autumn", inplace=True)
season_hour_df.season.replace(4, "Winter", inplace=True)

work_day_df = day_df.groupby("workingday").agg({
    'casual': 'mean',
    'registered': 'mean',
    'cnt': 'mean',
}).reset_index().sort_values("workingday")
work_day_df.workingday.replace(0, "Weekend", inplace=True)
work_day_df.workingday.replace(1, "Weekday", inplace=True)

work_hour_df = hour_df.groupby(["workingday", "hr"]).agg({
    'casual': 'mean',
    'registered': 'mean',
    'cnt': 'mean',
}).reset_index().sort_values(["workingday", "hr"])
work_hour_df.workingday.replace(0, "Weekend", inplace=True)
work_hour_df.workingday.replace(1, "Weekday", inplace=True)

# Streamlit Dashboard
st.header("Bike Sharing Report Analysis")

# Seasonal Daily
st.subheader("Seasonal Daily Bike Sharing Report")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

df = season_day_df.loc[season_day_df['cnt'] == season_day_df.cnt.max()].iloc[0]
with col1:
    st.metric("Peak Season", value=df['season'])

with col2:
    st.metric("Total", value=f"{df['cnt']:,}")

with col3:
    st.metric("Highest Casuals", value=f"{df['casual']:,}")

with col4:
    st.metric("Highest Registered", value=f"{df['registered']:,}")

fig, ax = plt.subplots(figsize=(16, 8))
season_day_df.drop(columns='cnt').set_index('season').plot(kind='barh', stacked=True, color=['blue', 'orange'], ax=ax)
plt.xlim(0, 1.2e6)
plt.grid()

st.pyplot(fig)

# Seasonal Hourly
st.subheader("Seasonal Hourly Bike Sharing Report")

fig, ax = plt.subplots(1, 2, figsize=(16, 8))

work_set = set(season_hour_df["season"])
for work in work_set:
    df = season_hour_df.loc[season_hour_df["season"] == work]
    ax[0].plot(df['hr'], df['casual'], label=work)
    ax[1].plot(df['hr'], df['registered'], label=work)

ax[0].grid()
ax[0].set_title("Average Casual Hourly Bike Rental Frequency")
ax[0].set_xlabel("Hour")
ax[0].set_ylabel("Casuals")
ax[0].set_xticks(range(0, 24))
ax[0].legend(loc="upper left")
ax[0].set_xlim(0, 23)

ax[1].grid()
ax[1].set_title("Average Registered Hourly Bike Rental Frequency")
ax[1].set_xlabel("Hour")
ax[1].set_ylabel("Registered")
ax[1].set_xticks(range(0, 24))
ax[1].legend(loc="upper left")
ax[1].set_xlim(0, 23)

st.pyplot(fig)

# Working Daily
st.subheader("Working Day Daily Bike Sharing Report")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.metric("Weekday Peak Time", value="8AM, 5PM")

with col2:
    st.metric("Weekend Peak Time", value="1PM")

with col3:
    df = work_day_df.loc[work_day_df["workingday"] == "Weekday"].iloc[0]["cnt"]
    st.metric("Highest Average Weekday", value=f"{int(round(df, 0)):,}")

with col4:
    df = work_day_df.loc[work_day_df["workingday"] == "Weekend"].iloc[0]["cnt"]
    st.metric("Highest Average Weekend", value=f"{int(round(df, 0)):,}")

fig, ax = plt.subplots(figsize=(16, 8))

work_day_df.drop(columns='cnt').set_index('workingday').plot(kind='barh', stacked=True, color=['blue', 'orange'], ax=ax)
plt.xlim(0, 5000)
plt.grid()

st.pyplot(fig)

# Working Hourly
st.subheader("Working Day Hourly Bike Sharing Report")
fig, ax = plt.subplots(1, 3, figsize=(20, 8))

work_set = set(work_hour_df["workingday"])
for work in work_set:
    df = work_hour_df.loc[work_hour_df["workingday"] == work]
    ax[0].plot(df['hr'], df['casual'], label=work)
    ax[1].plot(df['hr'], df['registered'], label=work)
    ax[2].plot(df['hr'], df['cnt'], label=work)

ax[0].grid()
ax[0].set_title("Average Casual Hourly Bike Rental Frequency")
ax[0].set_xlabel("Hour")
ax[0].set_ylabel("Casuals")
ax[0].set_xticks(range(0, 24))
ax[0].legend(loc="upper left")
ax[0].set_xlim(0, 23)

ax[1].grid()
ax[1].set_title("Average Registered Hourly Bike Rental Frequency")
ax[1].set_xlabel("Hour")
ax[1].set_ylabel("Registered")
ax[1].set_xticks(range(0, 24))
ax[1].legend(loc="upper left")
ax[1].set_xlim(0, 23)

ax[2].grid()
ax[2].set_title("Average Total Hourly Bike Rental Frequency")
ax[2].set_xlabel("Hour")
ax[2].set_ylabel("Total")
ax[2].set_xticks(range(0, 24))
ax[2].legend(loc="upper left")
ax[2].set_xlim(0, 23)

st.pyplot(fig)

# Footer
st.caption("Dicoding Made by Evans")
