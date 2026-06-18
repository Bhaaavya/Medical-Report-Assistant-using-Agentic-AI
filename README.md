# 🏥 Medical Report Assistant (Agentic AI)

An AI-powered Medical Report Assistant built using FastAPI, PostgreSQL, LangGraph, Gemini, and LangSmith that helps patients understand complex medical reports through intelligent multi-agent workflows, multilingual explanations, conversational Q&A, and audio narration.

The system is designed to bridge the gap between medical professionals and patients by converting technical medical reports into simple, understandable explanations that can be read, listened to, and discussed in multiple languages.

---

# 📌 Problem Statement

Healthcare providers generate highly detailed reports containing medical terminology, abbreviations, laboratory values, radiology findings, and clinical observations. While these reports are essential for doctors, they are often difficult for patients and caregivers to understand.

Millions of patients face challenges such as:

* Difficulty understanding medical jargon.
* Reports written only in English despite local language preferences.
* Anxiety caused by unfamiliar findings and terminology.
* Lack of immediate access to doctors for clarification.
* Dependence on internet searches that often provide misleading information.
* Limited literacy levels that make reading lengthy reports difficult.

The challenge is even greater in rural and semi-urban regions where patients may not be comfortable reading English or interpreting healthcare documentation.

As a result, patients frequently misunderstand their reports, miss important information, or remain unaware of the significance of their medical findings.

---

# 🎯 Proposed Solution

Medical Report Assistant uses Agentic AI to transform complex medical reports into patient-friendly explanations.

The system allows users to:

* Upload medical reports.
* Automatically extract and structure report content.
* Generate simplified explanations.
* Receive explanations in multiple languages.
* Ask questions about their reports.
* Generate audio narration for low-literacy users.
* Access safety-filtered educational responses.

The goal is not to replace healthcare professionals but to improve accessibility, understanding, and patient engagement.

---

# 🚀 Key Features

### 📄 Medical Report Processing

* PDF Upload Support
* Intelligent Document Parsing using Docling
* PyMuPDF Fallback Extraction
* Structured Text Extraction
* Medical Finding Identification
* Report Classification

### 🤖 Agentic AI Workflow

Built using LangGraph Multi-Agent Architecture.

Specialized agents perform:

* Report Intake
* Summarization
* Explanation Generation
* Safety Validation
* Translation
* Question Answering
* Audio Generation

### 🌍 Multilingual Support

Supports:

* English
* Hindi
* Kannada
* Tamil
* Telugu

Users can receive explanations and answers in their preferred language.

### 🎙 Audio Narration

Generate spoken explanations of medical reports.

Useful for:

* Elderly patients
* Low-literacy users
* Visually impaired users
* Regional language speakers

### 💬 Conversational Report Q&A

Users can ask:

* What are the main findings?
* Is anything abnormal?
* What does this term mean?
* What should I discuss with my doctor?

The system answers using report-specific context.

### 🛡 Safety Layer

Responses are reviewed before delivery.

The system:

* Prevents diagnosis claims.
* Prevents treatment recommendations.
* Prevents medication prescriptions.
* Adds medical disclaimers.
* Generates educational-only responses.

### 📊 Observability

Integrated with LangSmith for:

* Agent tracing
* Workflow monitoring
* Debugging
* Execution analysis

---

# 🏗 System Architecture

```text
User
 │
 ▼
FastAPI Backend
 │
 ▼
LangGraph Orchestrator
 │
 ├── Intake Agent
 ├── Summary Agent
 ├── Explanation Agent
 ├── Safety Agent
 ├── Translation Agent
 ├── QA Agent
 └── Audio Agent
 │
 ▼
Gemini LLM
 │
 ▼
PostgreSQL Database
```

---

# 🔄 Agent Workflow

## Patient Explanation Workflow

```text
Upload Report
      │
      ▼
Docling Extraction
      │
      ▼
Intake Agent
      │
      ▼
Summary Agent
      │
      ▼
Explanation Agent
      │
      ▼
Safety Agent
      │
      ▼
Translation Agent
      │
      ▼
Patient-Friendly Explanation
```

---

## Question Answering Workflow

```text
User Question
      │
      ▼
QA Agent
      │
      ▼
Safety Validation
      │
      ▼
Localized Response
```

---

## Audio Narration Workflow

```text
Report
      │
      ▼
Summary Agent
      │
      ▼
Explanation Agent
      │
      ▼
Safety Agent
      │
      ▼
Translation Agent
      │
      ▼
Audio Agent
      │
      ▼
MP3 Narration
```

---

# 🛠 Tech Stack

## Backend

* FastAPI
* SQLAlchemy
* PostgreSQL

## AI & Agentic Framework

* Gemini
* LangGraph
* LangSmith

## Document Intelligence

* Docling
* PyMuPDF

## Audio Processing

* gTTS

## Authentication

* JWT
* Passlib
* Python-Jose

## Testing

* Pytest

---

# 🗄 Database Design

### Users

Stores:

* User Profiles
* Authentication Information

### Reports

Stores:

* Uploaded Report Metadata
* Report Information

### Report Texts

Stores:

* Extracted Report Content
* Extraction Metadata

### Clinical Findings

Stores:

* Structured Medical Findings

### Agent Outputs

Stores:

* Summaries
* Explanations
* Translations
* Workflow Results

### Conversations

Stores:

* Questions
* Answers
* Language Metadata

### Audio Files

Stores:

* Generated Audio Metadata
* Audio File Paths

---

# ⚙ Installation

## Clone Repository

```bash
git clone <repository-url>
cd medical_report_assistant
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=
SECRET_KEY=
GEMINI_API_KEY=
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=medical-report-assistant
LANGSMITH_TRACING=true
```

## Run Application

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://localhost:8000/docs
```

---

# 📡 API Endpoints

## Authentication

```text
POST /auth/register
POST /auth/login
GET  /auth/me
```

## Reports

```text
POST   /reports/upload
GET    /reports/list
DELETE /reports/{report_id}
```

## Analysis

```text
POST /analysis/{report_id}/summary
POST /analysis/{report_id}/explain
```

## Chat

```text
POST /chat/{report_id}/ask
GET  /chat/{report_id}/history
```

## Audio

```text
POST /audio/{report_id}/generate
```

---

# 🧪 Testing

Run:

```bash
pytest
```

Coverage Includes:

* Authentication Testing
* Report Testing
* Analysis Testing
* Chat Testing

---

# 📈 Future Enhancements

* Medical Image Analysis
* Specialist Routing Agents
* Human-in-the-Loop Validation
* Advanced RAG Integration
* Doctor Dashboard
* Hospital Information System Integration
* Mobile Application Support

---

# ⚠ Medical Disclaimer

This application is intended solely for educational and informational purposes.

The system does not provide medical diagnosis, treatment recommendations, prescriptions, or professional healthcare advice.

Users should always consult qualified healthcare professionals regarding medical decisions and health concerns.

---

# 👨‍💻 Author

**Bhavya K**

FastAPI • LangGraph • Generative AI • Machine Learning • Agentic AI
