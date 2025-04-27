import os
from colorama import Fore, Style, init

# Variables globales: Colores en formato ANSI escape code
reset_color_code = "\033[0m"
red_color = "\033[91m"
green_color = "\033[92m"
yellow_color = "\033[93m"
blue_color = "\033[94m"
purple_color = "\033[95m"
cyan_color = "\033[96m"

# Inicializar colorama (autoreset=False para mantener colores hasta cambio explícito)
init(autoreset=False)

# Variable global para almacenar el último color
_LAST_COLOR = Fore.WHITE + Style.NORMAL

def gotoxy(x=None, y=None):            
    if x is not None and y is not None:
        # Mover a posición X,Y específica
        print("%c[%d;%df" % (0x1B, y, x), end="")
    elif x is not None:
        # Mover solo columna (X), mantener fila actual
        print("%c[%dG" % (0x1B, x), end="")
    elif y is not None:
        # Mover solo fila (Y), mantener columna actual
        print("%c[%dd" % (0x1B, y), end="")



def clear_screen():
    os.system("cls") 

def mensaje(msg,f,c):
    pass

# Función para cambiar color y mantenerlo activo
def set_color(color: str) -> None:
    global _LAST_COLOR
    _LAST_COLOR = color
    print(color, end='')  # Aplica el color sin resetear

def get_last_color():
    """Obtiene el último color configurado"""
    return _LAST_COLOR

def reset_color() -> None:
    """Resetea a los valores por defecto"""
    global _LAST_COLOR
    _LAST_COLOR = Fore.WHITE + Style.NORMAL
    print(Style.RESET_ALL, end='')

def clear_last_lines(n: int)->None:
    # Borra las últimas `n` líneas en la terminal
    print(f"\033[{n}F\033[J", end='')
        
