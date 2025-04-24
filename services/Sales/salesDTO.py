from typing import Any, Dict, List
from services.Sales.calculos import Icalculo
from datetime import date
from models.customer import  GenericCustomer
from models.product import Product

class SaleDetail:
    _line=0
    def __init__(self,product:Product, quantity:float = 0):
        SaleDetail._line += 1
        self.__id:int = SaleDetail._line
        self.product: Product = product
        self.sale_price:float = product.sale_price
        self.quantity:float = quantity
    
    @property
    def id(self) -> int:
        # Getter para obtener el valor del límite de crédito del cliente VIP
        return self.__id
    
    def __repr__(self):
        # Método especial para representar la clase Cliente como una cadena
        return f'{self.id} {self.product.product_name} {self.sale_price} {self.quantity}'  
        
class Sale(Icalculo):
    next:int = 0
    FACTOR_IVA:float = 0.12

    def __init__(self,client :GenericCustomer):
        Sale.next += 1
        self.__invoice:int = Sale.next
        self.date = date.today()
        self.customer:GenericCustomer = client
        self.subtotal:float = 0
        self.percentage_discount:float = client.discount 
        self.discount : float = 0
        self.iva:float = 0 
        self.total:float = 0
        self.sale_detail:List[SaleDetail]= []
    
    @property
    def invoice(self) ->int:
        # Getter para obtener el valor del límite de crédito del cliente VIP
        return self.__invoice
    
    def __repr__(self):
        # Método especial para representar la clase Cliente como una cadena
        return f'Factura# {self.invoice} {self.date} {self.customer.fullName} {self.total}'  
    
    def cal_iva(self,iva:float=0.12,valor:float=0) ->float:
        return round(valor*iva,2)
    
    def cal_discount(self,valor:float=0,discount:float=0)->float:
        return valor * discount
    
    def add_detail(self,prod:Product, qty:float)->None:
        # composicion entre detventa y venta
        detail = SaleDetail(prod,qty)
        self.subtotal += round(detail.sale_price* detail.quantity,2)
        # self.discount = self.subtotal*self.percentage_discount
        self.discount = self.cal_discount(self.subtotal,self.percentage_discount)     
        # self.iva = round((self.subtotal-self.discount)*Sale.FACTOR_IVA,2)
        self.iva = self.cal_iva(Sale.FACTOR_IVA,self.subtotal-self.discount)
        self.total = round(self.subtotal+self.iva-self.discount,2)
        self.sale_detail.append(detail)  

    def getJson(self)->Dict[str, Any]:
        # Método especial para representar la clase venta como diccionario
        pay="No definido"
        if ( self.get_customer_type ==1 and self.discount> 0) : 
            pay = "Tarjeta"
        elif (self.get_customer_type ==1 and self.discount ==0):   
            pay = "Efectivo"
        elif (self.get_customer_type ==2):
            pay = "Credito"
        
        invoice= {"id":self.invoice,
                "Fecha":self.date.strftime("%Y-%m-%d"),
                "dni": self.customer.dni ,
                "fullName": self.customer.fullName,
                "pay" : pay,
                "subtotal":self.subtotal,
                "descuento": self.discount,
                "iva": self.iva,
                "total": self.total,
                "detail":[]}
                
        for det in self.sale_detail:
            invoice["detail"].append(
                {
                "id":det.product.id,
                "product_name":det.product.product_name,
                "sale_price": det.sale_price,
                "quantity": det.quantity
                }
            )  
        return invoice
    
    @property
    def get_customer_type (self) ->int:
        return self.customer.customer_type
    
    @property
    def get_credit_limit (self) ->float:
        return self.customer.credit_limit

    
