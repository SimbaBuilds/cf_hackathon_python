from fastapi import HTTPException, APIRouter
from uuid import UUID
from app.agent.agent_schemas import ChatRequest, ChatResponse
from app.utils.chat import get_chat_response
import logging

router = APIRouter()
logger = logging.getLogger(__name__)



@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, user_id: UUID = None, db=None) -> ChatResponse:
    try:
        logger.info(f"Received chat request with {len(request.messages)} messages")
        
        # Get response using the utility function, passing all messages and settings
        response = get_chat_response(
            messages=request.messages,
            user_id=user_id,
            db=db,
            provider=request.provider,
            model=request.model
        )
        
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