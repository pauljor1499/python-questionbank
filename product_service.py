from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

def product_serializer(product) -> dict:
    return {
        "_id": str(product["_id"]),
        "name": product["name"],
        "description": product.get("description"),
        "price": product["price"],
        "stock": product["stock"]
    }

class ProductService:
    def __init__(self, db_client: str):
        self.client = AsyncIOMotorClient(db_client)
        self.db = self.client["test-product"]
        self.collection = self.db["products"]

    # Create a product
    async def create_product(self, product_data: dict):
        result = await self.collection.insert_one(product_data)  # Awaiting asynchronous insertion
        return str(result.inserted_id)

    # Get a single product by ID
    async def get_product(self, product_id: str):
        product = await self.collection.find_one({"_id": ObjectId(product_id)})  # Awaiting asynchronous query
        if product:
            return product_serializer(product)
        return None

    # Update a product by ID
    async def update_product(self, product_id: str, product_data: dict):
        result = await self.collection.update_one({"_id": ObjectId(product_id)}, {"$set": product_data})  # Awaiting async update
        if result.modified_count:
            product = await self.get_product(product_id)  # Awaiting the asynchronous retrieval of the updated product
            return product
        return None

    # Delete a product by ID
    async def delete_product(self, product_id: str):
        result = await self.collection.delete_one({"_id": ObjectId(product_id)})  # Awaiting async deletion
        return result.deleted_count > 0

    # List all products
    async def list_products(self, price: float = None):
        pipeline = []
        if price is not None:
            pipeline.append({
                "$match": {"price": price}  # Add price filter if provided
            })
        products = await self.collection.aggregate(pipeline).to_list(100)  # Awaiting async aggregation and limiting to 100
        return [product_serializer(product) for product in products]
