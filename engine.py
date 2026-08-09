import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class BugAgent:
    def __init__(self, model_name: str = "llama-3.1-8b-instant"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is missing.")
            
        self.llm = ChatGroq(
            temperature=0.2,
            model_name=model_name,
            api_key=self.api_key
        )
        self.parser = StrOutputParser()

    def generate_reproduction_test(self, parsed_error: dict, ast_context: str) -> str:
        """
        Synthesizes a PyTest script designed to replicate the provided error.
        """
        template = """
        You are an elite QA Automation Engineer. Write a single PyTest script that 
        triggers a fatal, unhandled exception to crash the test.
        
        ERROR DETAILS:
        - File: {file_path}
        - Function: {function_name}
        - Error Message: {error_message}
        
        RELEVANT SOURCE CODE (AST EXTRACT):
        {ast_context}
        
        INSTRUCTIONS:
        1. Write a plain Python test function that calls the failing code directly.
        2. DO NOT use `pytest.raises()` or any try/except blocks. Let the exception crash the function raw.
        
        EXAMPLE OF EXACTLY WHAT TO WRITE:
        def test_crash():
            calc = Calculator()
            calc.divide(10, 0)  # This must execute bare so it crashes the test!
        
        3. Do NOT include markdown code blocks (like ```python). Return ONLY the raw code.
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["file_path", "function_name", "error_message", "ast_context"]
        )
        
        chain = prompt | self.llm | self.parser
        
        raw_code = chain.invoke({
            "file_path": parsed_error.get("file_path", "Unknown"),
            "function_name": parsed_error.get("function_name", "Unknown"),
            "error_message": parsed_error.get("error_message", "Unknown"),
            "ast_context": ast_context
        })
        
        return self._clean_output(raw_code)

    def _clean_output(self, code: str) -> str:
        """Strips markdown code fences if the LLM ignores instructions."""
        code = code.strip()
        if code.startswith("```python"):
            code = code[9:]
        if code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
        return code.strip()