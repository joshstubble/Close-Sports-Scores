# Import the required libraries
from bs4 import BeautifulSoup
import requests

# Define the URL that you want to scrape
url = "https://www.foxsports.com/live"

# Use the requests library to download the HTML from the URL
response = requests.get(url)

# Use the BeautifulSoup library to parse the HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Find the elements on the page that contain the live scores
score_elements = soup.find_all('div', class_='wisbb_score')

# Loop through the score elements and print the scores
for element in score_elements:
    print(element.text)
