import streamlit as st

# List of cartoon image URLs
cartoon_images = [
    "assets\\ganesh.png",
    "assets\\ganesh.png",
    "assets\\ganesh.png",
    # Add more image URLs as needed
]

# Streamlit UI
# Streamlit UI
def main():

    # Display images in a gallery format
    col1, col2, col3 = st.columns(3)  # Adjust the number of columns as per layout preference

    for i, image_url in enumerate(cartoon_images):
        with eval(f"col{(i % 3) + 1}"):
            st.image(image_url, width=200, use_column_width='auto', caption=f"Image {i + 1}")

if __name__ == "__main__":
    main()