import streamlit as st
import requests
import json
import os
from components.model_selector import render_model_selector
from components.cost_display import render_cost_display
from components.pdf_content_selector import render_pdf_selector
from components.question_input import render_question_input
from components.summarize import render_summarize_button
 
API_BASE_URL = os.getenv("BACKEND_URL", "https://backend-980441147674.us-east1.run.app")
API_URL = os.getenv("BACKEND_URL", "https://backend-980441147674.us-east1.run.app")
 
def initialize_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "GPT-4o"
    if "pdf_content" not in st.session_state:
        st.session_state.pdf_content = None
    if "pdf_name" not in st.session_state:
        st.session_state.pdf_name = None
    if "selected_text" not in st.session_state:
        st.session_state.selected_text = None
    if "token_usage" not in st.session_state:
        st.session_state.token_usage = {
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_cost": 0
        }
    # 新增一个 show_upload 控制上传区域是否可见
    if "show_upload" not in st.session_state:
        st.session_state.show_upload = False
    # 添加一个标志来追踪summarize操作是否正在进行
    if "is_summarizing" not in st.session_state:
        st.session_state.is_summarizing = False
 
def display_chat_history():
    """Display the chat history in a conversational format."""
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
 
def process_query(query):
    if not st.session_state.pdf_content and not st.session_state.pdf_name:
        st.warning("Please upload a PDF document first.")
        return
 
    # 用户消息
    st.session_state.chat_history.append({"role": "user", "content": query})
 
    # 获取响应
    payload = {
        "model": st.session_state.selected_model,
        "question": query,
        "pdf_content": st.session_state.pdf_content,
        "pdf_name": st.session_state.pdf_name,
        "selected_text": st.session_state.selected_text
    }
 
    try:
        response = requests.post(f"{API_URL}/ask_question", json=payload)
        response.raise_for_status()
        result = response.json()
 
        answer = result.get("answer", "Sorry, I couldn't process your question.")
        
        # 添加助手消息到历史记录
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
 
        # 更新 token usage
        if "token_usage" in result:
            st.session_state.token_usage["total_input_tokens"] += result["token_usage"]["input_tokens"]
            st.session_state.token_usage["total_output_tokens"] += result["token_usage"]["output_tokens"]
            st.session_state.token_usage["total_cost"] += result["token_usage"].get("cost", 0)
 
    except Exception as e:
        st.session_state.chat_history.append({"role": "assistant", "content": f"Error: {str(e)}"})
    
    # 使用新的API进行页面重新渲染
    st.rerun()
 
def generate_summary():
    if not st.session_state.pdf_content and not st.session_state.pdf_name:
        st.warning("Please upload a PDF document first.")
        return
    
    # Set summarizing flag to True
    st.session_state.is_summarizing = True
    
    with st.chat_message("user"):
        st.markdown("Can you summarize this document for me?")
    st.session_state.chat_history.append({"role": "user", "content": "Can you summarize this document for me?"})
 
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Generating summary...")
 
        payload = {
            "model": st.session_state.selected_model,
            "pdf_content": st.session_state.pdf_content,
            "pdf_name": st.session_state.pdf_name,
            "selected_text": st.session_state.selected_text
        }
 
        try:
            response = requests.post(f"{API_URL}/summarize", json=payload)
            response.raise_for_status()
            result = response.json()
 
            summary = result.get("summary", "Sorry, I couldn't generate a summary.")
            message_placeholder.markdown(summary)
 
            st.session_state.chat_history.append({"role": "assistant", "content": summary})
 
            if "token_usage" in result:
                st.session_state.token_usage["total_input_tokens"] += result["token_usage"]["input_tokens"]
                st.session_state.token_usage["total_output_tokens"] += result["token_usage"]["output_tokens"]
                st.session_state.token_usage["total_cost"] += result["token_usage"].get("cost", 0)
 
        except Exception as e:
            message_placeholder.markdown(f"Error: {str(e)}")
        
        # Reset summarizing flag
        st.session_state.is_summarizing = False
 
def upload_pdf(uploaded_file):
    """Helper function to upload PDF via multipart/form-data and store content in session."""
    if uploaded_file is None:
        return
    files = {
        "file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf"),
    }
    try:
        resp = requests.post(f"{API_URL}/upload_pdf", files=files)
        resp.raise_for_status()
        data = resp.json()
 
        st.session_state.pdf_name = data.get("name", uploaded_file.name)
        st.session_state.pdf_content = data.get("content", "")
        st.session_state.selected_text = None
        st.success(f"PDF '{uploaded_file.name}' uploaded and processed!")
    except Exception as e:
        st.error(f"Upload failed: {str(e)}")
 
def main():
    # 1. 宽屏布局
    st.set_page_config(page_title="PDF AI Assistant", layout="wide")
    
    # 2. 注入自定义 CSS，增大聊天区宽度
    st.markdown(
        """
        <style>
        /* 将主内容区的最大宽度设置为1200px或更大 */
        section.main > div.block-container {
            max-width: 1600px;
        }
        
        /* 增加聊天消息的宽度 */
        .stChatMessage {
            width: 100%;
            max-width: 1200px;
        }
        
        /* 确保聊天消息内容可以占满整个可用宽度 */
        .stChatMessage .stChatMessageContent {
            width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    initialize_session_state()

    # 左侧Sidebar（只保留部分内容，如模型选择、上传等）
    with st.sidebar:
        st.title("PDF AI Assistant")
        render_model_selector()
        st.markdown("### PDF Actions")
        st.divider()
        render_cost_display()

    # 主区域
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header("Chat with your PDF")
        
        # 放在这里：将 summarize 按钮放在聊天区上方或下方都可以，根据你的需求调整位置
        if render_summarize_button() and not st.session_state.is_summarizing:
            generate_summary()
        
        display_chat_history()
        
        # ============ 底部输入栏，修改列宽比例以扩大输入框 ============ #
        # 调整比例为 [0.05, 0.85, 0.1]，让输入框占据更多空间
        col_plus, col_input, col_send = st.columns([0.05, 0.85, 0.1])
        
        with col_plus:
            if st.button("➕", use_container_width=True):
                st.session_state.show_upload = not st.session_state.show_upload

        with col_input:
            user_input = st.text_input("Your message", value="", label_visibility="collapsed")

        with col_send:
            if st.button("Send", use_container_width=True):
                if user_input.strip():
                    process_query(user_input)
                else:
                    st.warning("Please enter a message.")
    
    with col2:
        if st.session_state.pdf_content:
            with st.expander("PDF Preview", expanded=False):
                st.markdown(
                f"""
                <div style="height:600px; overflow-y:auto; border:1px solid #ccc; padding:1rem;">
                {st.session_state.pdf_content}
                </div>
                """,
                unsafe_allow_html=True
                )


    if st.session_state.show_upload:
        with st.expander("Upload a PDF", expanded=True):
            uploaded_file = st.file_uploader("Select PDF", type=["pdf"])
            if uploaded_file:
                upload_pdf(uploaded_file)

    selected_pdf, pdf_content = render_pdf_selector(API_BASE_URL)
    if pdf_content:
        st.success(f"Content loaded from {selected_pdf}.md")

if __name__ == "__main__":
    main()