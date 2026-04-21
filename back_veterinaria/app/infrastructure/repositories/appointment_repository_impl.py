"""
Implementación del repositorio de citas
"""
from typing import Optional, List, Tuple
from datetime import date, time, datetime
from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload
from app.infrastructure.database.models.appointment import Appointment
from app.infrastructure.database.models.pet import Pet


def _first_day_n_months_ago(months: int) -> date:
    """Primer día del mes, retrocediendo (months - 1) meses desde el mes actual."""
    d = date.today().replace(day=1)
    y, m = d.year, d.month
    for _ in range(max(months - 1, 0)):
        m -= 1
        if m < 1:
            m = 12
            y -= 1
    return date(y, m, 1)


def _apply_species_sex_filters(query, species: Optional[str], sex: Optional[str]):
    """Filtra por mascota; citas sin mascota quedan fuera si hay filtro activo."""
    s = (species or "").strip().lower()
    if s and s not in ("todos", "all", "todas"):
        if s == "perro":
            query = query.filter(
                Pet.id.isnot(None),
                or_(
                    func.lower(Pet.species).like("%perro%"),
                    func.lower(Pet.species).like("%dog%"),
                ),
            )
        elif s == "gato":
            query = query.filter(
                Pet.id.isnot(None),
                or_(
                    func.lower(Pet.species).like("%gato%"),
                    func.lower(Pet.species).like("%cat%"),
                ),
            )
        else:
            query = query.filter(
                Pet.id.isnot(None),
                func.lower(Pet.species).like(f"%{s}%"),
            )
    sx = (sex or "").strip().lower()
    if sx and sx not in ("todos", "all", "todas"):
        if "macho" in sx:
            query = query.filter(
                Pet.id.isnot(None),
                func.lower(Pet.gender).like("%macho%"),
            )
        elif "hembra" in sx:
            query = query.filter(
                Pet.id.isnot(None),
                func.lower(Pet.gender).like("%hembra%"),
            )
    return query


class AppointmentRepositoryImpl:
    """Implementación concreta del repositorio de citas"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, appointment_id: int) -> Optional[Appointment]:
        """Obtener cita por ID"""
        return (
            self.db.query(Appointment)
            .options(joinedload(Appointment.pet))
            .filter(Appointment.id == appointment_id)
            .first()
        )
    
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Obtener citas de un usuario"""
        return (
            self.db.query(Appointment)
            .options(joinedload(Appointment.pet))
            .filter(Appointment.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Obtener todas las citas (para veterinarios/admin)"""
        return (
            self.db.query(Appointment)
            .options(joinedload(Appointment.pet))
            .order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_vet_history(
        self,
        skip: int = 0,
        limit: int = 100,
        species: Optional[str] = None,
        sex: Optional[str] = None,
    ) -> List[Appointment]:
        """
        Historial clínico para veterinario: todas las citas completadas, canceladas o pasadas.
        """
        today = date.today()
        history_filter = or_(
            Appointment.status.in_(["completed", "cancelled"]),
            Appointment.appointment_date < today,
        )
        q = (
            self.db.query(Appointment)
            .options(joinedload(Appointment.pet))
            .outerjoin(Pet, Appointment.pet_id == Pet.id)
            .filter(history_filter)
        )
        q = _apply_species_sex_filters(q, species, sex)
        return (
            q.order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def _appointments_in_range_query(
        self, species: Optional[str], sex: Optional[str], cutoff: date
    ):
        q = (
            self.db.query(Appointment)
            .outerjoin(Pet, Appointment.pet_id == Pet.id)
            .filter(Appointment.appointment_date >= cutoff)
        )
        return _apply_species_sex_filters(q, species, sex)

    def get_analytics_aggregates(
        self,
        species: Optional[str],
        sex: Optional[str],
        range_months: int = 12,
    ) -> Tuple[list[tuple[datetime, int]], list[tuple[str, int]], int, int, int]:
        """
        Devuelve:
        - filas (mes_truncado, count) citas en rango
        - filas (status, count) en rango
        - total citas en rango
        - mascotas distintas atendidas (con pet_id) en rango
        - seguimiento: mascotas distintas con cita futura pendiente/confirmada (filtros de mascota)
        """
        cutoff = _first_day_n_months_ago(range_months)
        today = date.today()

        month_trunc = func.date_trunc("month", Appointment.appointment_date)
        month_rows = (
            self._appointments_in_range_query(species, sex, cutoff)
            .with_entities(month_trunc, func.count(Appointment.id))
            .group_by(month_trunc)
            .order_by(month_trunc)
            .all()
        )

        status_rows = (
            self._appointments_in_range_query(species, sex, cutoff)
            .with_entities(Appointment.status, func.count(Appointment.id))
            .group_by(Appointment.status)
            .all()
        )

        total = (
            self._appointments_in_range_query(species, sex, cutoff)
            .with_entities(func.count(Appointment.id))
            .scalar()
            or 0
        )

        unique_pets = (
            self._appointments_in_range_query(species, sex, cutoff)
            .filter(Appointment.pet_id.isnot(None))
            .with_entities(func.count(func.distinct(Appointment.pet_id)))
            .scalar()
            or 0
        )

        follow_q = (
            self.db.query(Appointment)
            .outerjoin(Pet, Appointment.pet_id == Pet.id)
            .filter(
                Appointment.pet_id.isnot(None),
                Appointment.appointment_date >= today,
                Appointment.status.in_(["pending", "confirmed"]),
            )
        )
        follow_q = _apply_species_sex_filters(follow_q, species, sex)
        follow_up = (
            follow_q.with_entities(func.count(func.distinct(Appointment.pet_id))).scalar() or 0
        )

        return month_rows, status_rows, int(total), int(unique_pets), int(follow_up)
    
    def get_by_date(self, appointment_date: date) -> List[Appointment]:
        """Obtener citas de una fecha específica"""
        return self.db.query(Appointment).filter(
            Appointment.appointment_date == appointment_date
        ).all()
    
    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Obtener citas por estado"""
        return self.db.query(Appointment).filter(
            Appointment.status == status
        ).offset(skip).limit(limit).all()
    
    def create(self, appointment: Appointment) -> Appointment:
        """Crear una nueva cita"""
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        return appointment
    
    def update(self, appointment: Appointment) -> Appointment:
        """Actualizar una cita existente"""
        self.db.commit()
        self.db.refresh(appointment)
        return appointment
    
    def delete(self, appointment_id: int) -> bool:
        """Eliminar una cita"""
        appointment = self.get_by_id(appointment_id)
        if appointment:
            self.db.delete(appointment)
            self.db.commit()
            return True
        return False
    
    def check_availability(self, appointment_date: date, appointment_time: time) -> bool:
        """Verificar si un horario está disponible"""
        existing = self.db.query(Appointment).filter(
            Appointment.appointment_date == appointment_date,
            Appointment.appointment_time == appointment_time,
            Appointment.status.in_(["pending", "confirmed"])
        ).first()
        return existing is None
