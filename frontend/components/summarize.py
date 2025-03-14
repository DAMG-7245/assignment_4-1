# components/summarize_button.py

import streamlit as st

def render_summarize_button():
    """
    Render a prominent summarize button that is enabled only when a PDF is loaded.
    
    Returns:
        bool: True if the button was clicked, False otherwise
    """
    # Determine if a PDF is loaded
    pdf_loaded = st.session_state.pdf_content is not None or st.session_state.pdf_name is not None
    
    # Create a container for the button with styling
    button_container = st.container()
    
    with button_container:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Use a colored button when PDF is loaded
            if pdf_loaded:
                button_style = """
                <style>
                div[data-testid="stButton"] button {
                    background-color: #4CAF50;
                    color: white;
                    font-weight: bold;
                    border: none;
                    padding: 10px 15px;
                    border-radius: 5px;
                }
                div[data-testid="stButton"] button:hover {
                    background-color: #45a049;
                }
                </style>
                """
                st.markdown(button_style, unsafe_allow_html=True)
                return st.button("📄 Summarize PDF", key="summarize_btn", disabled=not pdf_loaded, use_container_width=True)
            else:
                # Disabled style when no PDF is loaded
                return st.button("📄 Summarize PDF", key="summarize_btn", disabled=True, use_container_width=True)