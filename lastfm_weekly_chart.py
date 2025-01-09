# Required Libraries
import requests
import matplotlib.pyplot as plt
from collections import Counter
import os


# Getting the env (local) lastfm api key
from get_api_key import API_KEY

# Last.fm API Key (Replace with your own API Key from Last.fm)
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

# Fetch Recent Tracks
def fetch_recent_tracks(username, period="7day", limit=50):
    params = {
        "method": "user.gettopartists",
        "user": username,
        "api_key": API_KEY,
        "format": "json",
        "period": period,
        "limit": limit
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Process Data and Plot
def create_chart(username, data):
    artists = []
    for artist in data.get("topartists", {}).get("artist", []):
        artists.append(artist["name"])

    artist_counts = Counter(artists)
    artist_names = list(artist_counts.keys())
    artist_plays = list(artist_counts.values())

    plt.figure(figsize=(10, 6))
    plt.barh(artist_names, artist_plays, color="skyblue")
    plt.xlabel("Play Count")
    plt.ylabel("Artists")
    plt.title(f"{username}'s Top Artists (Last 7 Days)")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(f"{username}_weekly_chart.png")
    print(f"Chart saved as {username}_weekly_chart.png")

# Main Function
def main():
    username = "Malek_Dinari"  # Replace with the username dynamically later
    print(f"Fetching data for {username}...")
    data = fetch_recent_tracks(username)

    if data:
        print("Creating chart...")
        create_chart(username, data)
    else:
        print("Failed to fetch data.")

if __name__ == "__main__":
    main()
