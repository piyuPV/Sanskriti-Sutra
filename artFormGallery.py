import streamlit as st

def artFormGallery():
    st.title("Art Forms Gallery")

    images = [
        "assets/ganesh.png",
        "assets/ganesh.png",    
        "assets/ganesh.png",
        "assets/ganesh.png",
        "assets/ganesh.png",
        "assets/ganesh.png",
        "assets/ganesh.png",
        "assets/ganesh.png"
    ]

    # Create columns dynamically based on images
    cols = st.columns(3)  # Create 3 columns

    # Display images in a grid
    for idx, image_path in enumerate(images):
        with cols[idx % 3]:  # Use modulo to cycle through columns
            st.image(image_path, caption=f"Art Form {idx + 1}", use_container_width=True)
            
            # Add description under each image
            st.markdown("""
                <div style='background-color: rgba(0,0,0,0.7); padding: 10px; border-radius: 5px; margin: 5px 0; color: white;'>
                    <h4 style='margin:0;'>Art Form Details</h4>
                    <p style='margin:5px 0;'>Region: North India</p>
                    <p style='margin:5px 0;'>Style: Traditional</p>
                </div>
            """, unsafe_allow_html=True)

    # Add custom CSS for better spacing
    st.markdown("""
        <style>
        .stImage {
            margin-bottom: 10px;
        }
        img {
            border-radius: 10px;
            transition: transform 0.3s;
        }
        img:hover {
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)