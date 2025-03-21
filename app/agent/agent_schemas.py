# Define the data models
from typing import List, Literal, Dict, Any, Optional

from pydantic import BaseModel


class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    type: Literal["text", "image"] = "text"

class ChatRequest(BaseModel):
    messages: List[Message]
    provider: str = "openai"  # Default to OpenAI
    model: str = "gpt-4o"     # Default to GPT-4

class ChatResponse(BaseModel):
    response: str

class Action(BaseModel):
    """Represents an action that can be taken by the agent."""
    name: str
    description: str
    parameters: Dict[str, Any]
    returns: str
    example: Optional[str] = None