from typing import Dict, Any, List, Callable, Optional, Tuple
from uuid import UUID
import re
from dotenv import load_dotenv
import logging
from .model_providers import OpenAIProvider, AnthropicProvider
from .agent_schemas import Action, Message
from .prompt_templates import create_base_prompt

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class BaseAgent:
    def __init__(
        self,
        actions: List[Action],
        additional_context: str = None,
        custom_examples: Optional[List[Dict[str, str]]] = None,
        provider: str = "openai",
        model: str = "gpt-4o",
        temperature: float = 1.0,
        max_turns: int = 3
    ):
        """
        Initialize a base agent with customizable system prompt and actions.
        
        Args:
            actions: List of Action objects defining available actions with their handlers
            context: The context that defines the agent's behavior
            custom_examples: Optional list of example interactions
            provider: The model provider to use ('openai' or 'anthropic')
            model: The model to use
            temperature: The temperature parameter for generation
            max_turns: Maximum number of action/observation turns before returning
        """
        # Initialize the appropriate model provider
        if provider == "openai":
            self.model_provider = OpenAIProvider(model=model)
        elif provider == "anthropic":
            self.model_provider = AnthropicProvider(model=model)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
            
        self.temperature = temperature
        self.actions = {action.name: action for action in actions}  # Store actions by name
        self.messages = []
        self.action_re = re.compile('^Action: (\w+): (.*)$')
        self.max_turns = max_turns
        
        # Create the system prompt using the template
        system_prompt = create_base_prompt(
            actions=actions,
            additional_context=additional_context,
            examples=custom_examples
        )
        # logger.info(f"System prompt:\n{system_prompt}")
        
        # Initialize with system prompt
        if system_prompt:
            self.messages.append({
                "role": "system",
                "content": system_prompt,
                "type": "text"
            })
    
    def add_message(self, message: str | Dict[str, Any] | Message | List[Dict[str, Any] | Message]) -> None:
        """Add a message or list of messages to the conversation history."""
        if isinstance(message, list):
            for msg in message:
                if isinstance(msg, Message):
                    # Convert Pydantic model to dict
                    self.messages.append(msg.dict())
                elif isinstance(msg, dict) and 'role' in msg and 'content' in msg and 'type' in msg:
                    self.messages.append(msg)
                else:
                    raise ValueError("Each message must contain 'role', 'content', and 'type'.")
        elif isinstance(message, Message):
            # Convert Pydantic model to dict
            self.messages.append(message.dict())
        elif isinstance(message, dict):
            if 'role' in message and 'content' in message and 'type' in message:
                self.messages.append(message)
            else:
                raise ValueError("Message must contain 'role', 'content', and 'type'.")
        else:
            # Handle string input
            self.messages.append({
                "role": "user",
                "content": str(message),
                "type": "text"
            })

    def execute(self) -> str:
        """Execute a single turn of conversation with the model."""
        logger.info(f"Generating model response with {len(self.messages)} messages")
        response = self.model_provider.generate_response(self.messages, self.temperature)
        logger.info(f"Model response:\n{response}")
        return response

    def process_actions(self, result: str) -> tuple[Optional[str], Optional[str]]:
        """Process any actions in the model's response."""
        logger.info("Processing actions from response...")
        actions = [
            self.action_re.match(a)
            for a in result.split('\n')
            if self.action_re.match(a)
        ]
        
        if not actions:
            # Extract the response part (everything after the last Observation) - case insensitive
            response_lines = result.split('\n')
            response_start = 0
            for i, line in enumerate(response_lines):
                if line.lower().startswith('observation:'):
                    response_start = i + 1
            response = '\n'.join(response_lines[response_start:]).strip()
            return response, None
            
        action_name, action_input = actions[0].groups()
        logger.info(f"Processing action: {action_name} with input: {action_input}")
        
        if action_name not in self.actions:
            error_msg = f"Unknown action: {action_name}. Available actions: {', '.join(self.actions.keys())}"
            logger.error(error_msg)
            return error_msg, None
            
        try:
            action = self.actions[action_name]
            observation = action.handler(action_input)
            logger.info(f"Action executed successfully. Observation: {observation}")
            return None, f"Observation: {observation}"
        except Exception as e:
            error_msg = f"Error executing {action_name}: {str(e)}"
            logger.error(error_msg)
            return error_msg, None

    def query(self, messages: List[Message], user_id: UUID, db) -> Tuple[str, Optional[str]]:
        """
        Process a message through the agent, handling multiple turns of action/observation.
        
        Args:
            messages: The input message(s) to process
            user_id: The ID of the user making the request
            db: Database connection object
            
        Returns:
            A tuple containing (response, observation) where observation may be None
        """
        try:
            logger.info(f"Starting query for user {user_id}")
            self.add_message(messages)
            
            for turn in range(self.max_turns):
                logger.info(f"Processing turn {turn + 1}/{self.max_turns}")
                result = self.execute()
                self.messages.append({
                    "role": "assistant",
                    "content": result,
                    "type": "text"
                })
                
                response, observation = self.process_actions(result)
                logger.info(f"Response: {response}")
                logger.info(f"Observation: {observation}")
                if response is not None:
                    logger.info(f"Query complete with response: {response}")
                    return response
                    
                if observation is not None:
                    logger.info(f"Adding observation to messages: {observation}")
                    self.add_message(observation)
                else:
                    logger.info("No observation to process, ending query")
                    break
                    
            logger.warning("Max turns reached without final response")
            return "Max turns reached without final response", None
            
        except Exception as e:
            error_msg = f"Error in agent loop: {str(e)}"
            logger.error(error_msg)
            return error_msg, None 