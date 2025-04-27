from typing import Any, Dict, Optional

class ProductModel:
    def __init__(self, product_name: str, description: str = '', 
                 purchase_price: float = 0, sale_price: float = 0, 
                 stock: int = 0, id:Optional[int] = None) -> None:
       
        self.__product_name: str = product_name
        self.__description: str = description
        self.__purchase_price: float = purchase_price
        self.__sale_price: float = sale_price
        self.__stock: int = stock
        self.__id: int = id if id else  -1

    # Properties
    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int) -> None:
        self.__id = value

    @property
    def product_name(self) -> str:
        return self.__product_name

    @product_name.setter
    def product_name(self, value: str) -> None:
        self.__product_name = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str) -> None:
        self.__description = value

    @property
    def purchase_price(self) -> float:
        return self.__purchase_price

    @purchase_price.setter
    def purchase_price(self, value: float) -> None:
        self.__purchase_price = value

    @property
    def sale_price(self) -> float:
        return self.__sale_price

    @sale_price.setter
    def sale_price(self, value: float) -> None:
        self.__sale_price = value

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, value: int) -> None:
        self.__stock = value

    def to_dict(self) -> Dict[str, Any]:
        """Convert the product to a dictionary for serialization"""
        return {
            'id': self.__id,
            'product_name': self.__product_name.upper(),
            'description': self.__description,
            'purchase_price': self.__purchase_price,
            'sale_price': self.__sale_price,
            'stock': self.__stock
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create a ProductModel instance from a dictionary"""
        return cls(
            id=data.get('id', 0),
            product_name=data.get('product_name', ''),
            description=data.get('description', ''),
            purchase_price=data.get('purchase_price', 0.0),
            sale_price=data.get('sale_price', 0.0),
            stock=data.get('stock', 0)
        )