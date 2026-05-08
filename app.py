import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Page Configuration & State
st.set_page_config(page_title="AI Bug Reproducer", page_icon="🐛", layout="wide")

if "bug_input" not in st.session_state:
    st.session_state.bug_input = ""

# 2. Sidebar (The Architecture Flex)
with st.sidebar:
    st.header("🛠️ Architecture")
    st.markdown("""
    **Powered by:**
    * **Engine:** Groq Cloud + Llama 3 (8B)
    * **Orchestration:** LangChain
    * **Frontend:** Streamlit
    
    This agent analyzes raw stack traces to diagnose root causes, identify edge cases, and automatically generate reproduction test scripts.
    """)
    st.divider()
    st.markdown("### Built by Sparsh Srivastava")
    st.markdown("*Software Engineer | LeetCode Knight*")
    st.markdown("[🔗 LinkedIn](https://www.linkedin.com/in/your-profile) | [🐙 GitHub](https://github.com/your-username)")

# 3. Main Header
st.title("🐛 AI Bug Reproducer & Root Cause Analyzer")
st.markdown("Paste your stack trace below or try a sample bug. Our AI agent will diagnose the root cause and generate a reproduction script in seconds.")

# Secure API Key handling
# Try to get the key from your Mac's terminal first (Local Testing)
groq_api_key = os.getenv("GROQ_API_KEY")

# If it's not in the terminal, try Streamlit Secrets (Cloud Deployment)
if not groq_api_key:
    try:
        groq_api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        groq_api_key = None

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Input Stack Trace")
    
    # The "Lazy Recruiter" Feature
    st.caption("Try a sample bug:")
    btn_col1, btn_col2 = st.columns(2)
    if btn_col1.button("☕ Java NullPointer", use_container_width=True):
        st.session_state.bug_input = """Exception in thread "main" java.lang.NullPointerException: Cannot invoke "String.length()" because "username" is null
    at com.smartbank.auth.UserValidator.validate(UserValidator.java:14)
    at com.smartbank.auth.AuthService.login(AuthService.java:22)
    at com.smartbank.Main.main(Main.java:8)"""
        
    if btn_col2.button("🐍 Python IndexError", use_container_width=True):
        st.session_state.bug_input = """Traceback (most recent call last):
  File "data_pipeline.py", line 42, in process_batch
    current_record = batch_data[500]
IndexError: list index out of range"""

    error_input = st.text_area(
        "Raw Error Log", 
        value=st.session_state.bug_input,
        height=350, 
        placeholder="Paste your massive Java, Python, or JS stack trace here..."
    )
    
    analyze_btn = st.button("Analyze Bug 🔍", type="primary", use_container_width=True)

with col2:
    st.subheader("2. AI Diagnosis")
    
    if analyze_btn and error_input:
        if not groq_api_key:
            st.error("API Key not found. Please add your Groq API Key to the Streamlit secrets.")
        else:
            with st.spinner("🧠 Analyzing stack trace in the cloud..."):
                try:
                    llm = ChatGroq(
                        api_key=groq_api_key,
                        model_name="llama-3.1-8b-instant" 
                    )
                    
                    template = """
                    You are an expert Senior Software Engineer debugging a system crash.
                    Analyze the following error stack trace and provide a highly structured response.

                    Error/Stack Trace:
                    {stack_trace}

                    Do not write any introductory remarks. Provide exactly three sections formatted in Markdown:
                    1. **Root Cause:** A one-sentence, highly technical explanation of why this crashed.
                    2. **Edge Cases:** A bulleted list of 2-3 specific scenarios or inputs that trigger this bug.
                    3. **Reproduction Test:** A short, executable unit test script to reproduce the error.
                    CRITICAL INSTRUCTIONS: You must be extremely concise. Keep the Root Cause Diagnosis under 3 sentences. Do not include any conversational filler, introductory text, or concluding remarks. Output strictly the technical diagnosis, edge cases, and the code.
                    """
                    prompt = PromptTemplate(input_variables=["stack_trace"], template=template)
                    debug_chain = prompt | llm | StrOutputParser()
                    
                    result = debug_chain.invoke({"stack_trace": error_input})
                    
                    st.success("Analysis Complete!")
                    
                    # Output Polish: Splitting the text to hide the code in an expander
                    if "3. **Reproduction Test:**" in result:
                        parts = result.split("3. **Reproduction Test:**")
                        st.markdown(parts[0]) # Shows Root Cause and Edge Cases
                        
                        with st.expander("🛠️ View Reproduction Script"):
                            st.markdown(parts[1]) # Hides the generated code
                    else:
                        st.markdown(result)
                    
                except Exception as e:
                    st.error(f"Analysis failed. Error: {str(e)}")
                    
    elif analyze_btn:
        st.warning("⚠️ Please paste a stack trace first.")