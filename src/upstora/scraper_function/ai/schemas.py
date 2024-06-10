from pydantic import BaseModel

ecommerce_schema = {
    "properties": {
        "title": {"type": "string"},
        "taxonomy": {"type": "string"},
        "price": {"type": "string"},
        "ratings": {"type": "string"},
        "reviews": {"type": "string"},
        "bullets": {"type": "string"},
        "seller": {"type": "string"},
        "description": {"type": "string"},
        "brand": {"type": "string"},
        "Product_details": {"type": "string"},
        "legal_disclaimer": {"type": "string"},
        "reviews_text": {"type": "string"},
    },
    "required": [
        "title",
        "taxonomy",
        "price",
        "ratings",
        "reviews",
        "bullets",
        "seller",
        "description",
        "brand",
        "product_details",
        "legal_disclaimer",
        "reviews_text",
    ],
}


class SchemaNewsWebsites(BaseModel):
    title: str
    ListPrice: str
    brand: str
    color: str
    ratings: str
    about_this_item: str
    soldby: str
