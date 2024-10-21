# app.py
from flask import Flask, render_template, request
from scrapper import fetch_tiktok_data
from sentiment_analysis import analyze_sentiment
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form['url']
    comments = fetch_tiktok_data(url)
    results = analyze_sentiment(comments)
    
    visualize_results(results)
    
    return render_template('results.html', results=results)

def visualize_results(results):
    labels = results.keys()
    sizes = results.values()
    
    plt.bar(labels, sizes)
    plt.savefig('static/results.png')  # Save the visualization
    plt.close()

if __name__ == '__main__':
    app.run(debug=True)