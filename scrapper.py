# scraper.py
import requests
from bs4 import BeautifulSoup

def fetch_tiktok_data(link):
    # This function should use TikTok's API or scraping method to get data.
    # This is an example, you'll need to modify this.
    response = requests.get(link)
    
    if response.status_code != 200:
        raise Exception("Failed to load page")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Placeholder: extract comments or posts; you'll need to adjust the selectors
    comments = []
    for comment in soup.find_all('div', class_='comment-class'):  # Modify selector
        comments.append(comment.text)
        
    return comments