"""module to handle the loading of the models"""
from contextlib import asynccontextmanager
from ollama import Ollama
from tenacity import (
    retry,
    wait_random_exponential,
    stop_after_attempt
)
from ..logger import logger
from .llm_switcher import LLMSwitcher
from fastapi import FastAPI


# until loaded, the model does not exist
model = None


# helper function to load the model
@retry(wait=wait_random_exponential(min=5, max=12),
       stop=stop_after_attempt(5))
def load_model():
    """
    loads the model using ollama
    Args:
    :params model_name: name of the model to be loaded
    :returns: None
    """
    try:
        global model
        model = LLMSwitcher().load_model()
    except Exception as e:
        print(f'could not load the model: {e}')


# helper funciton to load model on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # model
    load_model()
    logger.info('model loaded successfully')
    yield

