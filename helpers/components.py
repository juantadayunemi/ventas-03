from ctypes import Array
from tkinter import BROWSE
from typing import Any
from colorama import Fore, Style
from helpers.utilities import  get_last_color, gotoxy, set_color
import time

class Menu:
    def __init__(self,titulo:str ="", opciones:list[Any]= [],col:int=6,fil:int=1):
        self.titulo:str = titulo
        self.opciones:list=opciones
        self.col:int = col
        self.fil:int = fil
        
    def printMenu(self) ->str:
        # Dibujar el menú
        gotoxy(self.col, self.fil)
        print(self.titulo)
        if (self.titulo == "SISTEMA DE FACTURACION"):
            self.fil += 1
            gotoxy(self.col -1, self.fil)
            print("-" * 25)

        self.col -= 5
        self.fil += 1
        print("")
        for opcion in self.opciones:
            self.fil += 1
            gotoxy(self.col, self.fil)
            print(opcion)
        
        # Posición para input (debajo del último ítem del menú)
        input_row = self.fil + 2
        error_row = input_row + 2
        current_color = get_last_color()
        gotoxy(self.col+5, input_row)

        while (True):
            # Mostrar input
            set_color(current_color)
            print("\033[2K", end="")  
            opc = input(f"Elija opcion[1...{len(self.opciones)}]: ").strip()
            
            # Validar opción
            if opc.isdigit() and 1 <= int(opc) <= len(self.opciones):
                return opc
                
            gotoxy(self.col+5, error_row)
            set_color(Fore.RED)  #cambio de color a rojo
            print("Opción incorrecta. Intente nuevamente...")
            time.sleep(2)
            gotoxy(self.col+5, error_row)
            print("\033[2K", end="")  
            gotoxy((self.col+5),input_row)
            print("\033[2K", end="")  
    


class Valida:
    """Clase para validar tipos de datos"""
    def solo_numeros_mayor_cero(self,mensajeError:str, col:int, fil:int):
        while True: 
            gotoxy(col,fil)   
            set_color(Fore.WHITE + Style.NORMAL)         
            valor = input()
            try:
                if int(valor) > 0:
                    break
            except:
                gotoxy(col,fil);print(Fore.RED + mensajeError)
                time.sleep(1)
                gotoxy(col,fil);print(len(mensajeError)*" ")
        return valor
    
    def solo_numeros(self,mensajeError:str, col:int, fil:int, isupdate=False):
        while True: 
            gotoxy(col,fil)   
            set_color(Fore.WHITE + Style.NORMAL)         
            valor = input().strip()

            # si esta acualizando puede retornar vacios
            if isupdate and  valor =="":
                return valor
            
            try:
                if valor.isdigit():
                     break
                else: 
                    gotoxy(col,fil);print(Fore.RED + mensajeError)
                    time.sleep(1)
                    gotoxy(col,fil);print(len(mensajeError)*" ")
            except:
                gotoxy(col,fil);print(Fore.RED + mensajeError)
                time.sleep(1)
                gotoxy(col,fil);print(len(mensajeError)*" ")
        
        return valor


    def validar_fecha(self, mensajeError: str, col: int, fil: int, isupdate=False):
        while True:
            gotoxy(col, fil)
            set_color(Fore.WHITE + Style.NORMAL)
            valor = input().strip()
            
            if isupdate and valor == "":
                return valor
                
            # Basic format validation
            if len(valor) != 10 or valor[2] != '/' or valor[5] != '/':
                self._show_error(col, fil, "Use formato dd/mm/aaaa con /")
                continue
                
            partes = valor.split('/')
            if len(partes) != 3:
                self._show_error(col, fil, "Formato inválido")
                continue
                
            # Numeric validation
            if not all(p.isdigit() for p in partes):
                self._show_error(col, fil, "Solo números y / permitidos")
                continue
                
            # Convert and validate
            try:
                dia, mes, ano = map(int, partes)
                
                # Validate ranges
                if mes < 1 or mes > 12:
                    raise ValueError("Mes inválido")
                    
                # Validate days in month
                if mes in [4, 6, 9, 11] and dia > 30:
                    raise ValueError("Este mes solo tiene 30 días")
                elif mes == 2:
                    # Leap year check
                    if (ano % 400 == 0) or (ano % 100 != 0 and ano % 4 == 0):
                        max_days = 29
                    else:
                        max_days = 28
                    if dia > max_days:
                        raise ValueError(f"Febrero solo tiene {max_days} días este año")
                elif dia > 31:
                    raise ValueError("Día inválido para este mes")
                    
                return valor
            except ValueError as e:
                self._show_error(col, fil, f"Fecha inválida: {str(e)}")

    def _show_error(self, col, fil, message):
        gotoxy(col, fil); print(Fore.RED + message)
        time.sleep(1)
        gotoxy(col, fil); print(" " * len(message))



    def solo_letras(self,mensaje:str,mensajeError:str) ->str: 
        while True:
            valor = str(input("          ------>   | {} ".format(mensaje)))
            if valor.isalpha():
                break
            else:
                print("          ------><  | {} ".format(mensajeError))
        return valor

    def solo_decimales(self, mensajeError: str, col: int, fil: int, decimales: int = 2) -> float:
        result  =0.00
        while True:
            gotoxy(col, fil)
            set_color(Fore.WHITE+ Style.NORMAL)
            valor = input()
            try:
                # Convertir a float y validar que sea positivo
                valor_float = float(valor)
                if valor_float <= 0:
                    raise ValueError("Debe ser mayor a 0")
                    
                # Redondear si se especificó
                if decimales is not None:
                    valor_float = round(valor_float, decimales)
                    
                return valor_float
                
            except ValueError:
                # Mostrar error y limpiar
                gotoxy(col, fil)
                print(Fore.RED + mensajeError)
                time.sleep(1)
                gotoxy(col, fil)
                print(len(mensajeError)*" ")

  
    def enter_data(self,mensajeError,col,fil, isupdate = False) ->str:
        while True: 
            gotoxy(col,fil)            
            valor = input().strip()
            
            if isupdate and valor =="":
                return valor 

            if len(valor.strip()) > 0:
                break
            else:
                gotoxy(col,fil);print(mensajeError)
                time.sleep(1)
                gotoxy(col,fil);print(" "*25)

        return valor.strip()
    
    def enter_empy(self,mensajeError,col,fil) ->str:
        while True: 
            gotoxy(col,fil)            
            valor = input()
            break            
        return valor.strip()

