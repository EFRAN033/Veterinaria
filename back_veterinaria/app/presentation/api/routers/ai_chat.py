from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from openai import OpenAI
from app.core.config import settings
from app.core.vet_knowledge import SYSTEM_PROMPT, CLINICAL_EXAMPLES
from app.core.dss.triage import assess_vitals
from app.core.dss.predictor import predict_severity
import re

router = APIRouter()

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    vitals: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    dss_data: Optional[Dict[str, Any]] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_with_vet_ai(request: ChatRequest):
    """AI Veterinary Assistant Chat using OpenAI with Few-Shot Learning & DSS"""
    try:
        messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        dss_output = None
        
        if request.vitals:
            triage_result = assess_vitals(request.vitals)
            ml_result = predict_severity(request.vitals)
            
            dss_output = {
                "triage": triage_result,
                "prediction": ml_result
            }
            
            dss_context = f"""
            [SISTEMA DE SOPORTE A LA DECISIÓN (DSS) - DATOS EN TIEMPO REAL]
            
            1. ANÁLISIS DE CONSTANTES (TRIAJE):
            - Nivel de Triaje: {triage_result['triage_level']}
            - Puntuación: {triage_result['triage_score']}
            - Alertas Activas: {', '.join(triage_result['alerts']) if triage_result['alerts'] else 'Ninguna'}
            - Índice de Shock: {triage_result['calculated_metrics'].get('shock_index', 'N/A')}
            
            2. PREDICCIÓN DE GRAVEDAD (MODELO ML LOCAL):
            - Predicción: {ml_result.get('ml_prediction', 'N/A')}
            - Confianza del Modelo: {ml_result.get('confidence', 0)}%
            
            INSTRUCCIÓN: Utiliza estos datos objetivos para fundamentar tu respuesta. Si el triaje es ROJO o la predicción es ALTA, prioriza la estabilización inmediata.
            """
            messages_payload.append({"role": "system", "content": dss_context})
        
        messages_payload.extend(CLINICAL_EXAMPLES)
        
        for msg in request.messages:
            clean_text = re.sub(r'!\[.*?\]\((.*?)\)', '', msg.content).strip()
            if not clean_text:
                clean_text = msg.content # Fallback if everything was an image link
            
            messages_payload.append({"role": msg.role, "content": clean_text})

        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=messages_payload,
            temperature=0.3
        )
        
        ai_response = response.choices[0].message.content
        return {"response": ai_response, "dss_data": dss_output}

    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        raise HTTPException(status_code=500, detail="Error communicating with AI service")
