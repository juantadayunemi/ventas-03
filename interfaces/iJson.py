from abc import ABC, abstractmethod
from typing import Any, List, Union

class iJson(ABC):
    @abstractmethod
    def save(self, data:List[dict]):
        ...

    @abstractmethod
    def read(self)->List[Any]:
        ...
 
    @abstractmethod
    def update(self, data:List[dict]):
        ...

    @abstractmethod
    def find(self, atributo: str, buscado: Any) -> List[dict]:
        ...

    @abstractmethod
    def delete(self, ids: Union[int, List[int]]) -> int:
        ...
        
    @abstractmethod
    def search(self, fields: Union[str, List[str]], sought: Any, exact_match: bool = False) -> List[dict]:
        ...