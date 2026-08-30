"""module to configure the large language model provider switcher logic"""
import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod


# model providers to iterate through
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.llms.groq import Groq
from litellm.router import Router
from llama_index.llms.litellm import LiteLLM

from tenacity import retry, wait_random_exponential, stop_after_attempt


# modules
from ..utils.logger import logger

# we need access to env variables
load_dotenv()


# enforcing every model provider class to be defined the same way
class LLM(ABC):
    """interface guilding model class creation"""
    @abstractmethod
    def _load_model(self):
        """
        DocString for load_model
        """


# Ollama
class OllamaClass(LLM):
    """
    Docstring for OllamaClass which uses ollama to load models
    """
    def __init__(self) -> None:
        """
        Docstring for __init__
        :param self: Description
        :param model_list: Description
        :type model_list: list[str]
        """
        self.model_name  = None
        self.model_list: list[str] = ['qwen3:4b', 'gemma3:4b']
        self.model  = self._load_model()

    def _load_model(self):
        """
        Generator that loads models from self.model_list one by one.
        """
        for model_name in self.model_list:
            try:
                model = Ollama(model=model_name)
                self.model_name = model_name
                logger.info(f"Selected model: {model_name}")
                return model
            except Exception as err:
                logger.error(f"Failed to init {model_name}: {err}")
        raise RuntimeError("No Ollama models could be initialized")


# Google genai
class GoogleGenAIClass(LLM):
    """provides access to google gemini models"""
    def __init__(self) -> None:
        self.model_name = "gemini-2.5-pro"
        self.api_key = os.environ["GOOGLE_GENAI_API_KEY"]
        self.model = self._load_model()

    @retry(wait=wait_random_exponential(10, 20), stop=stop_after_attempt(5))
    def _load_model(self):
        """loads model for use"""

        return GoogleGenAI(
            model=self.model_name,
            api_key=self.api_key,
        )


# Groq
class GroqClass(LLM):
    """provides access to groq models"""
    def __init__(self) -> None:
        self.model_name = "llama-3.3-70b-versatile"  # "llama-3.1-8b-instant"
        self.api_key = os.environ["GROQ_API_KEY"]
        self.model = self._load_model()

    @retry(wait=wait_random_exponential(10, 20), stop=stop_after_attempt(5))
    def _load_model(self):
        """loads model for use"""

        return Groq(
            model=self.model_name,
            api_key=self.api_key,
            )

class LiteLLMClass(LLM):
    """provides access to litellm models"""
    def __init__(self) -> None:
        self.model_name = "nvidia/meta/llama-3.1-70b-instruct"
        self.model = self._load_model()

    def _model_router(self):
        # Define multiple model instances or backup providers to spread the load
        # to avoid hitting rate limits
        model_list = [
            {
                "model_name": "nvidia-llama",
                "litellm_params": {
                    "model": "nvidia/meta/llama3-70b-instruct",
                    "api_key": os.environ["NVIDIA_API_KEY_1"],
                },
            },
            {
                "model_name": "nvidia-llama",
                "litellm_params": {
                    "model": "nvidia/meta/llama3-70b-instruct",
                    "api_key": os.environ["NVIDIA_API_KEY_2"], # Backup key
                },
            }
        ]

        # Initialize LiteLLM Router with automatic retries on 429 errors
        router = Router(
            model_list=model_list,
            num_retries=3,          # Automatically retry on 429 errors
            retry_after=5,          # Delay between retries in seconds
            cooldown_time=30        # Pause a key for 30s if it hits a rate limit
        )

        return router


    @retry(wait=wait_random_exponential(10, 20), stop=stop_after_attempt(5))
    def _load_model(self):
        """loads model for use"""

        return LiteLLM(
            model=self.model_name,
            router=self._model_router()
            )