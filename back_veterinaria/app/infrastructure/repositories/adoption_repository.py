from sqlalchemy.orm import Session
from app.infrastructure.database.models.adoption import Adoption
from app.application.dtos.adoption_dto import AdoptionCreate

class AdoptionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, adoption: AdoptionCreate) -> Adoption:
        db_adoption = Adoption(**adoption.model_dump())
        self.db.add(db_adoption)
        self.db.commit()
        self.db.refresh(db_adoption)
        return db_adoption

    def get_all(self) -> list[Adoption]:
        return self.db.query(Adoption).filter(Adoption.status == "available").all()

    def get_by_id(self, id: int) -> Adoption:
        return self.db.query(Adoption).filter(Adoption.id == id).first()
