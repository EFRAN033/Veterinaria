"""
Implementación del repositorio de productos
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.infrastructure.database.models.product import Product


class ProductRepositoryImpl:
    """Implementación concreta del repositorio de productos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Obtener producto por ID"""
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Product]:
        """Obtener todos los productos con paginación"""
        query = self.db.query(Product)
        if active_only:
            query = query.filter(Product.is_active == True)
        return query.offset(skip).limit(limit).all()
    
    def get_by_category(self, category: str, active_only: bool = True) -> List[Product]:
        """Obtener productos por categoría"""
        query = self.db.query(Product).filter(Product.category == category)
        if active_only:
            query = query.filter(Product.is_active == True)
        return query.all()
    
    def search(self, query: str, active_only: bool = True) -> List[Product]:
        """Buscar productos por nombre o descripción"""
        search_query = self.db.query(Product).filter(
            or_(
                Product.name.ilike(f"%{query}%"),
                Product.description.ilike(f"%{query}%")
            )
        )
        if active_only:
            search_query = search_query.filter(Product.is_active == True)
        return search_query.all()
    
    def create(self, product: Product) -> Product:
        """Crear un nuevo producto"""
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def update(self, product: Product) -> Product:
        """Actualizar un producto existente"""
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def delete(self, product_id: int) -> bool:
        """Eliminar un producto"""
        product = self.get_by_id(product_id)
        if product:
            self.db.delete(product)
            self.db.commit()
            return True
        return False
    
    def update_stock(self, product_id: int, quantity: int) -> bool:
        """Actualizar stock de un producto"""
        product = self.get_by_id(product_id)
        if product:
            product.stock += quantity
            self.db.commit()
            return True
        return False
