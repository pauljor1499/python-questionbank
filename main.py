import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get host and port from environment variables
host = os.getenv("HOST", "127.0.0.1")
port = int(os.getenv("PORT", 8002))

if __name__ == "__main__":
    uvicorn.run("src.app:app", host=host, port=port)
