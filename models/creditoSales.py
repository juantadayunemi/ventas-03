from typing import Any, List, Optional
from models.base import  BaseModel
from models.creditPayment import CreditPaymentModel

class CreditSalesModel(BaseModel):
    def __init__(self, invoice_number: int  = 0, total_credit: float = 0, 
                 credit_balance: float = 0, id: Optional[int] = None,
                 state: str = 'Pendiente', payments: List[CreditPaymentModel] = []):

        self.__id: int = id if id else -1
        self.__invoice_number: int = invoice_number
        self.__total_credit: float = total_credit
        self.__credit_balance: float = credit_balance
        self.__state : str = state 
        self.__payments: list[CreditPaymentModel] = payments


    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int) -> None:
        self.__id = value

    @property
    def invoice_number(self) -> int:
        return self.__invoice_number

    @invoice_number.setter
    def cabecera_venta(self, value:int) -> None:
        self.__invoice_number = value

    @property
    def total_credit(self) -> float:
        return self.__total_credit

    @total_credit.setter
    def total_credito(self, value: float) -> None:
        self.__total_credit = value

    @property
    def credit_balance(self) -> float:
        return self.__credit_balance

    @credit_balance.setter
    def saldo_credito(self, value: float) -> None:
        self.__credit_balance = value

    @property
    def state (self) -> str:
        return self.__state

    @state .setter
    def state (self, value: str) -> None:
        if not value in ('Pendiente','Parcial','Pagado'):
            raise ValueError("Opciones del estado incorrecto  validos(Pendiente, Parcial, Pagado)")
        
        self.__state  = value

    @property
    def payments(self) -> list[CreditPaymentModel]:
        return self.__payments

    @payments.setter
    def payments(self, value: list[CreditPaymentModel]) -> None:
        self.__payments = value



    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.__id,
            'invoice_number': self.__invoice_number,
            'total_credit': self.__total_credit,
            'credit_balance': self.__credit_balance,
            'state': self.__state,
            'payments': [pay.to_dict() for pay in self.__payments] if self.__payments else []
        }

    @classmethod
    def from_dict (cls, data: dict[str, Any]):
        return cls(
            id=data.get('id', 1),
            invoice_number=data.get('num_factura', ''),
            total_credit=data.get('total_credito', 0),
            credit_balance=data.get('saldo_credito', 0),
            state=data.get('estado', 'Pendiente'),
            payments=[CreditPaymentModel.from_dict(p) for p in data.get('pagos', [])]
        )

