# Jarvis – AI Desktop Assistant

Jarvis is a voice-controlled, AI-powered desktop personal assistant built with Python. It can perform a variety of tasks such as answering questions, fetching news and weather, controlling music playback, and managing system-level operations like shutdown, restart, and lock.

## Features

- **Voice Commands**: Wake word detection ("Jarvis") for hands-free operation.
- **System Control**: Shutdown, restart, lock screen, volume, and brightness control.
- **Web Shortcuts**: Quickly open Google, YouTube, and WhatsApp in your browser.
- **Weather Updates**: Get live weather information for any city using the OpenWeather API.
- **News Headlines**: Fetch the latest news headlines via NewsAPI.
- **Music Playback**: Play, pause, resume, and stop music using Spotify integration.
- **AI Q&A**: Ask questions and get intelligent answers using Perplexity/OpenAI.

## Setup

1. **Clone the repository** and navigate to the project directory.

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:  
   Create a `.env` file in the `JARVIS` directory with the following keys (see [.env](.env)):
    ```
    NEWSAPI_KEY=your_newsapi_key
    OPENROUTER_API_KEY=your_openrouter_api_key
    PERPLEXITY_API_KEY=your_perplexity_api_key
    SPOTIFY_CLIENT_ID=your_spotify_client_id
    SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
    SPOTIFY_REDIRECT_URI=your_spotify_redirect_uri
    OPENWEATHER_API_KEY=your_openweather_api_key
    ```

4. **Run Jarvis**:
    ```sh
    python jarvis_Main.py
    ```

## Usage

- Say "Jarvis" (or a wake phrase) to activate the assistant.
- Give commands such as:
    - "What is the weather in London?"
    - "Play [song name]"
    - "Open Google"
    - "Increase volume"
    - "Tell me the news"
    - "Shutdown the system"

## Project Structure

- [`jarvis_Main.py`](jarvis_Main.py): Main entry point and command processor.
- [`jarvis_controls.py`](jarvis_controls.py): System controls (volume, brightness, open apps).
- [`musiclibrary.py`](musiclibrary.py): Spotify music playback integration.
- [`weather.py`](weather.py): Weather fetching logic.
- `.env`: API keys and configuration (not tracked by git).

## Requirements

- Python 3.8+
- Microphone for voice input
- Internet connection for APIs

## APIs Used

- [OpenWeather](https://openweathermap.org/)
- [NewsAPI](https://newsapi.org/)
- [Spotify Web API](https://developer.spotify.com/)
- [Perplexity/OpenAI](https://www.perplexity.ai/)

## License

This project is for educational purposes.

---