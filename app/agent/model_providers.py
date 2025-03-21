from abc import ABC, abstractmethod
from typing import List, Dict, Any
from openai import OpenAI
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

class ModelProvider(ABC):
    """Abstract base class for different LLM providers"""
    
    @abstractmethod
    def generate_response(self, messages: List[Dict[str, Any]], temperature: float) -> str:
        """Generate a response from the model given a list of messages"""
        pass

class OpenAIProvider(ModelProvider):
    """OpenAI model provider implementation"""
    
    def __init__(self, model: str = "gpt-4"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
    
    def generate_response(self, messages: List[Dict[str, Any]], temperature: float) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature
        )
        return completion.choices[0].message.content

class AnthropicProvider(ModelProvider):
    """Anthropic model provider implementation"""
    
    def __init__(self, model: str = "claude-3-sonnet-20240229"):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = model
    
    def generate_response(self, messages: List[Dict[str, Any]], temperature: float) -> str:
        # Convert messages to Anthropic format
        system_prompt = next((msg["content"] for msg in messages if msg["role"] == "system"), None)
        
        # Build the messages for Anthropic
        anthropic_messages = []
        for msg in messages:
            if msg["role"] != "system":  # System message is handled separately
                anthropic_messages.append({
                    "role": "user" if msg["role"] == "user" else "assistant",
                    "content": msg["content"]
                })
        
        completion = self.client.messages.create(
            model=self.model,
            messages=anthropic_messages,
            system=system_prompt,
            temperature=temperature
        )
        return completion.content[0].text 