from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class EvaluationRequest(BaseModel):
    client_name: str
    context: Optional[str] = None

class AnalysisResult(BaseModel):
    filename: str
    file_type: str
    parsed_content_summary: str
    insights: List[str]
    metrics: Dict[str, Any]
    
class Recommendation(BaseModel):
    summary: str
    key_risks: List[str]
    key_benefits: List[str]
    final_verdict: str

class FullEvaluation(BaseModel):
    client_context: str
    analyses: List[AnalysisResult]
    recommendation: Recommendation

class RemoteFile(BaseModel):
    path: str
    name: str
    type: str

class RemoteFolder(BaseModel):
    name: str
    files: List[RemoteFile]
    
class EvaluateRemoteRequest(BaseModel):
    file_paths: List[str]
    client_name: str
    context: Optional[str] = None
