from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

def question_serializer(product) -> dict:
    return {
        "_id": str(product["_id"]),
        "name": product["name"],
        "description": product.get("description"),
        "price": product["price"],
        "stock": product["stock"]
    }

class QuestionService:
    def __init__(self, db_client: str):
        self.client = AsyncIOMotorClient(db_client)
        self.db = self.client["teacher-questionbank"]
        self.collection = self.db["questionbank"]

    # Create a product
    async def create_question(self, product_data: dict):
        result = await self.collection.insert_one(product_data)
        return str(result.inserted_id)

    # Get a single question by ID
    async def fetch_question(self, product_id: str):
        product = await self.collection.find_one({"_id": ObjectId(product_id)})
        if product:
            return question_serializer(product)
        return None

    # Update a question by ID
    async def update_question(self, product_id: str, product_data: dict):
        result = await self.collection.update_one({"_id": ObjectId(product_id)}, {"$set": product_data})
        if result.modified_count:
            product = await self.fetch_question(product_id)
            return product
        return None

    # Delete a question by ID
    async def delete_question(self, product_id: str):
        result = await self.collection.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0

    # Fetch all question
    async def fetch_questions(self, price: float = None):
        pipeline = []
        if price is not None:
            pipeline.append({
                "$match": {"price": price}  # Add price filter if provided
            })
        products = await self.collection.aggregate(pipeline).to_list(100)  # Awaiting async aggregation and limiting to 100
        return [question_serializer(product) for product in products]
