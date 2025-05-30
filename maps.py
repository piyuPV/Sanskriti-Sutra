import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static


def maps():
    st.title("Cultural Art Forms Map")
    
    try:
        # Load data
        json1 = "assets//states_india.geojson"
        df = pd.read_csv("assets//foreignVisit.csv")

        # Clean and rename
        df.rename(columns={'States/UTs *': 'state_name', 'Foreign - 2019': 'foreign_visits'}, inplace=True)
        df['state_name'] = df['state_name'].str.strip()  # remove leading/trailing spaces

        # Create folium map
        m = folium.Map(location=[23.47, 77.94], tiles='CartoDB positron', name="Light Map",
                    zoom_start=5, attr="My Data attribution")

        # Create Choropleth layer using full state names
        folium.Choropleth(
            geo_data=json1,
            name="choropleth",
            data=df,
            columns=["state_name", "foreign_visits"],
            key_on="feature.properties.st_nm",  # match with geojson field
            fill_color="YlOrRd",
            fill_opacity=0.7,
            line_opacity=0.1,
            legend_name="Foreign Visits (2019)"
        ).add_to(m)

        # Optional: Add popup for state names
        folium.GeoJson(
            json1,
            name="States",
            popup=folium.GeoJsonPopup(fields=["st_nm"])
        ).add_to(m)

        # Display
        folium_static(m, width=1600, height=950)
    except Exception as e:
        st.error(f"Error loading map: {str(e)}")
