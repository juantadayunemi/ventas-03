from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

from models.base import BaseModel


class ClientModel(ABC):

    def __init__(self,
                first_name:str = "Consumidor",
                last_name:str = "Final",
                dni:str = "9999999999999",
                id:Optional[int] = None,
                customer_type:Optional[int]=1,
                ):

        self.__id:int = -1 if not id else  id
        self.__dni:str = dni 
        self.__first_name:str = first_name
        self.__last_name:str = last_name
        self.__customer_type:int = customer_type if isinstance(customer_type, int) else  -1

    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, value:int ) ->None:
        self.__id = value

    @property
    def dni(self) -> str:
        return self.__dni
    
    @dni.setter
    def dni(self, value) -> None:
        if not isinstance( value , str):
            raise ValueError('El numero de identificacion debe ser de tipo texto')
        if len(value) in (10, 13):
            self.__dni = value
        else:
            self.__dni ="9999999999999"  
    
    @property
    def first_name(self)->str:
        return self.__first_name

    @first_name.setter
    def first_name(self, values) ->None:
        self.__first_name = values

    @property
    def last_name(self)->str:
        return self.__last_name

    @last_name.setter
    def last_name(self, values) ->None:
        self.__last_name = values

    @property
    def customer_type(self) -> int:
        return self.__customer_type
    
    @customer_type.setter
    def customer_type(self, value) -> None:
        self.__customer_type = value

    @property
    def fullName(self)-> str:
        return self.__first_name + ' ' + self.__last_name

    @property  
    @abstractmethod
    def discount(self) -> float:
        pass
    
    @property
    @abstractmethod
    def credit_limit(self) -> int:
        pass


class RegularClient(ClientModel):
    def __init__(self,
                first_name:str="Consumidor",
                last_name:str="Final",
                dni:str="9999999999",
                id:Optional[int] = None,
                card=False):
        
        self.__card = card
        super().__init__(first_name, last_name, dni=dni, id=id)  
            

    @property
    def credit_limit(self) -> int:
        return 0
    
    @property
    def discount(self) -> float:
        """10 % de descuento si tiene tarjeta."""
        return 0.1 if self.__card else 0
     
    def set_card(self, value : bool) -> None:
        self.__card = value



class VipClient(ClientModel):
    def __init__(self, 
                first_name:str="Consumidor",
                last_name:str="Final",
                dni:str="9999999999",
                id:Optional[int] = None):
        
        # Método constructor para inicializar los atributos de la clase VipClient
        self.__credit_limit:int = 10000  # Límite de crédito del cliente VIP
        super().__init__(first_name, last_name, dni=dni, id=id)  
              
    @property
    def credit_limit(self)-> int:
        return self.__credit_limit
    
    @credit_limit.setter
    def credit_limit(self, value)-> None:
        self.__credit_limit = value
    
    @property
    def discount(self)-> float:
        return 0

class CustomerModel(ClientModel, BaseModel):

    def __init__(self, dni: str, first_name: str, last_name: str, id: Optional[int] = None, 
               customer_type:Optional[int] = None, discount: Optional[float] = None,  credit_limit: Optional[int] = None) -> None:

   
        self.__discount =  discount if discount else 0
        self.__customer_type =  customer_type if  customer_type else 1
        self.__credit_limit =  credit_limit if  credit_limit else 0
        self.instance:Union[RegularClient, VipClient, None] = None
        super().__init__(first_name, last_name, dni=dni, id=id)  

        # Validation data
        if not isinstance(customer_type, int) or customer_type not in (1, 2):
            raise ValueError('customer_type debe ser 1 (Regular) o 2 (Vip)')
        
        if not isinstance(dni, str) or len( dni) == 0:
            raise ValueError('DNI debe ser de tipo texto y no vacío')
        
        if not isinstance(first_name, str) or len( first_name) == 0:
            raise ValueError('APELLIDO debe ser de tipo texto y no vacío')
        
        if not isinstance(last_name, str) or len( last_name) == 0:
            raise ValueError('NOMBRE debe ser de tipo texto y no vacío')
        
        super().__init__(dni= dni, first_name= first_name, last_name=last_name, customer_type = customer_type, id= id)


    def __customer_instance(self) -> Union[RegularClient, VipClient]:
        """Crea la instancia del cliente una sola vez al inicializar."""

        if  self.__instance:
            return self.__instance
        
        if self.__type == 1:
            self.__instance =  RegularClient(
                first_name=self.first_name,
                last_name=self.last_name,
                dni=self.__dni
            )
        else : 
            self.__instance = VipClient(
            first_name=self.first_name,
            last_name=self.last_name,
            dni=self.__dni
        )
        return  self.__instance
    

    @property
    def customer_type (self)-> int:
        return self.__type
    
    @customer_type.setter
    def customer_type (self, value)-> None:
        self.__type = value

    @property
    def discount(self) -> float:
        """Devuelve el descuento aplicable al cliente."""
        customer_instance = self.__customer_instance()
        if isinstance(customer_instance, RegularClient):
            return customer_instance.discount
        return 0.0
    
    @property
    def credit_limit(self) -> int:
        """Devuelve el límite de crédito del cliente."""
        customer_instance = self.__customer_instance()
        if isinstance(customer_instance, VipClient):
            return customer_instance.__credit_limit
        return 0

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.__id,
            'dni': self.__dni,
            'first_name': self.__first_name,
            'last_name': self.__last_name,
            'customer_type': self.__customer_type,
            'discount': self.discount,
            'credit_limit': self.credit_limit,
        }


    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        """Entrada de diccionario y lo convierte en un objeto que representa este modelo"""
        return cls(
            id=data.get('id', -1),
            dni=data.get('dni', ''),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            customer_type=data.get('customer_type', 1),
            discount=data.get('discount', 0),
            credit_limit=data.get('credit_limit', 0),
        )

    def set_card(self, card: bool)-> None:
        customer_instance = self.__customer_instance()
        if isinstance(customer_instance, RegularClient):
            customer_instance.set_card(card)

