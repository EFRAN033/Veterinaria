"""
Interfaz del repositorio de productos
"""
from typing import Protocol, Optional, List
from app.infrastructure.database.models.product import Product


class ProductRepository(Protocol):
    """Protocolo que define las operaciones del repositorio de productos"""
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Obtener producto por ID"""
        ...
    
    def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Product]:
        """Obtener todos los productos con paginación"""
        ...
    
    def get_by_category(self, category: str, active_only: bool = True) -> List[Product]:
        """Obtener productos por categoría"""
        ...
    
    def search(self, query: str, active_only: bool = True) -> List[Product]:
        """Buscar productos por nombre o descripción"""
        ...
    
    def create(self, product: Product) -> Product:
        """Crear un nuevo producto"""
        ...
    
    def update(self, product: Product) -> Product:
        """Actualizar un producto existente"""
        ...
    
    def delete(self, product_id: int) -> bool:
        """Eliminar un producto"""
        ...
    
    def update_stock(self, product_id: int, quantity: int) -> bool:
        """Actualizar stock de un producto"""
        ...
