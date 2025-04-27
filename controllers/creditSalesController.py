from datetime import date, datetime
import msvcrt 
from functools import reduce
from sys import exception
import time
from tkinter import dnd
from typing import Any, List
from colorama import Fore, Style
from numpy import true_divide
from pandas import value_counts
from prettytable import PrettyTable
from zmq import WSS_HOSTNAME
from databaseManagement.databaseManager import DataService
from models.creditoSales import CreditSalesModel
from models.company import CompanyModel
from helpers.utilities import clear_screen, green_color, reset_color_code, purple_color
from helpers.components import Valida
from helpers.utilities import gotoxy, set_color
from interfaces.iCrud import ICrud
from models.invoice import InvoiceModel


class CreditSalesController(ICrud):

    def __init__(self, data_service: DataService):
        self.data_service = data_service
        self.validar:Valida = Valida() 
          
    def create(self) ->None:
        # cabecera de la venta
        clear_screen()
        set_color(Fore.GREEN + Style.NORMAL)
        gotoxy(2,1);print("*"*90)
        gotoxy(30,2);print("Registro de cobro")
        gotoxy(17,3);print(CompanyModel.get_business_name())
    
        credit_sale: CreditSalesModel | None = None
        while credit_sale is None:
            # Limpiar línea y mostrar encabezado
            gotoxy(5, 4); print('\33[0J')
            gotoxy(5, 4); print(Fore.CYAN + "BUSCAR CRÉDITO" + Style.RESET_ALL)
            
            # Solicitar número de crédito
            gotoxy(5, 5); print(Fore.GREEN + "N° Crédito:" + Style.RESET_ALL, end=' ')
            credit_id = self.validar.enter_data("Ingrese número de factura (X para cancelar)", 18, 5).lower()
            
            # Opción para salir
            if credit_id == "x":
                gotoxy(5, 7); print(Fore.YELLOW + "Operación cancelada por el usuario" + Style.RESET_ALL)
                time.sleep(1.5)
                return
            
            # Validar formato numérico
            if not credit_id.isdigit():
                gotoxy(5, 7); print(Fore.RED + "ERROR: Debe ingresar solo números" + Style.RESET_ALL)
                gotoxy(5, 8); print(Fore.YELLOW + "Presione cualquier tecla para continuar..." + Style.RESET_ALL)
                input()
                continue
            
            # Buscar crédito
            credit_sale:CreditSalesModel | None = self.data_service.CreditSales.get(int(credit_id))
            
            if credit_sale is None:
                gotoxy(5, 7); print(Fore.RED + "ATENCIÓN: No se encontró crédito con este número" + Style.RESET_ALL)
                gotoxy(5, 8); print(Fore.YELLOW + "Verifique el número e intente nuevamente" + Style.RESET_ALL)
                time.sleep(2)
                continue
            
            if credit_sale.credit_balance == 0:
                gotoxy(5, 7); print(Fore.GREEN + "ESTADO: Este crédito ya está completamente pagado" + Style.RESET_ALL)
                gotoxy(5, 8); print(Fore.YELLOW + "No se requieren pagos adicionales" + Style.RESET_ALL)
                time.sleep(2)
                return
            
            # Si todo está correcto
            gotoxy(17, 5); print(Fore.WHITE + Style.BRIGHT+ f"{credit_sale.id} | {credit_sale.dni} {credit_sale.full_name}" + Style.RESET_ALL)
            break

        gotoxy(60,4);print(Fore.GREEN + Style.NORMAL+"Fecha  factura:"); gotoxy(76,4);print(Fore.WHITE + f"{credit_sale.date_credit}")
        gotoxy(60,5);print(Fore.GREEN + "Num.Factura   :");gotoxy(76,5);print(Fore.WHITE + f"{credit_sale.invoice_id}")
        gotoxy(60,6);print(Fore.GREEN + "Valor factura :");gotoxy(76,6);print(Fore.WHITE + f"{credit_sale.total_credit}")
        gotoxy(60,7);print(Fore.GREEN + "Valor pagado  :");gotoxy(76,7);print(Fore.WHITE + f"{ round( credit_sale.total_credit - credit_sale.credit_balance,2)}")
        gotoxy(60,8);print(Fore.GREEN +"Sado pendiente:") ;gotoxy(76,8);print(Fore.WHITE + f"{credit_sale.credit_balance}")

        # print header
        gotoxy(2,9);print(green_color+"_"*90 + reset_color_code) 
        gotoxy(5,10);print(purple_color+"Linea") 
        gotoxy(12,10);print("Valor pago") 
        gotoxy(30,10);print("Fecha (DD/MM/AAAA):") 
        gotoxy(60,10);print("n->Terminar"+reset_color_code)
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower() == "s":
            gotoxy(7, 10+line); print(line)
            gotoxy(15, 10+line)

            # Solicitar monto de pago
            payment_amount = self.validar.solo_decimales("Error: Ingrese un valor numérico válido", 12, 10+line)
            gotoxy(12, 10+line); print("{:>8.2f}".format(payment_amount))  # Mostrar con 2 decimales

            # Validar que no se exceda el saldo pendiente
            if credit_sale.credit_balance < payment_amount:
                gotoxy(12, 10+line)
                print(Fore.RED + f"¡Atención! Saldo pendiente: ${credit_sale.credit_balance:.2f}. No puede cobrar más que el saldo adeudado." + Fore.WHITE)
                time.sleep(2)
                gotoxy(12, 10+line); print("\33[0J5")  # Limpiar mensaje anterior
                continue

            # Solicitar fecha de pago
            date_pay = self.validar.validar_fecha("Formato de fecha inválido (Use DD/MM/AAAA)", 30, 10+line)
            
            # Procesamiento de la fecha
            if isinstance(date_pay, str):
                try:
                    date_pay = datetime.strptime(date_pay, "%d/%m/%Y").date()
                except ValueError:
                    gotoxy(30, 10+line)
                    print(Fore.YELLOW + "Usando fecha actual (formato incorrecto)" + Fore.WHITE)
                    time.sleep(1)
                    date_pay = date.today()
            elif date_pay is None:
                date_pay = date.today()
            
            gotoxy(30, 10+line); print("{:<10}".format(date_pay.strftime("%d/%m/%Y")))  # Formato consistente

            # Registrar el pago
            try:
                credit_sale.payments_collection.add(date_pay, payment_amount)
            except ValueError as e:
                gotoxy(30, 10+line)
                print(Fore.RED + f"Error al registrar pago: {str(e)}" + Fore.WHITE)
                time.sleep(2)
                gotoxy(30, 10+line); print(" " * 40)  # Limpiar mensaje de error
                continue

            # Actualizar display de saldos
            gotoxy(76, 6); print(Fore.WHITE + f"${credit_sale.total_credit:.2f}")
            gotoxy(76, 7); print(Fore.WHITE + f"${(credit_sale.total_credit - credit_sale.credit_balance):.2f}")
            gotoxy(76, 8); print(Fore.WHITE + f"${credit_sale.credit_balance:.2f}")

            gotoxy(67, 10+line); follow = follow=input() or "s" 
            gotoxy(67, 10+line); print(green_color + "✔" + reset_color_code)
            line += 1
            if  round(  credit_sale.credit_balance,2) == 0:
                follow ="n"

        processar=''
        while True:
            gotoxy(15,10+line);print ("\033[J")
            gotoxy(15,10+line+1);print(Fore.RED+"Esta seguro de guardar pagos(s/n):")
            gotoxy(50,10+line+1);processar = input().lower()
            if processar not  in  ('s','n'):
                continue
            break

        if processar == "s":
            gotoxy(15,12+line);print( Fore.GREEN + "Procesando ...")
            time.sleep(1)

            # update in data base
            result= self.data_service.CreditSales.update(credit_sale)
            if result:
                gotoxy(16,13+line);print(Fore.GREEN + "¡Pago guardado con éxito! " + "✓" + reset_color_code)
            else:
                gotoxy(16,13+line);print(Fore.RED + "Error: no se pudo guardar " + "✗" + reset_color_code)
        else:
            gotoxy(28,12+line);print("Pago Cancelada 🤣"+reset_color_code)    
        time.sleep(2)    

    def update(self) -> None:
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"ACTUALIZACIÓN DE COBROS"+" "*28+"██")
        
        credit_edit =None
        while True:
            gotoxy(2,4);print("\33[0J");gotoxy(7,4); print(Fore.GREEN + "Número de Cobro: " + Fore.WHITE)
            credit_id = self.validar.enter_data("Ingrese el número de cobro a modificar (X para salir): ", 25,4).lower()
            
            # Validación de salida
            if credit_id == "x":
                gotoxy(2,5); print(Fore.YELLOW + "Saliendo del menú de actualización..." + Fore.WHITE)
                time.sleep(1)
                return
            
            # Validación numérica
            if not credit_id.isdigit():
                gotoxy(2,5); print(Fore.RED + "ERROR: Debe ingresar un valor numérico" + Fore.WHITE)
                time.sleep(1.5)
                gotoxy(2,5); print(" "*50)  # Limpiar mensaje
                continue
                
            # Buscar el crédito
            credit_edit = self.data_service.CreditSales.get(int(credit_id))
            
            # Validaciones de estado
            if credit_edit is None:
                gotoxy(2,5); print(Fore.RED + "❌ No se encontró una deuda con este código" + Fore.WHITE)
                time.sleep(1.5)
                gotoxy(2,5); print(" "*50)
                continue
                
            if credit_edit.state == "Pagado":
                gotoxy(2,5); print(Fore.YELLOW + "⚠️ Esta deuda ya está completamente pagada - No se puede modificar" + Fore.WHITE)
                time.sleep(2)
                continue
                
            if credit_edit.state == "Pendiente":
                gotoxy(2,5); print(Fore.BLUE + "ℹ️  Esta deuda no tiene pagos registrados - Registre un pago primero" + Fore.WHITE)
                time.sleep(2)
                continue
            break   

        # Mostrar detalles del crédito
        gotoxy(5,5); print(Fore.GREEN + "━"*50)
        gotoxy(5,6); print(f"📄 Número de factura : {credit_edit.invoice_id:>10}")
        gotoxy(5,7); print(f"📅 Fecha de factura  : {credit_edit.date_credit:>12}")
        gotoxy(5,8); print(f"💵 Total crédito     : $ {credit_edit.total_credit:>10,.2f}")
        gotoxy(5,9); print(f"💰 Total pagado      : $ {(credit_edit.total_credit - credit_edit.credit_balance):>10,.2f}")
        gotoxy(5,10); print(f"⚖️  Saldo pendiente   : $ {credit_edit.credit_balance:>10,.2f}")
        gotoxy(5,11); print(Fore.GREEN + "━"*50)  
        gotoxy(5,12); print(Fore.GREEN + "    ---  DETALLE DE PAGOS  ----")  

        line = 1
        # Mostrar lista de pagos
        for item in credit_edit.payments:
            gotoxy(10, 13+line); print(f"{item.id:<4} {item.date_pay.strftime('%d/%m/%Y'):<10} ${item.value_pay:>10,.2f}")
            line += 1

        ids = [item.id for item in credit_edit.payments]
        id_select = -1

        while True:
            gotoxy(10, 13+line)
            id_result = input(Fore.CYAN + "Seleccione el ID de pago a modificar (X para cancelar): " + Fore.WHITE).lower()
            
            if id_result == "x":
                gotoxy(10, 14+line); print(Fore.YELLOW + "Operación cancelada por el usuario" + Fore.WHITE)
                time.sleep(1)
                return
            
            if not id_result.isdigit():
                gotoxy(10, 14+line); print(Fore.RED + "❌ Error: Debe ingresar un número válido" + Fore.WHITE)
                time.sleep(1.5)
                gotoxy(10, 14+line); print(" "*50)  # Limpiar mensaje
                continue
            
            id_result = int(id_result)
            if id_result not in ids:
                gotoxy(10, 14+line); print(Fore.RED + f"⚠️ El ID {id_result} no existe en la lista de pagos" + Fore.WHITE)
                time.sleep(1.5)
                gotoxy(10, 14+line); print(" "*50)  # Limpiar mensaje
                continue
            
            id_select = id_result
            break

        while True:
            try:
                # Eliminar pago seleccionado
                credit_edit.payments_collection.remove(id_select)
                
                # Solicitar nuevo valor
                gotoxy(5,15+line);print(Fore.MAGENTA +  "Ingrese el nuevo monto del pago:" + Fore.WHITE)
                newValue = self.validar.solo_decimales("Ingrese el nuevo monto del pago:",38, 15+line)

                # Validar que no exceda el saldo
                if credit_edit.credit_balance < newValue:
                    gotoxy(5,16+line)
                    print(Fore.RED + f"⚠️ Saldo deuda: ${credit_edit.credit_balance:.2f} - No puede cobrar más" + Fore.WHITE)
                    time.sleep(2)
                    gotoxy(5,16+line); print(" "*60)  # Limpiar mensaje
                    continue

                # Solicitar nueva fecha
                gotoxy(5,16+line)
                print(Fore.MAGENTA + "Fecha del pago (DD/MM/YYYY):" + Fore.WHITE)
                newdate = self.validar.validar_fecha("Formato: DD/MM/YYYY", 35, 16+line)
                date_pay = datetime.strptime(newdate, "%d/%m/%Y").date()

                # Registrar nuevo pago
                credit_edit.payments_collection.add(date_pay, newValue)
                gotoxy(5,18+line)
                print(Fore.GREEN + "✔ Pago actualizado correctamente" + Fore.WHITE)
                break

            except ValueError as e:
                gotoxy(5,18+line)
                print(Fore.RED + f"❌ Error: {str(e)}" + Fore.WHITE)
                time.sleep(2)
                gotoxy(5,18+line); print(" "*50)  # Limpiar mensaje
                continue

        # Confirmar cambios
        gotoxy(5,20+line)
        result = input(Fore.YELLOW + "¿Confirmar guardar los cambios? (S/N): " + Fore.WHITE).lower()

        if result == "s":
            resul_update =  self.data_service.CreditSales.update(credit_edit)
            gotoxy(5,22+line)
            if  resul_update:
                print(Fore.GREEN + "✅ Cambios guardados exitosamente!" + Fore.WHITE)
            else :
                print("❌ Operación cancelada - No se guardaron cambios")    
        else:
            gotoxy(5,22+line)
            print(Fore.YELLOW + "❌ Operación cancelada - No se guardaron cambios" + Fore.WHITE)

        time.sleep(1.5)
        return


    def delete(self) -> None:
        ...

    def consult(self) ->None:

        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de cobros"+" "*35+"██")
        gotoxy(2,4);invoice_num= input("Ingrese num. cobro: ")

        if invoice_num.isdigit():
            invoice_num = int(invoice_num)

            invoice = self.data_service.CreditSales.get(invoice_num)
                        
            # --- Imprimir cabecera de la factura ---
            if invoice is None:
                print(Fore.RED + "No hay datos...")
                time.sleep(1)
                return
     
            print("\n" + "=" * 50)
            print(f"CREDITO N°: {invoice.id} ESTADO: {invoice.state}".center(50))
            print("=" * 50)
            print(f"Fecha: {invoice.date_credit}")
            print(f"Cliente.: {invoice.dni} {invoice.full_name}")
         
            # --- Tabla de productos (detalle) ---
            table = PrettyTable()
            table.field_names = ["Fecha de pago", "valor"]
            table.align["Fecha de pago"] = "l"   
            table.align["valor"] = "r"


            for item in invoice.payments:

                table.add_row([f"{item.date_pay:}", f"$ {item.value_pay:,.2f}"])

            print(table)

            # --- Totales ---
            print("\n" + "-" * 50)
            print(f"Total credito  : ${invoice.total_credit:,.2f}".rjust(50))
            print(f"Pagado         : ${round(invoice.total_credit  - invoice.credit_balance,2):,.2f}".rjust(50))
            print(f"Saldo pendiente: ${invoice.credit_balance:,.2f}".rjust(50))
            print("=" * 50)
            print(f"ESTADO DE LA DEUDA: {invoice.state}".rjust(50).upper())
            print("=" * 50)

        else:    

            invoices:list[CreditSalesModel] = self.data_service.CreditSales.get_all()
            print("")
            for fac in invoices:
                print(
                    "{:<4} {:<12} {:<14} {:<25} {:>10,.2f} {:>10,.2f} {:<10}".format(  # Total alineado a la derecha (>)
                        fac.id,
                        fac.date_credit,
                        fac.dni, 
                        fac.full_name, 
                        fac.total_credit,
                        fac.credit_balance,
                        fac.state
                    )
                )

            totalCredit = reduce(lambda total, invoice: round(total+ invoice.total_credit,2),invoices,0)
            salso_pendiente = reduce(lambda total, invoice: round(total+ invoice.credit_balance,2),invoices,0)

            totales_map = list(map(lambda invoice: 1 if invoice.credit_balance > 0 else 0, invoices))
            cantidad_con_deuda = sum(totales_map)

            #print("filter cliente: ",total_client)
            #print(f"map Facturas:{totales_map}")
            print(f"            _____________________________________")
            print(f"              Credito total:{totalCredit:>10,.2f}")
            print(f"               Total pagado:{totalCredit - salso_pendiente:>10,.2f}")
            print(f"      Total saldo pendiente:{(salso_pendiente):>10,.2f}")
            print(f"facturas pendientes de pago:{cantidad_con_deuda:>10}")
            print("")
        print(Fore.RED+ "Presione cualquier tecla para continuar...")
        msvcrt.getch()  
