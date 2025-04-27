# models/invoice.py
from datetime import date
from typing import List, Dict, Any, Optional
from models.base import BaseModel
from models.invoiceDetail import InvoiceDetailModel

class InvoiceDetailsCollection:
    def __init__(self, invoice: 'InvoiceModel'): # type: ignore
        self.__invoice = invoice

    def add(self,product_id:int, product_name: str, sale_price: float, quantity: int) -> InvoiceDetailModel:
        new_detail = InvoiceDetailModel(
            product_id=product_id,
            product_name=product_name,
            sale_price=sale_price,
            quantity=quantity
        )
        self.__invoice._InvoiceModel_details.append(new_detail)
        self.__invoice._InvoiceModel__recalculate_totals()
        return new_detail

    def remove(self, detail_id: int) -> bool:
        return self.__invoice.remove_detail(detail_id)
    
