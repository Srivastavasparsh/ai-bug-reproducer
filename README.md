# 🐛 AI Bug Reproducer & QA Sandbox

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![Docker](https://img.shields.io/badge/Docker-Ephemeral_Containers-2496ED?style=for-the-badge&logo=docker)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-LLM_Orchestration-1C3C3C?style=for-the-badge)

An automated QA developer tool designed to eliminate the "it works on my machine" problem. This pipeline ingests raw Python stack traces, analyzes them using Abstract Syntax Tree (AST) parsing, synthesizes a reproduction script via LLM, and executes the test inside a secure, ephemeral Docker sandbox.

## 🚀 Live Demo

> [https://github.com/user-attachments/assets/4af85b86-024f-4537-bf59-f8a75593bd1b]

## 🧠 Architecture Flow

1. **AST Context Extraction:** Parses the provided stack trace to identify the failing file and line number, dynamically extracting the exact AST node and surrounding code block.
2. **LLM Test Synthesis:** Utilizes LangChain and Groq (Llama 3.1) to synthesize a raw, unhandled PyTest script designed to intentionally trigger the fatal crash without safety wrappers.
3. **Isolated Sandbox Execution:** Spools up a read-only (`mode='ro'`), ephemeral Docker container (Python 3.10-slim) to safely execute the generated script and capture the standard output/error logs.
4. **Interactive Dashboard:** Built with Streamlit for a fast, intuitive developer experience, complete with one-click code exports.

## 🛠️ Local Setup & Installation

**1. Clone the repository**
```bash
git clone [https://github.com/Srivastavasparsh/AI-Bug-Reproducer.git](https://github.com/Srivastavasparsh/AI-Bug-Reproducer.git)
cd AI-Bug-Reproducer

2. Install dependencies
pip install -r requirements.txt
pip install docker

3. Set environment variables
The application requires a Groq API key for Llama 3.1 inference
export GROQ_API_KEY = "your_api_key_here"

4. Start the Docker Daemon
Ensure Docker Desktop is running in the background. The app will verify the connection upon launch.

5. Launch the application
python3 -m streamlit run app.py

👨‍💻 Author
Sparsh Srivastava
