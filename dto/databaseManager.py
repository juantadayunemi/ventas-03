from typing import TypeVar, Generic
from dto.jsonReposit import JSONRepository
from env import ROOT_PATH
from models.company import CompanyModel
from models.creditoSales import CreditSalesModel
from models.customer import CustomerModel
from models.invoice import InvoiceModel
from models.invoiceDetail import InvoiceDetailModel

# Type variables for better type hints
T = TypeVar('T')
CreditSalesRepo = JSONRepository[CreditSalesModel]
CompanyRepo = JSONRepository[CompanyModel]
CustomerRepo = JSONRepository[CustomerModel]
InvoiceRepo = JSONRepository[InvoiceModel]
InvoiceDetailRepo = JSONRepository[InvoiceDetailModel]

class db:
    """Central database access point for all application entities"""
    
    def __init__(self) -> None:
        # Initialize all repositories with proper configuration
        self.__creditSales = JSONRepository(
            entity_class=CreditSalesModel,
            custom_path=ROOT_PATH,
            table_name='credit_sales',
            single_file=True
        )
        
        self.__company = JSONRepository(
            entity_class=CompanyModel,
            custom_path=ROOT_PATH,
            table_name='companies',
            single_file=True
        )
        
        self.__customer = JSONRepository(
            entity_class=CustomerModel,
            custom_path=ROOT_PATH,
            table_name='customers',
            single_file=True
        )
        
        self.__invoice = JSONRepository(
            entity_class=InvoiceModel,
            custom_path=ROOT_PATH,
            table_name='invoices',
            single_file=True
        )
        
        self.__invoiceDetail = JSONRepository(
            entity_class=InvoiceDetailModel,
            custom_path=ROOT_PATH,
            table_name='invoice_details',  # Fixed typo in table name
            single_file=False  # Details are stored within invoices
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
    def Invoice(self) -> InvoiceRepo:
        """Access to invoice repository"""
        return self.__invoice
    
    @property
    def InvoiceDetail(self) -> InvoiceDetailRepo:
        """Access to invoice detail repository"""
        return self.__invoiceDetail

    def initialize_database(self) -> None:
        """Initialize database structure if not exists"""
        # This ensures all directories are created
        for repo in [
            self.__creditSales,
            self.__company,
            self.__customer,
            self.__invoice,
            self.__invoiceDetail
        ]:
            # Accessing base_path triggers directory creation
            _ = repo.base_path