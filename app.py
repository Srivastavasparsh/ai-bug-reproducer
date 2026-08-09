import streamlit as st
import os
from parsers import ErrorParser
from engine import BugAgent
from sandbox import DockerSandbox

# --- 1. Page Configuration ---
st.set_page_config(page_title="AI Bug Reproducer", page_icon="🐛", layout="wide")

st.title("🐛 AI Bug Reproducer & QA Sandbox")
st.markdown("Automated stack trace parsing, PyTest synthesis, and isolated sandbox execution.")

# --- 2. System Initialization ---
@st.cache_resource
def init_system():
    """Initializes heavy components once to prevent reloading on every UI interaction."""
    try:
        agent = BugAgent()
        sandbox = DockerSandbox()
        return agent, sandbox, None
    except ValueError as e:
        return None, None, str(e)
    except Exception as e:
        return None, None, f"Sandbox Error: {str(e)}"

agent, sandbox, init_error = init_system()

# Sidebar: System Status
with st.sidebar:
    st.header("⚙️ System Status")
    if init_error:
        st.error(f"System Offline:\n{init_error}")
        st.info("Ensure GROQ_API_KEY is set and Docker Desktop is running.")
    else:
        st.success("✅ AI Engine: Online (Llama 3)\n✅ Docker Sandbox: Ready")
        
    st.divider()
    st.markdown("### Architecture Flow")
    st.markdown("1. **AST Parser**: Extracts failing node.\n2. **LLM Engine**: Synthesizes PyTest.\n3. **Docker**: Executes in isolated container.")

# --- 3. Main Interface ---
st.subheader("1. Paste Stack Trace")
default_trace = """Traceback (most recent call last):
  File "calculator.py", line 12, in divide
    return a / b
ZeroDivisionError: division by zero"""

trace_input = st.text_area("Raw Error Log / Stack Trace", value=default_trace, height=200)

if st.button("🚀 Analyze & Reproduce Bug", type="primary", disabled=bool(init_error)):
    with st.status("Initializing Automated QA Pipeline...", expanded=True) as status:
        
        # Step A: Parse Trace
        st.write("🔍 Parsing stack trace...")
        parsed_data = ErrorParser.parse_stack_trace(trace_input)
        
        if parsed_data["status"] == "error":
            status.update(label="❌ Parsing Failed", state="error", expanded=True)
            st.error(parsed_data["message"])
            st.stop()
            
        st.write(f"📂 Target identified: `{parsed_data['file_path']}` at line {parsed_data['line_number']}")
        
        # Step B: Extract AST Context
        st.write("🌳 Extracting AST context...")
        ast_context = ErrorParser.extract_failing_ast_node(
            parsed_data["file_path"], 
            parsed_data["line_number"]
        )
        
        # Step C: Generate Code
        st.write("🤖 Synthesizing PyTest reproduction script...")
        generated_test = agent.generate_reproduction_test(parsed_data, ast_context)
        
        # Step D: Sandbox Execution
        st.write("🐳 Spinning up ephemeral Docker sandbox...")
        sandbox_result = sandbox.run_test(generated_test)
        
        status.update(label="✅ Pipeline Execution Complete!", state="complete", expanded=False)

    # --- 4. Results Dashboard ---
    st.subheader("2. Diagnostic Results")
    
    # Use tabs for a clean, professional layout
    tab1, tab2, tab3 = st.tabs(["📊 Execution Results", "💻 Generated PyTest Code", "🧩 Parsed Context"])
    
    with tab1:
        if sandbox_result["success"]:
            st.success(f"🎯 **{sandbox_result['message']}**")
        else:
            st.warning(f"⚠️ **{sandbox_result['message']}**")
            
        st.markdown("**Sandbox Console Output:**")
        st.code(sandbox_result["logs"], language="bash")
        
    with tab2:
        st.markdown("**AI-Synthesized Unit Test:**")
        st.code(generated_test, language="python")
        # Add this right below the st.code line in tab2
        st.download_button(
            label="📥 Download test_reproduction.py",
            data=generated_test,
            file_name="test_reproduction.py",
            mime="text/plain"
        )
        
    with tab3:
        st.json(parsed_data)
        st.markdown("**AST Code Block Extracted:**")
        st.code(ast_context, language="python")