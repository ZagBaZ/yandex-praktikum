import os

from dotenv import load_dotenv

load_dotenv()

auth_token = os.getenv('TOKEN')
print(auth_token)
