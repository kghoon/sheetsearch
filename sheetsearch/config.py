import dotenv
from os import getenv


dotenv.load_dotenv(dotenv.find_dotenv())


PORT = getenv('PORT', 8000)

OPENAI_API_KEY = getenv('OPENAI_API_KEY')

CUSTOM_SEARCH_API_KEY = getenv('CUSTOM_SEARCH_API_KEY')

CUSTOM_SEARCH_CX = getenv('CUSTOM_SEARCH_CX')