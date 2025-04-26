from typing import Any, Dict, List
from models.creditoSales import CreditSalesModel
from models.creditPayment import CreditPaymentModel
from services.Sales import salesDTO
from services.Sales.calculos import Icalculo
from datetime import date
from models.product import ProductModel

class CreditoDetail:
    _line=0
    def __init__(self,product:CreditSalesModel, sale_price:float = 0):
        CreditoDetail._line += 1
        self.__id:int = CreditoDetail._line
        self.product: CreditSalesModel = product
        self.sale_price:float =0
        self.quantity:float = 0
    
    @property
    def id(self) -> int:
        # Getter para obtener el valor del límite de crédito del cliente VIP
        return self.__id
    

        
class Credito(Icalculo):
    next:int = 0
    FACTOR_IVA:float = 0.12

    def __init__(self,client :CreditSalesModel):
        Credito.next += 1
        self.__invoice:int = Credito.next
        self.date = date.today()
        self.creditoVenta:CreditSalesModel = client
        self.subtotal:float = 0
        self.percentage_discount:float =0
        self.discount : float = 0
        self.iva:float = 0 
        self.total:float = 0
        self.sale_detail:List[CreditPaymentModel]= []
    
    @property
    def invoice(self) ->int:
        # Getter para obtener el valor del límite de crédito del cliente VIP
        return self.__invoice

    def cal_iva(self,iva:float=0.12,valor:float=0) ->float:
        return round(valor*iva,2)
    
    def cal_discount(self,valor:float=0,discount:float=0)->float:
        return valor * discount

    def add_detail(self,id:int, feha_pago,  valor:float)->None:
        # composicion entre detventa y venta
        detail = CreditPaymentModel(id, fecha_pago= feha_pago, valor=valor )

        

        self.total = round(self.subtotal+self.iva-self.discount,2)
        self.sale_detail.append(detail)  
    def getJson(self)->Dict[str, Any]:
        # Método especial para representar la clase venta como diccionario
        invoice= {
              "id":self.invoice,
                "num_factura ":self.creditoVenta.num_factura,
                "total_credito ": self.creditoVenta.total_credito,
                "saldo_credito  ": self.creditoVenta.saldo_credito ,
                "estado  ": self.creditoVenta.estado ,
                "pagos":[]}
                
        for det in self.sale_detail:
            invoice["pagos"].append(
                {
                "id":det.id,
                "fecha_pago":det.fecha_pago,
                "valor ": det.valor ,
                }
            )  
        return invoice
    
