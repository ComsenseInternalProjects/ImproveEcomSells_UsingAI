import asyncio
import logging
from ..scraper_function.ai.trial_ai_op import AIFeatureExtractor
from ..scraper_function.bs4.bs_scraper_op import AmazonScraperBs
from ..scraper_function.selenium.selenium_scraper_op import AmazonScraperSelenium
from ..scraper_function.playwright.pw_scraper_op import AmazonScraperPw

logging.basicConfig(filename='scraper_logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

defult_dict = {
    "bullets": None,
    "title": None,
    "taxonomy": None,
    "price": None,
    "ratings": None,
    "reviews": None,
    "review_count": None,
    "seller": None,
    "description": None,
    "brand_story": None,
    "images": None,
    "video": None,
    "brand": None,
    "Product_details": None,
    "legal_disclaimer": None
}


def get_all_data(url,schema):

    try:
        scraper = AmazonScraperBs(url)
        bs_data = scraper.scrape()
    except Exception as e:
        print(f"Error in bsscraper: {e}")
        bs_data = defult_dict 

    try:
        scraper = AmazonScraperSelenium()
        selenium_data = scraper.scrape_product_details(url)
        logging.info("selenium pass")
    except Exception as e:
        print(f"Error in selenium: {e}")
        selenium_data = defult_dict 

    # try:
    #     scraper = AmazonScraperPw(url)
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(scraper.scrape_amazon_product())
    #     playwright_data = scraper.get_product_details()
    # except Exception as e:
    #     print(f"Error in playwright: {e}")
    #     playwright_data = defult_dict 

    try:
        # Create a new event loop for Playwright
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        scraper = AmazonScraperPw(url)
        loop.run_until_complete(scraper.scrape_amazon_product())
        playwright_data = scraper.get_product_details()
        logging.info("playwright pass")
    except Exception as e:
        print(f"Error in playwright: {e}")
        playwright_data = defult_dict 
    finally:
        loop.close()
    
    try:
        val_url = [url]
        ai_extractor = AIFeatureExtractor(schema=schema, urls=val_url)
        ai_data = ai_extractor.scrape_with_ai()
        logging.info("AI scrapper Pass")
    except Exception as e:
        print(f"Error in AI: {e}")
        ai_data = defult_dict 

    return selenium_data , playwright_data , ai_data, bs_data


data_dict = {
    "bullets": 'NA',
    "title": "NA",
    "taxonomy": "NA",
    "price": "NA",
    "ratings": "NA",
    "reviews": "NA",
    "review_count": "NA",
    "seller": "NA",
    "description": "NA",
    "brand_story": "NA",
    "images": "NA",
    "video": "NA",
    "brand": "NA",
    "Product_details": "NA",
    "legal_disclaimer": "NA"
}

def fill_data_dict(url):
    schema = {
    "properties": {
        "bullets": {"type": "string"},
        "title": {"type": "string"},
        "taxonomy": {"type": "string"},
        "price": {"type": "string"},
        "ratings": {"type": "string"},
        "reviews": {"type": "string"},
        "seller": {"type": "string"},
        "description": {"type": "string"},
        "brand": {"type": "string"},
        "Product_details": {"type": "string"},
        "legal_disclaimer": {"type": "string"},
        "reviews_text": {"type": "string"}
    },
    "required": ["bullets","title","taxonomy","price","ratings","reviews","seller","description","brand","product_details","legal_disclaimer","reviews_text"]
    }
    output = get_all_data(url,schema)
    selenium_data , playwright_data ,ai_data ,bs_data = output

    for key in data_dict:
        if selenium_data.get(key) is not None and selenium_data[key] not in (None, "",[], "None"):
            data_dict[key] = selenium_data[key]
        elif playwright_data.get(key) is not None and playwright_data[key] not in (None, "",[], "None"):
             data_dict[key] = playwright_data[key]
        elif ai_data.get(key) is not None and ai_data[key] not in (None, "",[], "None"):
             data_dict[key] = ai_data[key]
        elif bs_data.get(key) is not None and bs_data[key] not in (None, "",[], "None"):
            data_dict[key] = bs_data[key]
        
    return data_dict
if __name__ == "__main__":
   print(fill_data_dict("https://www.amazon.com/Aquaphor-Baby-Healing-Ointment-Advance/dp/B005UEB96K/ref=lp_18067174011_1_2?sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D"))
