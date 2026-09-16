import os
from dotenv import load_dotenv
load_dotenv()
from cerebras.cloud.sdk import Cerebras

client = Cerebras(api_key=os.environ.get('CEREBRAS_API_KEY'))
models = client.models.list()
for m in models.data:
    print(m.id)