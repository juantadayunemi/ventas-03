from typing import Any


class Product:
    def __init__(self, product_name: str, description: str = '', purchase_price: float = 0, sale_price: float = 0, stock: int = 0, id: int = 0) -> None:
        self.__product_name: str = product_name
        self.__description: str = description
        self.__purchase_price: float = purchase_price
        self.__sale_price: float = sale_price
        self.__stock: int = stock
        self.__id: int = id

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

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int) -> None:
        self.__id = value

    @property
    def getJson(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "product_name": self.product_name,
            "description": self.description,
            "purchase_price": self.purchase_price,
            "sale_price": self.sale_price,
            "stock": self.stock,
        }

    # Atributos usados para generar esta clase:
    # {
    #     'product_name': 'str',
    #     'description': 'str',
    #     'purchase_price': 'float = 0',
    #     'sale_price': 'float = 0',
    #     'stock': 'int = 0',
    #     'id': 'int = 0',
    # }
