from fastapi import FastAPI, HTTPException, Query
from models import Question, QuestionUpdate
from question_service import QuestionService
from typing import Optional

app = FastAPI()

db_url = "mongodb+srv://admin:admin@cluster0.aeltnpt.mongodb.net/"
product_service = QuestionService(db_url)

# Create a product
@app.post("/products/")
async def create_product(product: Question):
    product_data = product.model_dump()
    product_id = await product_service.create_product(product_data)
    return {"id": product_id}

# Get a single product by ID
@app.get("/products/{product_id}")
async def read_product(product_id: str):
    product = await product_service.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Update a product by ID
@app.put("/products/{product_id}")
async def update_product(product_id: str, product_update: QuestionUpdate):
    updated_data = {k: v for k, v in product_update.model_dump().items() if v is not None}
    if not await product_service.get_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    await product_service.update_product(product_id, updated_data)
    return {"msg": "Product updated"}

# Delete a product by ID
@app.delete("/products/{product_id}")
async def delete_product(product_id: str):
    if not await product_service.delete_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"msg": "Product deleted"}

# Fetch all questions
@app.get("/questions/")
async def fetch_questions(price: Optional[float] = Query(None)):
    products = await product_service.fetch_questions(price)
    return products