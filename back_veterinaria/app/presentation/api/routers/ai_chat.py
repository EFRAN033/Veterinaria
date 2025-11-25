from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from openai import OpenAI
from app.core.config import settings
from app.core.vet_knowledge import SYSTEM_PROMPT, CLINICAL_EXAMPLES

router = APIRouter()

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    response: str

import re
import base64
import os

@router.post("/chat", response_model=ChatResponse)
async def chat_with_vet_ai(request: ChatRequest):
    """AI Veterinary Assistant Chat using OpenAI with Few-Shot Learning"""
    try:
        # 1. Start with the System Prompt
        messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # 2. Add Few-Shot Examples
        messages_payload.extend(CLINICAL_EXAMPLES)
        
        # 3. Process User Messages (Text Only)
        for msg in request.messages:
            # We just pass the text content directly, ignoring any image markdown
            # or stripping it if we want to be cleaner, but passing it as text is fine too
            # as the system prompt no longer expects images.
            # To be clean, let's strip the image markdown so the AI doesn't see weird links.
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
        return {"response": ai_response}

    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        raise HTTPException(status_code=500, detail="Error communicating with AI service")
