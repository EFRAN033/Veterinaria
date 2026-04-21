"""
Garantiza filas mínimas en `services` (ids 1–4) al arrancar la API.

El front mapea tipos de solicitud a service_id fijos; si la tabla quedó vacía
(migración/seed no aplicados en la imagen Docker), POST /appointments fallaba.
"""
import logging
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import SessionLocal

logger = logging.getLogger(__name__)

_DEMO_ROWS = [
    (1, "Consulta", "Consulta veterinaria general", "consultation", 50.00, 30),
    (2, "Cuidado general", "Servicios de cuidado general", "general", 45.00, 45),
    (3, "Seguimiento clínico", "Consulta de seguimiento", "clinical", 55.00, 40),
    (4, "Estética", "Servicios de estética animal", "aesthetic", 60.00, 60),
]

_STMT = text(
    """
    INSERT INTO services (id, name, description, category, price, duration, is_active)
    SELECT :id, :name, :description, :category, :price, :duration, true
    WHERE NOT EXISTS (SELECT 1 FROM services WHERE id = :id)
    """
)


def ensure_demo_services_session(db: Session) -> None:
    """INSERT idempotente por fila usando la sesión dada (sin commit)."""
    for sid, name, desc, cat, price, duration in _DEMO_ROWS:
        db.execute(
            _STMT,
            {
                "id": sid,
                "name": name,
                "description": desc,
                "category": cat,
                "price": price,
                "duration": duration,
            },
        )


def ensure_demo_services_rows() -> None:
    """Misma lógica que el seed: abre sesión, aplica filas y hace commit."""
    db = SessionLocal()
    try:
        ensure_demo_services_session(db)
        db.commit()
        logger.info("[catalog] Servicios demo verificados (ids 1–4).")
    except Exception:
        db.rollback()
        logger.exception("[catalog] No se pudo asegurar el catálogo demo de servicios.")
        raise
    finally:
        db.close()
