import os
import requests
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

# Load API key
load_dotenv()
API_KEY = os.getenv("LASTFM_API_KEY")

if not API_KEY:
    st.error("API key not found! Please set LASTFM_API_KEY in your environment or .env file.")

BASE_URL = "http://ws.audioscrobbler.com/2.0/"

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
        image_url = album.get("image", [{}])[-1].get("#text", "")  # Fetch the largest image
        if image_url:
            images.append((f"{title} by {artist}", image_url))
    return images

# Function to display a 5x5 grid of album images
def create_image_grid(images, period):
    # Display the chart title with improved styling
    st.markdown(
        "<h1 style='text-align: center; font-size: 50px;'>Audiographia: User-Specific 5X5 Music Grid</h1>",
        unsafe_allow_html=True
    )
    
    fig, axes = plt.subplots(5, 5, figsize=(15, 15))
    for ax, (title, url) in zip(axes.flatten(), images):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        ax.imshow(img)
        ax.axis("off")
        ax.set_title(title, fontsize=8)
    # Disable unused axes if fewer than 25 albums
    for ax in axes.flatten()[len(images):]:
        ax.axis("off")
    
    fig.suptitle(f"Top Albums ({period})", fontsize=24, fontweight='bold')

    # Adjust grid spacing
    fig.subplots_adjust(hspace=0.5, wspace=0.5)
    st.pyplot(fig)

# Streamlit App
st.title("Audiographia: User-Specific 5X5 Music Grid")

username = st.text_input("Enter your Last.fm username:")
time_period = st.radio("Select a time period:", ("7 days", "1 month", "3 months", "6 months", "1 year", "Overall"))

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
            data = fetch_top_albums(username, period=period)
            images = extract_images(data)
            if images:
                create_image_grid(images, time_period)
            else:
                st.warning("No albums found for this user in the selected time period.")
        except Exception as e:
            st.error(f"Error fetching data: {e}")
    else:
        st.error("Please enter a Last.fm username.")
