from datetime import date
from colorama import Fore, Style
from controllers.creditSalesController import CreditSalesController
from controllers.customerController import CustomerController
from controllers.productController import ProductController
from controllers.salesController import SalesController
from helpers.components import Menu
from databaseManagement.databaseManager import  DataService

from helpers.utilities import clear_screen, gotoxy, set_color
import time
opc =""
#Menu Proceso Principal

if __name__ == "__main__":
    data_service   = DataService()  # Instancia de la base de datos

    _exit = "               <- Saliendo..."
    while opc !='6':  
        clear_screen()      
        # menu_main = Menu("SISTEMA DE FACTURACION",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,2)
        menu_main = Menu("SISTEMA DE FACTURACION",["1) Clientes","2) Productos","3) Ventas","4) Proveedores", "5) Crédito", "6) Salir"],20,2)
        # cambio de color de letra y bold
        set_color(Fore.LIGHTBLUE_EX + Style.BRIGHT)

        opc = menu_main.printMenu()

        #  clientes
        if opc == "1":

            opc1 = ''
            while opc1 !='5':
                customer_controller = CustomerController(data_service)
                clear_screen()  
                gotoxy(20, 1)
                print(Fore.BLUE + "╭───────╮")
                gotoxy(20, 2)
                print(Fore.BLUE + "│" + Fore.CYAN + "  👤  " + Fore.BLUE + "│  Menu Cientes")
                gotoxy(20, 3)
                print(Fore.BLUE + "╰───────╯" + Style.RESET_ALL)

                set_color(Fore.BLUE + Style.BRIGHT)  
                menu_clients = Menu("",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,3)
                opc1 = menu_clients.printMenu()
                if opc1 == "1":  # ingresar
                    customer_controller.create()

                elif opc1 == "2":  # Actualizar
                    customer_controller.update()

                elif opc1 == "3":  # Eliminar
                    customer_controller.delete()

                elif opc1 == "4":  # Consultar
                    customer_controller.consult()

                elif opc1 == "5":  # Consultar
                   print(Fore.GREEN + _exit)
                   time.sleep(1)             
        # productos 
        elif opc == "2":
            opc2 = ''
            while opc2 !='5':
                product = ProductController(data_service)
                clear_screen() 
                print(Fore.BLUE + """
                    ╭─────────╮
                    │ 🛒    │ Menu Productos
                    ╰─────────╯
                """ + Style.RESET_ALL)
                set_color(Fore.BLUE + Style.BRIGHT)   
                menu_products = Menu("",["1) ⊕ Ingresar","2) ✎ Actualizar","3) ✕ Eliminar","4) ⌕ Consultar","5) ← Salir"],20,3)
                opc2 = menu_products.printMenu()
                if opc2 == "1": # Add 1
                    product.create()
                
                elif opc2 == "2": # update
                    product.update()
               
                elif opc2 == "3": # delete
                     product.delete()
                
                elif opc2 == "4":  # search
                    product.consult()
                elif opc2 == "5":  # search
                    print(Fore.GREEN + _exit)
                    time.sleep(1)  
        # ventas
        elif opc == "3": 
            opc3 =''
            while opc3 !='5':
                clear_screen()
                print(Fore.BLUE + """
                    ╭─────────╮
                    │ 🧾    │  Menu Ventas
                    ╰─────────╯
                """ + Style.RESET_ALL)
                sales = SalesController(data_service)
                set_color(Fore.BLUE + Style.BRIGHT)
                menu_sales = Menu("",["1) Registro Venta","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,3)
                opc3 = menu_sales.printMenu()
                if opc3 == "1":  # registro de  venta
                    sales.create()
                    
                elif opc3 == "2": # actualizar
                     sales.update()

                elif opc3 == "3": #  eliminar
                    sales.delete()

                elif opc3 == "4": # consultar    
                    sales.consult()

                elif opc3 == "5":  # salir
                    print(Fore.GREEN + _exit)
                    time.sleep(1)  
        # supplier
        elif opc == "4":
            clear_screen()
            print('ups!!\2No disponible en esta version...')
            time.sleep(2)
            opc3 ='5'
            while opc3 !='5':
                clear_screen()
                suppCrud = CrudSales() # CrudSupplier()
                set_color(Fore.BLUE + Style.BRIGHT)
                menu_sales = Menu("Menu Proveedores",["1) Registro proveedor","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,2)
                opc3 = menu_sales.printMenu()
                if opc3 == "1":  # registro de  venta
                    suppCrud.create()
                    
                elif opc3 == "2": # actualizar
                     suppCrud.update()

                elif opc3 == "3": #  eliminar
                    suppCrud.delete()

                elif opc3 == "4": # consultar    
                    suppCrud.consult()

                elif opc3 == "5":  # salir
                    print(Fore.GREEN + _exit)
                    time.sleep(1)  

          
        # cobro de deudas
        elif opc == "5":
            opc3 =''
            while opc3 !='5':
                clear_screen()
                print(Fore.BLUE + """
                    ╭─────────╮
                    │ 💰   │ Menu Cobros  
                    ╰─────────╯
                """ + Style.RESET_ALL)
                credit_controller = CreditSalesController(data_service)
                set_color(Fore.BLUE + Style.BRIGHT)
                menu_sales = Menu("",["1) Registrar cobros","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,3)
                opc3 = menu_sales.printMenu()
                if opc3 == "1":  # registro de  venta
          
                    credit_controller.create()
                    
                elif opc3 == "2": # actualizar
                     credit_controller.update()

                elif opc3 == "3": #  eliminar
                    credit_controller.delete()

                elif opc3 == "4": # consultar    
                    credit_controller.consult()

                elif opc3 == "5":  # salir
                    print(Fore.GREEN + _exit)
                    time.sleep(1)  


            clear_screen()
      
