import streamlit as st
# Must be the first Streamlit command
st.set_page_config(layout="wide", page_title="Cultural Heritage Hub")
from streamlit_option_menu import option_menu
from streamlit_calendar import calendar
from events import events
from calender import culturalCalendar
import folium
from maps import maps
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




# Add background before the menu
add_bg_from_url()

if selected == "Home":
    home()

if selected == "Cultural Calendar":
    culturalCalendar()
    
if selected == "Maps":
    maps()

if selected == "Art-form Gallery":
    artFormGallery()

if selected == "Journery Planner":
    journeyPlanner()