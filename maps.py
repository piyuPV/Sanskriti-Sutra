import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
from folium.plugins import MarkerCluster, HeatMap, Draw
import json
from utils import get_translation  # Changed import

def maps():
    st.title(get_translation("maps_title"))

    # Add tabs for different map views
    tab1, tab2, tab3 = st.tabs([
        get_translation("heritage_sites"),
        get_translation("tourist_heatmap"),
        get_translation("custom_markers")
    ])

    with tab1:
        # Split into two columns
        col_left, col_right = st.columns([7,3])
        
        with col_left:
            # Load places data since we don't have heritage_df
            places_df = pd.read_csv("assets/places.csv", encoding='latin1')
            
            # Create base map
            m1 = folium.Map(location=[22.9734, 78.6569], zoom_start=5)
            
            # Add layer control
            layer_control = folium.LayerControl()
            
            # Create marker clusters for different categories
            heritage_cluster = MarkerCluster(name="Heritage Sites")
            temples_cluster = MarkerCluster(name="Temples")
            monuments_cluster = MarkerCluster(name="Monuments")
            
            # Filter and add heritage sites markers
            heritage_sites = places_df[places_df['interest'].str.contains('Heritage|Cultural', na=False)]
            temple_sites = places_df[places_df['interest'].str.contains('Religious|Temple|Spiritual', na=False)]
            monument_sites = places_df[places_df['interest'].str.contains('Monument|Fort|Palace', na=False)]
            
            # Add heritage markers
            for _, row in heritage_sites.iterrows():
                popup_html = f"""
                    <div style="width:200px">
                        <h4>{row['popular_destination']}</h4>
                        <p><b>Location:</b> {row['city']}, {row['state']}</p>
                        <p><b>Rating:</b> {row['google_rating']}⭐</p>
                        <p><b>Category:</b> {row['interest']}</p>
                    </div>
                """
                folium.Marker(
                    [row['latitude'], row['longitude']], 
                    popup=popup_html,
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(heritage_cluster)
            
            # Add temple markers
            for _, row in temple_sites.iterrows():
                popup_html = f"""
                    <div style="width:200px">
                        <h4>{row['popular_destination']}</h4>
                        <p><b>Location:</b> {row['city']}, {row['state']}</p>
                        <p><b>Rating:</b> {row['google_rating']}⭐</p>
                        <p><b>Category:</b> {row['interest']}</p>
                    </div>
                """
                folium.Marker(
                    [row['latitude'], row['longitude']], 
                    popup=popup_html,
                    icon=folium.Icon(color='purple', icon='home')
                ).add_to(temples_cluster)
            
            # Add monument markers
            for _, row in monument_sites.iterrows():
                popup_html = f"""
                    <div style="width:200px">
                        <h4>{row['popular_destination']}</h4>
                        <p><b>Location:</b> {row['city']}, {row['state']}</p>
                        <p><b>Rating:</b> {row['google_rating']}⭐</p>
                        <p><b>Category:</b> {row['interest']}</p>
                    </div>
                """
                folium.Marker(
                    [row['latitude'], row['longitude']], 
                    popup=popup_html,
                    icon=folium.Icon(color='orange', icon='building')
                ).add_to(monuments_cluster)
            
            # Add all clusters to map
            heritage_cluster.add_to(m1)
            temples_cluster.add_to(m1)
            monuments_cluster.add_to(m1)
            layer_control.add_to(m1)
            
            folium_static(m1, width=800, height=600)
        
        with col_right:
            st.markdown("""
                <div style='background-color: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;'>
                <h3 style='color: white;'>Site Details</h3>
                <div id="site-details" style='color: white;'>
                    Click on a marker to view details
                </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Display selected site info
            if 'selected_site' in st.session_state:
                st.markdown(f"""
                    <div style='color: white;'>
                    <h4>{st.session_state.selected_site['name']}</h4>
                    <p><b>Location:</b> {st.session_state.selected_site['location']}</p>
                    <p><b>Category:</b> {st.session_state.selected_site['category']}</p>
                    </div>
                """, unsafe_allow_html=True)

    with tab2:
        # Create heatmap from tourist data
        m2 = folium.Map(location=[22.9734, 78.6569], zoom_start=5)
        
        # Filter places with high ratings
        tourist_spots = places_df[places_df['google_rating'] >= 4.0]
        
        # Create heatmap data
        heat_data = [[row['latitude'], row['longitude']] for idx, row in tourist_spots.iterrows()]
        
        # Add heatmap layer
        HeatMap(heat_data).add_to(m2)
        
        # Add draw control for custom annotations
        draw = Draw(
            draw_options={
                'polyline': True,
                'rectangle': True,
                'circle': True,
                'marker': True,
                'circlemarker': False
            },
            edit_options={'edit': True}
        )
        draw.add_to(m2)
        
        folium_static(m2, width=1200, height=600)

    with tab3:
        # Custom marker placer
        st.write(get_translation("add_custom_markers"))
        
        # File uploader for custom locations
        uploaded_file = st.file_uploader(get_translation("upload_locations"), type="csv")
        
        m3 = folium.Map(location=[22.9734, 78.6569], zoom_start=5)
        
        if uploaded_file:
            custom_df = pd.read_csv(uploaded_file)
            for idx, row in custom_df.iterrows():
                folium.Marker(
                    [row['lat'], row['lon']],
                    popup=f"{row['name']}<br>{row['description']}",
                    icon=folium.Icon(color='green')
                ).add_to(m3)
        
        # Manual marker placement
        st.write(get_translation("or_add_manually"))
        col1, col2, col3 = st.columns(3)
        with col1:
            lat = st.number_input("Latitude", -90.0, 90.0, 22.9734)
        with col2:
            lon = st.number_input("Longitude", -180.0, 180.0, 78.6569)
        with col3:
            name = st.text_input(get_translation("location_name"))
            
        if st.button(get_translation("add_marker")):
            folium.Marker(
                [lat, lon],
                popup=name,
                icon=folium.Icon(color='blue')
            ).add_to(m3)
            
        folium_static(m3, width=1200, height=600)

    # Add legend and instructions
    st.markdown(f"""
        <div style='background-color: rgba(255,255,255,0.2); padding: 10px; border-radius: 5px;'>
        <h3>{get_translation("map_features")}</h3>
        <ul>
            <li>🔴 Heritage Sites - Historical and cultural landmarks</li>
            <li>🔵 Custom Markers - Your added locations</li>
            <li>🌡️ Heatmap - Popular tourist destinations</li>
            <li>✏️ Draw Tools - Create custom shapes and routes</li>
        </ul>
        <p>Use the tabs above to switch between different map views.</p>
        </div>
    """, unsafe_allow_html=True)
