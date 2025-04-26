from typing import Any, Dict
from models.customer import CustomerModel


class CustomerDTO():
    def __init__( self, customer:CustomerModel):

        self.__customer_generic:CustomerModel = customer


    @property
    def id (self)-> int:
        return self.__customer_generic.id
    
    @property
    def customer (self)-> CustomerModel:
        return self.__customer_generic


    def getJson(self) ->Dict[str, Any]:
        # Método especial para representar la clase venta como diccionario
        customer= {
            "id":self.id,
            "dni": self.customer.dni,
            "first_name":self.customer.first_name.upper(),
            "last_name":self.customer.last_name.upper(),
            "customer_type":self.customer.type,
            "discount": self.customer.discount,
            "credit_limit": self.customer.credit_limit
            }
        return customer