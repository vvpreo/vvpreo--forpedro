import asyncio
import os
import uuid
from pathlib import Path

import instructor
from openai import AsyncOpenAI
from pydantic import BaseModel, Field


class LegalAgentTestCase(BaseModel):
    """Test case for legal agent"""
    is_contract: bool = Field(..., description="Whether the text is a contract")
    contract_text: str = Field(..., min_length=300, max_length=1000, description="Raw contract text")


async def generate_test_case(is_contract: bool) -> LegalAgentTestCase:
    """Generate a single test case using OpenAI API"""
    client = instructor.from_openai(
        AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_APIKEY")
        )
    )

    system_prompt_for_positive_contract_generation = """You are a legal contract generator. Generate realistic contract text samples 
    that can be used for testing a legal risk analyzer. The contract should be between 300-1000 characters 
    and include realistic clauses about termination, liability, or payment terms."""

    system_prompt_for_negative_non_contract_generation = """You are a creative content writer. Generate engaging text samples 
    that are clearly NOT legal contracts - write casual blog posts, product reviews, news articles, personal stories, 
    recipes, travel guides, or technical documentation. The text should be between 300-1000 characters 
    and should have absolutely no legal language, clauses, or contractual elements whatsoever."""

    sys_prompt = system_prompt_for_positive_contract_generation if is_contract else system_prompt_for_negative_non_contract_generation
    user_prompt = "Generate a test contract sample" if is_contract else "Generate a test non-contract sample"

    response = await client.beta.chat.completions.parse(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format=LegalAgentTestCase
    )

    return response.choices[0].message.parsed


async def main():
    """Generate test cases and save them to data folder"""
    # Create data folder in the same directory as the script
    script_dir = Path(__file__).parent
    data_dir = script_dir / "test_data"
    data_dir.mkdir(exist_ok=True)

    for i in range(5):
        for is_contract in [True, False]:
            print(f"Generating test case {i + 1}...")
            try:
                test_case = await generate_test_case(is_contract=is_contract)

                # Generate random UID for the file
                file_uid = str(uuid.uuid4())
                file_path = data_dir / f"{is_contract}__{file_uid}.txt"

                # Save test case to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(test_case.contract_text)

                print(f"Saved test case to {file_path}")
            except Exception as e:
                print(f"Error generating test case {i + 1}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
