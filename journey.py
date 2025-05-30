import streamlit as st

def journeyPlanner():
    st.title("Journey Planner")
    
    st.markdown("""
    <div class="custom-text">
        <h3>Plan Your Cultural Journey</h3>
        <p>Use our journey planner to explore cultural sites, events, and experiences across India.</p>
        <p>Enter your preferences below to get started:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input fields for journey planning
    start_location = st.text_input("Starting Location", placeholder="Enter your starting point")
    destination = st.text_input("Destination", placeholder="Enter your destination")
    travel_date = st.date_input("Travel Date")
    
    if st.button("Plan Journey"):
        if start_location and destination:
            st.success(f"Journey planned from {start_location} to {destination} on {travel_date}.")
        else:
            st.error("Please fill in all fields to plan your journey.")