import ast
import re
import os

class ErrorParser:
    @staticmethod
    def parse_stack_trace(trace_text: str) -> dict:
        """
        Parses a raw Python stack trace using Regex to extract the point of failure.
        Returns the file path, line number, function name, and the specific error message.
        """
        # Regex to catch Python traceback format: File "path/to/file.py", line X, in <module>
        pattern = r'File "(.*?)", line (\d+), in (.*)'
        matches = re.findall(pattern, trace_text)
        
        # The actual error type and message is typically the very last line
        error_message = trace_text.strip().split('\n')[-1]
        
        if not matches:
            return {
                "status": "error",
                "message": "Could not confidently parse stack trace.", 
                "raw_error": error_message
            }
            
        # The last match in the traceback is usually the exact execution point of the crash
        last_call = matches[-1] 
        
        return {
            "status": "success",
            "file_path": last_call[0],
            "line_number": int(last_call[1]),
            "function_name": last_call[2],
            "error_message": error_message
        }
        
    @staticmethod
    def extract_failing_ast_node(file_path: str, target_line: int) -> str:
        """
        Reads the local file and uses Python's AST to surgically extract 
        the exact function or class block where the crash occurred.
        """
        if not os.path.exists(file_path):
            return "Source file not found locally. Proceeding with trace context only."
            
        with open(file_path, 'r', encoding='utf-8') as file:
            source_code = file.read()
            
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return "SyntaxError detected in source file preventing AST parsing."
            
        # Traverse the AST to find the node enclosing our target line
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
                    if node.lineno <= target_line <= node.end_lineno:
                        # Extract the exact lines of code from the source
                        lines = source_code.split('\n')
                        return '\n'.join(lines[node.lineno-1:node.end_lineno])
                        
        return "Could not isolate specific AST code block; line number may be outside a standard function."

# Quick local test block
if __name__ == "__main__":
    sample_trace = """
    Traceback (most recent call last):
      File "/app/auth_service.py", line 42, in process_login
        user = db.get_user(payload['user_id'])
    KeyError: 'user_id'
    """
    print(ErrorParser.parse_stack_trace(sample_trace))