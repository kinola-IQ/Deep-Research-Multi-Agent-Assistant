"""module to keeptrack of agent workflow"""

from llama_index.core.workflow import Event


# events
class FeedbackEvent(Event):
    """
    Docstring for FeedbackEvent
    """
    feedback: str


class ReviewEvent(Event):
    """
    Docstring for ReviewEvent
    """
    report: str


class GenerateEvent(Event):
    """
    Docstring for GenerateEvent
    """
    research_topic: str


class QuestionEvent(Event):
    """
    Docstring for QuestionEvent
    """
    question: str


class AnswerEvent(Event):
    """
    Docstring for AnswerEvent
    """
    question: str
    answer: str


class ProgressEvent(Event):
    """
    Docstring for ProgressEvent
    """
    msg: str
