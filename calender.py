import streamlit as st
from streamlit_calendar import calendar
import pandas as pd
from datetime import datetime

def culturalCalendar():
    st.title("Indian Cultural Calendar")
    
    # Read festival data from new CSV
    festivals_df = pd.read_csv("assets/festivalCalendar.csv")
    
    # Create events list
    calendar_events = []
    
    # Color scheme for different festival types
    colors = {
        "Yes": "#FF9F1C",  # Cultural festivals
        "No": "#2EC4B6"    # Other festivals
    }
    
    # Convert festivals to calendar events
    for _, row in festivals_df.iterrows():
        date_str = f"{row['Date']} {row['Year']}"
        date = datetime.strptime(date_str, "%B %d %Y")
        
        calendar_events.append({
            "title": row['Festival name'],
            "start": date.strftime("%Y-%m-%d"),
            "end": date.strftime("%Y-%m-%d"),
            "display": "block",
            "backgroundColor": colors[row['Cultural Festival']],
            "extendedProps": {
                "type": "Cultural Festival" if row['Cultural Festival'] == "Yes" else "Festival",
                "day": row['Day'],
                "description": f"Celebrated on {row['Day']}, {row['Date']} {row['Year']}"
            }
        })

    # Calendar options
    calendar_options = {
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,listWeek"
        },
        "initialView": "dayGridMonth",
        "selectable": True,
        "height": 600,
        "themeSystem": "bootstrap"
    }

    # Display calendar with events
    selected_event = calendar(events=calendar_events, options=calendar_options)

    # Display event details when selected
    if selected_event:
        with st.expander("Festival Details", expanded=True):
            st.markdown(f"""
                <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;'>
                    <h3>{selected_event.get('title', 'Festival')}</h3>
                    <p><b>Date:</b> {selected_event.get('start', '')}</p>
                    <p><b>Type:</b> {selected_event.get('extendedProps', {}).get('type', 'Festival')}</p>
                    <p>{selected_event.get('extendedProps', {}).get('description', '')}</p>
                </div>
            """, unsafe_allow_html=True)

    # Add legend
    st.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-top: 20px;'>
            <h4>Festival Types:</h4>
            <p>🟧 Cultural Festivals</p>
            <p>🟦 Other Festivals</p>
        </div>
    """, unsafe_allow_html=True)
