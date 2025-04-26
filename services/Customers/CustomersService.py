import copy
import msvcrt
import os
import time
from typing import Any, Dict, List, Optional, Tuple
from colorama import Fore, Style
from components.header import Header_print
from models import customer
from services.Customers.CustomerDTO import CustomerDTO
from models.company import CompanyModel
from helpers.jsonManager import JsonFile
from helpers.utilities import clear_screen, get_last_color, gotoxy, set_color
from interfaces.iCrud  import ICrud
from helpers.components import Valida
from env import  ROOT_PATH 
from models.customer import  CustomerModel

class CrudCustomer(ICrud):


    def __init__(self):
        self.__filename = os.path.join(ROOT_PATH, "files","customers.json")
        self.json_file = JsonFile(self.__filename)
        self.validar:Valida = Valida() 

    def create(self) ->None:

        # imprime cabecera de vrntas
        start_x, start_y = Header_print("Agregando nuevo cliente..")
    
        flat:bool = True
        while flat: 
            
          
            gotoxy(1,4)
            print("\033[0J", end="") 

            set_color(Fore.BLUE + Style.NORMAL)
            gotoxy(10,5);print(f"Seleccione el tipo de cliente:")
            gotoxy(5,6);print(f"1) Cliente Personal")
            gotoxy(5,7);print(f"2) Cliente Cooporativo")
            gotoxy(8,8)

            current_style = get_last_color()
            customer_type:int = -1

            while True:
                optioCustomer = input("Seleccione una opción válida:").lower()

                if optioCustomer == "x":
                    return
                
                if optioCustomer .isdigit() and optioCustomer in ('1','2') :
                    customer_type = int(optioCustomer)
                    break
                else:
                    gotoxy(8,9)
                    print(Fore.RED + "Opcion invalida..")
                    time.sleep(2)
                    gotoxy(8,9)
                    print("\033[2K", end="") 
                    gotoxy(8,8)
                    print("\033[2K", end="") 
                    set_color(current_style)
        
            # Reimprimo la cabecera  ya con los datos seleccionados      
            gotoxy(10,5);print("\033[2K", end="") 
            client_type = "Personal" if customer_type == 1 else "Corporativo"
            print(Fore.LIGHTMAGENTA_EX + f"Tipo de Cliente: {client_type}")

            gotoxy(5,6);print("\033[0J", end="") 
 
            gotoxy(5,7); print("-"*70)

            gotoxy(5,8);print("DNI                 Apellidos                          Nombres")
            
            set_color(Fore.WHITE + Style.NORMAL)
            dni=self.validar.solo_numeros("Error: Solo numeros",5,9)
            first_name = self.validar.enter_data("Err:Ingresar apellido",25,9)
            last_name = self.validar.enter_data("Err:Ingresar nombre",60,9)

            client = self.json_file.find("dni",dni)

            # ya existe un cliente con esta cedula
            if (len(client)>0 ):
                gotoxy(10,10); print(Fore.RED + "Ya está registrado un cliente con este dni")
                response = input("Desea intentar con otro numero: s/n?")
                if response.lower() !="s":
                    flat = False
                    break
                else:
                   continue
            newCustomer = CustomerModel(
                dni=dni, first_name= first_name, 
                last_name= last_name, customer_type = customer_type, id = 2)
            
            customerDTO = CustomerDTO(newCustomer)
            customers = self.json_file.read()

            ult_invoices = 1
            if len(customers)>0:
                 ult_invoices = customers[-1]["id"]+1

            data:Dict[str, Any] = customerDTO.getJson()
            data["id"]=ult_invoices
            customers.append(data)
                  
            # clean screen
            gotoxy(10,12); print("\033[0J", end="")
            message = "Esta todo listo!!\nDesea guardar esta información s/n? "
            save_respnse =   input(Fore.LIGHTMAGENTA_EX+ Style.BRIGHT + message)
            if (save_respnse.lower() == "s"):
                self.json_file.save(customers)
                flat = False
                gotoxy(10,14); print(Fore.LIGHTGREEN_EX +"Cliente guardado exitosamente..")
            else:
                gotoxy(10,14); print(Fore.LIGHTGREEN_EX+"No guardaste!!.\nRegresamos al menu anterior")
                flat = False

            time.sleep(2)

        set_color(current_style)

    def update(self) ->None:

        # print header
        start_x, start_y  = Header_print("Actualización del Cliente")
        # Buscar cliente
        client:CustomerModel | None = self.Select_customer(start_x, start_y)
       
        if not client: 
            return
       
        self.__show_one_customer(5,6, client, "CLIENTE A MODIFICAR")
       
        # Tabla de edición
        set_color(Fore.YELLOW + Style.BRIGHT)
        gotoxy(5, 14); print("INGRESE LOS NUEVOS DATOS (deje vacío para mantener el actual)")
        gotoxy(5, 15); print("┌──────────────┬──────────────────────────────┬────────────────────────┐")
        gotoxy(5, 16); print("│   DNI        │          Apellidos           │       Nombres          │")
        gotoxy(5, 17); print("├──────────────┼──────────────────────────────┼────────────────────────┤")
        
        # Campos editables
        fields = [
            {'name': 'dni', 'label': 'DNI', 'x': 7, 'y': 18, 'width': 15, 'validator': self.validar.solo_numeros},
            {'name': 'first_name', 'label': 'Apellidos', 'x': 23, 'y': 18, 'width': 25, 'validator': self.validar.enter_data},
            {'name': 'last_name', 'label': 'Nombres', 'x': 55, 'y': 18, 'width': 25, 'validator': self.validar.enter_data}
        ]
        
        gotoxy(5, 19); print("└──────────────┴──────────────────────────────┴────────────────────────┘")
        
        # Tipo de cliente
        set_color(Fore.LIGHTBLUE_EX)
        gotoxy(5, 21); print("Tipo: (1) Personal , (2) Corporativo")
        gotoxy(5, 22); print(f"Actual: {client.customer_type} ({'Personal' if client.customer_type == 1 else 'Corporativo'})")
        
        # Editar campos
        custome_dto = CustomerDTO(client)
        new_data = custome_dto.getJson() 
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
                
        
        # Editar tipo de cliente
        gotoxy(5, 23); print("Nuevo tipo (1/2): ")

        while True:
            gotoxy(22, 23)
            print("\033[0J", end="")
            gotoxy(22, 23)
            tipo = input()
            if tipo in ('1', '2'):
                new_data['customer_type'] = int(tipo)
                break
        
        # Confirmación
        set_color(Fore.LIGHTMAGENTA_EX)
        gotoxy(5, 25); print("¿Guardar cambios? (S/N): ")
        gotoxy(30, 25)
        confirm =input().lower()
    
        if confirm.lower() == 's':
            new_data["first_name"] = (new_data["first_name"]).upper()
            new_data["last_name"] = (new_data["last_name"]).upper()
            self.json_file.update(new_data)
            gotoxy(5, 27); set_color(Fore.GREEN); print("! Cliente actualizado correctamente!")
        else:
            gotoxy(5, 27); set_color(Fore.YELLOW); print("⚠ Cambios descartados")
        
        time.sleep(2)

    def Select_customer(self, x:int, y:int)-> CustomerModel | None:
          customer = None
          while not customer:
            set_color(Fore.LIGHTMAGENTA_EX)
            gotoxy(x, y + 1); print("\033[0J", end="")  # Limpiar desde posición actual
            search = input("Buscar cliente (ID/DNI/Nombre) o 'x' para salir: ")
            
            if search.lower() == 'x':
                return None
            
            customer = self._find_client(search)
            if not customer:
              self.__show_error("❌ Cliente no encontrado!", 5, y+2)
              continue

            # si hay varios clientes
            elif len(customer) > 1:
                set_color(Fore.CYAN + Style.BRIGHT)
                gotoxy(5, y+2); print("\033[0J", end="")  # Limpiar antes de mostrar tabla
                selected_client = self.__show_list(customer, 5, y+2,"HAY VARIOS CLIENTES ENCONTRADOS")
                if selected_client:
                    customer = [selected_client]  # Convertir a lista para consistencia
                else:
                    return None  # Volver a buscar si canceló
            
            
          
          return customer[0] if  customer else None
    
    def _find_client(self,search_term:str) ->List[Any]:
        """Busca un cliente según el criterio de búsqueda"""

        results: List[Dict[str, Any]] = []

        if search_term.isdigit():
            if search_term.startswith("0"):
                results =  self.json_file.find("dni", search_term)  # Búsqueda por cédula (Ecuador)
            elif len(search_term) <= 3:
                results =  self.json_file.find("id", int(search_term))   # Búsqueda por ID interno
            else:
                results  =  self.json_file.find("dni", search_term) # Búsqueda por cédula normal
        elif len(search_term):
            results =  self.json_file.search(["first_name", "last_name"], search_term) # x apellido y nombre
        else:
             results =  self.json_file.read()
       
        # convertir OBJETO
        customers: List[CustomerModel] = []

        for client_data in results:
            customer = CustomerModel(
                id = client_data.get('id', 1),
                dni=client_data.get('dni', ''),
                first_name=client_data.get('first_name', ''),
                last_name=client_data.get('last_name', ''),
                customer_type=client_data.get('customer_type', 1) ,
                
            )
            customers.append(customer)
        
        return customers

    def __show_error(self,message:str, x:int, y:int):
        """Muestra un mensaje de error en posición fija"""
        gotoxy(x, y)
        print(Fore.RED + message)
        time.sleep(2)
   
   
    def __generate_client_table(self, clients: list, title: str = "") -> str:
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
        table.field_names = ["ID", "DNI", "Apellidos", "Nombres", "Tipo"]
        table.align["ID"] = "l"
        table.align["DNI"] = "r"
        table.align["Apellidos"] = "l"
        table.align["Nombres"] = "l"
        table.align["Tipo"] = "l"
        
        if title:
            table.title = f" {title} "  # PrettyTable centra automáticamente los títulos
        
        for client in clients:
            table.add_row([
                client['id'],
                client['dni'],
                client['first_name'],
                client['last_name'],
                "Personal" if client['customer_type'] == 1 else "Corporativo"
            ])
        
        return table.get_string()

    def __display_table_with_selection(self, table_str: str, x: int, y: int) -> tuple:
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

    def __show_list(self, clients: list, x: int, y: int, title: str = "") -> CustomerModel | None:
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
        table_str = self.__generate_client_table(clients, title)
        
        # Mostrar tabla y obtener posición final
        x, y = self.__display_table_with_selection(table_str, x, y)
        
        # Opciones de selección
        gotoxy(x, y + 1)
        print(Fore.YELLOW + "Seleccione un cliente por ID o presione 'x' para cancelar")
        gotoxy(x, y + 2)
        selected_id = input("ID del cliente: ")
        
        if selected_id.lower() == 'x':
            return None
        
        # Buscar cliente seleccionado
        for client in clients:
            if str(client['id']) == selected_id:
                return client
        
        self.__show_error("ID no válido", x, y + 3)
        return None

    def __show_one_customer(self,x,y,client:CustomerModel, title:str)-> Tuple[int, int]:
         # limpiar y mostrar el cliente
        gotoxy(x, y+1)
        print("\033[0J", end="")

        set_color(Fore.CYAN + Style.BRIGHT)
        y += 1;gotoxy(x, y); print(f"{title}")
        y += 1;gotoxy(x, y); print(f"ID: {client.id}")
        y += 1;gotoxy(x, y); print(f"DNI: {client.dni}")
        y += 1;gotoxy(x, y); print(f"Apellidos: {client.first_name}")
        y += 1;gotoxy(x, y); print(f"Nombre: {client.last_name}")
        y += 1;gotoxy(x, y); print(f"Tipo: {'Personal' if client.customer_type == 1 else 'Corporativo'}")
        y += 1;gotoxy(x, y); print("-"*70)
        
        return (x,y)
    
  
    
    def delete(self) ->None:
        start_x, start_y = Header_print("Eliminando cliente")
        customer_delete = self.Select_customer(start_x, start_y)
 
        if not customer_delete : 
            return
        # print the customer select
        x, y = self.__show_one_customer(5,7, customer_delete, "CLIENTE A ELIMINAR")
       
        while True:
            gotoxy(x,y+1); print("\033[0J", end="")
            gotoxy(x+15,y+1)
            response = input("Esta seguro de eliminar? s/n: ")
            if not response.lower() in ("s","n"):
                continue
            if response.lower() == "n":
                return
            
            # delete the customer 
            row_affected = self.json_file.delete(customer_delete.id)
            if (row_affected):
                gotoxy(5,y+2)
                print(Fore.RED + "Cliente eliminado")
                time.sleep(1)
            break

    def consult(self) ->None:
        
        start_x, start_y = Header_print("LISTADO DE CLIENTES")
        customers = self.json_file.read()
 
        if not customers  or len(customers) == 0 : 
            gotoxy(5,start_y+ 1); print(Fore.RED+ "No hay datos para mostrar..")
            print(Fore.GREEN+ "Presione cualquier tecla para continuar...")
            msvcrt.getch()  
            return
        # print the customer select
       
        table = self.__generate_client_table(customers,"")
        x, y = self.__display_table_with_selection(table, 5, 5)
        gotoxy(5,y+1)
        print(Fore.GREEN+ "Presione cualquier tecla para continuar...")
        msvcrt.getch()  