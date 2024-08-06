import requests
from bs4 import BeautifulSoup
import time

reviewlist = []

def get_soup(url):
    try:
        r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 5})  # Increased wait time
        r.raise_for_status()  # Ensure we notice bad responses
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {url}")
        print(e)
        return None

def get_reviews(soup):
    if soup is None:
        return
    
    reviews = soup.find_all('div', {'data-hook': 'review'})
    if not reviews:
        print("No reviews found on this page.")
    for item in reviews:
        try:
            title = item.find('a', {'data-hook': 'review-title'}).text.strip()
            rating = item.find('i', {'data-hook': 'review-star-rating'}).text.strip()
            rating = int(rating[0])  # Assuming the rating is in format "X out of 5 stars"
            body = item.find('span', {'data-hook': 'review-body'}).text.strip()
            review = {
                'review_title': title,
                'review_rating': rating,
                'review_body': body
            }
            reviewlist.append(review)
        except Exception as e:
            print("Error parsing review:")
            print(e)

# Loop through pages
for i in range(1, 10):
    url = f'https://www.amazon.in/Daikin-Inverter-Display-Technology-MTKL50U/product-reviews/B0BK1KS6ZD/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={i}'
    print(f"Fetching URL: {url}")
    soup = get_soup(url)
    
    # Print the soup object to verify content
    print(soup.prettify()[:1000])  # Print the first 1000 characters of the soup for inspection
    
    get_reviews(soup)
    print(f"Total reviews collected: {len(reviewlist)}")
    
    if soup and not soup.find('li', {'class': 'a-disabled a-last'}):
        time.sleep(2)  # Adding delay between requests
    else:
        print("No more pages found or an error occurred.")
        break

# Print the collected reviews

print(len(reviewlist))
