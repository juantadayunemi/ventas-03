from typing import Any

from models.base import BaseModel

class CompanyModel(BaseModel):
    def __init__(self, ruc:str, company_name: str, id:int = 1) -> None:
        self.__id: int = id
        self.__ruc: str = ruc
        self.__company_name: str = company_name

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.__id,
            'ruc': self.__ruc,
            'company_name': self.__company_name,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        """Entrada de diccionario y lo convierte en un objeto que representa este modelo"""
        return cls(
            id=data.get('id', 1),
            ruc=data.get('ruc', ''),
            company_name=data.get('company_name', ''),
        )
    
    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int) -> None:
        self.__id = value

    @property
    def ruc(self) -> str:
        return self.__ruc

    @ruc.setter
    def ruc(self, value: str) -> None:
        self.__ruc = value

    @property
    def company_name(self) -> str:
        return self.__company_name

    @company_name.setter
    def company_name(self, value: str) -> None:
        self.__company_name = value

    @property
    def getJson(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "company_name": self.company_name
        }

    
    def get_business_data(self) -> dict[str, Any]:
        """Versión como método que retorna diccionario"""
        return {
            "ruc": self.ruc,
            "company_name": self.company_name
        }
    
    @staticmethod
    def get_business_name() -> str:
        return f"Empresa:Corporación el Rosado  Ruc:0876543294001"
