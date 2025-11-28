import sys
import os

# Add the current directory to sys.path to make imports work
sys.path.append(os.getcwd())

from app.application.services.ai_service import AIService
from app.core.config import settings

def test_ai():
    print(f"OpenAI API Key present: {bool(settings.OPENAI_API_KEY)}")
    if not settings.OPENAI_API_KEY:
        print("WARNING: OpenAI API Key is missing!")
    
    try:
        service = AIService()
        data = {
            "service_type": "consultation",
            "pet_name": "Firulais",
            "species": "Perro",
            "symptoms": "Vómitos y diarrea",
            "urgency": "Alta"
        }
        print("Analyzing service request...")
        result = service.analyze_service_request(data)
        print("Result:")
        print(result)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai()
