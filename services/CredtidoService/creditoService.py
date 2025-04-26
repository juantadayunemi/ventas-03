import datetime
import msvcrt 
from functools import reduce
import os
import time
from typing import Any, List
from colorama import Fore, Style
from prettytable import PrettyTable
from models.creditoSales import CreditSalesModel
from services.CredtidoService import creditoDTO
from services.Sales.salesDTO import Sale
from models.company import CompanyModel
from models.product import ProductModel
from helpers.utilities import clear_screen, green_color, reset_color_code, purple_color
from helpers.components import Valida
from helpers.jsonManager import JsonFile
from helpers.utilities import gotoxy, set_color
from interfaces.iCrud import ICrud
from env import ROOT_PATH


class CrudVentaCredito(ICrud):

    def __init__(self):
        self.__filename = os.path.join(ROOT_PATH, "files","ventasCredito.json")
        self.json_file = JsonFile(self.__filename)
        self.validar:Valida = Valida() 
          
    def create(self) ->None:
        ...
        # cabecera de la venta

        clear_screen()
        set_color(Fore.GREEN + Style.NORMAL)
        gotoxy(2,1);print("*"*90)
        gotoxy(30,2);print("Registro de cobro")
        gotoxy(17,3);print(CompanyModel.get_business_name())
      

        gotoxy(5,4) ;  print(f"N.Coobr#:")
        numFact=self.validar.solo_numeros("Err: Ingrese num fact.",15,4)
        

        gotoxy(30, 4) ;print(Fore.GREEN + Style.NORMAL + "Fecha (DD/MM/AAAA): ")
        fecha = self.validar.validar_fecha("Formato inválido", 50, 4)
  
        gotoxy(66,4);print(Fore.GREEN + Style.NORMAL+"Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Factura:")
     
        customer = None
        message = ""
        while not customer:
            print(Fore.WHITE)
            message = ""
            dni=self.validar.enter_data("Err: Ingrese cliente",25,6)
            if (dni.lower() == "x"):
                return
            
            gotoxy(23,6); print(" "*42)
            customer = self._find_client(dni)
            if not customer:
                message = "Proveedor no existe"
            elif (len (customer)> 1 ):
                message = f"Hay {len(customer)} clientes similares, Sé más especifico.."
           
            if len(message)> 0 :
                gotoxy(23,6);print(Fore.RED+ message)
                customer  = None
                time.sleep(1)
                gotoxy(23,6);print(len(message) * " ")
                continue

            customer = customer[0]
            break
        

       
        # CONVER TOCUSTOMER GENERCI
        self.customer:CreditSalesModel = customer
        
        supplier_name = f"{self.customer.id } {self.customer.num_factura}"  
        supplier_display = (supplier_name[:37]).strip()
        gotoxy(25,6);print(Fore.WHITE + supplier_display)

      
        purchase:creditoDTO.Credito =  creditoDTO.Credito(self.customer)
        # print header
        gotoxy(2,8);print(green_color+"_"*90 + reset_color_code) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("valor pago    ") 
  
   
        gotoxy(70,9);print("n->Terminar"+reset_color_code)
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line)

            # enter product
            search_product= self.validar.enter_data("Error: ingreSE VALOR DE PAGO",12,9+line)
            
            # id
            gotoxy(12,9+line);print("{:<5}".format(search_product))  
  
            purchase.add_detail(1, datetime.date.today(), float( search_product ))
         
            gotoxy(76,4);print(round(purchase.subtotal,2))
            gotoxy(76,5);print(round(purchase.discount,2))
            gotoxy(76,6);print(round(purchase.iva,2))
            gotoxy(76,7);print(round(purchase.total,2))
            gotoxy(74,9+line);follow=input() or "s"  
            gotoxy(76,9+line);print(green_color+"✔"+ reset_color_code)  
            line += 1

        # save process
        procesar =""
        while True:
        #    if self.customer.total_credito >  search_product> 0:
        #         print('')
           

            gotoxy(15,9+line);print ("\033[J")
            gotoxy(15,9+line+1);print(Fore.RED+"Esta seguro de grabar la comapra(s/n):")
            gotoxy(54,9+line+1);procesar = input().lower()
            if procesar not  in  ('s','n'):
                continue
            break

        if procesar == "s":
            gotoxy(15,12+line);print( Fore.BLUE + "Procesando ...")
            time.sleep(1)
            id = 1
            invoices = self.json_file.read()
            if len (invoices) >0:
                id = invoices[-1]["id"]+1
            data = purchase.getJson()
            data["id"]=id
            
            invoices.append(data)
            self.json_file.save(invoices)
            gotoxy(16,13+line);print( Fore.GREEN  + "😊 Compra Grabada satisfactoriamente"+reset_color_code)
        else:
            gotoxy(28,12+line);print("🤣 Compra Cancelada 🤣"+reset_color_code)    
        time.sleep(2)    
    

    def _find_client(self,search_term:str) ->List[Any]:
        """Busca un cliente según el criterio de búsqueda"""

        results: List[dict[str, Any]] = []

        if search_term.isdigit():
            if search_term.startswith("0"):
                results =  self.json_file.find("id", search_term)  # Búsqueda por cédula (Ecuador)
            elif len(search_term) <= 3:
                results =  self.json_file.find("id", int(search_term))   # Búsqueda por ID interno
            else:
                results  =  self.json_file.find("dni", search_term) # Búsqueda por cédula normal
        elif len(search_term):
            results =  self.json_file.search(["first_name", "last_name"], search_term) # x apellido y nombre
        else:
             results =  self.json_file.read()
       
        # convertir OBJETO
        customers: List[CreditSalesModel] = []

        for client_data in results:
            customer = CreditSalesModel(
                id = client_data.get('id', 1),
                num_factura=client_data.get('num_factura', ''),
                total_credito=client_data.get('total_credito', ''),
                saldo_credito=client_data.get('saldo_credito', ''),
                estado=client_data.get('estado', '') ,
                pagos=client_data.get('pagos', []) ,
                
            )
            customers.append(customer)
        
        return customers


    def update(self) ->None:
        ...
    
    def delete(self) -> None:
        ...

    def consult(self) ->None:

        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de compras"+" "*35+"██")
        gotoxy(2,4);invoice_num= input("Ingrese Factura: ")
        if invoice_num.isdigit():
            invoice_num = int(invoice_num)

            invoice = self.json_file.find("id",invoice_num)
                        
            # --- Imprimir cabecera de la factura ---
            if len(invoice) == 0 :
                print(Fore.RED + "No hay datos...")
                time.sleep(1)
                return
            invoice  = invoice[0]
            print("\n" + "=" * 50)
            print(f"FACTURA N°: {invoice['id']}".center(50))
            print("=" * 50)
            print(f"Fecha: {invoice['Fecha']}")
            print(f"Provee.: {invoice["ruc"]} {invoice['supplier_name']}")
         
            # --- Tabla de productos (detalle) ---
            table = PrettyTable()
            table.field_names = ["Producto", "Precio", "Cantidad", "Subtotal"]
            table.align["Producto"] = "l"  # Alinear a la izquierda
            table.align["Precio"] = "r"    # Alinear a la derecha
            table.align["Cantidad"] = "r"
            table.align["Subtotal"] = "r"

            for item in invoice['detail']:
                subtotal = item['sale_price'] * item['quantity']
                table.add_row([item['product_name'], f"${item['sale_price']:.2f}", item['quantity'], f"${subtotal:,.2f}"])

            print(table)

            # --- Totales ---
            print("\n" + "-" * 50)
            print(f"Subtotal: ${invoice['subtotal']:,.2f}".rjust(50))
            print(f"Descuento: -${invoice['descuento']:,.2f}".rjust(50))
            print(f"IVA (12%): ${invoice['iva']:,.2f}".rjust(50))
            print("=" * 50)
            print(f"TOTAL: ${invoice['total']:,.2f}".rjust(50).upper())
            print("=" * 50)

        else:    

            invoices = self.json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                print(
                    "{:<4} {:<12} {:<14} {:<25} {:>13,.2f}".format(  # Total alineado a la derecha (>)
                        fac['id'], 
                        fac['Fecha'],
                        fac['ruc'], 
                        fac['supplier_name'], 
                        fac['total']
                    )
                )

            suma = reduce(lambda total, invoice: round(total+ invoice["total"],2),invoices,0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))

            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            #print("filter cliente: ",total_client)
            #print(f"map Facturas:{totales_map}")
            print(f"            _____________________________________")
            print(f"              max Factura:{max_invoice:,.2f}")
            print(f"              min Factura:{min_invoice:,.2f}")
            print(f"              sum Factura:{tot_invoices:,.2f}")
            print(f"              reduce Facturas:{suma:,.2f}")
            print("")
        print(Fore.RED+ "Presione cualquier tecla para continuar...")
        msvcrt.getch()  
