import pandas as pd
from pypdf import PdfReader
from docx import Document
from typing import Any, Dict
import os
from fastapi import UploadFile

class Ingestor:
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error parsing PDF: {str(e)}"

    @staticmethod
    def parse_docx(file_path: str) -> str:
        try:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            return f"Error parsing DOCX: {str(e)}"

    @staticmethod
    def parse_xlsx(file_path: str) -> Dict[str, Any]:
        try:
            # Return a dict of sheet_name -> list of records
            dfs = pd.read_excel(file_path, sheet_name=None)
            data = {}
            for sheet, df in dfs.items():
                # Convert timestamps to string to avoid JSON serialization issues
                df = df.astype(object).where(pd.notnull(df), None)
                data[sheet] = df.to_dict(orient='records')
            return data
        except Exception as e:
            return {"error": f"Error parsing XLSX: {str(e)}"}

    @staticmethod
    def identify_file_type(filename: str) -> str:
        ext = filename.split('.')[-1].lower()
        if ext == 'pdf':
            return 'presentation' # or contract
        elif ext in ['xlsx', 'xls', 'csv']:
            return 'spreadsheet'
        elif ext in ['docx', 'doc']:
            return 'contract'
        return 'unknown'
