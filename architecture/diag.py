from diagrams import Diagram, Cluster, Edge
from diagrams.programming.language import Python
from diagrams.onprem.container import Docker
from diagrams.onprem.inmemory import Redis

from diagrams.saas.chat import Slack  # For chat/LLM icons
from diagrams.onprem.network import Nginx  # For API/server icons
from diagrams.onprem.client import Users  # For frontend
from diagrams.programming.framework import Flask  # Similar to FastAPI
from diagrams.custom import Custom

# Define custom icons for components not available in standard library
with Diagram("LLM_Architecture", show=False, direction="TB"):
    
    # Define main user interaction point
    with Cluster("User Interface"):
        streamlit = Users("Streamlit Frontend")  # Using Users icon for frontend
    
    # Define backend services
    with Cluster("Backend Services"):
        with Cluster("API Layer"):
            fastapi = Flask("FastAPI Backend")  # Using Flask as it's similar to FastAPI
        
        with Cluster("PDF Processing"):
            pdf_processor = Python("PDF Processor")  # Using Python icon
            markdown_converter = Python("Markdown Converter")
        
        with Cluster("LLM Integration"):
            litellm = Slack("LiteLLM Client")  # Using Slack icon for LLM client
            
            with Cluster("LLM Providers"):
                gpt4o = Slack("GPT-4o")
                gemini = Slack("Gemini-Flash")
                claude = Slack("Claude")
                deepseek = Slack("DeepSeek")
                grok = Slack("Grok")
            
            token_manager = Python("Token Manager")
    
    # Define storage and messaging
    redis = Redis("Redis Event Streaming")
    
    # Define relationships
    streamlit >> Edge(label="API Requests") >> fastapi
    fastapi >> Edge(label="Process PDFs") >> pdf_processor
    pdf_processor >> Edge(label="Convert to Markdown") >> markdown_converter
    
    fastapi >> Edge(label="Publish Events") >> redis
    redis >> Edge(label="Consume Events") >> fastapi
    
    fastapi >> Edge(label="LLM Requests") >> litellm
    litellm >> token_manager
    
    litellm >> gpt4o
    litellm >> gemini
    litellm >> claude
    litellm >> deepseek
    litellm >> grok
    
    markdown_converter >> Edge(label="Processed Data") >> redis
