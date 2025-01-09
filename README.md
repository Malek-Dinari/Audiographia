Audiographia
============

Audiographia is a Python-based application that generates a weekly chart of your favorite music based on your Last.fm scrobbling data. Whether you're curious about your listening trends or want to visually showcase your top artists, Audiographia provides an intuitive and educational way to explore your music habits.

Features
--------

-   Fetches your top artists from Last.fm over the last 7 days.

-   Visualizes your weekly music data as a horizontal bar chart.

-   Saves the chart as an image file for sharing or personal archiving.

-   Easy to deploy using tools like Streamlit, Gradio, or Vercel.

Getting Started
---------------

### Prerequisites

-   Python 3.7 or higher

-   A Last.fm account

-   A Last.fm API key (register at Last.fm API)

### Installation

1.  Clone the repository:

    ```
    git clone https://github.com/your-username/Audiographia.git
    cd Audiographia
    ```

2.  Install the required Python libraries:

    ```
    pip install requests matplotlib
    ```

3.  Replace `YOUR_LASTFM_API_KEY` in the script with your own Last.fm API key.

### Usage

1.  Run the script:

    ```
    python audiographia.py
    ```

2.  The application will fetch your top artists from the last 7 days and generate a bar chart.

3.  The chart will be saved as `<username>_weekly_chart.png` in the current directory.

Example
-------

Future Plans
------------

-   Deploy Audiographia to a web interface using Streamlit or Gradio for user-friendly access.

-   Add support for additional time periods (e.g., monthly, yearly).

-   Include more customizable visualization options.

-   Explore integration with other music platforms like Spotify.

Contributing
------------

Contributions are welcome! Feel free to fork the repository and submit a pull request with your improvements.

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
---------------

-   Last.fm API for providing the data.

-   The Python open-source community for libraries like Matplotlib and Requests.

* * * * *

Happy listening and exploring with **Audiographia**! 🎵
