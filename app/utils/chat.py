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
        results = list(ddgs.text(query, max_results=5))
        if not results:
            return "No results found."
            
        # Handle both old and new response formats
        snippets = []
        for result in results:
            if isinstance(result, dict):
                snippet = result.get('snippet') or result.get('body') or result.get('text', '')
                title = result.get('title', '')
                link = result.get('link', '')
            else:
                # If result is not a dict, convert to string
                snippet = str(result)
                title = ''
                link = ''
                
            if title and link:
                snippets.append(f"{title}\n{snippet}\nSource: {link}")
            else:
                snippets.append(snippet)
                
        logger.debug(f"Web search returned {len(snippets)} results")
        return "\n\n".join(snippets)
    except Exception as e:
        logger.error(f"Error during web search: {str(e)}")
        raise



def get_chat_response(messages: List[Message], user_id: UUID = None, db=None) -> str:
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
    WEB_SEARCH_EXAMPLE = """Web Search Example:
State: The user is asking about the Trump administration's recent use of the 1787 Alien Enemies Act.
Thought: This requires current information from news sources so I should invoke an action to search the web.
Action: web_search: Trump administration recent use of the 1787 Alien Enemies Act
Observation: [Search Results]
Response to Client: The administration recently declared Tren De Aragua a foreign terrorist organization and invoked the act to deport them.  This situation highlights the nuanced relationship between the executive and judicial branches of government and the need for better delineation of powers.
"""

    NO_ACTION_EXAMPLE = """No Action Example:
State: The user is greeting me.
Thought: This is a greeting and no action is needed.
Action: none: No action needed
Observation: [No action taken]
Response to Client: Hello! How can I help you today?
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
        example="Action: web_search: Current inflation rate in United States 2024",
        handler=web_search
    )

    try:
        head_agent = BaseAgent(
            actions=[web_search_action],
            custom_examples=[WEB_SEARCH_EXAMPLE, NO_ACTION_EXAMPLE],
            additional_context="You are a helpful AI assistant that can search the web and answer questions.",
            temperature=1.0,
            provider="openai",
            model="gpt-4o",
            max_turns=4
        )
        logger.debug("Agent initialized successfully")
        
        full_response = head_agent.query(messages, user_id, db)
        logger.debug(f"Raw agent response: {full_response}")
        
        # Extract the response part from the tuple
        if isinstance(full_response, tuple):
            response_text = full_response[0]
        else:
            response_text = full_response
            
        # If the response is already processed (no prefix), return it directly
        if not response_text.lower().startswith('thought:') and not response_text.lower().startswith('action:'):
            return response_text
            
        # Otherwise, extract the response part after "Response to Client:"
        response_marker = "response to client:"
        if response_marker in response_text.lower():
            marker_start = response_text.lower().find(response_marker)
            return response_text[marker_start + len(response_marker):].strip()
        
        # Fallback only if we have a malformed response
        logger.warning("Response format not as expected, returning full response")
        logger.info(f"Full response:\n {response_text}")
        return response_text
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        raise
