from fastapi import FastAPI, Request
import openai
import redis
from elasticsearch import Elasticsearch
import os

app = FastAPI()

# Initialize Redis and Elasticsearch clients
redis_client = redis.Redis(host='localhost', port=6379, db=0)
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Set OpenAI API key
openai.api_key = os.getenv("sk-proj-hFm4VU0vtfaNy2pslItbT3BlbkFJ0pVyRqRcoGnxAdAsSY2c")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data["message"]
    
    # Retrieve relevant information from the corpus
    response = es.search(index="wine_corpus", query={"match": {"content": user_message}})
    
    if response['hits']['total']['value'] > 0:
        answer = response['hits']['hits'][0]['_source']['content']
    else:
        answer = "Please contact the business directly for more information."
    
    return {"answer": answer}

# For development, use this command to run the app:
# uvicorn main:app --reload
