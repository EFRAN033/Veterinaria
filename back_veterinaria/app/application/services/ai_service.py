import json
from openai import OpenAI
from app.core.config import settings
from app.core.prompts import PROMPTS, INTENT_CLASSIFICATION_PROMPT

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY, max_retries=0)
        self.model = "gpt-4o-mini"

    def classify_intent(self, message: str) -> str:
        """
        Clasifica la intención o especialidad del caso clínico.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un clasificador de casos clínicos veterinarios."},
                    {"role": "user", "content": INTENT_CLASSIFICATION_PROMPT.format(message=message)}
                ],
                temperature=0.0,
                max_tokens=20
            )
            category = response.choices[0].message.content.strip().upper()
            if category not in PROMPTS:
                return "GENERAL"
            return category
        except Exception as e:
            print(f"Error classifying intent: {e}")
            return "GENERAL"

    def generate_response(self, messages: list, vitals: dict = None, pet_id: int = None, image_data: str = None, db = None) -> dict:
        """
        Genera una respuesta enriquecida usando OpenAI, con soporte multimodal.
        """
        # ... (rest of the function setup) ...
        # (I need to keep the logic up to the try block, so I will target the try/except block specifically or the whole function if easier.
        # Actually, I can just replace the __init__ and the try/except block in generate_response.
        # But replace_file_content works on contiguous blocks.
        # I will replace __init__ first, then the try/except block.)

    # Wait, I can't do two replace calls in one step if they are for the same file unless I use multi_replace.
    # I will use multi_replace_file_content.


    def generate_response(self, messages: list, vitals: dict = None, pet_id: int = None, image_data: str = None, db = None) -> dict:
        """
        Genera una respuesta enriquecida usando OpenAI, con soporte multimodal.
        """
        # 1. Clasificar intención y condición (Triage)
        last_user_message = next((m.content for m in reversed(messages) if m.role == "user"), "")
        category = self.classify_intent(last_user_message)
        
        # 2. Construir System Prompt Dinámico
        system_prompt = PROMPTS.get(category, PROMPTS["GENERAL"])
        
        # 3. Construir historial de mensajes
        ai_messages = [{"role": "system", "content": system_prompt}]
        
        # Inyectar historial si existe
        if pet_id and db:
            history_context = self._get_patient_history(pet_id, db)
            if history_context:
                ai_messages.append({"role": "system", "content": f"HISTORIAL MÉDICO DEL PACIENTE:\n{history_context}"})

        # Agregar mensajes de usuario
        for msg in messages:
            ai_messages.append({"role": msg.role, "content": msg.content})
            
        # 4. Manejo de Imágenes (Multimodal)
        if image_data:
            # Si hay imagen, agregamos un mensaje de usuario con la imagen
            # Nota: Esto asume que el último mensaje es el que acompaña a la imagen o se envía sola.
            # Para simplificar, añadimos un mensaje explícito de sistema/usuario con la imagen.
            ai_messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": "Aquí tienes una imagen clínica adjunta. Analízala en contexto con el caso."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            })

        # Agregar contexto de constantes vitales si existen
        if vitals:
            vitals_context = f"""
            [CONSTANTES VITALES ACTUALES]
            FC: {vitals.get('heart_rate', 'N/A')}
            FR: {vitals.get('respiratory_rate', 'N/A')}
            Temp: {vitals.get('temperature', 'N/A')}
            TLLC: {vitals.get('capillary_refill', 'N/A')}
            PA: {vitals.get('systolic_bp', 'N/A')}
            """
            ai_messages.append({"role": "system", "content": vitals_context})
            
        # Agregar historial de chat
        for msg in messages:
            ai_messages.append({"role": msg.role, "content": msg.content})

        # 4. Definir esquema de respuesta estructurada (Function Calling / JSON Mode)
        # Usamos JSON mode para garantizar estructura
        ai_messages.append({
            "role": "system", 
            "content": """
            Responde SIEMPRE en formato JSON con la siguiente estructura:
            {
                "response": "Tu respuesta clínica detallada aquí (usa markdown)",
                "clinical_insights": {
                    "differentials": [
                        {"name": "Enfermedad A", "probability": "Alta/Media/Baja", "reasoning": "Breve explicación de por qué se sospecha esto basado en los síntomas."}
                    ],
                    "recommended_tests": [
                        {"name": "Hemograma completo", "purpose": "Evaluar anemia e infección"}
                    ],
                    "treatment_focus": ["Hidratación", "Antibioterapia"],
                    "calculated_dosages": [{"drug": "Amoxicilina", "dose": "250mg", "frequency": "Cada 12h", "notes": "Dosis basada en peso 10kg"}],
                    "safety_alerts": [{"level": "High/Medium/Low", "message": "Riesgo de interacción entre X e Y"}],
                    "follow_up": {"duration": "24 horas", "reason": "Reevaluar hidratación"},
                    "references": ["Cita bibliográfica o guía clínica relevante (opcional)"]
                }
            }
            Los 'differentials' deben ser las 3-5 causas más probables. INCLUYE SIEMPRE el campo 'reasoning'.
            En 'recommended_tests', INCLUYE SIEMPRE el campo 'purpose' explicando qué buscamos con esa prueba.
            SIEMPRE que sugieras medicamentos en 'treatment_focus' o 'response', intenta calcular la dosis exacta en 'calculated_dosages' usando el peso del paciente (si está disponible en el contexto).
            SIEMPRE verifica interacciones medicamentosas. Si sugieres combinaciones con riesgo (ej. AINEs + Corticoides), agrega una alerta en 'safety_alerts'.
            SIEMPRE sugiere un tiempo de seguimiento ('follow_up') basado en la gravedad del caso.
            """
        })

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=ai_messages,
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            parsed_content = json.loads(content)
            
            return {
                "response": parsed_content.get("response", ""),
                "clinical_insights": parsed_content.get("clinical_insights", None),
                "category": category
            }
            
        except Exception as e:
            print(f"Error generating AI response: {e}")
            error_msg = "Lo siento, hubo un error al procesar tu consulta."
            if "rate_limit" in str(e).lower() or "429" in str(e):
                error_msg = "⚠️ El sistema está saturado (Límite de cuota OpenAI alcanzado). Por favor espera unos segundos."
            
            return {
                "response": error_msg,
                "clinical_insights": None,
                "category": "ERROR"
            }

    def generate_report(self, messages: list, pet_id: int = None, db = None) -> str:
        """
        Genera un reporte clínico formal basado en la conversación.
        """
        try:
            # Construir contexto
            context = ""
            if pet_id and db:
                context = self._get_patient_history(pet_id, db)
            
            chat_history = "\n".join([f"{m.role.upper()}: {m.content}" for m in messages])
            
            prompt = f"""
            Actúa como un Veterinario Senior redactando un historial clínico formal.
            Basado en la siguiente conversación y contexto, genera un reporte médico profesional.
            
            CONTEXTO:
            {context}
            
            CONVERSACIÓN:
            {chat_history}
            
            FORMATO REQUERIDO (Markdown):
            # REPORTE CLÍNICO VETERINARIO
            
            ## 1. Reseña y Anamnesis
            [Resumen de los síntomas y motivo de consulta]
            
            ## 2. Hallazgos Clínicos
            [Interpretación de los datos aportados]
            
            ## 3. Diagnóstico Presuntivo
            [Principales sospechas]
            
            ## 4. Plan Diagnóstico y Terapéutico
            [Pruebas y tratamientos sugeridos]
            
            ## 5. Recomendaciones
            [Instrucciones para el propietario]
            
            Firma: Asistente IA Veterinario
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": prompt}],
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating report: {e}")
            return "Error al generar el reporte clínico."

    def _get_patient_history(self, pet_id: int, db) -> str:
        """
        Recupera el historial médico del paciente desde la base de datos.
        """
        try:
            from app.infrastructure.database.models.appointment import Appointment
            from app.infrastructure.database.models.pet import Pet
            
            # Obtener datos de la mascota
            pet = db.query(Pet).filter(Pet.id == pet_id).first()
            if not pet:
                return ""
                
            # Obtener últimas 5 citas
            appointments = db.query(Appointment).filter(
                Appointment.pet_id == pet_id
            ).order_by(Appointment.appointment_date.desc()).limit(5).all()
            
            history_str = f"""
            [HISTORIAL CLÍNICO DEL PACIENTE]
            Nombre: {pet.name}
            Especie: {pet.species}
            Raza: {pet.breed}
            Edad: {pet.age} años
            Peso: {pet.weight} kg
            
            Últimas Consultas:
            """
            
            for app in appointments:
                history_str += f"- {app.appointment_date}: {app.notes or 'Sin notas'}\n"
                
            return history_str
            
        except Exception as e:
            print(f"Error fetching patient history: {e}")
            return ""
