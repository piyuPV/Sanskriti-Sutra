import streamlit as st
# Set page config must be the first Streamlit command
st.set_page_config(page_title="DeVine", layout="wide")

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from learnQuiz import learnQuiz
from streamlit_option_menu import option_menu
from events import events
from calender import culturalCalendar
from journey import journeyPlanner
from artFormGallery import artFormGallery
import folium
from maps import maps
from chatbot import chatbot
from streamlit_folium import folium_static
# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
EXAMPLE_NO = 1


# Add custom CSS
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{get_base64_of_bin_file("assets/bg.avif")}");
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
                options=["Home", "Cultural Calendar", "Maps", "Art-form Gallery", "Journery Planner", "Learn and Play Quiz", "Chatbot"],  # required
                icons=['house-fill', 'calendar-event-fill', 'geo-alt-fill', 'palette-fill', 'compass-fill', 'book-fill','chat-quote-fill'],
                menu_icon="bank",  # optional
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
    st.markdown('<p class="big-font">Cultural Heritage Hub</p>', unsafe_allow_html=True)
    
    # Load datasets
    foreign_visits = pd.read_csv("assets/foreignVisit.csv")
    festivals = pd.read_csv("assets/festivals_kaggle.csv")
    quarterly_visitors = pd.read_csv("assets/Country Quater Wise Visitors.csv")

    # Create dashboard layout
    tab1, tab2 = st.tabs(["Visitor Analytics", "Festival Calendar"])
    
    with tab1:
        col1, col2 = st.columns([2,1])
        
        with col1:
            # Map visualization
            st.markdown('<div class="custom-text"><h3>Foreign Visitors Distribution</h3></div>', unsafe_allow_html=True)
            
            # Add year selector
            year = "2019"
            column_name = f"Foreign - {year}"
            
            fig = px.scatter_mapbox(foreign_visits, 
                                  lat="latitude", 
                                  lon="longitude",
                                  size=column_name,
                                  hover_name="States/UTs *",
                                  hover_data=[column_name],
                                  color="Growth rate - FTV 2019/18",
                                  zoom=3.5,
                                  mapbox_style="carto-positron")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Top 5 states
            st.markdown('<div class="custom-text"><h3>Top 5 States</h3></div>', unsafe_allow_html=True)
            metric = st.radio("Select Metric", ["Foreign Visitors", "Domestic Visitors", "Growth Rate"])
            
            if metric == "Foreign Visitors":
                column = "Foreign - 2019"
            elif metric == "Domestic Visitors":
                column = "Domestic - 2019"
            else:
                column = "Growth rate - FTV 2019/18"
                
            top_5 = foreign_visits.nlargest(5, column)
            fig2 = px.bar(top_5, 
                         x='States/UTs *', 
                         y=column,
                         title=f"Top 5 States by {metric}")
            st.plotly_chart(fig2, use_container_width=True)
        
        # Quarterly trends
        st.markdown('<div class="custom-text"><h3>Quarterly Visitor Trends by Country</h3></div>', unsafe_allow_html=True)
        
        # Clean column names for quarterly data
        quarters = [col for col in quarterly_visitors.columns if 'quarter' in col.lower() and '2019' in col]
        
        # Country selector with search
        selected_country = st.selectbox(
            "Select Country",
            quarterly_visitors['Country of Nationality'].unique(),
            index=0
        )
        
        # Get data for selected country
        country_data = quarterly_visitors[quarterly_visitors['Country of Nationality'] == selected_country]
        
        # Create quarterly trend visualization
        quarter_values = country_data[quarters].iloc[0].values
        quarter_labels = ['Q1', 'Q2', 'Q3', 'Q4']
        
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=quarter_labels, y=quarter_values))
        fig3.update_layout(
            title=f"Quarterly Visitors from {selected_country} (2019)",
            xaxis_title="Quarter",
            yaxis_title="Visitors %"
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        # Additional visualization - Country comparison
        st.markdown('<div class="custom-text"><h3>Country Comparison</h3></div>', unsafe_allow_html=True)
        selected_countries = st.multiselect(
            "Select Countries to Compare",
            quarterly_visitors['Country of Nationality'].unique(),
            default=quarterly_visitors['Country of Nationality'].unique()[:3]
        )
        
        comparison_data = quarterly_visitors[
            quarterly_visitors['Country of Nationality'].isin(selected_countries)
        ]
        
        fig4 = go.Figure()
        for country in selected_countries:
            country_data = comparison_data[
                comparison_data['Country of Nationality'] == country
            ]
            fig4.add_trace(go.Scatter(
                x=quarter_labels,
                y=country_data[quarters].iloc[0].values,
                name=country,
                mode='lines+markers'
            ))
            
        fig4.update_layout(
            title="Country-wise Quarterly Comparison (2019)",
            xaxis_title="Quarter",
            yaxis_title="Visitors %"
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    with tab2:
        # Festival Calendar
        st.markdown('<div class="custom-text"><h3>Upcoming Festivals</h3></div>', unsafe_allow_html=True)
        festivals['Date'] = pd.to_datetime(festivals['Date'] + ' ' + festivals['Year'].astype(str))
        current_festivals = festivals.sort_values('Date')[['Festival name', 'Date', 'Day']].head(10)
        st.dataframe(current_festivals, use_container_width=True)

    # Add custom CSS for dashboard
    st.markdown("""
        <style>
        .custom-text {
            background-color: rgba(0,0,0,0.7);
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            color: white;
        }
        .plotly-graph {
            background-color: rgba(255,255,255,0.9);
            border-radius: 10px;
            padding: 10px;
        }
        </style>
    """, unsafe_allow_html=True)




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

if selected == "Learn and Play Quiz":  
    learnQuiz()

if selected == "Chatbot":
    chatbot()