import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_calendar import calendar
from events import events  

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
