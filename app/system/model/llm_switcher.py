"""module to handle switching of large language models providers"""
from .llms import OllamaClass
from ..logger import logger


# swircher class
class LLMSwitcher:
    """
    Docstring for LLMSwitcher
    """

    # factory method to handle dynamic switching
    def _get_llm(self, provider: str = 'ollama'):
        """switches providers based on speed or presence of errors"""
        if provider.lower() == 'ollama':
            model_provider = OllamaClass()
            logger.info(f'ollama provider loaded.\
                         model name = {model_provider.model_name}')
            return model_provider.model

    def load_model(self):
        """
        utilizes the factory method _get_llm to dynamically switch bwtween
        providers
        """
        model = self._get_llm()
        return model
