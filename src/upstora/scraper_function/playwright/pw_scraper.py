import asyncio
import logging
import re
from playwright.async_api import async_playwright

logging.basicConfig(filename='scraper_logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class AmazonScraperPw:
    def __init__(self, url):
        self.url = url
        self.product_details = {}

    async def scrape_amazon_product(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()

            try:
                await page.goto(self.url)

                await self._extract_product_title(page)
                await self._extract_product_price(page)
                await self._extract_product_rating(page)
                await self._extract_reviews(page)
                await self._extract_bullet_points(page)
                await self._extract_product_description(page)
                await self._extract_brand_story(page)
                await self._extract_images(page)
                await self._extract_video(page)
                await self._extract_taxonomy(page)

            except Exception as e:
                logging(f"Error while scraping product details using playwright: {e}")

            finally:
                await browser.close()

    async def _extract_product_title(self, page):
        try:
            product_title = await page.evaluate('(element) => element.textContent', await page.query_selector('span#productTitle'))
            self.product_details["title"] = product_title.strip() if product_title else None
        except:
            self.product_details["title"] = None
            #self.logger.error(f"Error extracting product title: {e}")

    async def _extract_product_price(self, page):
        try:
            product_price_element = await page.evaluate('(element) => element.textContent', await page.query_selector('span.a-offscreen'))
            self.product_details["price"] = product_price_element.strip() if product_price_element else None
        except:
            self.product_details["price"] = None
            #self.logger.error(f"Error extracting product price: {e}")

    async def _extract_product_rating(self, page):
        try:
            product_rating_element = await page.evaluate('(element) => element.textContent', await page.query_selector('span#acrCustomerReviewText'))
            self.product_details["ratings"] = product_rating_element.strip() if product_rating_element else None
        except:
            self.product_details["ratings"] = None
            #self.logger.error(f"Error extracting product rating: {e}")

    async def _extract_reviews(self, page):
        try:
            num_reviews_element = await page.evaluate('(element) => element.textContent', await page.query_selector('span.a-size-base.a-color-base'))
            self.product_details["reviews"] = num_reviews_element.strip() if num_reviews_element else None
        except:
            self.product_details["reviews"] = None
            #self.logger.error(f"Error extracting number of reviews: {e}")

    async def _extract_bullet_points(self, page):
        try:
            bullet_list_element = await page.query_selector('div#feature-bullets')
            formatted_bullet = []
            if bullet_list_element:
                bullet_points = await bullet_list_element.query_selector_all('li')
                formatted_bullet = [f"bullet {i}~ {await bullet_point.text_content()}" for i, bullet_point in enumerate(bullet_points, 1)]
            self.product_details["bullets"] = formatted_bullet
        except:
            self.product_details["bullets"] = ['bullet 1~ NA']
            #self.logger.error(f"Error extracting bullet points: {e}")

    async def _extract_product_description(self, page):
        try:
            product_description_element = await page.evaluate('(element) => element.textContent', await page.query_selector('div#productDescription'))
            self.product_details["description"] = product_description_element.strip() if product_description_element else None
        except:
            self.product_details["description"] = None
            #self.logger.error(f"Error extracting product description: {e}")
    async def _extract_brand_story(self, page):
        try:
            brand_story_element =await page.evaluate('(element) => element.textContent', await page.query_selector('div#aplus'))
            self.product_details = brand_story_element.strip() if brand_story_element else None 
        except:
            self.product_details["brand_story"] = None

    async def _extract_images(self, page):
        try:
            html = await page.content()
            images = re.findall('"hiRes":"(.+?)"', html)
            jpg_image_urls = images[:3] if images else [""]
            self.product_details["images"] = jpg_image_urls
        except:
            self.product_details["images"] = None
            #self.logger.error(f"Error extracting images: {e}")

    async def _extract_video(self, page):
        try:
            script_tags = await page.query_selector_all('script[type="a-state"]')
            mp4_url_pattern = r'https://[^"]+\.mp4'
            product_video_urls = "None"

            for script_tag in script_tags:
                script_content = await script_tag.inner_text()
                mp4_urls = re.findall(mp4_url_pattern, script_content)
                if mp4_urls:
                    product_video_urls = mp4_urls[0]
                    break

            self.product_details["video"] = product_video_urls
        except:
            self.product_details["video"] = None
            #self.logger.error(f"Error extracting video: {e}")

    async def _extract_taxonomy(self, page):
        try:
            taxonomy_element = await page.query_selector('div#wayfinding-breadcrumbs_feature_div')
            if taxonomy_element:
                taxonomy_links = await taxonomy_element.query_selector_all('a')
                taxonomy = [await link.text_content() for link in taxonomy_links]
                taxonomy = [item.strip() for item in taxonomy]
                taxonomy_str = " > ".join(taxonomy)
            else:
                taxonomy_str = ""
            self.product_details["taxonomy"] = taxonomy_str
        except:
            self.product_details["taxonomy"] = None
            #self.logger.error(f"Error extracting taxonomy: {e}")

    def get_product_details(self):
        return self.product_details

if __name__ == "__main__":
    amazon_url = "https://www.amazon.com/Mucinex-Strength-Congestion-Expectorant-Guaifenesin/dp/B0057UUGRU/ref=sxin_16_pa_sp_search_thematic_sspa?content-id=amzn1.sym.a2e12efe-e275-4efd-81b9-095fa99ad91f%3Aamzn1.sym.a2e12efe-e275-4efd-81b9-095fa99ad91f&crid=36OX8MAQI3XDJ&cv_ct_cx=medicines&keywords=medicines&pd_rd_i=B0057UUGRU&pd_rd_r=83e35466-63d8-4369-b4aa-cd0bf6451ad8&pd_rd_w=qwfwP&pd_rd_wg=wC4eD&pf_rd_p=a2e12efe-e275-4efd-81b9-095fa99ad91f&pf_rd_r=BZ4AQGKCJ771YMZR3TXE&qid=1698213426&s=apparel&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sprefix=medicine%2Cfashion%2C295&sr=1-4-364cf978-ce2a-480a-9bb0-bdb96faa0f61-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9zZWFyY2hfdGhlbWF0aWM&psc=1"

    scraper = AmazonScraperPw(amazon_url)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scraper.scrape_amazon_product())
    product_info = scraper.get_product_details()
    print(product_info)
