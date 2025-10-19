# 🎭 TikTok Sentiment Analysis

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Framework-red.svg)](https://streamlit.io/)
[![NLP](https://img.shields.io/badge/NLP-TextBlob%20%7C%20VADER-green.svg)](https://github.com/cjhutto/vaderSentiment)
[![License](https://img.shields.io/badge/License-MIT-gray.svg)](LICENSE)

A **Python + Streamlit web application** that performs **sentiment analysis on TikTok video comments**, combining **web scraping** and **natural language processing (NLP)** to understand user sentiment trends in TikTok content.

🔗 **Live Demo:** [TikTok Sentiment Analysis App](https://tiktok-sentiment-analysis.streamlit.app)

---

## 🧩 Features

* 🕵️ Extracts TikTok video **metadata and comments**
* 🧠 Performs **sentiment analysis** using **TextBlob** and **VADER**
* 📊 Classifies sentiments as **Positive**, **Negative**, or **Neutral**
* ⚖️ Measures **sentiment intensity** (Strong / Moderate / Weak)
* 📈 Visualizes sentiment distribution with dynamic charts
* 🌐 Runs entirely in a **Streamlit web interface**

---

## 🗂️ Project Structure

| File                    | Description                                              |
| ----------------------- | -------------------------------------------------------- |
| `sentiment_analysis.py` | Main Streamlit app — handles UI and sentiment processing |
| `scrapper.py`           | Handles TikTok scraping (comments & metadata extraction) |

---

## ⚙️ How It Works

1. User inputs a **TikTok video URL**
2. The app scrapes **comments and engagement data**
3. Text data is cleaned, tokenized, and analyzed using:

   * [TextBlob](https://textblob.readthedocs.io/)
   * [VADER Sentiment Analyzer](https://github.com/cjhutto/vaderSentiment)
4. Sentiments are classified and plotted for intuitive visualization

---

## 🚧 Limitations

* Requires valid **TikTok video URLs**
* May be affected by **TikTok API or DOM structure changes**
* Sentiment analysis currently optimized for **English text**

  * Non-English comments are auto-translated (fallback) but may reduce accuracy

---

## 🧠 Use Cases

* Social media analytics
* Trend detection for TikTok content creators
* Academic research in sentiment analysis
* Brand reputation monitoring

---

## ⚖️ Disclaimer

This tool is provided **for educational and research purposes only**.
Users are responsible for ensuring compliance with **TikTok’s Terms of Service** and any applicable data policies.

---

## 🪪 License

This project is licensed under the **MIT License** — free for learning, modification, and research use.
