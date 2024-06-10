from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import logging

logging.basicConfig(filename='scraper_logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AmazonScraperSelenium:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        self.driver = webdriver.Chrome(
            options=options,
            service=Service()
            # executable_path="./drivers/chromedriver"
        )

    def scrape_product_details(self, product_url):
        product_details = {}

        try:
            self.driver.get(product_url)

            self._extract_product_title(product_details)
            self._extract_product_price(product_details)
            self._extract_product_rating(product_details)
            self._extract_num_reviews(product_details)
            self._extract_bullet_points(product_details)
            self._extract_product_description(product_details)
            self._extract_images(product_details)
            self._extract_video(product_details)
            self._extract_taxonomy(product_details)
            self._extract_review_count(product_details)

        except Exception as e:
            logging.error(f"Error while scraping product details using selenium: {e}")
            product_details = None 

        return product_details

    def _extract_product_title(self, product_details):
        try:
            product_title = self.driver.find_element(By.XPATH, '//span[@id="productTitle"]').text
            product_details['title'] = product_title.strip() if product_title else None
        except:
            product_details['title'] = None
            #self.logger.error(f"Error extracting product title: {e}")

    def _extract_product_price(self, product_details):
        try:
            product_price = self.driver.find_element(By.XPATH, '//span[@class="a-offscreen"]').text
            product_details['price'] = product_price.strip() if product_price else None
        except:
            product_details['price'] = None
            #self.logger.error(f"Error extracting product price: {e}")

    def _extract_product_rating(self, product_details):
        try:
            product_rating = self.driver.find_element(By.XPATH, '//span[@id="acrCustomerReviewText"]').text
            product_details['ratings'] = product_rating.strip() if product_rating else None
        except:
            product_details['ratings'] = None
            #self.logger.error(f"Error extracting product rating: {e}")

    def _extract_num_reviews(self, product_details):
        try:
            num_reviews = self.driver.find_element(By.XPATH, '//span[@class="a-size-base a-color-base"]').text
            product_details['reviews'] = num_reviews.strip() if num_reviews else None
        except:
            product_details['reviews'] = None
            #self.logger.error(f"Error extracting number of reviews: {e}")

    def _extract_bullet_points(self, product_details):
        try:
            bullet_list = self.driver.find_element(By.ID, "feature-bullets")
            bullet_points = bullet_list.find_elements(By.TAG_NAME, "li")
            formatted_bullets = [f"bullet {i}~ {bullet.text.strip()}" for i, bullet in enumerate(bullet_points, 1)]
            product_details['bullets'] = formatted_bullets if formatted_bullets else ['bullet 1~ NA']
        except Exception as e:
            product_details['bullets'] = ['bullet 1~ NA']
            #self.logger.error(f"Error extracting bullet points: {e}")

    def _extract_product_description(self, product_details):
        try:
            product_description = self.driver.find_element(By.ID, 'productDescription').text
            product_details['description'] = product_description.strip() if product_description else None
        except:
            product_details['description'] = None
            #self.logger.error(f"Error extracting product description: {e}")

    def _extract_images(self, product_details):
        try:
            html = self.driver.page_source
            images = re.findall('"hiRes":"(.+?)"', html)
            jpg_image_urls = images[:3] if images else None
            product_details['images'] = jpg_image_urls
        except:
            product_details['images'] = None
            #self.logger.error(f"Error extracting images with Selenium: {e}")

    def _extract_video(self, product_details):
        try:
            script_tags = self.driver.find_elements(By.XPATH, "//script[@type='a-state']")
            mp4_url_pattern = r'https://[^"]+\.mp4'
            found_first_video = False

            for script_tag in script_tags:
                script_content = script_tag.get_attribute("innerHTML")
                mp4_urls = re.findall(mp4_url_pattern, script_content)
                if mp4_urls:
                    for mp4_url in mp4_urls:
                        if not found_first_video:
                            product_video_urls = mp4_url
                            found_first_video = True

            product_details['video'] = product_video_urls if found_first_video else "None"
        except:
            product_details['video'] = None
            #self.logger.error(f"Error extracting video URL with Selenium: {e}")

    def _extract_taxonomy(self, product_details):
        try:
            taxonomy = []
            taxonomy_element = self.driver.find_element(By.XPATH, '//div[@id="wayfinding-breadcrumbs_feature_div"]')
            taxonomy_links = taxonomy_element.find_elements(By.TAG_NAME, 'a')
            taxonomy = [link.text.strip() for link in taxonomy_links]
            taxonomy_str = " > ".join(taxonomy) if taxonomy else None
            product_details['taxonomy'] = taxonomy_str
        except:
            product_details['taxonomy'] = None
            #self.logger.error(f"Error extracting taxonomy: {e}")

    def _extract_review_count(self, product_details):
        try:
            link_element = self.driver.find_element(By.CSS_SELECTOR, 'a[data-hook="see-all-reviews-link-foot"]')
            href = link_element.get_attribute("href")
            self.logger.info(href)
            self.driver.get(href)
            content_element = self.driver.find_element(By.CSS_SELECTOR, '[data-hook="cr-filter-info-review-rating-count"]')
            review_count_text = content_element.text

            try:
                match = re.search(r'(\d{1,3}(?:,\d{3})*)(?=\s*with reviews)', review_count_text)
                review_count = match.group(1) if match else None
            except AttributeError:
                review_count = None
            product_details['review_count'] = review_count
        except:
            #self.logger.error(f"Error extracting review count: {e}")
            product_details['review_count'] = None

if __name__ == "__main__":
    product_url = 'https://www.amazon.com/Hanes-Full-zip-Eco-smart-athletic-sweatshirts/dp/B00JUM4CT4/?_encoding=UTF8&pd_rd_w=6xKyM&content-id=amzn1.sym.64be5821-f651-4b0b-8dd3-4f9b884f10e5&pf_rd_p=64be5821-f651-4b0b-8dd3-4f9b884f10e5&pf_rd_r=R569TVEY39DHCH46AW6B&pd_rd_wg=8e6Z8&pd_rd_r=fa67eb38-52fd-4829-8329-d3f13dcd4e72&ref_=pd_gw_crs_zg_bs_7141123011&th=1'
    scraper = AmazonScraperSelenium()
    product_info = scraper.scrape_product_details(product_url)
    print(product_info)

