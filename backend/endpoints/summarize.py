from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, Optional
import logging
from litellm import completion
from utils.redis_stream import RedisStreamClient
from utils.cost_logger import CostLogger
from dotenv import load_dotenv
import os

load_dotenv()  


router = APIRouter(tags=["LLM Integration"])
redis_client = RedisStreamClient()
cost_logger = CostLogger()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# 模型映射配置
MODEL_MAPPING = {
    "GPT-4o": "gpt-4o",
    "Gemini-Flash": "gemini/gemini-2.0-flash",
    "DeepSeek": "deepseek/deepseek-coder",
    "Claude": "claude-3-opus-20240229",
    "Grok": "xai/grok-2-latest"
}

def create_summary_system_prompt(document_name: Optional[str] = None) -> str:
    """
    为摘要任务生成系统提示语

    Args:
        document_name: 可选的文档名称，用于提供上下文

    Returns:
        格式化后的系统提示语
    """
    doc_context = f"document '{document_name}'" if document_name else "the provided document"
    return f"""
    You are an AI research assistant specializing in technical document analysis. 
    Please provide a structured summary of {doc_context} including:
    
    1. Key concepts and definitions
    2. Main arguments or findings
    3. Supporting evidence or data
    4. Technical specifications (if applicable)
    5. Conclusions and recommendations
    
    Format the summary using Markdown with clear section headings.
    """.strip()

@router.post("/summarize", 
    response_model=Dict[str, Any],
    summary="Generate document summary",
    response_description="The generated summary with token usage")
async def summarize(
    payload: Dict[str, Any] = Body(
        ...,
        examples={
            "normal": {
                "summary": "Standard summary request",
                "value": {
                    "model": "GPT-4o",
                    "pdf_content": "# Research Paper\n\nAbstract: ...",
                    "pdf_name": "quantum_computing.pdf",
                    "selected_text": None
                }
            }
        }
    )
) -> Dict[str, Any]:
    """
    使用 LLM 生成 PDF 内容的结构化摘要

    - **model**: LLM 模型选择（默认：GPT-4o）
    - **pdf_content**: 完整的 PDF 文本内容
    - **pdf_name**: 文档名称（上下文用）
    - **selected_text**: 可选的部分文本进行摘要

    返回 JSON 包含：
    - summary: 生成的 Markdown 格式摘要
    - token_usage: API token 消耗情况
    """
    try:
        # 验证输入
        if not payload.get("pdf_content") and not payload.get("selected_text"):
            raise HTTPException(
                status_code=400,
                detail="Either pdf_content or selected_text must be provided"
            )

        # 提取参数
        model_name = payload.get("model", "GPT-4o")
        content = payload.get("selected_text") or payload.get("pdf_content")
        pdf_name = payload.get("pdf_name")

        # 生成系统提示语
        system_prompt = create_summary_system_prompt(pdf_name)

        # 根据官方用法构造消息列表调用 LLM API
        response = completion(
            model=MODEL_MAPPING.get(model_name, "openai/gpt-4o"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ],
            max_tokens=1500,
            temperature=0.3
        )

        if not response.choices:
            raise HTTPException(
                status_code=500, 
                detail="Empty response from LLM provider"
            )

        summary = response.choices[0].message.content
        token_usage = {
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }

        logger.info(
            f"Summary generated for {pdf_name or 'unnamed document'} "
            f"using {model_name} ({token_usage['total_tokens']} tokens)"
        )
        
        await redis_client.publish("llm_usage", {
            "operation": "summarize",
            "model": model_name,
            "document": pdf_name,
            "token_usage": token_usage
        })
        
        cost_logger.log_cost(model_name, token_usage)

        return {
            "summary": summary,
            "token_usage": token_usage
        }

    except HTTPException as http_err:
        logger.warning(f"Client error: {http_err.detail}")
        raise
    except Exception as e:
        logger.error(f"Summary generation failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Summary generation failed: {str(e)}"
        ) from e
