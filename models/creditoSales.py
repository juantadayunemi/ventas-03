from datetime import date
from typing import Any, List, Optional

from flask.cli import routes_command
from models.base import  BaseModel
from models.creditPayment import CreditPaymentModel
from models.creditPaymentsCollection import CreditPaymentsCollection

class CreditSalesModel(BaseModel):
    def __init__(self, invoice_id:int, date_credit:date ,dni:str, full_name:str, total_credit:float , 
                 credit_balance:float = -1, id: Optional[int] = None,
                 state: str = 'Pendiente', payments: List[CreditPaymentModel] = []):

        self.__id: int = id if id else -1
        self.__invoice_id: int = invoice_id
        self.__date_credit: date = date_credit
        self.__dni: str = dni
        self.__full_name: str = full_name
        self.__total_credit: float =round(total_credit,2)
        self.__credit_balance: float = round(total_credit,2) if  credit_balance ==-1  else round(credit_balance,2)
        self.__total_pay  = 0
        self.__state : str = state 
        self.__payments: list[CreditPaymentModel] = payments


    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int) -> None:
        self.__id = value

    @property
    def invoice_id(self) -> int:
        return self.__invoice_id

    @invoice_id.setter
    def invoice_id(self, value:int) -> None:
        self.__invoice_id = value

    @property
    def total_credit(self) -> float:
        return self.__total_credit

    @total_credit.setter
    def total_credit(self, value: float) -> None:
        self.__total_credit = value

    @property
    def credit_balance(self) -> float:
        return self.__credit_balance

    @credit_balance.setter
    def credit_balance(self, value: float) -> None:
        self.__credit_balance = value

    @property
    def state (self) -> str:
        return self.__state

    @property
    def payments(self) -> list[CreditPaymentModel]:
        return self.__payments

    @payments.setter
    def payments(self, value: list[CreditPaymentModel]) -> None:
        self.__payments = value

    @property
    def full_name(self) ->str:
        return self.__full_name
    
    @property
    def dni(self) ->str:
        return self.__dni
    
    @property
    def date_credit(self) ->date:
        return self.__date_credit
    
    @date_credit.setter
    def date_credit(self, value) ->None:
        self.__date_credit = value

    def add_detail(self, date_pay: date, value_pay: float) -> CreditPaymentModel:
        """Agrega un nuevo item al detalle de pagos sin id"""
        new_detail = CreditPaymentModel(
            date_pay=date_pay,
            value_pay=value_pay,
            # No pasamos id, se generará automáticamente
        )
        self.__payments.append(new_detail)
        self.__recalculate_totals()
        return new_detail

    def remove_detail(self, detail_id: int) -> bool:
        """Elimina un item del detalle por su ID"""
        for i, detail in enumerate(self.__payments):
            if detail.id == detail_id:
                self.__payments.pop(i)
                self.__recalculate_totals()  # actualizamos los totales
                return True
        return False

    def __recalculate_totals(self):
        """Recalcula automáticamente total deuda y total pendiente"""
        self.__total_pay = round( sum(detail.value_pay for detail in self.__payments) ,2)
        
        if self.__total_pay > self.__total_credit:
            raise ValueError(
                f"Error: Los pagos (${self.__total_pay:.2f}) "
                f"superan el crédito (${self.__total_credit:.2f})."
            )
        
        self.__credit_balance = round(self.__total_credit - self.__total_pay,2)
        self.__state = "Pagado" if self.__total_credit == self.__total_pay else "Parcial" if   self.__total_pay > 0 else "Pendiente"


    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.__id,
            'invoice_id': self.__invoice_id,
            'date_credit': self.__date_credit,
            'dni': self.__dni,
            'full_name': self.__full_name,
            'total_credit': self.__total_credit,
            'credit_balance': self.__credit_balance,
            'state': self.__state,
            'payments': [pay.to_dict() for pay in self.__payments] if self.__payments else []
        }

    @classmethod
    def from_dict (cls, data: dict[str, Any]):
        return cls(
            id=data.get('id', 1),
            dni=data.get('dni', ''),
            full_name=data.get('full_name', ''),
            invoice_id=data.get('invoice_id', ''),
            date_credit=data.get('date_credit', date.today()),
            total_credit=data.get('total_credit', 0),
            credit_balance=data.get('credit_balance', 0),
            state=data.get('state', 'Pendiente'),
            payments=[CreditPaymentModel.from_dict(p) for p in data.get('payments', [])]
        )

    @property
    def payments_collection(self) -> CreditPaymentsCollection:
        return CreditPaymentsCollection(self)