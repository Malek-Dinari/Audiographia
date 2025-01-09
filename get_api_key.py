import os

API_KEY = os.getenv("LASTFM_API_KEY")

if not API_KEY:
    raise ValueError("No API key found! Set the LASTFM_API_KEY environment variable.")