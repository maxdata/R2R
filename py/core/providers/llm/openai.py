import logging
import os
from typing import Any

from openai import AsyncAzureOpenAI

from core.base.abstractions import GenerationConfig
from core.base.providers.llm import CompletionConfig, CompletionProvider

logger = logging.getLogger()


class OpenAICompletionProvider(CompletionProvider):
    def __init__(self, config: CompletionConfig, *args, **kwargs) -> None:
        super().__init__(config)
        if config.provider != "azure_openai":
            logger.error(f"Invalid provider: {config.provider}")
            raise ValueError(
                "AzureOpenAICompletionProvider must be initialized with config with `azure_openai` provider."
            )
        if not os.getenv("AZURE_OPENAI_API_KEY"):
            logger.error("Azure OpenAI API key not found")
            raise ValueError(
                "Azure OpenAI API key not found. Please set the AZURE_OPENAI_API_KEY environment variable."
            )
        self.client = AsyncAzureOpenAI(api_key=os.getenv("AZURE_OPENAI_API_KEY"))
        logger.debug("AzureOpenAICompletionProvider initialized successfully")

    def _get_base_args(self, generation_config: GenerationConfig) -> dict:
        args = {
            "model": generation_config.model,
            "temperature": generation_config.temperature,
            "top_p": generation_config.top_p,
            "stream": generation_config.stream,
            "max_tokens": generation_config.max_tokens_to_sample,
        }
        if generation_config.functions is not None:
            args["functions"] = generation_config.functions
        if generation_config.tools is not None:
            args["tools"] = generation_config.tools
        if generation_config.response_format is not None:
            args["response_format"] = generation_config.response_format
        return args

    async def _execute_task(self, task: dict[str, Any]):
        messages = task["messages"]
        generation_config = task["generation_config"]
        kwargs = task["kwargs"]

        args = self._get_base_args(generation_config)
        args["messages"] = messages
        args = {**args, **kwargs}

        logger.debug(f"Executing async Azure OpenAI task with args: {args}")
        try:
            response = await self.client.chat.completions.create(**args)
            logger.debug("Async Azure OpenAI task executed successfully")
            return response
        except Exception as e:
            logger.error(f"Async Azure OpenAI task execution failed: {str(e)}")
            raise

    def _execute_task_sync(self, task: dict[str, Any]):
        messages = task["messages"]
        generation_config = task["generation_config"]
        kwargs = task["kwargs"]

        args = self._get_base_args(generation_config)
        args["messages"] = messages
        args = {**args, **kwargs}

        logger.debug(f"Executing sync Azure OpenAI task with args: {args}")
        try:
            response = self.client.chat.completions.create(**args)
            logger.debug("Sync Azure OpenAI task executed successfully")
            return response
        except Exception as e:
            logger.error(f"Sync Azure OpenAI task execution failed: {str(e)}")
            raise
