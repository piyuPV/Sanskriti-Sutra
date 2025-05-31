import streamlit as st
from streamlit_calendar import calendar
import pandas as pd
from datetime import datetime as dt
import os

def culturalCalendar():
    st.title("🇮🇳 Indian Festival Calendar")

    try:
        festivals_df = pd.read_csv("assets/fest.csv", encoding='utf-8')

        calendar_events = []
        festival_colors = {
            'Religious': {'color': '#FF9F1C', 'emoji': '🕉️'},
            'Cultural': {'color': '#2EC4B6', 'emoji': '🎨'},
            'National': {'color': '#E71D36', 'emoji': '🎌'}
        }

        # Build calendar event list
        for _, row in festivals_df.iterrows():
            try:
                festival_name = row['Festival Name']
                date_str = f"{row['Date']} {row['Year']}"
                event_date = dt.strptime(date_str, "%B %d %Y")

                if str(row['Cultural Festival']).strip().lower() == 'yes':
                    festival_type = 'Cultural'
                elif any(word in festival_name.lower() for word in ['diwali', 'eid', 'christmas', 'guru', 'jayanti', 'puja', 'navratri']):
                    festival_type = 'Religious'
                elif any(word in festival_name.lower() for word in ['republic', 'independence', 'gandhi']):
                    festival_type = 'National'
                else:
                    festival_type = 'Religious'

                description = str(row['Description']).strip() if 'Description' in row else f"Celebrated on {row['Day']}, {row['Date']} {row['Year']}"

                calendar_events.append({
                    "title": f"{festival_colors[festival_type]['emoji']} {festival_name}",
                    "start": event_date.strftime("%Y-%m-%d"),
                    "end": event_date.strftime("%Y-%m-%d"),
                    "backgroundColor": festival_colors[festival_type]['color'],
                    "textColor": "#FFFFFF",
                    "extendedProps": {
                        "name": festival_name,
                        "type": festival_type,
                        "day": row['Day'],
                        "description": description,
                        "date": event_date.strftime("%d %B %Y")
                    }
                })
            except Exception as e:
                st.warning(f"Error processing: {row.get('Festival Name', 'Unknown')} - {str(e)}")

        calendar_options = {
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "dayGridMonth,dayGridYear"
            },
            "initialView": "dayGridMonth",
            "selectable": True,
            "height": 650
        }

        st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
        selected_event = calendar(events=calendar_events, options=calendar_options)

        if selected_event and selected_event.get("callback") == "eventClick":
            props = selected_event.get("event", {}).get("extendedProps", {})
            st.write("DEBUG - extendedProps:", props)

            festival_name = props.get("name", "").strip()
            image_name = festival_name.lower().replace(" ", "_") + ".png"
            image_path = f"assets/{image_name}"

            cols = st.columns([1, 3])
            with cols[0]:
                if os.path.exists(image_path):
                    st.image(image_path, width=160)
                else:
                    st.image("assets/ganesh.png", caption="Default Image", width=160)

            with cols[1]:
                st.markdown(f"""
                    ### {festival_name}
                    **Type:** {props.get('type', '')}  
                    **Day:** {props.get('day', '')}  
                    **Date:** {props.get('date', '')}  
                    **Description:**  
                    {props.get('description', '')}
                """)
        else:
            st.info("ℹ️ Click on a **festival event** (not a date) to view its details.")



        # Legend
        st.markdown("""
            <div style='background: rgba(255,255,255,0.1); 
                       padding: 15px; 
                       border-radius: 10px;
                       margin-top: 20px;
                       color: #E8B04B;'>
                <h4>Festival Types</h4>
                <p>🕉️ Religious Festivals</p>
                <p>🎨 Cultural Festivals</p>
                <p>🎌 National Festivals</p>
            </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error loading festival data: {str(e)}")
        st.write("Please check if the `fest.csv` file exists and is properly formatted.")
