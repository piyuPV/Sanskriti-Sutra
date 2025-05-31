import streamlit as st
import pandas as pd
from dateutil import parser
import re
from streamlit_calendar import calendar
from datetime import datetime
from PIL import Image
import os


# --- Load data ---
def culturalCalendar():
    df = pd.read_csv("assets/fest.csv")

    # Combine date + year and parse
    df['Date_Str'] = df['Date'].astype(str) + ' ' + df['Year'].astype(str)
    def safe_parse(date_str):
        try:
            return parser.parse(date_str)
        except:
            return None
    df['ParsedDate'] = df['Date_Str'].apply(safe_parse)
    df = df.dropna(subset=['ParsedDate'])

    # Create image-safe file names
    def sanitize_filename(name):
        return re.sub(r'\W+', '_', name.strip()).lower()
    df['ImageFile'] = df['Festival Name'].apply(sanitize_filename)

    # Build calendar events
    events = []
    for _, row in df.iterrows():
        events.append({
            "title": row['Festival Name'],
            "start": row['ParsedDate'].strftime('%Y-%m-%d'),
            "allDay": True
        })

    # --- Streamlit UI ---
    st.title("🎊 Indian Festival Calendar")

    calendar_options = {
        "initialView": "dayGridMonth",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,dayGridYear"
        },
        "height": 650,
    }

    selected = calendar(events=events, options=calendar_options)
    # st.write("Selected Event Object:", selected)

    # --- Show details if a festival is clicked ---
    # --- Show details if a festival is clicked ---
    if selected and 'eventClick' in selected:
        event_data = selected['eventClick']['event']
        title = event_data['title']

        if title in df['Festival Name'].values:
            fest = df[df['Festival Name'] == title].iloc[0]

            # Show image
            image_path = f"assets/{fest['ImageFile']}.jpg"
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((500, 500))
                st.image(img)
            else:
                st.warning(f"Image not found for {fest['Festival Name']}")


            # Show details
            st.markdown(f"### {fest['Festival Name']}")
            st.markdown(f"**Type:** {fest['Cultural Festival']}")
            st.markdown(f"**Date:** {fest['ParsedDate'].strftime('%Y-%m-%d')}")
            st.markdown(f"**Day:** {fest['Day']}")
            st.markdown(f"**Description:** {fest['Description']}")
        else:
            st.error(f"Festival '{title}' not found in data.")
    else:
        st.info("📅 Click on a festival from the calendar to view its details.")

