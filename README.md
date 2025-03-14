# LLM

### **Project Summary**

BACKEND URL: https://backend-980441147674.us-east1.run.app

FRONTEND URL :https://frontend-980441147674.us-east1.run.app

Demo Link:

Codelab:

Video Link:

## Overview
This application provides a comprehensive solution for processing, analyzing, and interacting with PDF documents using Large Language Models (LLMs). The system allows users to upload PDF files, convert them to Markdown format, and leverage various LLMs to summarize content and answer specific questions about the documents.

The architecture follows a modern microservices approach with a Streamlit frontend for user interaction, FastAPI backend for request handling, Redis for event streaming, and LiteLLM for unified access to multiple LLM providers. Token usage tracking is implemented to monitor and report on API costs.

## Features

### **PDF Management**
- Upload new PDF documents  
- Convert PDFs to Markdown format  
- Select from previously processed documents  

### **LLM Integration**
- Select from multiple LLM providers (OpenAI, Google, Anthropic, DeepSeek, XAI)  
- Generate document summaries  
- Ask specific questions about document content  
- View token usage and cost metrics  

### **System Features**
- Event-driven architecture with Redis streams  
- Comprehensive token usage tracking  
- Error handling and logging  
- Docker containerization for easy deployment  

## Tech Stack

### **Frontend: Streamlit**
- Interactive web interface  
- PDF selection and upload  
- LLM provider selection  
- Summary and Q&A functionality  

### **Backend: FastAPI**
- RESTful API endpoints  
- PDF processing and storage  
- LLM request handling  
- Token usage tracking  

### **LLM Integration: LiteLLM**
- Unified API for multiple LLM providers  
- Token counting and cost calculation  
- Error handling and retries  

### **Infrastructure**
- Redis for event streaming and communication  
- Docker for containerization  
- Docker Compose for multi-service orchestration  

## User Guide

### **Selecting a PDF**
1. Launch the application  
2. Choose between:  
   - **Select Existing PDF**: Pick from previously processed documents  
   - **Upload New PDF**: Upload a new PDF file for processing  

### **Working with LLMs**
1. Select your preferred LLM provider from the dropdown:  
   - GPT-4o  
   - Gemini-Flash  
   - Claude  
   - DeepSeek  
   - Grok  

2. Choose an operation:  
   - **Summarize Document**: Generate a comprehensive summary of the document  
   - **Ask a Question**: Enter a specific question about the document content  

### **Viewing Results**
- Summaries and answers appear in the designated output areas  
- Token usage statistics display below each result, showing:  
  - **Input tokens used**  
  - **Output tokens generated**  
  - **Total cost of the operation**  

---

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pdf-processing-api.git
cd pdf-processing-api

# Create a virtual environment
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate


### **Configuration**
The application uses environment variables for configuration:

# 🚀 Project Setup – FastAPI + Docker + LiteLLM Integration  

## ✅ Prerequisites  
- Python ≥ 3.9  
- Docker & Docker Compose  
- OpenAI / Claude / Gemini API Keys  
  - `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc. (stored in `.env` file)  

---

## 🛠 FastAPI Setup (Local Development)  

### **1. Install Dependencies**  
```bash
cd backend/
pip install -r requirements.txt


bash
Copy
Edit
# PDF storage location
export PDF_STORAGE_DIR="./pdf_storage"

# LiteLLM configuration
export LITELLM_API_URL="http://localhost:4000/v1"

# API keys for LLM providers
export OPENAI_API_KEY="your-openai-key"
export GOOGLE_API_KEY="your-google-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export DEEPSEEK_API_KEY="your-deepseek-key"
export XAI_API_KEY="your-xai-key"

. Run FastAPI
bash
Copy
Edit
uvicorn backend.main:app --reload
Visit: http://localhost:8000/docs
🐳 Docker-Based Deployment (Recommended)
1. Build & Run with Docker Compose
bash
Copy
Edit
docker compose up --build
2. Access Services
Streamlit Frontend: http://localhost:8501
FastAPI Backend: http://localhost:8000/docs
Redis: localhost:6379
🤖 LiteLLM Integration & Cost Tracking
All model interactions are routed through a centralized LiteLLMClient, ensuring consistent API management. This abstraction simplifies multi-provider integration across:

OpenAI GPT-4o
Claude 3 Sonnet
Gemini Flash
DeepSeek, Grok, etc.
🔍 Cost Tracking Powered by CostLogger
Every LLM query tracks:
✅ Input/Output tokens
✅ Individual cost components
✅ Total cost estimation
✅ Logs saved in JSONL format (per day)

Example log entry (./cost_logs/cost_log_YYYY-MM-DD.jsonl):
json
Copy
Edit
{
  "timestamp": "2025-03-13T10:45:23",
  "model": "GPT-4o",
  "input_tokens": 345,
  "output_tokens": 223,
  "input_cost": 0.00345,
  "output_cost": 0.00669,
  "total_cost": 0.01014
}
📊 Daily Summary Report
Use CostLogger.get_daily_summary() to retrieve total cost and usage by model and date. This enables:

Full observability
Cost transparency
Support for audit, billing, and analytics
