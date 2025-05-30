import streamlit as st
import folium
from streamlit_folium import folium_static

def maps():
    st.title("Cultural Heritage Map")
    
    # Extended list of Cultural landmarks in India
    landmarks = {
        "Taj Mahal": [27.1751, 78.0421, "Agra, Uttar Pradesh", "Mughal Architecture"],
        "Red Fort": [28.6562, 77.2410, "Delhi", "Mughal Fort"],
        "Qutub Minar": [28.5244, 77.1855, "Delhi", "Indo-Islamic Architecture"],
        "Humayun’s Tomb": [28.5933, 77.2507, "Delhi", "Mughal Architecture"],
        "Ajanta Caves": [20.5519, 75.7033, "Maharashtra", "Ancient Buddhist Art"],
        "Ellora Caves": [20.0268, 75.1794, "Maharashtra", "Rock-cut Architecture"],
        "Gateway of India": [18.9218, 72.8347, "Mumbai, Maharashtra", "Colonial Architecture"],
        "Khajuraho Temples": [24.8318, 79.9199, "Madhya Pradesh", "Temple Architecture"],
        "Sanchi Stupa": [23.4793, 77.7395, "Madhya Pradesh", "Buddhist Monument"],
        "Konark Sun Temple": [19.8876, 86.0945, "Odisha", "Ancient Architecture"],
        "Jagannath Temple": [19.8068, 85.8312, "Puri, Odisha", "Hindu Temple Architecture"],
        "Brihadeeswarar Temple": [10.7828, 79.1312, "Thanjavur, Tamil Nadu", "Chola Architecture"],
        "Meenakshi Temple": [9.9195, 78.1191, "Madurai, Tamil Nadu", "Dravidian Architecture"],
        "Hampi Monuments": [15.3350, 76.4600, "Karnataka", "Vijayanagara Architecture"],
        "Mysore Palace": [12.3052, 76.6552, "Karnataka", "Royal Architecture"],
        "Gol Gumbaz": [16.8302, 75.7116, "Bijapur, Karnataka", "Islamic Architecture"],
        "Charminar": [17.3616, 78.4747, "Hyderabad, Telangana", "Qutb Shahi Architecture"],
        "Golkonda Fort": [17.3833, 78.4011, "Hyderabad, Telangana", "Fortified Citadel"],
        "Rani ki Vav": [23.8561, 72.1019, "Patan, Gujarat", "Stepwell Architecture"],
        "Sun Temple, Modhera": [23.5937, 71.9999, "Gujarat", "Hindu Temple Architecture"],
        "Victoria Memorial": [22.5448, 88.3426, "Kolkata, West Bengal", "British Colonial Architecture"],
        "Howrah Bridge": [22.5850, 88.3468, "Kolkata, West Bengal", "Engineering Marvel"],
        "Mahabodhi Temple": [24.6951, 84.9916, "Bodh Gaya, Bihar", "Buddhist Temple"],
        "Nalanda University Ruins": [25.1357, 85.4439, "Bihar", "Ancient University"],
        "Shanti Stupa": [34.1717, 77.5852, "Leh, Ladakh", "Peace Pagoda"],
        "Leh Palace": [34.1653, 77.5848, "Leh, Ladakh", "Tibetan Architecture"]
    }
    
    # Create the base map with custom tiles parameter
    m = folium.Map(location=[22.9734, 78.6569], zoom_start=5, tiles=None)
    
    # Add tile layers in reverse order (first added becomes default)
    satellite = folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite View'
    ).add_to(m)
    
    street = folium.TileLayer(
        'OpenStreetMap',
        name='Street View'
    ).add_to(m)
    
    # Set satellite view as default
    satellite.add_to(m)

    # Add cultural landmarks
    for name, info in landmarks.items():
        html = f"""
        <div style="font-family: Arial; width: 180px;">
            <h4>{name}</h4>
            <p><b>Location:</b> {info[2]}</p>
            <p><b>Known for:</b> {info[3]}</p>
        </div>
        """
        
        folium.Marker(
            location=[info[0], info[1]],
            popup=folium.Popup(html, max_width=250),
            tooltip=name,
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Display map in Streamlit
    st.markdown("""
        <style>
        .folium-map { 
            width: 100%; 
            height: 100%;
            margin: 0 auto;
        }
        </style>
    """, unsafe_allow_html=True)
    
    folium_static(m, width=1200, height=600)
    
    # Add legend
    st.markdown("""
        <div style='background-color: rgba(255,255,255,0.7); padding: 10px; border-radius: 5px;'>
        <h3>Map Legend</h3>
        <p>🔴 Cultural Heritage Sites</p>
        <p>Use the layer control (top right) to switch between Street and Satellite views</p>
        </div>
    """, unsafe_allow_html=True)
