from abc import ABC, abstractmethod

class ICrud(ABC):
 
    @abstractmethod    
    def create(sef):
        pass
    @abstractmethod   
    def update(sef):
        pass
    @abstractmethod 
    def delete(sef):
        pass
    @abstractmethod 
    def consult(sef):
        pass
    
