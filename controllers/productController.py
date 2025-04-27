import msvcrt
import os
import time
from typing import Tuple
from colorama import Fore, Style
from components.header import Header_print
from databaseManagement.databaseManager import DataService
from models.product import ProductModel
from helpers.utilities import  get_last_color, gotoxy, set_color
from interfaces.iCrud  import ICrud
from helpers.components import Valida
from env import ROOT_PATH 

class ProductController(ICrud):
    
    def __init__(self, data_sevice:DataService) ->None:
        self.validar:Valida = Valida() 
        self.data_service:DataService =data_sevice
    def create(self):
        # cabecera de la venta
        start_x, start_y = Header_print("Agregando nuevo producto..")

        while True: 
            
            gotoxy(1,4)
            print("\033[0J", end="") 

            set_color(Fore.BLUE + Style.NORMAL)
          
            current_style = get_last_color()

            gotoxy(5,7); print("-"*70)

            gotoxy(5,8);print("DESCRIPCION                    PRECIO        STOCK")
            
            set_color(Fore.WHITE + Style.NORMAL)
            product_name=self.validar.enter_data("Error: Ingrese datos",5,9)
            sale_price = self.validar.solo_decimales("Err: que sea decimal",36,9)
            stock = self.validar.solo_numeros("Err: que sea numérico",50,9)

          
            new_product = ProductModel(product_name=product_name, sale_price=sale_price, stock= int(stock))

            # clean screen
            gotoxy(10,12); print("\033[0J", end="")
            set_color(Fore.LIGHTMAGENTA_EX+ Style.BRIGHT)
            save_respnse =   input("Esta todo listo!!\nDesea guardar esta información s/n?").lower()
            if (save_respnse == "s"):
                self.data_service.Product.add(new_product)
                gotoxy(10,14); print(Fore.RED +"Producto guardado exitosamente..")
                break   
            else:
                gotoxy(10,14); print(Fore.GREEN+"No guardaste!!.\nRegresamos al menu anterior")
                break

        time.sleep(2)

        set_color(current_style)

    def update(self) ->None:
        # print header
        current_style = get_last_color()
        start_x, start_y   = Header_print("Actualización del Producto")
        # Buscar product
        product_edit = self.__select_product(start_x, start_y)
       
        if product_edit is None: 
            set_color(current_style)
            return
       
        self.__show_one_product(5,6, product_edit, "PRODUCTO A MODIFICAR")
       
        # Tabla de edición
        set_color(Fore.YELLOW + Style.BRIGHT)
        gotoxy(5, 14); print("INGRESE LOS NUEVOS DATOS (deje vacío para mantener el actual)")
        gotoxy(5, 15); print("┌────────────────────────────────┬────────────────┬───────────────┐")
        gotoxy(5, 16); print("│  PRODUCTO                      │   Precio       │     Stock     │")
        gotoxy(5, 17); print("├────────────────────────────────┼────────────────┼───────────────┤")
        
        # Campos editables
        fields = [
            {'name': 'product_name', 'label': 'Producto', 'x': 7, 'y': 18, 'width': 35, 'validator': self.validar.enter_data},
            {'name': 'sale_price', 'label': 'Precio venta', 'x': 40, 'y': 18, 'width': 10, 'validator': self.validar.solo_decimales},
            {'name': 'stock', 'label': 'Stock', 'x': 60, 'y': 18, 'width': 10, 'validator': self.validar.solo_numeros}
        ]
        
        gotoxy(5, 19); print("└────────────────────────────────┴────────────────┴───────────────┘")
        

        # Editar campos

        for field in fields:
            gotoxy(field['x'], field['y'])
            set_color(Fore.WHITE + Style.BRIGHT)
            try:
                new_value = field['validator'](mensajeError=f"Error en {field['label']}",
                                col=field['x'],
                                fil=field['y'])
                
              
                 # usamos setattr para asignar dinamicamente
                if hasattr(product_edit, field['name']):
                    setattr(product_edit, field['name'], new_value)
                else:
                    raise AttributeError(f"El campo {field['name']} no existe en ProductModel")

            except Exception as e:
                self.__show_error(f"Error: {str(e)}", 5, 24)
                return
                
        # Confirmación
        set_color(Fore.LIGHTMAGENTA_EX)
        gotoxy(5, 21); print("¿Guardar cambios? (S/N): ")
        gotoxy(30, 21)
        confirm =input(Fore.WHITE).lower()
    
        if confirm.lower() == 's':
            self.data_service.Product.add(product_edit)
            gotoxy(5, 27); set_color(Fore.GREEN); print("! Producto actualizado correctamente!")
        else:
            gotoxy(5, 27); set_color(Fore.YELLOW); print("⚠ Cambios descartados")
            set_color(current_style)
        time.sleep(2)

    def __select_product(self, x:int, y:int)-> ProductModel | None:
          product = None
          while not product:
            set_color(Fore.LIGHTMAGENTA_EX)
            gotoxy(x, y + 1); print("\033[0J", end="")
            message = "Buscar producto (ID/Nombre) o 'x' para salir: "
            print(message)
            gotoxy(x + len(message), y + 1)
            search = input(Fore.WHITE)
            
            if search.lower() == 'x':
                return None
            
            product =  ProductController.find_product( self.data_service ,search)
            if  product is None:
              self.__show_error(Fore.RED + "❌ Producto no encontrado!", 5, y+2)
              continue

            # si hay varios clientes
            elif len(product) > 1:
                set_color(Fore.CYAN + Style.BRIGHT)
                gotoxy(5, y+2); print("\033[0J", end="")  # Limpiar antes de mostrar tabla
                selected_product = self.__show_list(product, 5, y+2,"HAY VARIOS PRODUCTOS ENCONTRADOS")
                if selected_product:
                    product = [selected_product]  # Convertir a lista para consistencia
                else:
                    return None  # Volver a buscar si canceló
            
            
          
          return product[0] if  product else None
    

    @staticmethod
    def find_product(data_service: 'DataService', search_term: str) -> list[ProductModel]:
        """Busca productos según criterio de búsqueda (ID, nombre exacto o parcial)"""
        if not search_term:
            return data_service.Product.get_all()

        search_term = search_term.strip().lower()
        
        # Búsqueda por ID (exacta)
        if search_term.isdigit():
            if len(search_term) <= 3:  # Búsqueda por ID numérico corto
                product = data_service.Product.get(int(search_term))
                return [product] if product else []
            else:  # Números más largos (códigos de barras, etc.)
                return data_service.Product.find("barcode", search_term) or \
                    data_service.Product.find("id", int(search_term))
        
        # Búsqueda por nombre (parcial o exacto)
        results = data_service.Product.search(
            fields=["product_name", "description", "category"],  # Campos a buscar
            search_term=search_term
        )
        
        # Ordenar resultados por relevancia (nombres que empiezan con el término primero)
        return sorted(results, 
                    key=lambda p: (
                        not p.product_name.lower().startswith(search_term),
                        not search_term in p.product_name.lower(),
                        p.product_name
                    ))

    
    def __show_error(self,message:str, x:int, y:int) ->None:
        """Muestra un mensaje de error en posición fija"""
        gotoxy(x, y)
        print(Fore.RED + message)
        time.sleep(2)
   
   
    def __generate_product_table(self, products:list[ProductModel], title: str = "") -> str:
        """
        Genera una tabla formateada de clientes en formato PrettyTable
        
        Args:
            clients: Lista de diccionarios con datos de clientes
            title: Título opcional para la tabla
            
        Returns:
            str: Tabla formateada como string
        """
        from prettytable import PrettyTable
        
        table = PrettyTable()
        table.field_names = ["ID", "PRODUCTO", "Ultima compra", "Precio venta", "Stock",]
        table.align["ID"] = "l"
        table.align["PRODUCTO"] = "l"
        table.align["Precio compra"] = "r"
        table.align["Precio venta"] = "r"
        table.align["Stock"] = "r"
              
        if title:
            table.title = f" {title} "  # PrettyTable centra automáticamente los títulos
        
        for product in products:
            table.add_row([
                product.id,
                product.product_name,
                product.purchase_price,
                product.sale_price,
                product.stock
            ])
        
        return table.get_string()

    def __display_table_with_selection(self, table_str: str, x: int, y: int) -> Tuple:
        """
        Muestra una tabla en posición (x,y) y maneja la selección
        
        Args:
            table_str: Tabla formateada como string
            x: Posición horizontal inicial
            y: Posición vertical inicial
            
        Returns:
            tuple: (x, y) de la posición final, o None si se canceló
        """
        lines = table_str.split('\n')
        
        # Mostrar tabla línea por línea
        for i, line in enumerate(lines):
            gotoxy(x, y + i)
            print(line)
        
        # Posición para mensajes debajo de la tabla
        return (x, y + len(lines))

    def __show_list(self, products: list[ProductModel], x: int, y: int, title: str = "") ->ProductModel | None:
        """
        Muestra lista de clientes en tabla y permite selección
        
        Args:
            clients: Lista de clientes a mostrar
            x: Posición horizontal inicial
            y: Posición vertical inicial
            title: Título opcional para la tabla
            
        Returns:
            dict: Cliente seleccionado o None si se canceló
        """
        # Generar tabla
        table_str = self.__generate_product_table(products, title)
        
        # Mostrar tabla y obtener posición final
        x, y = self.__display_table_with_selection(table_str, x, y)
        
        # Opciones de selección
        gotoxy(x, y + 1)
        print(Fore.YELLOW + "Seleccione un producto por ID o presione 'x' para cancelar")
        gotoxy(x, y + 2)
        selected_id = input("ID del producto: ")
        
        if selected_id.lower() == 'x':
            return None
        
        # Buscar cliente seleccionado
        for product in products:
            if product.id==  int(selected_id):
                return product
        
        self.__show_error("ID no válido", x, y + 3)
        return None

    def __show_one_product(self,x,y,product:ProductModel, title:str)-> Tuple[int, int]:
         # limpiar y mostrar el cliente
        gotoxy(x, y+1)
        print("\033[0J", end="")

        set_color(Fore.CYAN + Style.BRIGHT)
        y += 1;gotoxy(x, y); print(f"{title}")
        y += 1;gotoxy(x, y); print(f"ID: {product.id}")
        y += 1;gotoxy(x, y); print(f"PRODUCTO: {product.product_name}")
        y += 1;gotoxy(x, y); print(f"Precio venta: {product.sale_price}")
        y += 1;gotoxy(x, y); print(f"Stock: {product.stock}")
        y += 1;gotoxy(x, y); print("-"*70)
        
        return (x,y)
    

    def delete(self) ->None:

        current_style = get_last_color()
        x ,y = Header_print("Eliminando producto")
        product_delete = self.__select_product(x, y)
 
        if not product_delete : 
            return
        # print the customer select
        x, y = self.__show_one_product(5,7, product_delete, "PRODUCTO A ELIMINAR")
       
        while True:
            gotoxy(x,y+1); print("\033[0J", end="")
            gotoxy(x+15,y+1)
            set_color(Fore.LIGHTMAGENTA_EX + Style.BRIGHT)
            message = "Esta seguro de eliminar? s/n: " 
            print(message)
            gotoxy(x+15 +len(message),y+1)
            response = input(Fore.WHITE)
            if not response.lower() in ("s","n"):
                continue
            if response.lower() == "n":
                return
            
            # delete the customer 
            row_affected =self.data_service.Product.remove(product_delete.id)
            gotoxy(5,y+3)
            if row_affected == 0:
                print(Fore.RED + "No se eliminó")
            else: 
                print(Fore.GREEN +"Proceso exitoso")  

            time.sleep(1)
            break

        set_color(current_style)
    


    def consult(self) ->None:

        start_x, start_y = Header_print("LISTADO DE PRODUCTOS")

        products:list[ProductModel]  = self.data_service.Product.get_all()
 
        if not products  or len(products) == 0 : 
            gotoxy(5,start_y+ 1); print(Fore.RED+ "No hay datos para mostrar..")
            print(Fore.GREEN+ "Presione cualquier tecla para continuar...")
            msvcrt.getch()  
            return
        # print the customer select
       
        table = self.__generate_product_table(products,"")
        x, y = self.__display_table_with_selection(table, 5, 5)
        gotoxy(5,y+1)
        print(Fore.GREEN+ "Presione cualquier tecla para continuar...")
        msvcrt.getch()  