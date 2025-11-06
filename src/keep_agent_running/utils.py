from openai import OpenAI

from pydantic import BaseModel, Field
from typing import Type
import json


class LLMConfig(BaseModel):
    """Configuration for vLLM-hosted language models."""
    base_url: str = Field(..., description="Base URL of the vLLM server (e.g., http://10.4.33.17:80/v1)")
    api_key: str = Field(default="dummy-key", description="API key (not used for most vLLM deployments)")
    model_name: str = Field(..., description="Name of the model to use (e.g., inarikami/DeepSeek-R1-Distill-Qwen-32B-AWQ)")
    temperature: float = Field(default=0.1, description="Sampling temperature for generation")
    max_tokens: int = Field(default=2000, description="Maximum tokens to generate")


def make_output_into_pydantic_models(output: str, pydantic_model: Type[BaseModel], llm_config: LLMConfig) -> BaseModel:
    """
    Convert a text output into a Pydantic model using a vLLM-hosted LLM.
    
    Args:
        output: The text output to convert
        pydantic_model: The Pydantic model class to convert to
        llm_config: Configuration for the vLLM-hosted LLM
    
    Returns:
        An instance of the pydantic_model with data extracted from output
    """
    # Create OpenAI client from config
    llm = OpenAI(
        base_url=llm_config.base_url,
        api_key=llm_config.api_key
    )
    
    # Get the JSON schema from the Pydantic model
    schema = pydantic_model.model_json_schema()
    
    # Create a system prompt that instructs the LLM to extract structured data
    system_prompt = f"""You are a data extraction assistant. Your task is to extract information from the provided text and return it as a JSON object that matches the following schema:

{json.dumps(schema, indent=2)}

Rules:
1. Return ONLY valid JSON that matches the schema exactly
2. Do not include any explanations, markdown formatting, or additional text
3. If a field is not present in the input, use null or an appropriate default value
4. Ensure all required fields are present"""

    # Call the LLM
    response = llm.chat.completions.create(
        model=llm_config.model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": output}
        ],
        temperature=llm_config.temperature,
        max_tokens=llm_config.max_tokens
    )
    
    # Extract the content and clean it if needed
    content = response.choices[0].message.content
    
    # Some models might wrap JSON in markdown code blocks or include thinking tags
    if "```json" in content:
        # Extract JSON from markdown code block
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    
    # Remove <think> tags if present (DeepSeek R1 models often include these)
    if "<think>" in content:
        # Extract content after </think>
        parts = content.split("</think>")
        if len(parts) > 1:
            content = parts[1].strip()
    
    # Validate and return the Pydantic model
    return pydantic_model.model_validate_json(content)


if __name__ == "__main__":
    # Configure your vLLM-hosted model
    llm_config = LLMConfig(
        base_url="http://10.4.33.17:80/v1",
        model_name="inarikami/DeepSeek-R1-Distill-Qwen-32B-AWQ",
        temperature=0.1,
        max_tokens=2000
    )

    # Define the target Pydantic model
    class Person(BaseModel):
        name: str
        age: int
        occupation: str

    # Test the function
    text = "John is a 30 year old software engineer"
    person = make_output_into_pydantic_models(text, Person, llm_config)
    print(person)  