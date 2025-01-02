import os
os.system('pip install requests')
import json
import re
import nltk
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from langdetect import detect
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import streamlit as st
from scrapper import TikTokExtractor

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

# Set page configuration
st.set_page_config(page_title="TikTok Comment Sentiment Analysis", layout="wide", page_icon="analysis.ico")

# Function to detect language and preprocess comment
def preprocess_comment_with_language_detection(comment):
    try:
        lang = detect(comment)
        stop_words = stopwords.words(lang) if lang in stopwords.fileids() else stopwords.words('english')
    except:
        stop_words = stopwords.words('english')

    comment = comment.lower()  # Lowercase
    comment = re.sub(r'[^a-zA-Z\s]', '', comment)  # Remove non-alphabetic characters
    tokens = word_tokenize(comment)  # Tokenize
    filtered_tokens = [word for word in tokens if word not in stop_words]  # Remove stopwords

    return filtered_tokens if filtered_tokens else ["unknown"]

# Function to perform sentiment analysis
def analyze_sentiment(comment):
    blob_analysis = TextBlob(comment)
    polarity = blob_analysis.sentiment.polarity
    subjectivity = blob_analysis.sentiment.subjectivity

    sia = SentimentIntensityAnalyzer()
    vader_scores = sia.polarity_scores(comment)

    if polarity > 0 and vader_scores['compound'] > 0.05:
        overall_sentiment = "Positive"
    elif polarity < 0 and vader_scores['compound'] < -0.05:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"

    intensity = "Moderate"
    if abs(vader_scores['compound']) > 0.6:
        intensity = "Strong"
    elif abs(vader_scores['compound']) < 0.3:
        intensity = "Weak"

    return {
        "overall_sentiment": overall_sentiment,
        "polarity": polarity,
        "subjectivity": subjectivity,
        "vader_scores": vader_scores,
        "intensity": intensity
    }

# Streamlit GUI
st.title("TikTok Comment Sentiment Analysis")

# Input TikTok video URL
st.write("Enter A TikTok Video:")
st.write("Copy it from the URL on the search bar...")
video_url = st.text_input("Example: https://www.tiktok.com/username/video/7452354083213775")
col11, col12, col13, col14 = st.columns(4)

with col11:
    analyze_button = st.button("Analyze Sentiments")

if analyze_button:
    if not video_url:
        st.error("Please enter a TikTok video URL.")
    else:
        try:
            output_file = "output.json"

            # Run the TikTok scraper
            with col12:
                st.info("Running TikTok scraper...")
                scraper = TikTokExtractor(url=video_url, output=output_file, file_type='json')
                scraper.run()

            with col13:
                st.success("TikTok scraper completed successfully!")

            # Load JSON data
            with col14:
                st.info("Loading data from JSON...")
            with open(output_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            col1, col2, col3 = st.columns(3)

            with col1:
                # Display video metadata
                st.subheader("Video Metadata")
                metadata = data["metadata"]
                st.write(f"**Video ID:** {metadata['idVideo']}")
                st.write(f"**Username:** {metadata['uniqueId']} ({metadata['nickname']})")
                st.write(f"**Description:** {metadata['description']}")
                st.write(f"**Total Likes:** {metadata['totalLike']}")
                st.write(f"**Total Comments:** {metadata['totalComment']}")
                st.write(f"**Total Shares:** {metadata['totalShare']}")
                st.write(f"**Created At:** {metadata['createTime']}")
                st.write(f"**Duration:** {metadata['duration']} seconds")

            with col2:
                # Separator
                st.subheader(" ")
                st.write("->")

            with col3:
                # Perform sentiment analysis
                st.subheader("Sentiment Analysis Results")
                comments = [c for c in data.get("comments", []) if c.get("comment")]
                sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

                for comment_data in comments:
                    comment = comment_data["comment"]
                    pre = preprocess_comment_with_language_detection(comment)
                    processed_comment = " ".join(pre)
                    sentiment = analyze_sentiment(processed_comment)
                    sentiment_counts[sentiment["overall_sentiment"]] += 1

                # Display sentiment analysis results as a bar chart
                labels = list(sentiment_counts.keys())
                values = list(sentiment_counts.values())

                fig, ax = plt.subplots()
                ax.bar(labels, values, color=["green", "red", "gray"])
                ax.set_title("Sentiment Analysis of Comments")
                ax.set_ylabel("Number of Comments")
                ax.set_xlabel("Sentiment")
                st.pyplot(fig)

            # Display comments and their sentiment
            st.subheader("Detailed Comments and Sentiments")
            for comment_data in comments:
                comment = comment_data["comment"]
                username = comment_data.get("username", "Anonymous")
                pre = preprocess_comment_with_language_detection(comment)
                processed_comment = " ".join(pre)
                sentiment = analyze_sentiment(processed_comment)

                st.write({
                    "username": username,
                    "comment": comment,
                    "sentiment": sentiment["overall_sentiment"],
                    "intensity": sentiment["intensity"]
                })

            # Cleanup
            os.remove(output_file)

        except Exception as e:
            st.error(f"An error occurred: {e}")
