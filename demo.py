import streamlit as st
from datetime import datetime, date
import calendar
import os
import base64

def get_image_as_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Verify assets directory exists
if not os.path.exists('assets'):
    os.makedirs('assets')
    st.warning("Created assets directory - please add your images there")

# Sample data with images - using absolute paths
date_images = {
    '2023-12-25': f"data:image/png;base64,{get_image_as_base64('assets/ganesh.png')}",
    '2023-10-31': f"data:image/png;base64,{get_image_as_base64('assets/ganesh.png')}",
    '2023-07-04': f"data:image/png;base64,{get_image_as_base64('assets/ganesh.png')}",
    '2023-02-14': f"data:image/png;base64,{get_image_as_base64('assets/ganesh.png')}"
}

# Sidebar controls
st.sidebar.header("Calendar Controls")
year = st.sidebar.number_input("Year", min_value=2000, max_value=2100, value=datetime.now().year)
month = st.sidebar.selectbox("Month", list(calendar.month_name[1:]), index=datetime.now().month-1)

# Get calendar data
cal = calendar.monthcalendar(year, list(calendar.month_name).index(month))

# CSS for calendar styling
st.markdown("""
<style>
.calendar {
    width: 100%;
    margin: 0 auto;
    font-family: Arial, sans-serif;
}
.calendar-header {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    text-align: center;
    font-weight: bold;
    margin-bottom: 10px;
}
.calendar-week {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    min-height: 80px;
    margin-bottom: 5px;
}
.calendar-day {
    border: 1px solid #e0e0e0;
    padding: 5px;
    position: relative;
}
.calendar-day.today {
    background-color: #fff8e1;
}
.calendar-day.other-month {
    color: #bdbdbd;
}
.calendar-day-number {
    position: absolute;
    top: 5px;
    right: 5px;
    font-weight: bold;
}
.calendar-day-image {
    margin-top: 20px;
    text-align: center;
}
.calendar-day-image img {
    max-width: 100%;
    max-height: 40px;
}
</style>
""", unsafe_allow_html=True)

# Generate calendar HTML
html = '<div class="calendar">'
html += '<div class="calendar-header">'
for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
    html += f'<div>{day}</div>'
html += '</div>'

today = datetime.now().date()

for week in cal:
    html += '<div class="calendar-week">'
    for i, day in enumerate(week):
        if day == 0:
            # Empty day (from previous/next month)
            html += '<div class="calendar-day other-month"></div>'
            continue
            
        date_str = f"{year}-{list(calendar.month_name).index(month):02d}-{day:02d}"
        css_class = "calendar-day"
        if date(year, list(calendar.month_name).index(month), day) == today:
            css_class += " today"
            
        html += f'<div class="{css_class}">'
        html += f'<div class="calendar-day-number">{day}</div>'
        
        if date_str in date_images:
            # Check if image exists
            if os.path.exists(date_images[date_str]):
                html += f'<div class="calendar-day-image"><img src="{date_images[date_str]}" alt="Event"></div>'
            else:
                st.error(f"Image not found at: {date_images[date_str]}")
                html += '<div class="calendar-day-image">⚠️ Image missing</div>'
            
        html += '</div>'
    html += '</div>'
html += '</div>'

# Display calendar
st.title(f"{month} {year}")
st.markdown(html, unsafe_allow_html=True)