import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_calendar import calendar
from events import events
import folium
from streamlit_folium import folium_static
# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
EXAMPLE_NO = 1


# Add custom CSS
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{get_base64_of_bin_file("image.png")}");
            background-attachment: fixed;
            background-size: cover;
            background-position: center;
        }}
        .big-font {{
            font-size: 50px !important;
            color: #fff;
            text-shadow: 2px 2px 4px #000;
        }}
        .custom-text {{
            color: #fff;
            background-color: rgba(0,0,0,0.7);
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    import base64
    return base64.b64encode(data).decode()


def streamlit_menu(example=1):
    if example == 1:
        # 1. as sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title=None,  # required
                options=["Home", "Cultural Calendar", "Maps", "Art-form Gallery", "Journery Planner"],  # required
                icons=["house", "calendar", "map"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
            )
        return selected

    if example == 2:
        # 2. horizontal menu w/o custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Home", "Cultural Calendar", "Maps", "Art-form Gallery", "Journery Planner"],  # required
            icons=["house", "book", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
        return selected

    if example == 3:
        # 2. horizontal menu with custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Home", "Cultural Calendar", "Maps", "Art-form Gallery", "Journery Planner"],  # required
            icons=["house", "book", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "rgba(0,0,0,0.7)"},
                "icon": {"color": "#gold", "font-size": "25px"},
                "nav-link": {
                    "font-size": "20px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#rgba(255,255,255,0.1)",
                    "color": "#fff"
                },
                "nav-link-selected": {"background-color": "#c17900"},
            },
        )
        return selected

selected = streamlit_menu(example=EXAMPLE_NO)

def home():
    st.markdown('<p class="big-font">Welcome to the Cultural Heritage Hub</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            '<div class="custom-text">'
            '<h3>Discover Traditional Art Forms</h3>'
            '<p>Immerse yourself in the rich tapestry of cultural heritage, '
            'from classical dance forms to ancient musical traditions.</p>'
            '</div>',
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            '<div class="custom-text">'
            '<h3>Upcoming Cultural Events</h3>'
            '<p>• Traditional Dance Festival - Dec 15</p>'
            '<p>• Art Exhibition - Dec 20</p>'
            '<p>• Cultural Workshop - Dec 25</p>'
            '</div>',
            unsafe_allow_html=True
        )


def culturalCalendar():
    st.title("Cultural Calendar")
    calendar_options = {
        "initialView": "dayGridMonth",
        "editable": True,
        "selectable": True,
        "eventContent": """function(arg) {
            let container = document.createElement('div');
            container.style.display = 'flex';
            container.style.alignItems = 'center';
            
            if (arg.event.extendedProps && arg.event.extendedProps.image) {
                let img = document.createElement('img');
                img.src = arg.event.extendedProps.image;
                img.style.width = '20px';
                img.style.height = '20px';
                img.style.marginRight = '5px';
                img.style.objectFit = 'cover';
                img.style.borderRadius = '50%';
                container.appendChild(img);
            }
            
            let title = document.createElement('span');
            title.innerText = arg.event.title;
            container.appendChild(title);
            
            return { domNodes: [container] };
        }""",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay"
        },
        "height": 600,
        "aspectRatio": 1.35
    }

    selected_event = calendar(events=events, options=calendar_options)

    if selected_event:
        st.write("Selected event:", selected_event)
        if "url" in selected_event:
            st.markdown(f"[View Event Details]({selected_event['url']})")


def maps():
    try:
        st.title("Traditional Art Forms Across India")
        
        # Add CSS to ensure map container is visible
        st.markdown("""
            <style>
                .folium-map {
                    width: 100%;
                    height: 500px;
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    z-index: 1;
                    background-color: white;
                }
                [data-testid="stVerticalBlock"] {
                    gap: 0px;
                }
            </style>
        """, unsafe_allow_html=True)
        
        # Create map with explicit width and height
        m = folium.Map(
            location=[20.5937, 78.9629],
            zoom_start=4,
            width='100%',
            height='100%'
        )
        
        # Art forms data for different states
        art_locations = [
            {"name": "Madhubani Painting", "state": "Bihar", "loc": [25.6838, 85.7977], 
             "desc": "Traditional folk art from Bihar, known for geometric patterns"},
            {"name": "Warli Art", "state": "Maharashtra", "loc": [19.7515, 75.7139], 
             "desc": "Tribal art form using basic geometric shapes"},
            {"name": "Kathakali", "state": "Kerala", "loc": [10.8505, 76.2711], 
             "desc": "Classical dance form with elaborate costumes"},
            {"name": "Tanjore Painting", "state": "Tamil Nadu", "loc": [11.1271, 78.6569], 
             "desc": "Classical painting style with gold foil overlays"},
            {"name": "Phad Painting", "state": "Rajasthan", "loc": [27.0238, 74.2179], 
             "desc": "Scroll painting depicting folk tales"},
            {"name": "Pattachitra", "state": "Odisha", "loc": [20.9517, 85.0985], 
             "desc": "Traditional cloth-based scroll painting"},
        ]
        
        # Debug information
        st.write("Map Status: Initializing...")
        
        # Display filters and map with adjusted column ratio
        col1, col2 = st.columns([4, 1])  # Adjusted ratio
        
        with col2:
            st.markdown("### Filter Art Forms")
            selected_states = st.multiselect(
                "Select States",
                options=list(set(art["state"] for art in art_locations)),
                default=list(set(art["state"] for art in art_locations))
            )
        
        with col1:
            # Show filtered map with container styling
            filtered_map = folium.Map(
                location=[20.5937, 78.9629],
                zoom_start=4,
                width=800,  # Explicit width
                height=600  # Explicit height
            )
            
            # Add markers
            for art in art_locations:
                if art['state'] in selected_states:
                    html = f"""
                        <div style='width: 200px'>
                            <h4>{art['name']}</h4>
                            <p><b>State:</b> {art['state']}</p>
                            <p>{art['desc']}</p>
                        </div>
                    """
                    folium.Marker(
                        location=art['loc'],
                        popup=folium.Popup(html, max_width=300),
                        tooltip=art['name'],
                        icon=folium.Icon(color='red', icon='info-sign')
                    ).add_to(filtered_map)
            
            # Debug information
            st.write("Rendering map...")
            
            # Render map with error handling
            try:
                folium_static(filtered_map, width=800, height=600)
                st.success("Map loaded successfully!")
            except Exception as e:
                st.error(f"Error rendering map: {str(e)}")
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.write("Please try refreshing the page.")

def artFormGallery():
    pass

def journeyPlanner():
    pass


# Add background before the menu
add_bg_from_url()

if selected == "Home":
    home()

if selected == "Cultural Calendar":
    culturalCalendar()
    
if selected == "maps":
    maps()

if selected == "Art-form Gallery":
    artFormGallery()

if selected == "Journery Planner":
    journeyPlanner()