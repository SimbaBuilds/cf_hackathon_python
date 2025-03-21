# Define the data models
from typing import List, Literal, Dict, Any, Optional, Callable

from pydantic import BaseModel


class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    type: Literal["text", "image"] = "text"

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    response: str

class Action(BaseModel):
    """Represents an action that can be taken by the agent."""
    name: str
    description: str
    parameters: Dict[str, Dict[str, Any]]
    returns: str
    example: Optional[str] = None
    handler: Callable

    class Config:
        arbitrary_types_allowed = True