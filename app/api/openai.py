import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class OpenAIConnector:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.GPT_MODEL = "gpt-4o-mini"
        self.client = OpenAI(api_key=self.openai_api_key)
        
    async def get_response(self, prompt, system_prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.GPT_MODEL,
                messages=[
                    {"role": "user", "content": prompt},
                    {"role": "system", "content": system_prompt}
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in OpenAI API call: {e}")
            return f"Error generating response: {e}"