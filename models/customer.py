from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union


class Client(ABC):

    def __init__(self,
                first_name:str = "Consumidor",
                last_name:str = "Final",
                dni:str = "9999999999999",
                type:Optional[int]=1,
                id:int = 1):
        
        # Método constructor para inicializar los atributos de la clase Cliente
        self.first_name:str = first_name
        self.last_name:str = last_name
        self.__dni:str = dni 
        self.__id:int = id
        self.__type:int = type  # type: ignore 
                    
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
  

    def __str__(self) -> str:
        # Método especial para representar la clase Cliente como una cadena
        return f'Cliente: {self.__dni} | {self.fullName}'  
    
    @property
    def fullName(self)-> str:
        return self.first_name + ' ' + self.last_name
    
    @property
    def type(self) -> int:
        return self.__type
    
    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, value:int ) ->None:
        self.__id = value

     
    @property  
    @abstractmethod
    def discount(self) -> float:
        pass
    
    @property
    @abstractmethod
    def credit_limit(self) -> int:
        pass

    def show(self) -> None:
        # Método para imprimir los detalles del cliente en la consola
        print('   Nombres    Dni')
        print(f'{self.fullName}  {self.dni}')    





class RegularClient(Client):
    def __init__(self,
                first_name:str="Consumidor",
                last_name:str="Final",
                dni:str="9999999999",
                card=False):
        
        self.__card = card
        super().__init__(first_name, last_name, dni)  
            
    def __str__(self):
        # Método especial para representar la clase RetailClient como una cadena
        return f'Client: {self.fullName} Descuento:{self.discount * 100} %'
      
    def show(self)->None:
        # Método para imprimir los detalles del cliente minorista en la consola
        print(f'Cliente Minorista: DNI:{self.dni} Nombre:{self.first_name} {self.last_name} Descuento:{self.discount*100}%')     

    def getJson(self) -> Dict[str, Any]:
        # Método para imprimir los detalles del cliente minorista en la consola
        return {"dni":self.dni,"nombre":self.first_name,"apellido":self.last_name,"valor": self.discount}
    
    @property
    def credit_limit(self) -> int:
        return 0
    
     
    def set_card(self, value : bool) -> None:
        self.__card = value

    @property
    def discount(self) -> float:
        """10 % de descuento si tiene tarjeta."""
        return 0.1 if self.__card else 0
    


class VipClient(Client):
    def __init__(self, 
                first_name:str="Consumidor",
                last_name:str="Final",
                dni:str="9999999999"):
        
        # Método constructor para inicializar los atributos de la clase VipClient
        super().__init__(first_name, last_name, dni)  
        self.__limit:int = 10000  # Límite de crédito del cliente VIP
              
    @property
    def limit(self)-> int:
        return self.__limit
    
    @property
    def credit_limit(self)-> int:
        return self.__limit
    
    @property
    def discount(self)-> float:
        return 0
    
    
    @limit.setter
    def limit(self, value)-> None:
        self.__limit = 10000 if (value < 10000 or value > 20000) else value 
  
    def __str__(self) -> str:
        # Método especial para representar la clase VipClient como una cadena
        return f'Cliente: {self.fullName} Cupo: {self.limit}'
            
    def show(self)-> None:
        # Método para imprimir los detalles del cliente VIP en la consola
        print(f'Cliente Vip: DNI:{self.dni} Nombre: {self.first_name} {self.last_name} Cupo: {self.limit}')     
        
    def getJson(self) ->dict[str, Any]:
        # Método para imprimir los detalles del cliente VIP en la consola
        return {"dni":self.dni,"nombre":self.first_name,"apellido":self.last_name,"valor": self.limit}


class GenericCustomer(Client):

    def __init__(self, dni: str, first_name: str, last_name: str, customer_type: int, id:int = 1) -> None:
        self.__dni:str = dni
        self.first_name:str = first_name 
        self.last_name:str = last_name
        self.__type:int = customer_type  

        self.__instance:Union[RegularClient, VipClient, None] = None

        # Validation data
        if not isinstance(customer_type, int) or customer_type not in (1, 2):
            raise ValueError('customer_type debe ser 1 (Regular) o 2 (Vip)')
        
        if not isinstance(dni, str) or len( dni) == 0:
            raise ValueError('DNI debe ser de tipo texto y no vacío')
        
        if not isinstance(first_name, str) or len( first_name) == 0:
            raise ValueError('APELLIDO debe ser de tipo texto y no vacío')
        
        if not isinstance(last_name, str) or len( last_name) == 0:
            raise ValueError('NOMBRE debe ser de tipo texto y no vacío')
        
        super().__init__(dni= dni, first_name= first_name, last_name=last_name, type = customer_type, id= id)

    @property
    def id (self)-> int:
        return super().id
    
    @id.setter
    def id (self, value)-> None:
        super().id =  value



    
    @property
    def dni (self)-> str:
        return self.__dni
    
    @dni.setter
    def dni(self, value:str)-> None:
        super().dni = value
        self.__dni = value

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
            return customer_instance.limit
        return 0


    def set_card(self, card: bool)-> None:
        customer_instance = self.__customer_instance()
        if isinstance(customer_instance, RegularClient):
            customer_instance.set_card(card)

