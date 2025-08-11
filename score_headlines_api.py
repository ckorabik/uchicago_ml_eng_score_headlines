"""Score Headlines API"""

import logging
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


model = SentenceTransformer("all-MiniLM-L6-v2")
clf = joblib.load("models/svm.joblib")
logger.info("Model loaded successfully")


def classify_headlines(headlines_list):
    """Classify headlines from a file."""
    predictions = [model.encode(headline) for headline in headlines_list]
    predictions = []
    for headline in headlines_list:
        encoded = model.encode(headline)
        predictions.append(clf.predict([encoded])[0])
    return predictions


@app.get("/status")
def status():
    """API status check."""
    logger.info("Status check called")
    d = {"status": "OK"}
    return d


class ClientData(BaseModel):
    """Pydantic client data class."""

    headlines: list[str]


@app.post("/score_headlines")
def score_headlines(client_info: ClientData):
    """POST method. Accepts list of headlines and returns list of labels."""
    try:
        labels_list = classify_headlines(client_info.headlines)
        logger.info("Successfully scored %d headlines.", len(labels_list))
        return {"labels": labels_list}
    except Exception as e:
        logger.error("Error processing item: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
