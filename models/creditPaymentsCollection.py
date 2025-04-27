from datetime import date
from models.creditPayment import CreditPaymentModel

class CreditPaymentsCollection:
    def __init__(self, credit_sales: 'CreditSalesModel'):  # type: ignore
        self.__credit_sales = credit_sales

    def add(self, date_pay: date, value_pay: float) -> CreditPaymentModel:
        # Validar que el pago no exceda el saldo pendiente
        if value_pay > self.__credit_sales.credit_balance:
            raise ValueError(f"El pago excede el saldo pendiente (${self.__credit_sales.credit_balance:.2f})")
        
        # Usar métodos públicos en lugar de acceder a atributos privados
        new_payment = self.__credit_sales.add_detail(date_pay, value_pay)
        return new_payment

    def remove(self, detail_id: int) -> bool:
        return self.__credit_sales.remove_detail(detail_id)
    
    