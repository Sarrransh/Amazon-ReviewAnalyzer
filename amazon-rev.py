
import requests
from bs4 import BeautifulSoup
import time
import mysql.connector

reviewlist=[]
product_name=''

def det_login():
    splash_url = 'http://localhost:8050/execute'
    with open('login.lua', 'r') as file:
        lua_source = file.read()

    payload = {
        'lua_source': lua_source
    }

    r = requests.post(splash_url, json=payload)
    if r.status_code == 200:
        print("Login successful")
    else:
        print(f"Error during login: {r.status_code}")

#login is not working, check later
    
def get_soup(url):
    
    r= requests.get('http://localhost:8050/render.html', params={'url':url, 'wait':2})
    soup = BeautifulSoup(r.text,'html.parser')
    return soup

def get_reviews(soup):
    time.sleep(3)
    reviews = soup.find_all('div',{'data-hook':'review'})
    try:
        for item in reviews:
            parts = item.find('a',{'data-hook':'review-title'}).text.split('\n',1)
            reviews = {
            'review_title':parts[1],
            'review_rating':int(parts[0][0]),
            'review_body':item.find('span',{'data-hook':'review-body'}).text.strip()
            }
            reviewlist.append(reviews)
            
    except:
        pass

        

det_login()

for i in range(1,10):
    url = 'https://www.amazon.in/Aristocrat-Polypropylene-Lightweight-Combination-Warranty/product-reviews/B0D4VBLM2H/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews'+'&pageNumber=' + str(i)
    soup=get_soup(url)
    get_reviews(soup)
    print(len(reviewlist))
    if not soup.find('li',{'class':'a-disabled a-last'}):
        pass
    else:
        break

product_name=soup.find('a',{'data-hook':'product-link'}).text.strip()
product_name=product_name.replace(' ','_')


def save_reviews_to_db():
    table_name='table2'
    
    reviews=reviewlist
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='saransh',
            database='amazon_reviews'
        )
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS `{table_name}` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            review_title VARCHAR(255),
            review_rating INT,
            review_body TEXT
        )
        """
        cursor = connection.cursor()
        cursor.execute(create_table_query)


        # Create a dynamic SQL query with the specified table name
        insert_query = f"""
        INSERT INTO `{table_name}` (review_title, review_rating, review_body)
        VALUES (%s, %s, %s)
        """

        for review in reviews:
            cursor.execute(insert_query, (review['review_title'], int(review['review_rating']), review['review_body']))

        connection.commit()
        cursor.close()
        connection.close()
        print(f"Reviews inserted successfully into the `{table_name}` table.")
        

    except mysql.connector.Error as error:
        print(f"Failed to insert into MySQL table {error}")

print(product_name)

save_reviews_to_db()



#  db_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'passwd': 'saransh',
#     'database': 'db'
# }



# import requests
# from bs4 import BeautifulSoup
# reviewlist=[]

# def get_soup(url):
#     splash_url = 'http://localhost:8050/execute'
#     with open('login.lua', 'r') as file:
#         lua_source = file.read()

#     payload = {
#         'lua_source': lua_source,
#         'url': url
#     }

#     r = requests.post(splash_url, json=payload)
#     soup = BeautifulSoup(r.text, 'html.parser')
#     return soup

# def get_reviews(soup):
#     reviews = soup.find_all('div',{'data-hook':'review'})
#     try:
#         for item in reviews:
#             parts = item.find('a',{'data-hook':'review-title'}).text.split('\n',1)
#             reviews = {
#             'review_title':parts[1],
#             'review_rating':int(parts[0][0]),
#             'review_body':item.find('span',{'data-hook':'review-body'}).text.strip()
#             }
#             reviewlist.append(reviews)
            
#     except:
#         pass

        

# for i in range(1,10):
#     url = 'https://www.amazon.in/Daikin-Inverter-Display-Technology-MTKL50U/product-reviews/B0BK1KS6ZD/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=' + str(i)
#     soup=get_soup(url)
#     get_reviews(soup)
#     print(len(reviewlist))
#     if not soup.find('li',{'class':'a-disabled a-last'}):
#         pass
#     else:
#         break

