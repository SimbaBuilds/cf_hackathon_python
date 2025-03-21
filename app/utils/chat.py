import logging
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from app.agent.base_agent import BaseAgent
from app.agent.agent_schemas import Action, Message
from uuid import UUID
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

def web_search(query: str) -> str:
    """Search the web using DuckDuckGo."""
    logger.info(f"Performing web search with query: {query}")
    try:
        ddgs = DDGS()
        results = ddgs.text(query, max_results=5)
        snippets = [result['snippet'] for result in results]
        logger.debug(f"Web search returned {len(snippets)} results")
        return "\n".join(snippets)
    except Exception as e:
        logger.error(f"Error during web search: {str(e)}")
        raise



def get_chat_response(messages: List[Message], user_id: UUID = None, db=None, provider: str = "openai", model: str = "gpt-4o") -> str:
    """
    Create a web-search enabled agent and get response for messages.
    
    Args:
        messages: List of chat messages
        user_id: Optional user ID for tracking
        db: Optional database connection
        provider: The model provider to use
        model: The specific model to use
        
    Returns:
        The agent's response string
    """
    logger.info(f"Processing chat request - User ID: {user_id}")
    logger.debug(f"Received {len(messages)} messages")

    # Define example web search interaction as a multiline string
    WEB_SEARCH_EXAMPLE = """State: The user is asking about the Trump administration's recent use of the 1787 Alien Enemies Act.
Thought: This requires current information from news sources so I should invoke an action to search the web.
Action: web_search: Trump administration recent use of the 1787 Alien Enemies Act
Observation: [Search Results]
Response to Client: The administration recently declared Tren De Aragua a foreign terrorist organization and invoked the act to deport them.  This situation highlights the nuanced relationship between the executive and judicial branches of the government and the need for better delineation of powers.
"""
    # Define the web search action
    web_search_action = Action(
        name="web_search",
        description="Search the web for current information",
        parameters={
            "query": {
                "type": "string",
                "description": "The search query"
            }
        },
        returns="Text snippets from web search results",
        example="Action: web_search: Current inflation rate in United States 2024"
    )

    try:
        agent = BaseAgent(
            actions=[web_search_action],
            action_handlers={"web_search": web_search},
            custom_examples=[WEB_SEARCH_EXAMPLE],
            context="You are a helpful AI assistant that can search the web and answer questions.",
            provider=provider,
            model=model,
            temperature=1.0,
            max_turns=3
        )
        logger.debug("Agent initialized successfully")
        
        full_response = agent.query(messages, user_id, db)
        logger.debug(f"Raw agent response: {full_response}")
        
        # Extract only the response part - case insensitive matching but preserve original case
        response_marker = "response to client:"
        if response_marker in full_response.lower():
            # Find the actual index in the original string where the response starts
            marker_start = full_response.lower().find(response_marker)
            response = full_response[marker_start + len(response_marker):].strip()
            logger.info("Successfully processed chat response")
            return response
        
        # Fallback in case the expected format isn't found
        logger.warning("Response format not as expected, returning full response")
        logger.info(f"Full response:\n {full_response}")
        return full_response
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        raise
