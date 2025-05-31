import streamlit as st
import pandas as pd
from datetime import datetime
import calendar
from dateutil import parser
import re

# Load and preprocess the data
df = pd.read_csv("assets/fest.csv")

# Combine Date and Year columns into a full date string
df['Date_Str'] = df['Date'].astype(str) + ' ' + df['Year'].astype(str)

# Parse date with fallback
clean_dates = []
for i, date_str in enumerate(df['Date_Str']):
    try:
        clean_date = parser.parse(date_str)
        clean_dates.append(clean_date)
    except Exception:
        st.warning(f"Skipping row {i} due to invalid date: {date_str}")
        clean_dates.append(None)

df['ParsedDate'] = clean_dates
df = df.dropna(subset=['ParsedDate'])

# Standardize column access
df['Name'] = df['Festival Name']
df['Type'] = df['Cultural Festival']
df['Description'] = df['Description']

# Dynamically generate image filenames from festival names
def sanitize_filename(name):
    return re.sub(r'\W+', '_', name.strip()).lower()

df['ImageFile'] = df['Name'].apply(sanitize_filename)

# Create a dictionary mapping each date to its event details
events_by_date = {row['ParsedDate'].date(): row for _, row in df.iterrows()}

st.title("🎉 Festival Calendar")

# Select a month and year
year = st.selectbox("Select Year", sorted(df['ParsedDate'].dt.year.unique()))
month = st.selectbox("Select Month", list(calendar.month_name)[1:])  # Jan to Dec

month_num = list(calendar.month_name).index(month)
month_calendar = calendar.monthcalendar(year, month_num)

# Render calendar grid
st.subheader(f"{month} {year}")
selected_date = None

days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
cols = st.columns(7)
for i, day in enumerate(days):
    cols[i].markdown(f"**{day}**")

for week in month_calendar:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day == 0:
            cols[i].markdown(" ")
        else:
            date_obj = datetime(year, month_num, day).date()
            if date_obj in events_by_date:
                if cols[i].button(f"🎉 {day}", key=str(date_obj)):
                    selected_date = date_obj
            else:
                cols[i].markdown(f"{day}")

# Show event details
if selected_date:
    event = events_by_date[selected_date]
    image_path = f"assets/{event['ImageFile']}.jpg"
    st.image(image_path, use_container_width=True)
    st.markdown(f"### {event['Name']}")
    st.markdown(f"**Type:** {event['Type']}")
    st.markdown(f"**Date:** {event['ParsedDate'].strftime('%Y-%m-%d')}")
    st.markdown(f"**Day:** {event['Day']}")
    st.markdown(f"**Description:** {event['Description']}")
