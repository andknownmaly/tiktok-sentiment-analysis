import streamlit as st
from textblob import TextBlob
import json
import os
import subprocess
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from langdetect import detect
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Unduh resource NLTK yang diperlukan
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

# Function to load JSON data
def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Error loading JSON file: {e}")
        return None

# Function to run the TikTok scraper program
def run_tiktok_scraper(url, output_file, file_type="json"):
    """
    Run the TikTok scraper and save the output to a specified file.
    """
    command = f"python scrapper.py -u {url} -o {output_file} -f {file_type}"
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if process.returncode != 0:
        raise Exception(f"Error running scraper: {process.stderr.decode('utf-8')}")

# Function to detect language and preprocess comment
def preprocess_comment_with_language_detection(comment):
    # Detect language
    lang = detect(comment)
    
    # Load the appropriate stopwords based on the detected language
    try:
        stop_words = stopwords.words(lang) if lang in stopwords.fileids() else stopwords.words('english')
    except:
        stop_words = stopwords.words('english')
    
    # Preprocess the comment
    comment = comment.lower()  # Lowercase
    comment = re.sub(r'[^a-zA-Z\s]', '', comment)  # Remove non-alphabetic characters
    tokens = word_tokenize(comment)  # Tokenize
    filtered_tokens = [word for word in tokens if word not in stop_words]  # Remove stopwords
    
    return filtered_tokens

# Function to perform sentiment analysis
def analyze_sentiment(comment):
    """
    Analyze the sentiment of a given comment using TextBlob and VADER.
    
    Returns:
        A dictionary with detailed sentiment analysis results.
    """
    # TextBlob Analysis
    blob_analysis = TextBlob(comment)
    polarity = blob_analysis.sentiment.polarity
    subjectivity = blob_analysis.sentiment.subjectivity

    # VADER Analysis
    sia = SentimentIntensityAnalyzer()
    vader_scores = sia.polarity_scores(comment)

    # Determine overall sentiment
    if polarity > 0 and vader_scores['compound'] > 0.05:
        overall_sentiment = "Positive"
    elif polarity < 0 and vader_scores['compound'] < -0.05:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"

    # Classify sentiment intensity
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
video_url = st.text_input("Enter TikTok Video URL:")

if st.button("Analyze Sentiments"):
    if not video_url:
        st.error("Please enter a TikTok video URL.")
    else:
        try:
            output_file = "output.json"
            file_type = "json"

            # Run the TikTok scraper program
            st.info("Running TikTok scraper...")
            run_tiktok_scraper(video_url, output_file, file_type)
            st.success("TikTok scraper completed successfully!")

            # Load JSON data
            st.info("Loading data from json...")
            data = load_json(output_file)
            if not data:
                st.error("Failed to load data from output.json.")
                os.remove(output_file)

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

            # Perform sentiment analysis
            st.subheader("Sentiment Analysis Results")
            comments = data.get("comments", [])
            sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

            for comment_data in comments:
                comment = comment_data["comment"]
                sentiment = analyze_sentiment(comment)
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

            # Cleanup
            os.remove(output_file)  # Uncomment if you want to delete the file after use

        except Exception as e:
            st.error(f"An error occurred: {e}")
