from typing import Any, Optional
from models.base import BaseModel
from models.invoiceDetail import InvoiceDetailModel
from datetime import date

from models.invoiceDetailsCollection import InvoiceDetailsCollection

class InvoiceModel(BaseModel):
    """Modelo principal para facturas"""
    TAX_PERCENT = 0.15
    def __init__(self, 
                 dni: str, 
                 full_name: str,  
                 payment_method: str, 
                 discount_percentage:float,
                 subtotal: float = 0, 
                 discount: float = 0,  
                 tax: float =-1, 
                 total: float = 0,
                 details: list[InvoiceDetailModel] = [],
                 date_sales: Optional[date] = None,  
                 id: Optional[int] = None):
        
        self.__id: int = id if id is not None else -1  # Más explícito
        self.__date_sales: date = date_sales if date_sales else date.today()
        self.__dni: str = dni
        self.__full_name: str = full_name
        self.__payment_method = payment_method
        self.__discount_percentage = discount_percentage
        self.__subtotal: float = subtotal
        self.__discount: float = discount
        self.__tax: float = total * InvoiceModel.TAX_PERCENT  if  tax  == -1  else  tax
        self.__total: float = total
        self.__details: list[InvoiceDetailModel] = details if details is not None else []

    # Properties
    @property
    def id(self) ->int:
        return self.__id

    @id.setter
    def id(self, value:int) -> None:
        self.__id = value

    @property
    def date_sales(self) -> date:
        return self.__date_sales

    @date_sales.setter
    def date_sales(self, value: date) -> None:  # Nombre consistente
        if not isinstance(value, date):
            raise ValueError("La fecha debe ser del tipo date")
        self.__date_sales = value

    @property
    def dni(self) -> str:
        return self.__dni

    @dni.setter
    def dni(self, value: str) -> None:
        if not value.strip():
            raise ValueError("El DNI no puede estar vacío")
        self.__dni = value

    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        if not value.strip():
            raise ValueError("El nombre completo no puede estar vacío")
        self.__full_name = value

    @property
    def payment_method(self) -> str:
        return self.__payment_method

    @property
    def subtotal(self) -> float:
        return self.__subtotal

    @subtotal.setter
    def subtotal(self, value: float) -> None:
        if value < 0:
            raise ValueError("El subtotal no puede ser negativo")
        self.__subtotal = value


    @property
    def discount_percentage(self) -> float:
        return self.__discount_percentage

    @discount_percentage.setter
    def discount_percentage(self, value: float) -> None:
        if value < 0:
            raise ValueError("El descuento no puede ser negativo")
        self.__discount_percentage = value

    @property
    def discount(self) -> float:
        return self.__discount

    @discount.setter
    def discount(self, value: float) -> None:
        if value < 0:
            raise ValueError("El descuento no puede ser negativo")
        self.__discount = value

    @property
    def tax(self) -> float:
        return self.__tax

    @tax.setter
    def tax(self, value: float) -> None:
        if value < 0:
            raise ValueError("El impuesto no puede ser negativo")
        self.__tax = value

    @property
    def total(self) -> float:
        return self.__total

    @total.setter
    def total(self, value: float) -> None:
        if value < 0:
            raise ValueError("El total no puede ser negativo")
        self.__total = value

    @property
    def details(self) -> list[InvoiceDetailModel]:
        return self.__details

    @details.setter
    def details(self, value: list[InvoiceDetailModel]) -> None:
        if not all(isinstance(item, InvoiceDetailModel) for item in value):
            raise ValueError("Todos los items deben ser de tipo InvoiceDetailModel")
        self.__details = value

    def add_detail(self, product_id:int,product_name: str, sale_price: float, quantity: int) -> InvoiceDetailModel:
        """Agrega un nuevo item al detalle de la factura con ID autoincremental"""
        new_detail = InvoiceDetailModel(
            product_id=product_id,
            product_name=product_name,
            sale_price=sale_price,
            quantity=quantity
            # No pasamos id, se generará automáticamente
        )
        self.__details.append(new_detail)
        self.__recalculate_totals()
        return new_detail

    def remove_detail(self, detail_id: int) -> bool:
        """Elimina un item del detalle por su ID"""
        for i, detail in enumerate(self.__details):
            if detail.id == detail_id:
                self.__details.pop(i)
                self.__recalculate_totals()  # Actualizamos los totales
                return True
        return False

    def __recalculate_totals(self):
        """Recalcula automáticamente subtotal, impuestos y total"""
        self.__subtotal = round(sum(detail.subtotal for detail in self.__details),2)

        self.__discount =  round(self.__subtotal  * self.__discount_percentage,2)

        self.__tax = round((self.__subtotal - self.__discount ) * InvoiceModel.TAX_PERCENT, 2)
        # Aquí puedes agregar lógica para calcular descuentos e impuestos
        self.__total =  round( (self.__subtotal - self.__discount ) + self.__tax, 2)

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.__id,
            'date_sales': self.__date_sales.isoformat(),
            'dni': self.__dni,
            'full_name': self.__full_name,
            'payment_method': self.__payment_method,
            'discount_percentage': self.__discount_percentage,
            'subtotal': self.__subtotal,
            'discount': self.__discount,
            'tax': self.__tax,
            'total': self.__total,  
            'details': [detail.to_dict() for detail in self.__details]
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        return cls(
            id=data.get('id'),
            date_sales=data.get('date_sales', ''),
            dni=data.get('dni', ''),
            full_name=data.get('full_name', ''),
            payment_method=data.get('payment_method', ''),
            discount_percentage=data.get('discount_percentage', 0),
            subtotal=data.get('subtotal', 0.0),
            discount=data.get('discount', 0.0),
            tax=data.get('tax', 0.0),
            total=data.get('total', 0.0),
            details=[InvoiceDetailModel.from_dict(d) for d in data.get('details', [])]
        )

    def validate_totals(self) -> bool:
        """Valida que los cálculos sean consistentes"""
        calculated_subtotal = sum(detail.subtotal for detail in self.__details)

        calculated_total = calculated_subtotal - self.__discount + self.__tax
        
        return (
            abs(calculated_subtotal - self.__subtotal) < 0.01 and
            abs(calculated_total - self.__total) < 0.01
        )
   
    @property
    def details_collection(self) -> InvoiceDetailsCollection:
        return InvoiceDetailsCollection(self)