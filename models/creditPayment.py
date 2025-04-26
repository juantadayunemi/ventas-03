from datetime import date
from typing import Any, Optional

from models.base import BaseModel


class CreditPaymentModel(BaseModel):

    def __init__(self, date_pay: date = date.today(), value_pay: float = 0, id: Optional[int] = None) -> None:
        self.__date_pay: date = date_pay
        self.__id: int = id if id else -1
        self.__value_pay: float = value_pay

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.__id,
            'date_pay': self.__date_pay.isoformat(),  # convert date a string
            'value_pay': self.__value_pay
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        return cls(
            id=data.get('id',0),
            date_pay=date.fromisoformat(data['date_pay']),  # convert string a date
            value_pay=data.get('value_pay', 0.0)
        )
    
    @property
    def id(self) -> int:
        return self.__id
        
    @id.setter
    def id(self, value: int) -> None:
        self.__id = value

    @property
    def date_pay(self) -> date:
        return self.__date_pay
        
    @date_pay.setter
    def date_pay(self, value: date) -> None:
        self.__date_pay = value

    @property
    def value_pay(self) -> float:
        return self.__value_pay

    @value_pay.setter
    def value_pay(self, value: float) -> None:
        self.__value_pay = value

 
   