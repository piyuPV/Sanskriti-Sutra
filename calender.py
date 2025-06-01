import streamlit as st
import pandas as pd
from dateutil import parser
import re
from streamlit_calendar import calendar
from datetime import datetime
from PIL import Image
import os
from utils import get_translation


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
    st.title(get_translation("festival_calendar_title"))

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

    # --- Show details if a festival is clicked ---
    if selected and 'eventClick' in selected:
        event_data = selected['eventClick']['event']
        title = event_data['title']

        if title in df['Festival Name'].values:
            fest = df[df['Festival Name'] == title].iloc[0]

            # Create two columns for image and details
            col1, col2 = st.columns([1, 1])

            with col1:
                # Show image
                image_path = f"assets/calendar/{fest['ImageFile']}.jpg"
                if os.path.exists(image_path):
                    img = Image.open(image_path)
                    st.image(img, use_container_width=True)
                else:
                    st.warning(f"Image not found for {fest['Festival Name']}")

            with col2:
                # Show details in a styled container
                st.markdown("""
                    <style>
                    .festival-details {
                        background-color: rgba(255,255,255,0.1);
                        padding: 20px;
                        border-radius: 10px;
                        margin: 20px 0;
                        color: white;
                    }
                    </style>
                """, unsafe_allow_html=True)
                   
                # st.markdown('<div class="festival-details">', unsafe_allow_html=True)
                st.markdown(f"### {get_translation('festival_details')}")
                st.markdown(f"**{get_translation('festival_type')}:** {get_translation('cultural_festival') if fest['Cultural Festival'] == 'Yes' else get_translation('religious_festival')}")
                st.markdown(f"**Date:** {fest['ParsedDate'].strftime('%Y-%m-%d')}")
                st.markdown(f"**Day:** {fest['Day']}")
                st.markdown(f"**Description:** {fest['Description']}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error(f"Festival '{title}' not found in data.")
    else:
        st.info("📅 Click on a festival from the calendar to view its details.")

