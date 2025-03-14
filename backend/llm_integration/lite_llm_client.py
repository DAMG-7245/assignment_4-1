from litellm import completion
import os
import logging

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set environment variables for API keys
os.environ["OPENAI_API_KEY"] = "your-openai-key"
os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-key"
os.environ["GOOGLE_API_KEY"] = "your-google-key"
os.environ["DEEPSEEK_API_KEY"] = "your-deepseek-key"
os.environ["XAI_API_KEY"] = "your-xai-key"

async def generate_response(
    model: str,
    prompt: str,
    max_tokens: int = 1000,
    temperature: float = 0.7,
    system_message: str = None
):
    try:
        # Map your model names to litellm format
        model_mapping = {
            "GPT-4o": "openai/gpt-4o",
            "Gemini-Flash": "google/gemini-1.5-flash",
            "DeepSeek": "deepseek/deepseek-coder",
            "Claude": "anthropic/claude-3-sonnet-20240229",
            "Grok": "xai/grok-1"
        }
        
        provider_model = model_mapping.get(model, "openai/gpt-4o")
        
        # Construct messages
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        # Make API request through litellm
        response = completion(
            model=provider_model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        content = response.choices[0].message.content
        
        # Extract token usage
        token_usage = {
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        
        logger.info(
            f"Generated response for model {model} "
            f"({token_usage['input_tokens']} input, {token_usage['output_tokens']} output tokens)"
        )
        
        return {
            "content": content,
            "token_usage": token_usage
        }
        
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return {
            "content": f"I apologize, but I encountered an error while processing your request: {str(e)}",
            "token_usage": {
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0
            }
        }