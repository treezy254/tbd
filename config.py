import os
from dotenv import load_dotenv
import google.generativeai as genai
import logging
from utils import log_func

logger = logging.getLogger(__name__)

@log_func(logger)
def setup(model_name: str = 'gemini-pro') -> genai.GenerativeModel:
    with load_dotenv():
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            logger.error("GOOGLE_API_KEY not found in environment variables.")
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")

    genai.configure(api_key=api_key)
    logger.info("Genai configured successfully.")

    try:
        return genai.GenerativeModel(model_name)
    except Exception as e:
        logger.error(f"Error initializing model {model_name}: {e}")
        raise

if __name__ == "__main__":
    try:
        model = setup()
    except Exception as e:
        logger.critical(f"Failed to initialize the application: {e}")
        exit(1)