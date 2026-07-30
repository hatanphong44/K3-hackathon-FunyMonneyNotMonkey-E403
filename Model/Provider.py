import os
from openai import OpenAI


class OpenRouterProvider:
    def __init__(
        self,
        api_key=None,
        model="openai/gpt-4o-mini",
    ):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
        )

    def generate(
        self,
        prompt,
        system_prompt="You are a helpful assistant.",
    ):

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
        )

        return response.choices[0].message.content