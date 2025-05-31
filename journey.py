import streamlit as st
import google.generativeai as genai
import folium
from streamlit_folium import folium_static
import pandas as pd
from geopy.geocoders import Nominatim
from artFormGallery import artFormGallery

# Configure Gemini API
genai.configure(api_key="AIzaSyDfbJhxX-_eirTsG_FyqhEKNI7Fq4GHNds")
model = genai.GenerativeModel('gemini-1.5-flash')

def get_route_suggestions(origin, destination, mode):
    prompt = f"""
    Suggest the best route from {origin} to {destination} via {mode} transportation.
    Include:
    1. Estimated time
    2. Major stops/landmarks
    3. Recommended stops for food/rest
    4. Cultural attractions along the way
    Format as a bulleted list.
    Keep it concise and clear.
    """
    response = model.generate_content(prompt)
    return response.text

def get_route_guidance(origin, destination, mode):
    prompt = f"""Provide a detailed travel route from {origin} to {destination} via {mode}. Include:
    1. Estimated time and distance
    2. Best route to take
    3. Major stops and landmarks
    4. Cultural attractions on the way
    Keep it concise and clear."""
    
    response = model.generate_content(prompt)
    return response.text

def get_coordinates(city_name):
    # Read CSV with proper encoding
    places_df = pd.read_csv("assets/places.csv", encoding='latin1')
    
    # Get coordinates from places_df first
    city_data = places_df[places_df['city'].str.contains(city_name, case=False, na=False)]
    
    if not city_data.empty:
        return float(city_data.iloc[0]['latitude']), float(city_data.iloc[0]['longitude'])
    
    # Fallback to geocoding if city not in CSV
    geolocator = Nominatim(user_agent="my_agent")
    try:
        location = geolocator.geocode(f"{city_name}, India")
        return location.latitude, location.longitude
    except:
        return None, None

def plot_route(origin_coords, dest_coords):
    # Create map centered between origin and destination
    center_lat = (origin_coords[0] + dest_coords[0]) / 2
    center_lon = (origin_coords[1] + dest_coords[1]) / 2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=5)
    
    # Add markers for origin and destination
    folium.Marker(
        origin_coords,
        popup='Origin',
        icon=folium.Icon(color='green', icon='info-sign')
    ).add_to(m)
    
    folium.Marker(
        dest_coords,
        popup='Destination',
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    # Draw line between points
    folium.PolyLine(
        locations=[origin_coords, dest_coords],
        weight=2,
        color='blue',
        opacity=0.8
    ).add_to(m)
    
    return m

def journeyPlanner():
    st.title("Journey Planner and Guide to your Cultural Journey")
    st.subheader("Explore the Rich Cultural Heritage of India")

    # Top 10 destinations data
    destinations = {
        "Delhi": {
            "images": ["assets/delhi/image1.jpg", "assets/delhi/image2.jpg", "assets/delhi/image3.jpg"],
            "region": "North India",
            "route": "Via NH44 and Delhi Airport (DEL)",
            "attractions": ["Red Fort", "Qutub Minar", "Humayun's Tomb"]
        },
        "Mumbai": {
            "images": ["assets/ganesh.png", "assets/ganesh.png", "assets/ganesh.png"],
            "region": "Maharashtra",
            "route": "Via Mumbai Airport (BOM)",
            "attractions": ["Gateway of India", "Marine Drive", "Elephanta Caves"]
        },
        "Varanasi": {
            "images": ["assets/varanasi/image1.jpg", "assets/varanasi/image2.jpg", "assets/varanasi/image3.jpg"],
            "region": "Uttar Pradesh",
            "route": "Via NH19 and Varanasi Airport (VNS)",
            "attractions": ["Ghats", "Kashi Vishwanath Temple", "Sarnath"]
        },
        "Agra": {
            "images": ["assets/ganesh.png", "assets/ganesh.png", "assets/ganesh.png"],
            "region": "Uttar Pradesh",
            "route": "Via Yamuna Expressway",
            "attractions": ["Taj Mahal", "Agra Fort", "Fatehpur Sikri"]
        },
        "Jaipur": {
            "images": ["assets/ganesh.png", "assets/ganesh.png", "assets/ganesh.png"],
            "region": "Rajasthan",
            "route": "Via NH48 and Jaipur Airport (JAI)",
            "attractions": ["Amber Fort", "City Palace", "Hawa Mahal"]
        },
        "Pune": {
            "images": ["assets/ganesh.png", "assets/ganesh.png", "assets/ganesh.png"],
            "region": "Maharashtra",
            "route": "Via Mumbai-Pune Expressway",
            "attractions": ["Shaniwar Wada", "Aga Khan Palace", "Dagdusheth Temple"]
        }
    }

    # Initialize session state
    if 'show_route_form' not in st.session_state:
        st.session_state.show_route_form = {}
    
    # Display destinations in rows
    for destination, data in destinations.items():
        st.markdown(f"###  📍 {destination}")
        
        cols = st.columns(3)
        for idx, image_path in enumerate(data["images"]):
            with cols[idx]:
                st.image(image_path, use_container_width=True, output_format='auto', 
                        caption=f"Image {idx+1}", width=300)
        
        # Create columns for buttons and info
        col_button1, col_button2, col_info = st.columns([1, 1, 3])
        
        with col_button1:
            if st.button(f"Route to {destination}", key=f"route_{destination}"):
                st.session_state.show_route_form[destination] = True

        with col_button2:
            if st.button(f"More Images", key=f"art_{destination}"):
                artFormGallery()
        
        # Show form if button was clicked
        if st.session_state.show_route_form.get(destination, False):
            with col_info:
                with st.form(key=f"route_form_{destination}"):
                    st.write("Plan your journey:")
                    origin = st.text_input("Your starting point:")
                    mode = st.radio("Mode of transport:", ["Road", "Train", "Flight"])
                    url = f"https://www.google.com/search?q={origin}+to+{destination}+{mode}&oq=mumbai+to+delhi&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyEggBEEUYORiRAhixAxiABBiKBTIHCAIQABiABDINCAMQABiRAhiABBiKBTIHCAQQABiABDIHCAUQABiABDIHCAYQABiABDIHCAcQABiABDIHCAgQABiABDIHCAkQABiABNIBCDQyODNqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8"
                    # Form submit button
                    
                    if st.form_submit_button("Get Route Details"):
                        if origin:
                            with st.spinner("Getting route details..."):
                                route_info = get_route_guidance(origin, destination, mode)
                                st.success("Route found!")
                                st.markdown(f"""
                                    <div style='background-color: rgba(0,0,0,0.7); padding: 15px; border-radius: 5px; color: white;'>
                                        <h4>🗺️ Journey Details</h4>
                                        <p><b>From:</b> {origin}</p>
                                        <p><b>To:</b> {destination}</p>
                                        <p><b>Mode:</b> {mode}</p>
                                        <pre style='color: white; white-space: pre-wrap;'>{route_info}</pre>
                                        <a href='{url}' target='_blank' rel='noopener noreferrer'>
                                            <button style='background-color: #FF6B6B; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-top: 10px;'>
                                                Book Now 🏨
                                            </button>
                                        </a>
                                    </div>
                                """, unsafe_allow_html=True)
                                
                                # Get coordinates
                                origin_coords = get_coordinates(origin)
                                dest_coords = get_coordinates(destination)
                                if all(origin_coords) and all(dest_coords):
                                    # Plot route on map                                    
                                    st.markdown("### Route Map")
                                    m = plot_route(origin_coords, dest_coords)
                                    folium_static(m)
                                
                                else:
                                    st.error("Could not find coordinates for one or both cities")
                        else:
                            st.error("Please enter starting point")
        
        st.markdown("---")

