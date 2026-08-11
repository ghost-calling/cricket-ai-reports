import os
import time
import logging
from google import genai
from google.genai import errors
from dotenv import load_dotenv
from src.prompts import build_match_report_prompt

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_NAME = "gemini-flash-lite-latest"
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5

def generate_report(match: dict) -> str:
    prompt = build_match_report_prompt(match)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            return response.text.strip()

        except errors.ServerError as e:
            logger.warning(f"Attempt {attempt}/{MAX_RETRIES}: server unavailable ({e}). Retrying...")
            if attempt == MAX_RETRIES:
                raise RuntimeError(f"AI service unavailable after {MAX_RETRIES} attempts") from e
            time.sleep(RETRY_DELAY_SECONDS * attempt)

        except errors.ClientError as e:
            logger.error(f"Client error, not retrying: {e}")
            raise RuntimeError(f"AI request failed: {e}") from e

    raise RuntimeError("Unexpected failure in generate_report")