"""seed demo catalog services (ids 1-4)

El front envía service_id 1–4 al agendar desde solicitudes/chat.
Sin filas en `services`, create appointment lanza NotFoundException.

Revision ID: f9c8e7d6b5a4
Revises: e8a1c2b3d4f5
Create Date: 2026-04-21

"""
from alembic import op
import sqlalchemy as sa


revision = "f9c8e7d6b5a4"
down_revision = "e8a1c2b3d4f5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    inserts = [
        (
            1,
            "Consulta",
            "Consulta veterinaria general",
            "consultation",
            50.00,
            30,
        ),
        (
            2,
            "Cuidado general",
            "Servicios de cuidado general",
            "general",
            45.00,
            45,
        ),
        (
            3,
            "Seguimiento clínico",
            "Consulta de seguimiento",
            "clinical",
            55.00,
            40,
        ),
        (
            4,
            "Estética",
            "Servicios de estética animal",
            "aesthetic",
            60.00,
            60,
        ),
    ]
    for sid, name, desc, cat, price, duration in inserts:
        op.execute(
            sa.text(
                """
                INSERT INTO services (id, name, description, category, price, duration, is_active)
                SELECT :id, :name, :description, :category, :price, :duration, true
                WHERE NOT EXISTS (SELECT 1 FROM services WHERE id = :id)
                """
            ).bindparams(
                id=sid,
                name=name,
                description=desc,
                category=cat,
                price=price,
                duration=duration,
            )
        )


def downgrade() -> None:
    op.execute(sa.text("DELETE FROM services WHERE id IN (1, 2, 3, 4)"))
