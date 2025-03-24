from typing import Dict, Any, List, Optional, Union
from .agent_schemas import Action
from datetime import datetime
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
    additional_context: str = "No additional context",
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
1. Review the conversation and the most recent message from the user
2. Invoke available actions if necessary 
3. Provide a response to the human user

Note: The current date and time is {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Additional Context: {additional_context}

=== Thought Process ===
You must follow these example structures in your responses:

1. Thought: Explain your reasoning about what to do next
2. Action: Either invoke an action using exactly this format: Action: <action_name>: <parameters>
   OR if no action is needed, use: Action: none: No action needed
If an action is needed, stop your output here and you will be called again with the result of the action.
3. Observation: Either the result of the action, or "[No action taken]" if no action was needed
4. Response to Client: Your final response to the human user

Example structure:
Thought: The user is asking about X, which requires Y action
Action: Y: <parameters>
Observation: <result of Y action>
Response to Client: <final response>

OR when no action is needed:
Thought: This is a simple greeting that doesn't require any action
Action: none: No action needed
Observation: [No action taken]
Response to Client: Hello! How can I help you today?

Note: the human user will not see your Thought Process. They will only see the text after Response to Client:
"""

    # Convert base prompt to list of lines
    prompt_sections = base_prompt.split('\n')

    if actions:
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
            "=== Examples of Full Flow ===",
            "",
        ])
        
        if isinstance(examples, str):
            prompt_sections.append(examples)
        else:
            # Format the list of examples
            formatted_examples = []
            for i, example in enumerate(examples):
                formatted_examples.append(f"Example {i+1}:")
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

