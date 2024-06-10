import requests
import re
import json
import random
import logging
from bs4 import BeautifulSoup

class AmazonScraperBs:
    def __init__(self, url):
        self.url = url
        self.UA_STRINGS = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        ]
        self.HEADERS = {
            'User-Agent': random.choice(self.UA_STRINGS),
            'Accept-Language': 'en-US, en;q=0.5'
        }

    def get_html(self):
        try:
            html = requests.get(self.url, headers=self.HEADERS)
            html.raise_for_status()
            return html
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching the webpage in bs4: {e}")
            return None

    def get_soup(self, html):
        try:
            soup = BeautifulSoup(html.text, features="lxml")
            return soup
        except requests.exceptions.RequestException as e:
            return None

    def get_bullets(self, soup):
        try:
            feature_bullets_section = soup.find('div', {'id': 'feature-bullets'})
            bullet_points = feature_bullets_section.find_all('li')
            formatted_bullets = [f"bullet{idx + 1}~ {bullet.text.strip()}" for idx, bullet in enumerate(bullet_points)]
            return formatted_bullets
        except:
          return None

    def get_title(self, soup):
        try:
            title = soup.find('span', {'id': "productTitle"}).text.strip()
            return title
        except:
            return None

    def get_taxonomy(self , soup):
        try:
            taxonomy_elements = soup.find_all(class_='a-link-normal a-color-tertiary')
            taxonomy = [element.text.strip() for element in taxonomy_elements]
            taxonomy_str = " > ".join(taxonomy)
        except:
            taxonomy_str = "None"
        return taxonomy_str

    def get_reviews(self, soup):  
        try:
            reviews = soup.find("span", attrs={'class': 'a-size-base a-color-base'}).text.strip()
        except:
            reviews = "None"
        return reviews

    def get_ratings(self, soup):
        try:
            ratings_span = soup.find('span', {'id': 'acrCustomerReviewText'})
            ratings = ratings_span.text.strip()
        except:
            ratings = "None"
        return ratings

    def get_price(self , soup):
        try:
            price = soup.find('span', {'class':"a-offscreen"}).text.strip()
        except:
            price = "None"
        return price

    def get_des(self ,soup):
        try:
            product_description = soup.find('div', {'id': 'productDescription'}).text.strip()
        except:
            product_description = "None"
        return product_description

    def get_brand(self ,soup):
        try:
            brand_name = soup.find('span', {'class': 'a-size-base po-break-word'}).text.strip()
        except:
            brand_name = "None"
        return brand_name

    def get_product_details(self ,soup):
        try:
            product_details = soup.find('div', {'id': 'detailBulletsWithExceptions_feature_div'}).text.strip()
        except:
            product_details = None
        return product_details

    def get_legal_disclaimer(self ,soup):
        legal_disclaimer_data = None
        try:
            div_tags = soup.find_all('div', class_='a-section content')
            for div in div_tags:
                h4_tag = div.find('h4')
                if h4_tag and "Legal Disclaimer" in h4_tag.get_text():
                    legal_disclaimer = div.find_all('p')
                    for p in legal_disclaimer:
                        legal_disclaimer_data = p.get_text().strip()
        except:
           return legal_disclaimer_data


    def get_seller(self ,soup):
        try:
            seller = soup.find_all('a',{'class':'a-spacing-top-small a-link-normal'})
            seller_name = seller[0].text if seller else None
        except:
            seller_name = "None"
        return seller_name

    def get_images(self, html):
        try:
            images = re.findall('"hiRes":"(.+?)"', html.text) 
            jpg_image_urls = images[:3]

            return jpg_image_urls
        except:
            return "None"

    def get_video(self, soup):
        try:
            script_tags = soup.find_all('script', attrs={'type': 'a-state'})
            mp4_url_pattern = r'https://[^"]+\.mp4'
            found_first_video = False

            for script_tag in script_tags:
                script_content = script_tag.get_text()
                mp4_urls = re.findall(mp4_url_pattern, script_content)
                if mp4_urls:
                    for mp4_url in mp4_urls:
                        if not found_first_video:
                            return mp4_url
        except:
            return "None"
        
    def get_reviews_count(self ,soup):
        return "None"
    
    def scrape(self):
        html_data = self.get_html()
        if html_data:
            soup = self.get_soup(html_data)
            data_dict = {
                "bullets": self.get_bullets(soup),
                "title": self.get_title(soup),
                "taxonomy": self.get_taxonomy(soup),
                "price": self.get_price(soup),
                "ratings": self.get_ratings(soup),
                "reviews": self.get_reviews(soup),
                "review_count": self.get_reviews_count(soup),
                "seller": self.get_seller(soup),
                "description": self.get_des(soup),
                "images": self.get_images(html_data),
                "video": self.get_video(soup),
                "brand": self.get_brand(soup),
                "Product_details": self.get_product_details(soup),
                "legal_disclaimer": self.get_legal_disclaimer(soup)
            }
            return data_dict

if __name__ == "__main__":
    amazon_url = "https://www.amazon.com/Mucinex-Strength-Congestion-Expectorant-Guaifenesin/dp/B0057UUGRU/ref=cm_cr_arp_d_product_top?ie=UTF8"
    scraper = AmazonScraperBs(amazon_url)
    data = scraper.scrape()
    print(data)

