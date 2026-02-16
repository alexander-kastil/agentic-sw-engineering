# Refactor and Optimize Python Code

## Optimized code using Beautiful Soup

from bs4 import BeautifulSoup
import requests

url = "https://example.com/articles"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
article_titles = [tag.text for tag in soup.find_all("h2")]
print("Article titles:", article_titles)
