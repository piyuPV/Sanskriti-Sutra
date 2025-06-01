import streamlit as st

# Set page config must be the first Streamlit command
st.set_page_config(page_title="Sanskriti Sutra", layout="wide")

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = 'en'

from translations import TRANSLATIONS
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
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');
        
        * {{
            font-family: 'Poppins', sans-serif !important;
            font-weight: 300 !important;
        }}
        
        .stApp {{
            background-image: url("data:image/png;base64,{get_base64_of_bin_file("assets/basab.jpg")}");
            background-attachment: fixed;
            background-size: cover;
            background-position: center;
        }}
        .big-font {{
            font-size: 50px !important;
            font-weight: 700 !important;
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
        
        .stMarkdown, .stText, .stSelectbox, .stRadio, div.stButton > button, .stTab {{
            font-family: 'Quicksand', sans-serif !important;
            font-weight: 600 !important;
        }}
        
        div[data-testid="stSidebarNav"] li div {{
            font-family: 'Quicksand', sans-serif !important;
            font-weight: 600 !important;
        }}

        .plotly-graph text {{
            font-family: 'Quicksand', sans-serif !important;
            font-weight: 600 !important;
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


def get_translation(key):
    """Get translation with fallback to English or key itself"""
    lang = st.session_state.language
    if lang in TRANSLATIONS:
        # Try to get translation in selected language
        translation = TRANSLATIONS[lang].get(key)
        if translation:
            return translation
        # Fallback to English if key not found in selected language
        if lang != 'en':
            translation = TRANSLATIONS['en'].get(key)
            if translation:
                return translation
    # Return key itself if no translation found
    return key

def streamlit_menu(example=1):
    if example == 1:
        with st.sidebar:
            # Add decorative header to sidebar
            st.markdown("""
                <div style='text-align: center; padding: 10px; margin-bottom: 20px; background: linear-gradient(135deg, rgba(0,0,0,0.6), rgba(139,69,19,0.6)); border-radius: 10px; border: 1px solid rgba(255,255,255,0.2);'>
                    <h1 style='color: #FFD700; text-shadow: 2px 2px 4px #000000; font-family: "Cormorant Garamond", serif; margin-bottom: 5px;'>
                        संस्कृति सूत्र
                    </h1>
                    <h2 style='color: #ffffff; text-shadow: 1px 1px 2px #000000; font-family: "Cormorant Garamond", serif; font-size: 24px; margin-bottom: 5px;'>
                        Sanskriti Sutra
                    </h2>
                    <p style='color: #E6E6FA; font-style: italic; font-size: 14px; margin: 5px 0;'>
                        Weaving India's Cultural Tapestry
                    </p>
                    <div style='border-top: 1px solid rgba(255,255,255,0.3); margin: 10px 0;'></div>
                </div>
            """, unsafe_allow_html=True)
            
            # Define menu options with exact keys matching translations
            menu_options = [
                "Home",
                "Cultural Calendar", 
                "Maps",
                "Art-form Gallery",
                "Journey Planner",
                "Learn and Play Quiz",
                "Chatbot"
            ]
            
            # Translate menu options if Hindi or Marathi is selected
            if st.session_state.language == 'hi':
                menu_options = [TRANSLATIONS['hi'].get(option, option) for option in menu_options]
            elif st.session_state.language == 'mr':
                menu_options = [TRANSLATIONS['mr'].get(option, option) for option in menu_options]
            
            selected = option_menu(
                menu_title=None,
                options=menu_options,
                icons=['house-fill', 'calendar-event-fill', 'geo-alt-fill', 'palette-fill', 'compass-fill', 'book-fill', 'chat-quote-fill'],
                menu_icon="bank",
                default_index=0,
            )
            
            st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
            
            # Language selector using radio buttons
            selected_lang = st.radio(
                "🌐 Select Language/भाषा निवडा/भाषा चुनें",
                options=["English", "मराठी", "हिंदी"],
                horizontal=True,
                index=0 if st.session_state.language == 'en' 
                      else 1 if st.session_state.language == 'mr'
                      else 2
            )
            
            # Update session state language
            st.session_state.language = ('en' if selected_lang == "English" 
                                       else 'mr' if selected_lang == "मराठी" 
                                       else 'hi')
            
            # Convert Hindi or Marathi selection back to English for routing
            if st.session_state.language == 'hi' or st.session_state.language == 'mr':
                reverse_translations = {v: k for k, v in TRANSLATIONS['hi' if st.session_state.language == 'hi' else 'mr'].items()}
                selected = reverse_translations.get(selected, selected)
                
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
    st.markdown(f'<p class="big-font">Sanskriti Sutra: Weaving India\'s Cultural Tapestry</p>', unsafe_allow_html=True)
    
    # Load datasets with proper encoding
    foreign_visits = pd.read_csv("assets/foreignVisit.csv", encoding='latin1')
    festivals = pd.read_csv("assets/festivals_kaggle.csv", encoding='latin1')
    quarterly_visitors = pd.read_csv("assets/Country Quater Wise Visitors.csv", encoding='latin1')
    places_data = pd.read_csv("assets/places.csv", encoding='latin1')  # Added encoding parameter

    # Create dashboard tabs with translated names
    tab1, tab2, tab3 = st.tabs([
        get_translation("visitor_analytics"),
        get_translation("cultural_insights"),
        get_translation("festival_calendar")
    ])
    
    with tab1:
        st.markdown("""
            <div class="custom-text">
                <h3>Tourism Analytics Dashboard</h3>
                <p>Explore the dynamic patterns of tourism across India through interactive visualizations. 
                The scatter map shows foreign visitor distribution, with circle size indicating visitor volume 
                and colors representing growth rate. Hover over points to see detailed statistics.</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2,1])
        
        with col1:
            st.markdown(f'<div class="custom-text"><h3>{get_translation("visitors_distribution")}</h3></div>', unsafe_allow_html=True)
            
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
            st.markdown("""
                <div class="custom-text">
                    <h3>Top Performing States</h3>
                    <p>Compare the leading states based on visitor metrics. The bar chart highlights 
                    the top 5 states, allowing analysis of foreign visitors, domestic tourists, 
                    and year-over-year growth rates.</p>
                </div>
            """, unsafe_allow_html=True)
            
            metric = st.radio(
                get_translation("select_metric"),
                [
                    get_translation("foreign_visitors"),
                    get_translation("domestic_visitors"),
                    get_translation("growth_rate")
                ]
            )
            
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
        st.markdown(f'<div class="custom-text"><h3>{get_translation("quarterly_trends")}</h3></div>', unsafe_allow_html=True)
        
        # Clean column names for quarterly data
        quarters = [col for col in quarterly_visitors.columns if 'quarter' in col.lower() and '2019' in col]
        
        # Country selector with search
        selected_country = st.selectbox(
            get_translation("select_country"),
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
            title=f"{get_translation('quarterly_visitors')} {selected_country} (2019)",
            xaxis_title=get_translation("quarter"),
            yaxis_title=get_translation("visitors_percentage")
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        # Additional visualization - Country comparison
        st.markdown("""
            <div class="custom-text">
                <h3>Cross-Country Tourism Analysis</h3>
                <p>Compare visitor patterns across multiple countries simultaneously. The line graph 
                enables identification of common trends, seasonal variations, and relative tourism 
                volumes between different nationalities.</p>
            </div>
        """, unsafe_allow_html=True)
        
        selected_countries = st.multiselect(
            get_translation("select_countries"),
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
            title=get_translation("country_wise_quarterly_comparison"),
            xaxis_title=get_translation("quarter"),
            yaxis_title=get_translation("visitors_percentage")
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    with tab2:
        st.markdown("""
            <div class="custom-text">
                <h3>Cultural Heritage Insights</h3>
                <p>Discover the rich tapestry of India's cultural heritage through interactive 
                visualizations. The maps and charts reveal the distribution of art forms, cultural 
                sites, and traditional practices across different regions.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f'<div class="custom-text"><h3>{get_translation("cultural_heritage_distribution")}</h3></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Art Forms Distribution
            art_forms = places_data[places_data['interest'].str.contains('Art|Culture|Heritage', na=False)]
            art_by_state = art_forms.groupby('state').size().reset_index(name='count')
            
            fig_art = px.bar(art_by_state.nlargest(10, 'count'), 
                           x='state', 
                           y='count',
                           title=get_translation('top_states_by_cultural_heritage'),
                           color='count',
                           color_continuous_scale='Oranges')
            st.plotly_chart(fig_art, use_container_width=True)

        with col2:
            # Interest Categories Distribution
            interest_dist = places_data['interest'].value_counts()
            fig_interest = px.pie(values=interest_dist.values, 
                                names=interest_dist.index,
                                title=get_translation('distribution_of_cultural_experiences'),
                                color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig_interest, use_container_width=True)

        # Cultural Experience Map
        st.markdown(f'<div class="custom-text"><h3>{get_translation("cultural_experience_map")}</h3></div>', unsafe_allow_html=True)
        
        selected_experience = st.selectbox(
            get_translation("select_cultural_experience"),
            places_data['interest'].unique()
        )
        
        filtered_places = places_data[places_data['interest'] == selected_experience]
        
        fig_map = px.scatter_mapbox(filtered_places,
                                  lat='latitude',
                                  lon='longitude',
                                  hover_name='popular_destination',
                                  hover_data=['city', 'state', 'google_rating'],
                                  color='google_rating',
                                  size_max=15,
                                  zoom=4,
                                  title=f'{get_translation("locations_for")} {selected_experience}',
                                  mapbox_style="carto-positron")
        st.plotly_chart(fig_map, use_container_width=True)

        # Responsible Tourism Metrics
        st.markdown(f'<div class="custom-text"><h3>{get_translation("sustainable_tourism_insights")}</h3></div>', unsafe_allow_html=True)
        
        col3, col4 = st.columns([1, 1])
        
        with col3:
            st.markdown("""
                <div class="custom-text">
                    <h3>Cultural Experience Accessibility</h3>
                    <p>Explore the accessibility of cultural experiences through price range analysis. 
                    The pie chart breaks down attractions by cost category, from free experiences to 
                    premium cultural offerings.</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Price Range Distribution
            price_bins = [0, 50, 200, 500, 1000, float('inf')]
            price_labels = ['Free', 'Budget', 'Moderate', 'Premium', 'Luxury']
            places_data['price_category'] = pd.cut(places_data['price_fare'], 
                                                 bins=price_bins, 
                                                 labels=price_labels)
            
            price_dist = places_data['price_category'].value_counts()
            fig_price = px.pie(values=price_dist.values,
                             names=price_dist.index,
                             title=get_translation('price_range_distribution'),
                             color_discrete_sequence=px.colors.sequential.Greens)
            st.plotly_chart(fig_price, use_container_width=True)

        with col4:
            st.markdown("""
                <div class="custom-text">
                    <h3>Experience Quality Metrics</h3>
                    <p>Analyze the quality of different cultural experiences through visitor ratings. 
                    The bar chart compares average ratings across various experience types, helping 
                    identify the most appreciated cultural attractions.</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Rating Distribution
            rating_dist = places_data.groupby('interest')['google_rating'].mean().sort_values(ascending=False)
            fig_rating = px.bar(rating_dist,
                              title=get_translation('average_ratings_by_experience_type'),
                              color=rating_dist.values,
                              color_continuous_scale='Viridis')
            st.plotly_chart(fig_rating, use_container_width=True)

    with tab3:
        # Festival Calendar
        st.markdown(f'<div class="custom-text"><h3>{get_translation("upcoming_festivals")}</h3></div>', unsafe_allow_html=True)
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

if selected == "Journey Planner":  # Fixed spelling to match the menu option
    journeyPlanner()

if selected == "Learn and Play Quiz":  
    learnQuiz()

if selected == "Chatbot":
    chatbot()