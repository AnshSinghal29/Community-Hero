import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv('XAI_API_KEY'),
    base_url='https://api.groq.com/openai/v1'
)

try:
    res = client.chat.completions.create(
        model='qwen/qwen3.6-27b',
        messages=[{'role': 'user', 'content': 'Say hello in JSON: {"message": "hello"}'}]
    )
    print("RESPONSE:", repr(res.choices[0].message.content))
except Exception as e:
    print("ERROR:", str(e))
