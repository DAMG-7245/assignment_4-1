# PDF Processing and Analysis with LLMs
### **📄 Project Summary**  

BACKEND URL: https://backend-980441147674.us-east1.run.app

FRONTEND URL :https://frontend-980441147674.us-east1.run.app
 

Codelab: (https://damg-7245.github.io/assignment_4-1/)  

Video Link: https://youtu.be/sCctoLpPe6w

🚀 **Process, Analyze, and Interact with PDFs using LLMs**

---

## **📌 Overview**
This application provides a comprehensive solution for processing, analyzing, and interacting with PDF documents using **Large Language Models (LLMs)**. Users can upload PDFs, convert them to **Markdown format**, and utilize various LLMs to summarize content or answer specific questions.  

The system employs a modern microservices architecture with:  
✅ **Streamlit frontend** for user interaction  
✅ **FastAPI backend** for request handling  
✅ **Redis** for event streaming  
✅ **LiteLLM** for unified access to multiple LLM providers  

Additionally, the system tracks token usage to monitor and report API costs.

---

## **🔑 Features**

### **PDF Management**
- Upload new PDF documents  
- Convert PDFs to Markdown format  
- Select from previously processed documents  

### **LLM Integration**
- Choose from multiple LLM providers (OpenAI, Google, Anthropic, DeepSeek, XAI)  
- Generate document summaries  
- Ask specific questions about document content  
- View token usage and cost metrics  

### **System Features**
- Event-driven architecture with Redis streams  
- Comprehensive token usage tracking  
- Error handling and logging  
- Docker containerization for easy deployment  

---

## **✔ Technology Stack**

| **Category**       | **Tools Used** |
|------------------|--------------|
| **Frontend**       | Streamlit |
| **Backend**        | FastAPI |
| **Event Streaming**| Redis |
| **LLM Integration**| LiteLLM |
| **Containerization**| Docker & Docker Compose |
| **Programming Language** | Python 3.9+ |

---

## **🛠️ User Guide**

### **Selecting a PDF**
1. Launch the application.  
2. Choose between:  
   - **Select Existing PDF**: Pick from previously processed documents.  
   - **Upload New PDF**: Upload a new PDF file for processing.  

### **Working with LLMs**
1. Select your preferred LLM provider from the dropdown menu:  
   - GPT-4o  
   - Gemini Flash  
   - Claude  
   - DeepSeek  
   - Grok  

2. Choose an operation:  
   - **Summarize Document**: Generate a comprehensive summary of the document.  
   - **Ask a Question**: Enter a specific question about the document content.  

### **Viewing Results**
- Summaries and answers appear in the designated output areas.  
- Token usage statistics display below each result, showing:  
  - Input tokens used.  
  - Output tokens generated.  
  - Total cost of the operation.  

---

## **📂 Project Structure**
```plaintext
│   .dockerignore
│   .gitignore
│   AIUseDisclosure.md
│   Codelab.md
│   docker-compose.yml
│   Dockerfile.backend
│   Dockerfile.frontend
│   llm_architecture.png
│   README.md
│   requirements.txt
│
├───architecture
│       data_flow_diagram.png
│       diag.py
│       system_architecture.png
│
├───backend
│   │   main.py
│   │   __init__.py
│   │
│   ├───endpoints
│   │       ask_question.py
│   │       select_pdfcontent.py
│   │       summarize.py
│   │       upload_pdf.py
│   │
│   └───utils
│           cost_logger.py
│           redis_stream.py
│
├───docs
│       design_decision.md
│       team_contributions.md
│
└───frontend
    │   app.py
    │
    └───components
            cost_display.py
            file_upload.py
            model_selector.py
            pdf_content_selector.py
            question_input.py
            summarize.py
```
---

## **🚀 Installation & Setup**

### 1️⃣ Prerequisites:
Ensure you have:
- Python ≥ 3.9  
- Docker & Docker Compose installed  
- API keys for LLM providers (stored in `.env` file)  

### 2️⃣ Clone the Repository:

git clone https://github.com/DAMG-7245/assignment_4-1.git

### 3️⃣ Create a Virtual Environment:
python -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows
 
### 4️⃣ Install Dependencies:

pip install -r requirements.txt

---

## 🐳 **Docker-Based Deployment (Recommended)**

### Build & Run Services:
docker compose up --build

## **🛠️ Usage**

### 1️⃣ Run the FastAPI Backend
uvicorn src.api.main:app --reload

text
API will be available at: [Insert API Link here]

---

### 2️⃣ Run the Streamlit App
streamlit run src/streamlit_app/app.py

text
App will open at: [Insert Streamlit Link here]

---

### **3️⃣ Upload a PDF File **
* Upload a PDF file or enter a webpage URL in the Streamlit app.  
* The API processes the document and interacts with Large Language Models (LLMs) to analyze, summarize, and extract insights from the content.  
* Extracted content is converted into Markdown format and stored securely in AWS S3 (if enabled).  

---

## **📌 Expected Outcomes**
* A functional LLM-powered document processing system for analyzing and summarizing data.  
* A working API & Streamlit app that allow users to process PDFs & webpages using various LLMs.  
* Enhanced document analysis capabilities, including multilingual processing, contextual understanding, and efficient information extraction.  
* Comprehensive documentation of findings, code, and usage guidelines for seamless adoption.  

---

## 📌 AI Use Disclosure
This project uses:
- **LLMs** (e.g., OpenAI GPT-4, Claude 3 Sonnet) for document summarization and analysis.  
- **LiteLLM** for unified access to multiple LLM providers and token tracking.    

📄 See `AiUseDisclosure.md` for details on ethical considerations, transparency, and security measures related to AI usage.

---

## 👨‍💻 Authors
* Sicheng Bao (@Jellysillyfish13)  
* Yung Rou Ko (@KoYungRou)  
* Anuj Rajendraprasad Nene (@Neneanuj)  

---

## 📞 Contact
For questions or feedback, reach out via Big Data Course or open an issue on GitHub.


## 👨‍💻 Authors
* Sicheng Bao (@Jellysillyfish13)  
* Yung Rou Ko (@KoYungRou)  
* Anuj Rajendraprasad Nene (@Neneanuj)  

---

## 📞 Contact
For questions, reach out via Big Data Course or open an issue on GitHub.

