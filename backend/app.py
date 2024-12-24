from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import threading
import logging
from datetime import datetime

# Initialize the FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(
    filename="logs/api_logs.json",
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Load the summarization model
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

# Define the input data model
class SummarizationRequest(BaseModel):
    text: str
    threads: int

# Thread-safe function to handle summarization
def summarize_chunk(text, results, index):
    try:
        summary = summarizer(
            text, max_length=50, min_length=5, do_sample=False
        )[0]['summary_text']
        results[index] = summary
    except Exception as e:
        results[index] = str(e)

# Endpoint for summarization
@app.post("/summarize")
async def summarize(request: SummarizationRequest):
    logging.info("Request received for summarization.")
    text = request.text
    threads_count = request.threads

    # Split text into chunks for multi-threaded summarization
    chunks = [text] * threads_count  # Mock: Create threads_count copies of text for testing
    results = [None] * threads_count
    threads = []

    start_time = datetime.now()

    # Start threads for processing
    for i in range(threads_count):
        thread = threading.Thread(target=summarize_chunk, args=(chunks[i], results, i))
        threads.append(thread)
        thread.start()

    # Wait for threads to complete
    for thread in threads:
        thread.join()

    end_time = datetime.now()
    processing_time = (end_time - start_time).total_seconds()

    logging.info(f"Request processed in {processing_time} seconds.")
    return {"summaries": results, "processing_time": processing_time}
