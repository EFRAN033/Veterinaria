"""
Servicio de gestión de productos
Contiene la lógica de negocio para CRUD de productos
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.application.dtos.product_dto import ProductCreateDTO, ProductUpdateDTO, ProductDTO
from app.infrastructure.repositories.product_repository_impl import ProductRepositoryImpl
from app.infrastructure.database.models.product import Product
from app.core.exceptions import NotFoundException, ValidationException


class ProductService:
    """Servicio de gestión de productos"""
    
    def __init__(self, db: Session):
        self.db = db
        self.product_repo = ProductRepositoryImpl(db)
    
    def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[ProductDTO]:
        """Obtener todos los productos"""
        products = self.product_repo.get_all(skip=skip, limit=limit, active_only=active_only)
        return [ProductDTO.model_validate(product) for product in products]
    
    def get_by_id(self, product_id: int) -> ProductDTO:
        """Obtener producto por ID"""
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundException("Producto", product_id)
        return ProductDTO.model_validate(product)
    
    def get_by_category(self, category: str, active_only: bool = True) -> List[ProductDTO]:
        """Obtener productos por categoría"""
        products = self.product_repo.get_by_category(category, active_only=active_only)
        return [ProductDTO.model_validate(product) for product in products]
    
    def search(self, query: str, active_only: bool = True) -> List[ProductDTO]:
        """Buscar productos"""
        products = self.product_repo.search(query, active_only=active_only)
        return [ProductDTO.model_validate(product) for product in products]
    
    def create(self, product_data: ProductCreateDTO) -> ProductDTO:
        """
        Crear un nuevo producto
        
        Validaciones:
        - Precio mayor a 0
        - Stock no negativo
        """
        # Validar precio
        if product_data.price <= 0:
            raise ValidationException("El precio debe ser mayor a 0", field="price")
        
        # Validar stock
        if product_data.stock < 0:
            raise ValidationException("El stock no puede ser negativo", field="stock")
        
        # Crear producto
        new_product = Product(
            name=product_data.name,
            description=product_data.description,
            category=product_data.category,
            price=product_data.price,
            stock=product_data.stock,
            image_url=product_data.image_url
        )
        
        created_product = self.product_repo.create(new_product)
        return ProductDTO.model_validate(created_product)
    
    def update(self, product_id: int, product_data: ProductUpdateDTO) -> ProductDTO:
        """Actualizar un producto existente"""
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundException("Producto", product_id)
        
        # Validar precio si se proporciona
        if product_data.price is not None and product_data.price <= 0:
            raise ValidationException("El precio debe ser mayor a 0", field="price")
        
        # Validar stock si se proporciona
        if product_data.stock is not None and product_data.stock < 0:
            raise ValidationException("El stock no puede ser negativo", field="stock")
        
        # Actualizar campos
        if product_data.name is not None:
            product.name = product_data.name
        if product_data.description is not None:
            product.description = product_data.description
        if product_data.category is not None:
            product.category = product_data.category
        if product_data.price is not None:
            product.price = product_data.price
        if product_data.stock is not None:
            product.stock = product_data.stock
        if product_data.image_url is not None:
            product.image_url = product_data.image_url
        if product_data.is_active is not None:
            product.is_active = product_data.is_active
        
        updated_product = self.product_repo.update(product)
        return ProductDTO.model_validate(updated_product)
    
    def delete(self, product_id: int) -> bool:
        """Eliminar un producto"""
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundException("Producto", product_id)
        
        return self.product_repo.delete(product_id)
