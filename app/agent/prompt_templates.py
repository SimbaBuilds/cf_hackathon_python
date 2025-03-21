from typing import Dict, Any, List, Optional, Union
from .agent_schemas import Action

def format_action(action: Action) -> str:
    """Format a single action into a string description."""
    action_str = [
        f"{action.name}:",
        f"  Description: {action.description}",
        "  Parameters:"
    ]
    
    for param_name, param_details in action.parameters.items():
        param_type = param_details.get("type", "any")
        param_desc = param_details.get("description", "")
        action_str.append(f"    - {param_name} ({param_type}): {param_desc}")
    
    action_str.append(f"  Returns: {action.returns}")
    
    if action.example:
        action_str.append(f"  Example: {action.example}")
    
    return "\n".join(action_str)

def create_base_prompt(
    actions: List[Action],
    context: str,
    examples: Optional[Union[str, List[Union[str, Dict[str, str]]]]] = None
) -> str:
    """
    Create a base system prompt that can be customized.
    
    Args:
        actions: List of available actions the agent can perform
        context: Additional context about the agent's role and capabilities
        examples: Optional examples as either a multiline string, list of example dictionaries, or list of example strings
        
    Returns:
        A formatted system prompt combining all components
    """
    # Core prompt structure as a formatted multiline string
    base_prompt = f"""=== Context ===
You are an AI agent designed to interact with human users and invoke actions when necessary. Your role is to:
1. Review the request given context
2. Invoke specific actions when required
3. Provide responses to the human user

Additional Context: {context}

=== Thought Process ===
You operate in a loop of phases: Thought, Action, and Observation.
At the end of the loop you will output a Response.

1. Analyze the current situation and determine how to proceed
2. If an action is needed, request it using exactly this format: Action: <action_name>: <parameters>.  If multiple actions are needed, invoke only the one that needs to be done next.
3. View the results of the action
4. If more actions are needed, repeat the process. If not, provide a final response to the human user in exactly this format:
Response to Client: <response>
"""

    # Convert base prompt to list of lines
    prompt_sections = base_prompt.split('\n')

    # Add available actions section
    prompt_sections.extend([
        "",
        "=== Available Actions ===",
        "",
        "\n\n".join(format_action(action) for action in actions),
        "",
    ])

    # Add examples if provided
    if examples:
        prompt_sections.extend([
            "",
            "=== Examples ===",
            "",
        ])
        
        if isinstance(examples, str):
            prompt_sections.append(examples)
        else:
            # Format the list of examples
            formatted_examples = []
            for example in examples:
                if isinstance(example, str):
                    formatted_examples.append(example)
                else:
                    # Handle dictionary examples
                    formatted_example = []
                    for key, value in example.items():
                        formatted_example.append(f"{key}: {value}")
                    formatted_examples.append("\n".join(formatted_example))
            prompt_sections.append("\n\n".join(formatted_examples))
        
        prompt_sections.append("")

    # Combine all sections, filtering out empty strings
    return "\n".join(section for section in prompt_sections if section)

# Example usage:
example_web_search_action = Action(
    name="web_search",
    description="Search the web for current information",
    parameters={
        "query": {
            "type": "string",
            "description": "The search query"
        }
    },
    returns="Text snippets from web search results",
    example="Action: web_search: Current inflation rate in United States 2025"
)

# Example with multiline string format
example_prompt = create_base_prompt(
    actions=[example_web_search_action],
    context="This agent helps users find current information from the web.",
    examples="""State: The user is asking about the Trump administration's recent use of the 1787 Alien Enemies Act, and they are concerned about executive overreach.
Thought: This requires current information from news sources so I should invoke an action to search the web.
Action: web_search: Trump administration recent use of the 1787 Alien Enemies Act
Observation: The administration recently declared Tren De Aragua a foreign terrorist organization and invoked the act to deport them.  A local court has ruled that the administration's actions are unconstitutional and ordered them to stop, but the administration has refused to comply.
Response to Client: The administration recently declared Tren De Aragua a foreign terrorist organization and invoked the act to deport them.  This situation highlights the nuanced relationship between the executive and judicial branches of the government and the need for better delineation of powers.
"""
) 