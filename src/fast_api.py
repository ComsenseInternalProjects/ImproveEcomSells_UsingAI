import asyncio
import logging 
import math
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from mongo import connect_to_mongodb

from .upstora.process_data.asin_verify import asincheck
from .upstora.process_data.new_get_data import json_format

logging.basicConfig(filename='scraper_logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def remove_null_entries(obj):
    if isinstance(obj, list):
        return [remove_null_entries(item) for item in obj if item is not None]
    elif isinstance(obj, dict):
        return {key: remove_null_entries(value) for key, value in obj.items() if value is not None}
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    else:
        return obj
    
app = FastAPI()

origins = [
    "http://upstora-container",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    section: str
    data: List[dict]


@app.get("/amazon_scraper/{input_str}", response_model=List[Item])
async def data(input_str: str):
    try:
        data_status = asincheck(input_str)
        if data_status != "pass":
            error_response = [Item(section="error", data=[{"error": "Enter Valid ASIN"}])]
            return error_response
        
        output = await asyncio.to_thread(json_format, input_str)
        output_dict = json.loads(output)
        output_dict = remove_null_entries(output_dict)
        sections = output_dict.get("data", [])
        desired_output = []

        for section in sections:
            section_data = section.get("data", [])
            section_with_all_fields = Item(section=section["section"], data=section_data)
            desired_output.append(section_with_all_fields)
            logging.info("ASIN Info Generated Sucessfully")

        try:
            connected_collection = connect_to_mongodb("upstora", "upstora-data")
            if connected_collection is not None:
                connected_collection.insert_many([document.dict() for document in desired_output])
                logging.info("Data inserted successfully.")
            else:
                logging.info("Failed to connect to MongoDB.")
        except Exception as insertion_error:
            logging.error(f"Data insertion failed: {str(insertion_error)}")
        return desired_output

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        error_response = [Item(section="error", data=[{"error": "Sorry, something went wrong there. Try again."}])]
        return error_response
