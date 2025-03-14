from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, Optional
from utils.redis_stream import RedisStreamClient
from utils.cost_logger import CostLogger
import logging
from litellm import completion
import os

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure router
router = APIRouter(tags=["LLM Integration"])

# Initialize clients
redis_client = RedisStreamClient()
cost_logger = CostLogger()

# Model mapping for LiteLLM format
MODEL_MAPPING = {
    "GPT-4o": "openai/gpt-4o",
    "Gemini-Flash": "google/gemini-1.5-flash",
    "DeepSeek": "deepseek/deepseek-coder",
    "Claude": "anthropic/claude-3-sonnet-20240229",
    "Grok": "xai/grok-1"
}

@router.post("/ask_question")
async def ask_question(
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "model": "GPT-4o",
            "question": "What is the main topic of this document?",
            "pdf_content": "# Example PDF\n\n## Page 1\n\nThis is sample content.",
            "pdf_name": "example.pdf",
            "selected_text": None
        }
    )
) -> Dict[str, Any]:
    """
    Answer a question about PDF content using an LLM.
    
    Args:
        payload: Dict containing model, question, pdf_content, pdf_name, and selected_text
        
    Returns:
        Dict containing the answer and token usage information
    """
    try:
        # Extract parameters
        model_name = payload.get("model", "GPT-4o")
        question = payload.get("question")
        pdf_content = payload.get("pdf_content")
        pdf_name = payload.get("pdf_name")
        selected_text = payload.get("selected_text")
        
        if not question:
            raise HTTPException(status_code=400, detail="Missing question")
        if not pdf_content and not pdf_name:
            raise HTTPException(status_code=400, detail="Missing PDF content or name")
        
        # Determine what content to search
        context = selected_text if selected_text else pdf_content
        
        # Create the prompt for system message
        prompt = create_qa_prompt(question, context, pdf_name)
        
        # Map to LiteLLM model format
        model = MODEL_MAPPING.get(model_name, "openai/gpt-4o")
        
        # Prepare messages for LiteLLM
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ]
        
        # Call LLM to generate answer using LiteLLM
        response = completion(
            model=model,
            messages=messages,
            max_tokens=1000
        )
        
        # Extract answer and token usage
        answer = response.choices[0].message.content
        token_usage = {
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        
        # Log usage to Redis
        await redis_client.publish("llm_usage", {
            "action": "ask_question",
            "model": model_name,
            "pdf_name": pdf_name,
            "question": question,
            "token_usage": token_usage
        })
        
        # Log cost
        cost_logger.log_cost(model_name, token_usage)
        
        return {
            "answer": answer,
            "token_usage": token_usage
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")

def create_qa_prompt(question: str, context: str, document_name: Optional[str] = None) -> str:
    """
    Create a prompt for answering a question about document content.
    
    Args:
        question: The question to answer
        context: The context to search for answers
        document_name: Optional name of the document
        
    Returns:
        Formatted prompt string
    """
    doc_context = f"document '{document_name}'" if document_name else "the provided document"
    
    prompt = f"""
    You are an AI assistant that helps answer questions about documents.
    Please answer the following question about {doc_context}. Base your answer only on the 
    information provided in the context below. If the answer cannot be found in the context, please 
    state that clearly.
    
    Context:
    {context}
    """
    
    return prompt.strip()