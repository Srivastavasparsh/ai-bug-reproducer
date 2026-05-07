# 🐛 AI Bug Reproducer & Root Cause Analyzer

[![Live Deployment](https://img.shields.io/badge/Live_App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://sparsh-debug-agent.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-green?style=for-the-badge)](https://www.langchain.com/)

A cloud-deployed AI engineering tool designed to automate the most tedious phase of the software debugging lifecycle. 

This agent ingests raw, unstructured error logs (Java, Python, JS, etc.) and utilizes Large Language Models to instantly diagnose system crashes, identify triggering edge cases, and generate executable reproduction unit tests.

## 🚀 Live Demo
**Access the deployed application here:** [sparsh-debug-agent.streamlit.app](https://sparsh-debug-agent.streamlit.app)

## 🏗️ System Architecture & Tech Stack

This project is built with a focus on ultra-low latency inference and scalable AI orchestration.

* **LLM Engine:** Groq Cloud + Llama 3 (8B parameters) for specialized, high-speed LPU processing.
* **AI Orchestration:** LangChain for prompt templating and structured output parsing.
* **Frontend / Deployment:** Streamlit Community Cloud.

### The Pipeline Flow:
1. **Input Ingestion:** User pastes a raw stack trace via the Streamlit UI.
2. **Prompt Engineering:** LangChain injects the stack trace into a strict, highly-structured zero-shot prompt designed for technical software diagnostics.
3. **Inference:** The payload is routed to Groq's cloud infrastructure, utilizing Llama 3 to analyze the code execution path.
4. **Structured Output:** The response is parsed and formatted into three distinct deliverables: Root Cause, Edge Cases, and a Python/Java Reproduction Script.

## 💻 Local Quick Start

To run this agent on your local machine for development or testing:

**1. Clone the repository:**
```bash
git clone [https://github.com/Srivastavasparsh/ai-bug-reproducer.git](https://github.com/Srivastavasparsh/ai-bug-reproducer.git)
cd ai-bug-reproducer
