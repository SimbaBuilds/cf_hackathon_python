from os import getenv
from fastapi import HTTPException, APIRouter
from uuid import UUID
from app.agents.agent_schemas import ChatRequest, ChatResponse
from app.agents.head_agent import query_agent


router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, user_id: UUID, db=None) -> ChatResponse:
    try:
        # Convert messages to the format expected by query_agent
        messages = request.messages[0].content if request.messages else ""
        
        # Call query_agent instead of OpenAI
        response, observation = query_agent(messages, user_id, db)
        
        if not response:
            raise HTTPException(
                status_code=500,
                detail="No response received from agent"
            )
        
        return ChatResponse(response=response)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat request: {str(e)}"
        )