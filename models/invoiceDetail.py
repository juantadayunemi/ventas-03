from datetime import date
from typing import List, Dict, Any, Optional
from models.base import BaseModel

class InvoiceDetailModel(BaseModel):
    _next_id = 1
    """Modelo para los items detallados de una factura"""
    def __init__(self, 
                 product_id:int,
                 product_name: str, 
                 sale_price: float, 
                 quantity: int, 
                 id: Optional[int] = None):
        self.__id: int = id if id is not None else self._get_next_id()
        self.__product_id: int = product_id
        self.__product_name: str = product_name
        self.__sale_price: float = sale_price
        self.__quantity: float = quantity

    # Propiedades
    @property
    def id(self) -> Optional[int]:
        return self.__id

    @id.setter
    def id(self, value: Optional[int]) -> None:
        self.__id = value if value else 1

    @property
    def product_name(self) -> str:
        return self.__product_name

    @product_name.setter
    def product_name(self, value: str) -> None:
        if not value.strip():
            raise ValueError("El nombre del producto no puede estar vacío")
        self.__product_name = value

    @property
    def sale_price(self) -> float:
        return self.__sale_price

    @sale_price.setter
    def sale_price(self, value: float) -> None:
        if value <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        self.__sale_price = value

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float) -> None:
        if value < 1:
            raise ValueError("La cantidad debe ser al menos 1")
        self.__quantity = value

    @property
    def subtotal(self) -> float:
        """Calcula el subtotal (precio x cantidad)"""
        return round(self.__sale_price * self.__quantity, 2)
    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls._next_id
        cls._next_id += 1
        return current_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.__id,
            'product_id': self.__product_id,
            'product_name': self.__product_name,
            'sale_price': self.__sale_price,
            'quantity': self.__quantity,
            'subtotal': self.subtotal
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            id=data.get('id'),
            product_id=data['product_id'],
            product_name=data['product_name'],
            sale_price=data['sale_price'],
            quantity=data['quantity']
        )
