import boto3
import json
import asyncio
from botocore.config import Config

from app.core.config import settings
from .base import BaseLLM


class BedrockLLM(BaseLLM):

    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=settings.AWS_REGION,
            config=Config(
                retries={"max_attempts": 3},
                read_timeout=300,
                connect_timeout=60,
            ),
        )
        self.model_id = settings.BEDROCK_MODEL_ID

    async def generate(self, prompt: str) -> str:
        loop = asyncio.get_running_loop()

        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "temperature": 0.3,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        })

        response = await loop.run_in_executor(
            None,
            lambda: self.client.invoke_model(
                modelId=self.model_id,
                body=body
            )
        )

        result = json.loads(response["body"].read())
        return result["content"][0]["text"]
