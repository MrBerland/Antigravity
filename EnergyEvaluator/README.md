# Project: Renewable Energy Procurement Evaluator

## Objective
To build an AI-driven tool that evaluates renewable energy offers by analyzing presentations, contracts, and spreadsheets, providing deep comparative analysis and strategic recommendations using Gemini models.

## Architecture
1. **Frontend (UI)**: Next.js + Tailwind CSS.
   - Dashboard for uploading RFPs/Offers.
   - Visual comparison of metrics (Cost, Volume, Risk).
   - "Executive Summary" generator.
   
2. **Backend (API)**: Python (FastAPI).
   - **Ingestion Engine**: Extraction from PDF (Presentations), DOCX (Contracts), XLSX (Financials).
   - **Intelligence Layer**: 
     - *Vision Agent*: Reads charts/slides in presentations.
     - *Analyst Agent*: Crunches spreadsheet numbers (pandas).
     - *Legal Agent*: Finds contractual friction points.
     - *Synthesizer*: "Deep Thinking" formulation of the final advice.

3. **Data**: 
   - Local storage for documents (for now).
   - In-memory vector store or simple context window for Gemini.

## Tech Stack
- **Frontend**: Next.js 14, Recharts (Visualization), Framer Motion (Aesthetics).
- **Backend**: Python 3.9+, FastAPI, Pandas, Gemini (via google-generativeai).
- **AI**: Google Gemini Pro 1.5 (Multimodal).

## Current Status (Session 1)
- **Backend**: Implemented basic structure with FastAPI, Ingestion (PDF, DOCX, XLSX), and Gemini Agent integration.
- **UI**: Pending Node.js environment setup.

## Setup Instructions

### Backend
1. Navigate to `EnergyEvaluator`.
2. Activate virtual environment (created automatically): `source backend/venv/bin/activate` or use `backend/venv/bin/python`.
3. Run the server:
   ```bash
   backend/venv/bin/uvicorn backend.src.main:app --reload --port 8000
   ```
4. Access API Docs at `http://localhost:8000/docs`.

### Environment Variables
Create a `.env` file in `EnergyEvaluator` or `backend` with:
```
GEMINI_API_KEY=your_api_key_here
```

