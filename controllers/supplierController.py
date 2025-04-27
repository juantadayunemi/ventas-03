from databaseManagement.databaseManager import DataService
from helpers.components import Valida
from interfaces.iCrud  import ICrud

class SupplierController(ICrud):
    def __init__(self, data_base: DataService):
        self.data_base = data_base
        self.validar:Valida = Valida() 

 
    def create(self):
        ...

    def update(self):
        pass

    def delete(self):
        pass

    def consult(self):
        pass