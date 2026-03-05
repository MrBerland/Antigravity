from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import List, Optional
import shutil
import os
import uuid
from dotenv import load_dotenv

# Absolute imports based on project structure if running as module, or relative
# We will use relative imports assuming this is run/imported correctly
try:
    from .models import FullEvaluation, AnalysisResult, Recommendation, RemoteFolder, RemoteFile, EvaluateRemoteRequest
    from .ingestor import Ingestor
    from .agents import AgentManager
except ImportError:
    # Fallback for direct execution
    from models import FullEvaluation, AnalysisResult, Recommendation, RemoteFolder, RemoteFile, EvaluateRemoteRequest
    from ingestor import Ingestor
    from agents import AgentManager

# Load env vars
load_dotenv()

app = FastAPI(title="Renewable Energy Evaluator API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

agent_manager = AgentManager()

@app.get("/remote-files", response_model=List[RemoteFolder])
async def list_remote_files():
    folders = []
    # Walk the uploads directory
    for root, dirs, files in os.walk(UPLOAD_DIR):
        folder_name = os.path.basename(root)
        if folder_name == "uploads":
            folder_name = "Root"
            
        remote_files = []
        for file in files:
            if file.startswith('.'): continue
            
            file_path = os.path.join(root, file)
            # Make path relative to uploads for cleaner ID
            rel_path = os.path.relpath(file_path, UPLOAD_DIR)
            
            remote_files.append(RemoteFile(
                path=rel_path,
                name=file,
                type=file.split('.')[-1]
            ))
            
        if remote_files:
            folders.append(RemoteFolder(name=folder_name, files=remote_files))
            
    return folders

@app.post("/evaluate-remote", response_model=FullEvaluation)
async def evaluate_remote(request: EvaluateRemoteRequest):
    analyses = []
    
    for relative_path in request.file_paths:
        full_path = os.path.join(UPLOAD_DIR, relative_path)
        
        if not os.path.exists(full_path):
            continue
            
        try:
            filename = os.path.basename(full_path)
            doc_type = Ingestor.identify_file_type(filename)
            file_ext = filename.split('.')[-1]
            
            text_content = ""
            parsed_summary = ""
            
            if doc_type == 'presentation' or doc_type == 'contract':
                if 'pdf' in file_ext.lower():
                    text_content = Ingestor.parse_pdf(full_path)
                elif file_ext.lower() in ['docx', 'doc']:
                    text_content = Ingestor.parse_docx(full_path)
                parsed_summary = text_content[:200] + "..." if text_content else "No text extracted"
                
            elif doc_type == 'spreadsheet':
                data = Ingestor.parse_xlsx(full_path)
                text_content = str(data) 
                parsed_summary = f"Spreadsheet with sheets: {list(data.keys())}"
                
            else:
                 text_content = "Unknown file type"
                 parsed_summary = "Skipped"
            
            ai_analysis = await agent_manager.analyze_document(text_content, doc_type, filename)
            
            analyses.append(AnalysisResult(
                filename=filename,
                file_type=doc_type,
                parsed_content_summary=parsed_summary,
                insights=ai_analysis.get("insights", []),
                metrics=ai_analysis.get("metrics", {})
            ))
            
        except Exception as e:
            analyses.append(AnalysisResult(
                filename=os.path.basename(full_path),
                file_type="error",
                parsed_content_summary=str(e),
                insights=["Extraction failed"],
                metrics={}
            ))

    recommendation_data = await agent_manager.synthesize_recommendation(
        [a.dict() for a in analyses], 
        request.context or f"Client: {request.client_name}"
    )
    
    recommendation = Recommendation(
        summary=recommendation_data.get("summary", "No summary generated"),
        key_risks=recommendation_data.get("key_risks", []),
        key_benefits=recommendation_data.get("key_benefits", []),
        final_verdict=recommendation_data.get("final_verdict", "N/A")
    )

    return FullEvaluation(
        client_context=request.context or "No context provided",
        analyses=analyses,
        recommendation=recommendation
    )


@app.get("/")
async def root():
    return {"message": "Energy Evaluator API is running", "status": "active"}

@app.post("/evaluate", response_model=FullEvaluation)
async def evaluate_context(
    files: List[UploadFile] = File(...),
    client_name: str = Form("Unknown Client"),
    context: Optional[str] = Form(None)
):
    analyses = []
    
    for file in files:
        # Create temp file path
        file_ext = file.filename.split('.')[-1]
        temp_filename = f"{uuid.uuid4()}.{file_ext}"
        temp_path = os.path.join(UPLOAD_DIR, temp_filename)
        
        try:
            # Save uploaded file
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Identify and Ingest
            doc_type = Ingestor.identify_file_type(file.filename)
            text_content = ""
            parsed_summary = ""
            
            if doc_type == 'presentation' or doc_type == 'contract':
                if 'pdf' in file_ext.lower():
                    text_content = Ingestor.parse_pdf(temp_path)
                elif file_ext.lower() in ['docx', 'doc']:
                    text_content = Ingestor.parse_docx(temp_path)
                parsed_summary = text_content[:200] + "..." if text_content else "No text extracted"
                
            elif doc_type == 'spreadsheet':
                data = Ingestor.parse_xlsx(temp_path)
                text_content = str(data) # Convert to string for LLM for now
                parsed_summary = f"Spreadsheet with sheets: {list(data.keys())}"
                
            else:
                 text_content = "Unknown file type"
                 parsed_summary = "Skipped"
            
            # Analyze
            ai_analysis = await agent_manager.analyze_document(text_content, doc_type, file.filename)
            
            analyses.append(AnalysisResult(
                filename=file.filename,
                file_type=doc_type,
                parsed_content_summary=parsed_summary,
                insights=ai_analysis.get("insights", []),
                metrics=ai_analysis.get("metrics", {})
            ))
            
        except Exception as e:
            analyses.append(AnalysisResult(
                filename=file.filename,
                file_type="error",
                parsed_content_summary=str(e),
                insights=["Extraction failed"],
                metrics={}
            ))
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # Synthesize
    recommendation_data = await agent_manager.synthesize_recommendation(
        [a.dict() for a in analyses], 
        context or f"Client: {client_name}"
    )
    
    recommendation = Recommendation(
        summary=recommendation_data.get("summary", "No summary generated"),
        key_risks=recommendation_data.get("key_risks", []),
        key_benefits=recommendation_data.get("key_benefits", []),
        final_verdict=recommendation_data.get("final_verdict", "N/A")
    )

    return FullEvaluation(
        client_context=context or "No context provided",
        analyses=analyses,
        recommendation=recommendation
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
