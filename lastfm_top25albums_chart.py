import os
import requests
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Load API key
load_dotenv()
API_KEY = os.getenv("LASTFM_API_KEY")

if not API_KEY:
    st.error("API key not found! Please set LASTFM_API_KEY in your environment or .env file.")

BASE_URL = "http://ws.audioscrobbler.com/2.0/"

# Fallback placeholder image
PLACEHOLDER_URL = "https://via.placeholder.com/300?text=No+Image"

# Function to fetch user-specific top albums
def fetch_top_albums(user, limit=25, period="7day"):
    params = {
        "method": "user.gettopalbums",
        "user": user,
        "api_key": API_KEY,
        "format": "json",
        "limit": limit,
        "period": period,
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

# Function to extract image URLs and album titles
def extract_images(data):
    albums = data.get("topalbums", {}).get("album", [])
    images = []
    for album in albums:
        title = album.get("name", "Unknown Album")
        artist = album.get("artist", {}).get("name", "Unknown Artist")
        image_url = album.get("image", [{}])[-1].get("#text", PLACEHOLDER_URL)  # Fetch the largest image or placeholder
        images.append((f"{title} by {artist}", image_url))
    return images

# Function to display a customizable grid of album images
def create_image_grid(images, period, grid_size):
    st.markdown(
        "<h1 style='text-align: center; font-size: 50px;'>Audiographia: User-Specific Music Grid</h1>",
        unsafe_allow_html=True
    )

    fig, axes = plt.subplots(grid_size, grid_size, figsize=(grid_size * 3, grid_size * 3))
    for ax, (title, url) in zip(axes.flatten(), images):
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
        except Exception:
            response = requests.get(PLACEHOLDER_URL)
            img = Image.open(BytesIO(response.content))
        
        ax.imshow(img)
        ax.axis("off")
        ax.set_title(title, fontsize=8, wrap=True, pad=5, loc='center')

    for ax in axes.flatten()[len(images):]:
        ax.axis("off")

    fig.suptitle(f"Top Albums ({period})", fontsize=24, fontweight='bold')
    fig.subplots_adjust(hspace=0.6, wspace=0.3)
    st.pyplot(fig)

    # Save option
    save_path = "grid_output.png"
    fig.savefig(save_path, dpi=300)
    st.markdown(f"[Download the grid as an image]({save_path})")

# Streamlit App
st.title("Audiographia: User-Specific Music Grid")

username = st.text_input("Enter your Last.fm username:")
time_period = st.radio("Select a time period:", ("7 days", "1 month", "3 months", "6 months", "1 year", "Overall"))
grid_size = st.slider("Select grid size (e.g., 5x5):", min_value=2, max_value=7, value=5)

if st.button("Generate Grid"):
    if username:
        try:
            # Convert period to Last.fm format
            period_map = {
                "7 days": "7day",
                "1 month": "1month",
                "3 months": "3month",
                "6 months": "6month",
                "1 year": "12month",
                "Overall": "overall",
            }
            period = period_map[time_period]
            data = fetch_top_albums(username, limit=grid_size**2, period=period)
            images = extract_images(data)
            if images:
                create_image_grid(images, time_period, grid_size)
            else:
                st.warning("No albums found for this user in the selected time period.")
        except Exception as e:
            st.error(f"Error fetching data: {e}")
    else:
        st.error("Please enter a Last.fm username.")
