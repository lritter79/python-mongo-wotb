import requests
from dotenv import load_dotenv
import os
from pathlib import Path

embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"


def generate_embedding(text: str) -> list[float]:
    dotenv_path = Path(".env")
    load_dotenv(dotenv_path=dotenv_path)
    hf_token = os.getenv("HUGGING_FACE")
    response = requests.post(
        embedding_url,
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": text})

    if response.status_code != 200:
        raise ValueError(
            f"Request failed with status code {response.status_code}: {response.text}")

    return response.json()
