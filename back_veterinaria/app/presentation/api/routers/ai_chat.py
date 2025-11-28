from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.application.services.ai_service import AIService
from app.core.dss.triage import assess_vitals
from app.core.dss.predictor import predict_severity
import re

router = APIRouter()

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    vitals: Optional[Dict[str, Any]] = None
    pet_id: Optional[int] = None
    image_data: Optional[str] = None 

class ChatResponse(BaseModel):
    response: str
    dss_data: Optional[Dict[str, Any]] = None
    clinical_insights: Optional[Dict[str, Any]] = None
    category: str = "GENERAL"

@router.post("/chat", response_model=ChatResponse)
async def chat_with_vet_ai(request: ChatRequest, db: Session = Depends(get_db)):
    """AI Veterinary Assistant Chat using OpenAI with Few-Shot Learning & DSS"""
    try:
        ai_service = AIService()
        
        dss_output = None
        
        if request.vitals:
            triage_result = assess_vitals(request.vitals)
            ml_result = predict_severity(request.vitals)
            
            dss_output = {
                "triage": triage_result,
                "prediction": ml_result
            }
        
        ai_result = ai_service.generate_response(
            messages=request.messages, 
            vitals=request.vitals,
            pet_id=request.pet_id,
            image_data=request.image_data,
            db=db
        )
        
        print(f"DEBUG: AI Result keys: {ai_result.keys()}")
        print(f"DEBUG: Clinical Insights: {ai_result.get('clinical_insights')}")
        
        return {
            "response": ai_result["response"],
            "dss_data": dss_output,
            "clinical_insights": ai_result.get("clinical_insights"),
            "category": ai_result["category"]
        }
    except Exception as e:
        print(f"Error in AI Chat API: {e}")
        raise HTTPException(status_code=500, detail="Error communicating with AI service")

@router.post("/report", response_model=Dict[str, str])
async def generate_clinical_report(request: ChatRequest, db: Session = Depends(get_db)):
    """Generate a formal clinical report from the chat session"""
    try:
        ai_service = AIService()
        report = ai_service.generate_report(
            messages=request.messages,
            pet_id=request.pet_id,
            db=db
        )
        return {"report": report}
    except Exception as e:
        print(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail="Error generating report")
