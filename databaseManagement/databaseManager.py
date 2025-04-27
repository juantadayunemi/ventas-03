from typing import TypeVar, Generic
from databaseManagement.jsonReposit import JSONRepository
from env import ROOT_PATH
from models.company import CompanyModel
from models.creditPayment import CreditPaymentModel
from models.creditoSales import CreditSalesModel
from models.customer import CustomerModel
from models.invoice import InvoiceModel
from models.invoiceDetail import InvoiceDetailModel
from models.product import ProductModel

# Type variables for better type hints
T = TypeVar('T')
CreditSalesRepo = JSONRepository[CreditSalesModel]
ProductRepo = JSONRepository[ProductModel]
CompanyRepo = JSONRepository[CompanyModel]
CustomerRepo = JSONRepository[CustomerModel]
InvoiceRepo = JSONRepository[InvoiceModel]
InvoiceDetailRepo = JSONRepository[InvoiceDetailModel]
CreditPaymentRepo = JSONRepository[CreditPaymentModel]

class DataService :
    """Central database access point for all application entities"""
    
    def __init__(self) -> None:
        # Initialize all repositories with proper configuration
        self.__creditSales = JSONRepository(
            entity_class=CreditSalesModel,
            custom_path=ROOT_PATH,
            table_name='credit_sales'
        )
        
        self.__company = JSONRepository(
            entity_class=CompanyModel,
            custom_path=ROOT_PATH,
            table_name='companies'
        )
        
        self.__customer = JSONRepository(
            entity_class=CustomerModel,
            custom_path=ROOT_PATH,
            table_name='customers'
        )
        
        self.__invoice = JSONRepository(
            entity_class=InvoiceModel,
            custom_path=ROOT_PATH,
            table_name='invoices'
        )
        
        self.__invoiceDetail = JSONRepository(
            entity_class=InvoiceDetailModel,
            custom_path=ROOT_PATH,
            table_name='invoice_details',  # Fixed typo in table name
        )

        self.__creditPaymentDetail = JSONRepository(
                entity_class=CreditPaymentModel,
                custom_path=ROOT_PATH,
                table_name='payment_details'
            )
        
        self.__product = JSONRepository(
                entity_class=ProductModel,
                custom_path=ROOT_PATH,
                table_name='products'
            )

    @property
    def CreditSales(self) -> CreditSalesRepo:
        """Access to credit sales repository"""
        return self.__creditSales
    
    @property
    def Company(self) -> CompanyRepo:
        """Access to company repository"""
        return self.__company
    
    @property
    def Customer(self) -> CustomerRepo:
        """Access to customer repository"""
        return self.__customer
    
    @property
    def Product(self) -> ProductRepo: 
        """Access to payment detail repository"""
        return self.__product
    
    @property
    def Invoice(self) -> InvoiceRepo:
        """Access to invoice repository"""
        return self.__invoice
    
    @property
    def InvoiceDetail(self) -> InvoiceDetailRepo:
        """Access to invoice detail repository"""
        return self.__invoiceDetail

    @property
    def CreditPaymentDetail(self) -> CreditPaymentRepo: 
        """Access to payment detail repository"""
        return self.__creditPaymentDetail
    
    def initialize_database(self) -> None:
        """Initialize database structure if not exists"""
        # This ensures all directories are created
        for repo in [
            self.__creditSales,
            self.__company,
            self.__customer,
            self.__invoice,
            self.__invoiceDetail,
            self.__creditPaymentDetail,
            self.__product,

        ]:
            # Accessing base_path triggers directory creation
            _ = repo.base_path