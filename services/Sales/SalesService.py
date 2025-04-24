import datetime
import msvcrt 
from functools import reduce
import os
import time
from typing import Optional
from colorama import Fore, Style
from services.Customers.CustomersService import CrudCustomer
from services.Products.ProductService import CrudProduct
from services.Sales.salesDTO import Sale
from models.company import Company
from models.customer import GenericCustomer, RegularClient
from models.product import Product
from helpers.utilities import clear_screen,blue_color, green_color, reset_color_code, purple_color
from helpers.components import Menu,Valida
from helpers.jsonManager import JsonFile
from helpers.utilities import gotoxy, set_color
from interfaces.iCrud import ICrud
from env import ROOT_PATH
from prettytable import PrettyTable 

class CrudSales(ICrud):

    def __init__(self):
        self.__filename = os.path.join(ROOT_PATH, "files","invoices.json")
        self.json_file = JsonFile(self.__filename)
        self.validar:Valida = Valida() 
    
        self.product_service:CrudProduct = CrudProduct()
        self.customer_service:CrudCustomer = CrudCustomer()
        self.customer: GenericCustomer

    def create(self) ->None:
        # cabecera de la venta
        fecha_formateada = datetime.datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
        clear_screen()
        set_color(Fore.GREEN + Style.NORMAL)
        gotoxy(2,1);print("*"*90)
        gotoxy(30,2);print("Registro de Venta")
        gotoxy(17,3);print(Company.get_business_name)
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{fecha_formateada}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
     
        customer = None
        message = ""
        while not customer:
            print(Fore.WHITE)
            message = ""
            dni=self.validar.enter_data("Err: Ingrese cliente",23,6)
            if (dni.lower() == "x"):
                return
            
            gotoxy(23,6); print(" "*42)
            customer = self.customer_service._find_client(dni)
            if not customer:
                message = "Cliente no existe"
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
        self.customer:GenericCustomer = customer
      
        gotoxy(23,6);print(Fore.WHITE + self.customer.dni + "  " + self.customer.fullName)

        if (self.customer.customer_type == 1 ):
            while True:
                gotoxy(5,7)
                message = "Forma de pago: (1)Efectivo, (2)Tarjeta:"
                print(Fore.GREEN + Style.NORMAL + message)
                gotoxy(5 + len(message),7)
                reponse = input (Fore.WHITE)
                gotoxy(5,7)
                print((len(message) + 10) * " ")

                if reponse in ('1','2'):
                    self.customer.set_card(reponse == '2')
                    gotoxy(8,7);print(Fore.GREEN + Style.NORMAL + "Forma de pago:")
                    gotoxy(23,7);print(Fore.WHITE + f"Tarjeta {self.customer.discount *100}% descuento" if reponse == '2' else  Fore.WHITE + "Contado  (sin descuento)")
                    break
        else : 
            gotoxy(8,7);print(Fore.GREEN + Style.NORMAL + "Forma de pago:")
            gotoxy(23,7);print(Fore.WHITE + f"Crédito: (monto máximo $ {self.customer.credit_limit})")
             

        sale = Sale(self.customer)
        # print header
        gotoxy(2,8);print(green_color+"_"*90 + reset_color_code) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id") 
        gotoxy(17,9);print("Producto") 
        gotoxy(42,9);print("Precio") 
        gotoxy(51,9);print("Cantidad") 
        gotoxy(60,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar"+reset_color_code)
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line)

            search_product= self.validar.enter_data("Error: ingrese dato..",12,9+line)
          
            prods =  self.product_service._find_product(search_product)
            message = ""
            if not prods:
                gotoxy(12,9+line);print(Fore.RED + "✗ No existe"); time.sleep(1); gotoxy(12,9+line);print(Fore.WHITE+"\033[0J")
                continue

            if len(prods)>1:
                gotoxy(12,9+line);print(Fore.RED +"↳ hay Varios"); time.sleep(1); gotoxy(12,9+line);print(Fore.WHITE + "\033[0J")
                continue
            else:    
                prods = prods[0]
                product = Product( id=  prods.id, product_name = prods.product_name , sale_price =  prods.sale_price , stock = prods.stock)
                # id
                gotoxy(12,9+line);print("{:<5}".format(product.id))  

                gotoxy(17,9+line);print(product.product_name)   # nombre del producto
                gotoxy(40,9+line);print("\033[0J")
                gotoxy(42,9+line);print("{:>7}".format( f"{product.sale_price:.2f}"))     # precio de vwnta
              
                # cantidad
                gotoxy(55,9+line)
                qyt=int(self.validar.solo_numeros("Error:Solo numeros",55,9+line))
                gotoxy(51,9+line);print("\033[0J")
                gotoxy(51,9+line);print("{:>8}".format(qyt))

                gotoxy(61,9+line);print("{:>8}".format(f"{product.sale_price*qyt:.2f}"))
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+ reset_color_code)  
                line += 1

        # save process
        procesar =""
        while True:
            gotoxy(15,9+line);print ("\033[J")
            gotoxy(15,9+line+1);print(Fore.RED+"Esta seguro de grabar la venta(s/n):")
            gotoxy(54,9+line+1);procesar = input().lower()
            if procesar not  in  ('s','n'):
                continue
            if procesar =="s" and sale.get_customer_type == 2 and sale.total >  sale.get_credit_limit:
                gotoxy(15,9+line + 3); 
                gotoxy(15, 9 + line + 3)
                print("El cliente VIP tiene un límite de ${:,.2f}.".format(sale.get_credit_limit))

                gotoxy(15, 9 + line + 4)
                print("No se puede guardar la venta.")

                time.sleep(3)
                gotoxy(15,9+line+3);print ("\033[J")
                continue
            break
       


        if procesar == "s":
            gotoxy(15,12+line);print( Fore.BLUE + "Procesando ...")
            time.sleep(1)
            id = 1
            invoices = self.json_file.read()
            if len (invoices) >0:
                id = invoices[-1]["id"]+1
            data = sale.getJson()
            data["id"]=id
            
            invoices.append(data)
            self.json_file.save(invoices)
            gotoxy(16,13+line);print( Fore.GREEN  + "😊 Venta Grabada satisfactoriamente"+reset_color_code)
        else:
            gotoxy(28,12+line);print("🤣 Venta Cancelada 🤣"+reset_color_code)    
        time.sleep(2)    
    
    def update(self) ->None:
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Actualización de facturas"+" "*28+"██")
        gotoxy(2,4)
        invoice_num= input("Igrese el N° de factura a moficar: ")
        gotoxy(2,5)
        print( Fore.RED + "A un no disponible en esta versión:")
        time.sleep(2)
    
    def delete(self) -> None:

        print('\033c', end='')
        gotoxy(2,1);print(Fore.RED+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Eliminar de Venta"+" "*35+"██")
     
        invoice = None
        while True:
            gotoxy(2,4)
            print('\033[0J', end='')
            invoice_num= input("Ingrese el N° de factura a eliminar o (x) para salir: ").lower()
            if invoice_num == "x":
                return
            if not invoice_num.isdigit() : 
               continue
            
            invoice = self.json_file.find("id", int( invoice_num))

            if len(invoice) == 0 :
                print(Fore.RED + "No hay , intente con otro num.")
                time.sleep(2)
                continue
            else:
                invoice = invoice[0]
                break

        # print resum
        set_color(Fore.GREEN + Style.BRIGHT)
        print("\n" + "=" * 50)
        print(f"FACTURA N°: {invoice['id']}".center(50))
        print("=" * 50)
        print(f"Fecha: {invoice['Fecha']}")
        print(f"Cliente: {invoice["dni"]} {invoice['fullName']}")
        print(f"Forma de pago: {invoice["pay"]}")
        print(f"Total: {invoice["total"]}\n")
    
        #question 
        while True :
            gotoxy(5,14)
            print("\33[0j", end="")
            result = input(Fore.RED + "Esta seguro de eliminar s/n ?: ").lower()
            if not  result in ('s','n'):
                continue

            elif result == "n":
                print(Fore.GREEN + "Cancelo!!")
                time.sleep(1)
                return
            break

        result  = self.json_file.delete(invoice["id"])
        gotoxy(5,16)
        if result == 0:
            print(Fore.RED + "No se eliminó!!")
        else: 
            print(Fore.GREEN + "Proceso esxitoso!!")
        time.sleep(2)    

    def consult(self) ->None:

        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Venta"+" "*35+"██")
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
            print(f"Cliente: {invoice["dni"]} {invoice['fullName']}")
            print(f"Forma de pago: {invoice["pay"]}\n")

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
                    "{:<4} {:<12} {:<14} {:<25} {:>13,.2f}  {:<7}".format(
                        fac['id'], fac['Fecha'],fac['dni'], fac['fullName'], fac['total'],fac['pay']
                    )
                )

            suma = reduce(lambda total, invoice: round(total+ invoice["total"],2),invoices,0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["fullName"] == "Dayanna Vera", invoices))

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
