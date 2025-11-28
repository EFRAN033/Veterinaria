from sqlalchemy.orm import Session
from app.infrastructure.repositories.adoption_repository import AdoptionRepository
from app.application.dtos.adoption_dto import AdoptionCreate, AdoptionResponse
import base64
import os
import uuid

class AdoptionService:
    def __init__(self, db: Session):
        self.repository = AdoptionRepository(db)
        self.UPLOAD_DIR = "static/uploads/adoptions"
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)

    def create_adoption(self, adoption_data: AdoptionCreate) -> AdoptionResponse:
        # Handle image processing if needed (assuming images are already URLs or handled elsewhere, 
        # but if they are base64 strings, we should save them here. 
        # For now, let's assume the frontend sends base64 and we save it)
        
        processed_images = []
        for img in adoption_data.images:
            if img.startswith("data:image"):
                try:
                    header, encoded = img.split(",", 1)
                    file_ext = header.split(";")[0].split("/")[1]
                    filename = f"{uuid.uuid4()}.{file_ext}"
                    filepath = os.path.join(self.UPLOAD_DIR, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(base64.b64decode(encoded))
                    
                    processed_images.append(f"/static/uploads/adoptions/{filename}")
                except Exception as e:
                    print(f"Error saving image: {e}")
                    # If error, maybe skip or keep original if it's a URL
                    processed_images.append(img) 
            else:
                processed_images.append(img)
        
        adoption_data.images = processed_images
        return self.repository.create(adoption_data)

    def get_all_adoptions(self) -> list[AdoptionResponse]:
        return self.repository.get_all()
