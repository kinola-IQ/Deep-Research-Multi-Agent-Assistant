"""module to formate made reuests to workflow"""
from pydantic import BaseModel


# we need consistent formatting for made requests and agent response
class UserRequest(BaseModel):
    """blueprint for user reuests"""
    query: str


class AgentResponse(BaseModel):
    """blueprint for agent response"""
    response: str
