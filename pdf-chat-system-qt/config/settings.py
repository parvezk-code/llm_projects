# config/settings.py

from dotenv import load_dotenv
import os


class Settings:

    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model   = os.getenv("OPENAI_MODEL")

        if not self.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY not found. "
                "Please add it to your .env file."
            )