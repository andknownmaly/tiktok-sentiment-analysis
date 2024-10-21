# sentiment_analysis.py
from textblob import TextBlob

def analyze_sentiment(comments):
    sentiment_results = {'positive': 0, 'negative': 0, 'neutral': 0}
    
    for comment in comments:
        analysis = TextBlob(comment)
        # Classify the polarity
        if analysis.sentiment.polarity > 0:
            sentiment_results['positive'] += 1
        elif analysis.sentiment.polarity < 0:
            sentiment_results['negative'] += 1
        else:
            sentiment_results['neutral'] += 1
    
    return sentiment_results