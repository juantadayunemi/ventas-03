from typing import Any, Dict
from models.product import Product


class ProductDTO():

    def __init__( self, product:Product):
   
        self.__product:Product = product

    @property
    def id (self)-> int:
        return self.__product.id
    
    @property
    def product (self)-> Product:
        return self.__product


    def getJson(self) ->Dict[str, Any]:
        # Método especial para representar la clase venta como diccionario
        product= {
            "id":self.id,
            "product_name": self.product.product_name.upper(),
            "description":self.product.description,
            "purchase_price":self.product.purchase_price,
            "sale_price":self.product.sale_price,
            "stock":self.product.stock
            }
        return product
        