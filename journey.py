import streamlit as st
import google.generativeai as genai
import folium
from streamlit_folium import folium_static
from artFormGallery import artFormGallery

# Configure Gemini API
genai.configure(api_key="YOURKEYY")
model = genai.GenerativeModel('gemini-1.5-flash')

def get_route_suggestions(origin, destination, mode):
    prompt = f"""
    Suggest the best route from {origin} to {destination} via {mode} transportation.
    Include:
    1. Estimated time
    2. Major stops/landmarks
    3. Recommended stops for food/rest
    4. Cultural attractions along the way
    5. Safety tips
    Format as a bulleted list.
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

def journeyPlanner():
    st.title("Journey Planner and Guide to your Cultural Journey")
    st.subheader("Explore the Rich Cultural Heritage of India")

    # Destinations data with multiple images per destination
    destinations = {
        "Delhi": {
            "images": ["assets/delhi/LotusDelhi.jpg", "assets/delhi/delhi.jpg", "assets/delhi/delhiminar.jpg"],
            "region": "North India",
            "route": "Via NH44 and Delhi Airport (DEL)",
            "attractions": ["Red Fort", "Qutub Minar", "Humayun's Tomb"]
        },
        "Varanasi": {
            "images": ["assets/ganesh.png", "assets/ganesh.png", "assets/ganesh.png"],
            "region": "North India",
            "route": "Via NH19 and Varanasi Airport (VNS)",
            "attractions": ["Ghats", "Temples", "Old City"]
        },
        "Jaipur": {
            "images": ["assets/ganesh.png", "assets/ganesh.png", "assets/ganesh.png"],
            "region": "North India",
            "route": "Via NH48 and Jaipur Airport (JAI)",
            "attractions": ["Amber Fort", "City Palace", "Hawa Mahal"]
        }
    }

    # Custom CSS for consistent image sizes
    st.markdown("""
        <style>
        .journey-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 10px;
            transition: transform 0.3s;
        }
        .journey-image:hover {
            transform: scale(1.05);
        }
        .button-container {
            display: flex;
            gap: 10px;
        }
        .stButton button {
            width: 100%;
            background-color: #2c3e50;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'show_route_form' not in st.session_state:
        st.session_state.show_route_form = {}
    
    # Display destinations in rows
    for destination, data in destinations.items():
        st.markdown(f"### {destination}")
        
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
                                    </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.error("Please enter starting point")
        
        st.markdown("---")
