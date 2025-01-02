# TikTok Sentiment Analysis

A Python application that performs sentiment analysis on TikTok video comments, combining web scraping capabilities with natural language processing to analyze user sentiment.

🔗 Try it here: [TikTok Sentiment Analysis App](https://tiktok-sentiment-analysis.streamlit.app)

## Features

- Extracts video metadata and comments from TikTok videos
- Performs sentiment analysis on comments using TextBlob and VADER
- Provides sentiment classification (Positive, Negative, Neutral)
- Measures sentiment intensity (Strong, Moderate, Weak)
- Visualizes sentiment distribution through graphs
- Streamlit web interface for easy interaction

## Project Structure

- `sentiment_analysis.py`: Main application with Streamlit interface and sentiment analysis logic
- `scrapper.py`: TikTok data extraction module for comments and metadata

## Limitations

- Requires valid TikTok video URLs
- Subject to TikTok's API limitations
- English-focused sentiment analysis (falls back to English for other languages)

<!--## License

MIT License-->

## Disclaimer

This tool is for educational purposes only. Users are responsible for compliance with TikTok's terms of service and API usage policies.
