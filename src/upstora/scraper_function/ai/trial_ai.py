import logging
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import BeautifulSoupTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_extraction_chain
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="./.env")

logger = logging.getLogger(__name__)

openai_api_key = os.getenv('OPENAI_API_KEY')

class AIFeatureExtractor:
    def __init__(self, schema, urls):
        self.llm = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo-16k-0613", request_timeout=120,
                             openai_api_key=openai_api_key)
        self.schema = schema
        self.urls = urls

    def extract(self, content: str):
        return create_extraction_chain(schema=self.schema, llm=self.llm).run(content)

    def scrape_with_ai(self):
        try:
            loader = AsyncChromiumLoader(self.urls)
            docs = loader.load()
            bs_transformer = BeautifulSoupTransformer()
            docs_transformed = bs_transformer.transform_documents(
                docs, tags_to_extract=["span"]
            )

            # Grab the first 1000 tokens of the site
            splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=4000, chunk_overlap=0
            )
            splits = splitter.split_documents(docs_transformed)

            try:
                # Process the first split
                extracted_content = self.extract(content=splits[0].page_content)

                bullet_points = extracted_content['bullets'].split("\n")
                formatted_bullets = []

                for i, point in enumerate(bullet_points, 1):
                    formatted_bullet = f'bullet {i}~ {point.strip()}'
                    formatted_bullets.append(formatted_bullet)

                extracted_content['bullets'] = formatted_bullets

            except Exception as e:
                #logger.error(f"Error extracting content: {str(e)}")
                extracted_content = {'bullets': ['bullet 1~ NA']}
        except Exception as e:
            self.logger.error(f"Error while scraping product details Using AI: {e}")
            extracted_content = None

        return extracted_content


if __name__ == "__main__":
    urls = ["https://www.amazon.com/Hanes-Full-zip-Eco-smart-athletic-sweatshirts/dp/B00JUM4CT4/?_encoding=UTF8&pd_rd_w=6xKyM&content-id=amzn1.sym.64be5821-f651-4b0b-8dd3-4f9b884f10e5&pf_rd_p=64be5821-f651-4b0b-8dd3-4f9b884f10e5&pf_rd_r=R569TVEY39DHCH46AW6B&pd_rd_wg=8e6Z8&pd_rd_r=fa67eb38-52fd-4829-8329-d3f13dcd4e72&ref_=pd_gw_crs_zg_bs_7141123011&th=1"]
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
        "required": ["bullets", "title", "taxonomy", "price", "ratings", "reviews", "seller", "description", "brand",
                     "product_details", "legal_disclaimer", "reviews_text"]
    }

    ai_extractor = AIFeatureExtractor(schema=schema, urls=urls)
    extracted_content = ai_extractor.scrape_with_ai()
    print(extracted_content)

