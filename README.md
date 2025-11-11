# Personal AI Chatbot of Faria Jaheen

> An intelligent, self-descriptive chatbot that answers questions about **Faria Jaheen**, built with **Gradio**, **OpenAI’s GPT models**, and deployed on **Hugging Face Spaces** for interactive access.

[![Live Demo](https://img.shields.io/badge/HuggingFace-Live%20Demo-yellow?logo=huggingface)](https://huggingface.co/spaces/fariaj/career_conversation)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-5.x-orange?logo=gradio)](https://gradio.app)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green?logo=openai)](https://platform.openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

---

## 🎯 Overview

This chatbot acts as a **personal knowledge assistant** that lets visitors ask questions about my background, academic research, and technical experience.  
It demonstrates how conversational AI can transform a résumé or portfolio into an interactive experience—bridging self-presentation, NLP, and web deployment.

---

## 🧩 Architecture

| Layer | Technology | Purpose |
|:--|:--|:--|
| **Frontend (UI)** | [Gradio](https://gradio.app) | Lightweight web interface for input / output |
| **Backend Logic** | Python 3.12 | Handles environment loading, prompt design, and API orchestration |
| **LLM Engine** | [OpenAI GPT-4o](https://platform.openai.com/docs/models/gpt-4o) | Generates context-aware answers |
| **Deployment** | [Hugging Face Spaces](https://huggingface.co/spaces) | Server-less hosting with version control |
| **Version Control** | [GitHub](https://github.com/fariaj) | Collaboration, issues, and community pull requests |

---

## ⚙️ Installation

```bash
git clone https://github.com/fariaj/personal-chatbot-hf.git
cd personal-chatbot-hf
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # then edit with your OpenAI key
python app.py
