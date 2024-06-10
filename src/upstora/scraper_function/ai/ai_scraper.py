import asyncio
import re

# from scraper_function.ai import extract , ecommerce_schema, ascrape_playwright
from .ai_extractor import extract
from .schemas import ecommerce_schema
from .scrape import ascrape_playwright

# scraper_function/ai/ai_scraper.py
# from scraper_function.ai.ai_extractor import extract
# from scraper_function.ai.schemas import ecommerce_schema
# from scraper_function.ai.scrape import ascrape_playwright


async def scrape_and_extract_with_playwright_with_retry(
    url, tags, schema, token_limit=5000
):
    try:
        pre_html_content = await ascrape_playwright(url, tags)
        html_content = re.sub(r"\s+", " ", pre_html_content)
        print("Extracting content with LLM")
        html_content_fits_context_window_llm = html_content[:token_limit]
        extracted_content = extract(
            schema=schema, content=html_content_fits_context_window_llm
        )
        return extracted_content
    except Exception as e:
        return None


def all_data(url):
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
    data = loop.run_until_complete(
        scrape_and_extract_with_playwright_with_retry(
            url=url,
            tags=["h1", "h2", "h3", "h4", "ul", "table", "span"],
            schema=ecommerce_schema,
        )
    )

    print(data)
    bullet_points = data[0]["bullets"].split("\n")
    formatted_bullets = []

    for i, point in enumerate(bullet_points, 1):
        formatted_bullet = f"bullet {i}: {point.strip()}"
        formatted_bullets.append(formatted_bullet)

    data[0]["bullets"] = formatted_bullets
    return data[0]


if __name__ == "__main__":
    amazon_url = "https://www.amazon.com/Hanes-Full-zip-Eco-smart-athletic-sweatshirts/dp/B096NFX7V7/?_encoding=UTF8&pd_rd_w=6xKyM&content-id=amzn1.sym.64be5821-f651-4b0b-8dd3-4f9b884f10e5&pf_rd_p=64be5821-f651-4b0b-8dd3-4f9b884f10e5&pf_rd_r=R569TVEY39DHCH46AW6B&pd_rd_wg=8e6Z8&pd_rd_r=fa67eb38-52fd-4829-8329-d3f13dcd4e72&ref_=pd_gw_crs_zg_bs_7141123011&th=1"
    print(all_data(amazon_url))
