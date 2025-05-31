import streamlit as st
from utils import get_translation

def artFormGallery():
    st.title(get_translation("art_gallery_title"))

    images = [
    "assets/gallery/48.jpg",
    "assets/gallery/49.jpg",
    "assets/gallery/50.jpg",
    "assets/gallery/51.jpg",
    "assets/gallery/52.jpg",
    "assets/gallery/53.jpg",
    "assets/gallery/54.jpg",
    "assets/gallery/55.jpg",
    "assets/gallery/56.jpg",
    "assets/gallery/57.jpg",
    "assets/gallery/58.jpg",
    "assets/gallery/59.jpg",
    "assets/gallery/60.jpg",
    "assets/gallery/61.jpg",
    "assets/gallery/62.jpg",
    "assets/gallery/63.jpg",
    "assets/gallery/64.jpg",
    "assets/gallery/65.jpg",
    "assets/gallery/66.jpg",
    "assets/gallery/67.jpg",
    "assets/gallery/68.jpg",
    "assets/gallery/69.jpg",
    "assets/gallery/70.jpg",
    "assets/gallery/71.jpg",
    "assets/gallery/72.jpg",
    "assets/gallery/73.jpg",
    "assets/gallery/74.jpg",
    "assets/gallery/75.jpg",
    "assets/gallery/76.jpg",
    "assets/gallery/77.jpg",
    "assets/gallery/78.jpg",
    "assets/gallery/79.jpg",
    "assets/gallery/80.jpg",
    "assets/gallery/81.jpg",
    "assets/gallery/82.jpg",
    "assets/gallery/83.jpg",
    "assets/gallery/84.jpg",
    "assets/gallery/85.jpg",
    "assets/gallery/86.jpg",
    "assets/gallery/87.jpg",
    "assets/gallery/88.jpg",
    "assets/gallery/89.jpg"
]


    # Create columns dynamically based on images
    cols = st.columns(3)  # Create 3 columns

    # Display images in a grid
    for idx, image_path in enumerate(images):
        with cols[idx % 3]:  # Use modulo to cycle through columns
            try:
                st.image(image_path, caption=" ", use_container_width=True)
            except:
                st.error(get_translation("image_not_found"))

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