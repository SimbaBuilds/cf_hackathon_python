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
        
        # Add the "none" action to the list of actions
        none_action = Action(
            name="none",
            description="No action needed",
            parameters={},
            returns="No action taken",
            handler=lambda _: "No action taken"
        )
        all_actions = [none_action] + actions
        self.actions = {action.name: action for action in all_actions}  # Store actions by name
        
        self.messages = []
        self.action_re = re.compile('^Action: (\w+): (.*)$')
        self.max_turns = max_turns
        
        # Create the system prompt using the template
        system_prompt = create_base_prompt(
            actions=all_actions,
            additional_context=additional_context,
            examples=custom_examples
        )
        logger.info(f"System prompt:\n{system_prompt}")
        
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
        
        # Extract thought, action, observation and response using regex
        thought_match = re.search(r'^Thought: (.*)$', result, re.MULTILINE)
        action_match = re.search(r'^Action: (\w+): (.*)$', result, re.MULTILINE)
        observation_match = re.search(r'^Observation: (.*)$', result, re.MULTILINE)
        response_match = re.search(r'^Response to Client: (.*)$', result, re.MULTILINE)
        
        # If we only have a Response to Client, this is a direct response
        if response_match and not any([thought_match, action_match, observation_match]):
            logger.info("Processing direct response without Thought/Action/Observation")
            return response_match.group(1).strip(), None
        
        # If we have a complete response (all fields), process it normally
        if all([thought_match, action_match, observation_match, response_match]):
            action_name, action_input = action_match.groups()
            logger.info(f"Processing complete response with action: {action_name}")
            
            if action_name not in self.actions:
                error_msg = f"Unknown action: {action_name}. Available actions: {', '.join(self.actions.keys())}"
                logger.error(error_msg)
                return error_msg, None
                
            try:
                action = self.actions[action_name]
                observation = action.handler(action_input)
                logger.info(f"Action executed successfully. Observation: {observation}")
                
                # If this was the final response (no more actions needed), return the Response to Client
                if action_name == "none":
                    return response_match.group(1).strip(), None
                
                # Otherwise, return None to continue the conversation loop with the observation
                return None, f"Observation: {observation}"
            except Exception as e:
                error_msg = f"Error executing {action_name}: {str(e)}"
                logger.error(error_msg)
                return error_msg, None
        
        # If we have a thought and action but no observation/response, this is a mid-process response
        if thought_match and action_match and not observation_match and not response_match:
            action_name, action_input = action_match.groups()
            logger.info(f"Processing mid-process response with action: {action_name}")
            
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
        
        # If we have a thought but no action, this is an incomplete response
        if thought_match and not action_match:
            logger.error("Response contains Thought but no Action")
            return "Error: Response missing Action", None
            
        # If we have an action but no thought, this is an invalid response
        if action_match and not thought_match:
            logger.error("Response contains Action but no Thought")
            return "Error: Response missing Thought", None
            
        # If we have an observation but no thought/action, this is an invalid response
        if observation_match and not (thought_match and action_match):
            logger.error("Response contains Observation but missing Thought or Action")
            return "Error: Response missing Thought or Action", None
            
        # If we have a response but no thought/action/observation, this is an invalid response
        if response_match and not (thought_match and action_match and observation_match):
            logger.error("Response contains Response to Client but missing required components")
            return "Error: Response missing required components", None
            
        # If we have no recognizable components, this is an invalid response
        logger.error("Response contains no recognizable components")
        return "Error: Response contains no recognizable components", None

    def query(self, messages: List[Message], user_id: UUID, db) -> str:
        """
        Process a message through the agent, handling multiple turns of action/observation.
        
        Args:
            messages: The input message(s) to process
            user_id: The ID of the user making the request
            db: Database connection object
            
        Returns:
            The final response string to send to the client
        """
        try:
            logger.info(f"Starting query for user {user_id}")
            self.add_message(messages)
            
            action_count = 0
            while True:
                result = self.execute()
                self.messages.append({
                    "role": "assistant",
                    "content": result,
                    "type": "text"
                })
                
                response, observation = self.process_actions(result)
                logger.info(f"Response: {response}")
                logger.info(f"Observation: {observation}")
                
                # If we got a response, return it
                if response is not None:
                    logger.info(f"Query complete with response: {response}")
                    return response
                    
                # If we got an observation, we executed an action
                if observation is not None:
                    action_count += 1
                    logger.info(f"Action {action_count}/{self.max_turns} executed")
                    
                    if action_count >= self.max_turns:
                        logger.warning("Max actions reached without final response")
                        return "Max actions reached without final response"
                        
                    logger.info(f"Adding observation to messages: {observation}")
                    self.add_message(observation)
                else:
                    logger.info("No observation to process, ending query")
                    break
                    
            logger.warning("Query ended without final response")
            return "Query ended without final response"
            
        except Exception as e:
            error_msg = f"Error in agent loop: {str(e)}"
            logger.error(error_msg)
            return error_msg 