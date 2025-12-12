"""module to configure the large language model provider switcher logic"""
from abc import ABC, abstractmethod
import time

# model providers to iterate through
from ollama import Ollama

# modules
from ..logger import logger


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
        self.model_list: list[str] = ['qwen3:4b', 'gemma3:4b']
        self.model, self.model_name: str = self._load_model()

    def _load_model(self):
        """
        Generator that loads models from self.model_list one by one.
        - Measures load time for each model.
        - Skips models that take longer than 5 seconds to load.
        - Yields and returns successfully loaded model.
        """
        for model_name in self.model_list:
            start_time = time.perf_counter()
            try:
                model = Ollama(model_name)
            except Exception as err:
                logger.info(f'error occured: {err}')
            load_time = time.perf_counter() - start_time
            logger.info(f"Model {model_name} loaded in {load_time:.2f}s")
            if load_time <= 5:
                logger.info(f"Model {model_name} successfully loaded in {load_time:.2f}s")
                yield model, model_name
                return  # stop after first fast model
