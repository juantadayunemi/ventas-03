from colorama import Fore, Style
from helpers.components import Menu
from services.Products.ProductService import CrudProduct
from services.Sales.SalesService import CrudSales
from services.Customers.CustomersService import CrudCustomer
from helpers.utilities import clear_screen, set_color
import time

# from services.Purchase.PurchaseService import CrudPurchase
# from services.Supplier.supplierService import CrudSupplier

#Menu Proceso Principal
opc:str = ''

if __name__ == "__main__":
    _exit = "               <- Saliendo..."
    while opc !='4':  
        clear_screen()      
        menu_main = Menu("SISTEMA DE FACTURACION",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,2)
        # menu_main = Menu("SISTEMA DE FACTURACION",["1) Clientes","2) Productos","3) Ventas","4) Proveedores", "5) Compras", "6) Salir"],20,2)
        # cambio de color de letra y bold
        set_color(Fore.LIGHTBLUE_EX + Style.BRIGHT)

        opc = menu_main.printMenu()

        #  clientes
        if opc == "1":

            opc1 = ''
            while opc1 !='5':
                customers = CrudCustomer()
                clear_screen()  
                set_color(Fore.BLUE + Style.BRIGHT)  
                menu_clients = Menu("Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,2)
                opc1 = menu_clients.printMenu()
                if opc1 == "1":  # ingresar
                    customers.create()

                elif opc1 == "2":  # Actualizar
                    customers.update()

                elif opc1 == "3":  # Eliminar
                    customers.delete()

                elif opc1 == "4":  # Consultar
                    customers.consult()

                elif opc1 == "5":  # Consultar
                   print(Fore.GREEN + _exit)
                   time.sleep(1)             
        # productos 
        elif opc == "2":
            opc2 = ''
            while opc2 !='5':
                product = CrudProduct()
                clear_screen() 
                set_color(Fore.BLUE + Style.BRIGHT)   
                menu_products = Menu("🛍️  Menu Productos",["1) ⊕ Ingresar","2) ✎ Actualizar","3) ✕ Eliminar","4) ⌕ Consultar","5) ← Salir"],20,2)
                opc2 = menu_products.printMenu()
                if opc2 == "1": # Add 
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
                sales = CrudSales()
                set_color(Fore.BLUE + Style.BRIGHT)
                menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,2)
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

        elif opc == "4":
            opc3 =''
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


            clear_screen()
      
        elif opc == "5":
            opc3 =''
            while opc3 !='5':
                clear_screen()
                suppCrud = CrudSales() # CrudPurchase()
                set_color(Fore.BLUE + Style.BRIGHT)
                menu_sales = Menu("Menu Compras",["1) Registrar compra","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,2)
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


            clear_screen()
      
