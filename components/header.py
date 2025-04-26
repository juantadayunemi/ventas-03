from typing import Tuple

from colorama import Fore, Style

from helpers.utilities import clear_screen, gotoxy, set_color
from models.company import CompanyModel

def Header_print( title:str)->Tuple[int, int]:
    clear_screen()
    set_color(Fore.GREEN + Style.BRIGHT)
    gotoxy(2, 1); print("*"*90)
    gotoxy(30, 2); print(f"{title}")
    gotoxy(17, 3); print(f"{CompanyModel.get_business_name()}")
    gotoxy(2, 4); print("-"*90)
    return (2,5)