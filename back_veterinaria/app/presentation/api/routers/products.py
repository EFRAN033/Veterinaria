"""
Router de productos refactorizado con arquitectura limpia
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.application.services.product_service import ProductService
from app.application.dtos.product_dto import ProductCreateDTO, ProductUpdateDTO, ProductDTO
from app.presentation.dependencies.auth import get_current_admin_user
from app.infrastructure.database.models.user import User
from app.core.exceptions import NotFoundException, ValidationException

router = APIRouter()


@router.get("/", response_model=List[ProductDTO])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Obtener todos los productos activos
    Opcionalmente filtrar por categoría o buscar por nombre/descripción
    """
    product_service = ProductService(db)
    
    if search:
        return product_service.search(search, active_only=True)
    elif category:
        return product_service.get_by_category(category, active_only=True)
    
    return product_service.get_all(skip=skip, limit=limit, active_only=True)


@router.get("/{product_id}", response_model=ProductDTO)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Obtener un producto por ID
    """
    try:
        product_service = ProductService(db)
        return product_service.get_by_id(product_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.post("/", response_model=ProductDTO, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Crear un nuevo producto (solo administradores)
    """
    try:
        product_service = ProductService(db)
        return product_service.create(product_data)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.put("/{product_id}", response_model=ProductDTO)
async def update_product(
    product_id: int,
    product_data: ProductUpdateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Actualizar un producto (solo administradores)
    """
    try:
        product_service = ProductService(db)
        return product_service.update(product_id, product_data)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Eliminar un producto (solo administradores)
    """
    try:
        product_service = ProductService(db)
        product_service.delete(product_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
