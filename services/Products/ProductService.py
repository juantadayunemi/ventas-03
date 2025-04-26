import msvcrt
import os
import time
from typing import Any, Dict, List, Optional, Tuple, Union
from colorama import Fore, Style
from components.header import Header_print
from services.Products.ProductDTO import ProductDTO
from models.company import CompanyModel
from models.product import ProductModel
from helpers.jsonManager import JsonFile
from helpers.utilities import clear_screen, get_last_color, gotoxy, set_color
from interfaces.iCrud  import ICrud
from helpers.components import Valida
from env import ROOT_PATH 

class CrudProduct(ICrud):
    
    def __init__(self):
        self.__filename = os.path.join(ROOT_PATH, "files","products.json")
        self.json_file = JsonFile(self.__filename)
        self.validar:Valida = Valida() 
    def create(self):
        # cabecera de la venta
        start_x, start_y = Header_print("Agregando nuevo producto..")
    
        flat:bool = True
        while flat: 
            
          
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
            
            productDTO = ProductDTO(new_product)
            products = self.json_file.read()

            id = 1
            if len(products)>0:
                 id = products[-1]["id"]+1

            data = productDTO.getJson()
            data["id"]=id
            products.append(data)
                  
            # clean screen
            gotoxy(10,12); print("\033[0J", end="")
            set_color(Fore.LIGHTMAGENTA_EX+ Style.BRIGHT)
            save_respnse =   input("Esta todo listo!!\nDesea guardar esta información s/n?").lower()
            if (save_respnse == "s"):
                self.json_file.save(products)
                flat = False
                gotoxy(10,14); print(Fore.RED +"Producto guardado exitosamente..")
            else:
                gotoxy(10,14); print(Fore.GREEN+"No guardaste!!.\nRegresamos al menu anterior")
                flat = False

            time.sleep(2)

        set_color(current_style)

    def update(self) ->None:
        # print header
        current_style = get_last_color()
        start_x, start_y   = Header_print("Actualización del Producto")
        # Buscar product
        product = self.Select_product(start_x, start_y)
       
        if not product: 
            set_color(current_style)
            return
       
        self.__show_one_product(5,6, product, "PRODUCTO A MODIFICAR")
       
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
        product_dt = ProductDTO(product)
        new_data =   product_dt.getJson()

        for field in fields:
            gotoxy(field['x'], field['y'])
            set_color(Fore.WHITE + Style.BRIGHT)
            try:
                new_value = field['validator'](mensajeError=f"Error en {field['label']}",
                                col=field['x'],
                                fil=field['y'])
                
                if new_value:  # Solo actualizar si hay valor
                    new_data[field['name']] = new_value
            except Exception as e:
                self.__show_error(f"Error: {str(e)}", 5, 24)
                return
                
        # Confirmación
        set_color(Fore.LIGHTMAGENTA_EX)
        gotoxy(5, 21); print("¿Guardar cambios? (S/N): ")
        gotoxy(30, 21)
        confirm =input(Fore.WHITE).lower()
    
        if confirm.lower() == 's':
            new_data["product_name"] = (new_data["product_name"]).upper()
            self.json_file.update(new_data)
            gotoxy(5, 27); set_color(Fore.GREEN); print("! Producto actualizado correctamente!")
        else:
            gotoxy(5, 27); set_color(Fore.YELLOW); print("⚠ Cambios descartados")
            set_color(current_style)
        time.sleep(2)

    def Select_product(self, x:int, y:int)-> ProductModel | None:
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
            
            product = self._find_product(search)
            if not product:
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
    
    def _find_product(self,search_term:str) -> List[ProductModel] | None:
        """Busca un producto según el criterio de búsqueda"""
        dict_data: list[dict[str, Any]] = []

        if search_term.isdigit():
            if search_term.startswith("0"):
                dict_data = self.json_file.find("product_name", search_term)  # ejme 0400 ml 
            elif len(search_term) <= 3:
                dict_data =  self.json_file.find("id", int(search_term))   # Búsqueda por ID interno
            else:
                dict_data =  self.json_file.find("product_name", search_term) # Búsqueda por nombre del producto
        elif len(search_term) > 0:
            dict_data =    self.json_file.search(["product_name"], search_term) # x nombre del producto
        else:
             dict_data =    self.json_file.read()

        products : list[ProductModel] = []
        for item in dict_data:
            product = ProductModel(
                  product_name =item['product_name'],
                  description = item['description'],
                  purchase_price = item['purchase_price'],
                  sale_price = item['sale_price'],
                  stock = item['stock'],
                  id = item['id']
                 )

            products.append(product)

        return products
    
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
        start_x ,start_y= Header_print("Eliminando producto")
        product_delete = self.Select_product(start_x, start_y)
 
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
            row_affected =self.json_file.delete(product_delete.id)
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

        products:List[ProductModel] | None = self._find_product("")
 
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