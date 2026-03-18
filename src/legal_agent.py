import os

import instructor
from openai import AsyncOpenAI

from schemas import AnalyzeResponse

system_prompt = '''
You are a helpful assistant that analyzes contracts.
'''


async def analyze_contract_text(text: str) -> AnalyzeResponse:
    try:
        client = instructor.from_openai(
            AsyncOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_APIKEY")
            )
        )

        response = await client.beta.chat.completions.parse(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            response_format=AnalyzeResponse
        )

        return response.choices[0].message.parsed

    except Exception:
        raise
