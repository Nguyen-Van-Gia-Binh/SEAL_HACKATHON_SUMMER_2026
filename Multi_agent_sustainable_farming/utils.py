from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.gemini import GeminiModel
from dotenv import load_dotenv
import os

load_dotenv(override=True)

def get_model():
    provider = os.getenv('PROVIDER', 'gemini').lower()
    llm = os.getenv('MODEL_CHOICE', 'gemini-2.5-flash')
    api_key = os.getenv('LLM_API_KEY', '')

    if provider == 'gemini' or llm.startswith('gemini-'):
        return GeminiModel(
            model_name=llm,
            api_key=api_key
        )
    else:
        base_url = os.getenv('BASE_URL', 'https://api.openai.com/v1')
        return OpenAIModel(
            model_name=llm,
            base_url=base_url,
            api_key=api_key
        )
