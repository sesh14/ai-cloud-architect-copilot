import json
import re
from json import JSONDecodeError

from app.infrastructure.llm.bedrock import BedrockLLM
from app.infrastructure.llm.openai import OpenAILLM
from app.core.config import settings
from app.domain.models import ArchitectureResponse
from app.core.logging import logger


class ArchitectService:

    def __init__(self):
        if settings.LLM_PROVIDER == "bedrock":
            self.llm = BedrockLLM()
        else:
            self.llm = OpenAILLM()

    def _clean_json(self, raw_output: str) -> str:
        raw_output = raw_output.strip()
        match = re.search(r"\{.*\}", raw_output, re.DOTALL)
        if match:
            return match.group(0)
        return raw_output

    async def generate_architecture(self, use_case: str) -> ArchitectureResponse:

        base_prompt = f"""
You are a Principal AWS Solutions Architect.

Design a production-grade AWS architecture for:

{use_case}

Respond ONLY in valid JSON.

Schema:
{{
  "services": ["short AWS service names only"],
  "security": "max 5 bullet points",
  "scalability": "max 5 bullet points",
  "cost_optimization": "max 5 bullet points"
}}

Rules:
- Keep responses concise.
- Do NOT include explanations outside JSON.
"""

        for attempt in range(3):

            logger.info(
                "architecture_generation_attempt",
                attempt=attempt + 1,
                use_case=use_case
            )

            raw_output = await self.llm.generate(base_prompt)

            try:
                cleaned = self._clean_json(raw_output)
                parsed = json.loads(cleaned)
                validated = ArchitectureResponse(**parsed)

                logger.info("architecture_generation_success")

                return validated

            except (JSONDecodeError, TypeError) as e:
                logger.warning(
                    "invalid_json_from_model",
                    error=str(e)
                )

                base_prompt += "\n\nIMPORTANT: Return ONLY raw JSON."

        logger.error("architecture_generation_failed_after_retries")
        raise Exception("Model failed to return valid structured JSON.")
