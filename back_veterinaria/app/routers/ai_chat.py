from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random

router = APIRouter()

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_vet_ai(request: ChatRequest):
    """
    Mock AI Veterinary Assistant Chat
    """
    user_message = request.messages[-1].content.lower()
    
    # Simple keyword-based mock responses
    if "vomit" in user_message or "vómito" in user_message:
        response = "El vómito en las mascotas puede deberse a muchas causas, desde una indigestión simple hasta algo más serio. Si es un episodio único y el animal está animado, puedes esperar. Si es persistente o hay sangre, acude al veterinario inmediatamente."
    elif "comer" in user_message or "appetite" in user_message:
        response = "La falta de apetito es un signo de alerta. Si tu mascota no ha comido en 24 horas, deberías traerla a consulta para descartar infecciones u otros problemas."
    elif "vacuna" in user_message or "vaccine" in user_message:
        response = "Las vacunas son esenciales. Para perros, las principales son Parvovirus, Moquillo, y Rabia. ¿Te gustaría agendar una cita para vacunación?"
    else:
        response = "Entiendo tu preocupación. Como asistente virtual, te recomiendo observar los síntomas. Si notas decaimiento, fiebre o dolor, lo mejor es agendar una cita con nuestros especialistas."
        
    return {"response": response}
