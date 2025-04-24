import json
from re import L
from typing import Any, Dict, List, Union
from interfaces.iJson import iJson

class JsonFile(iJson):
    
    def __init__(self, filename):
        self.filename:str = filename

    def save(self, data):
        """Guarda los datos siempre como lista, incluso si hay un solo elemento."""
        with open(self.filename, 'w') as file:
            json.dump(data if isinstance(data, list) else [data], file, indent=4)

    def update(self, new_data):
        """
        Actualiza uno o varios registros en el archivo JSON.
        
        Args:
            new_data (dict|list): Puede ser:
                - Un diccionario con los datos actualizados (debe contener 'id')
                - Una lista de diccionarios para múltiples actualizaciones
        
        Returns:
            bool: True si se realizó al menos una actualización, False en caso contrario
        """
        try:
            # Leer datos existentes
            current_data = self.read()
            
            # Convertir a lista si es un solo item
            items_to_update = new_data if isinstance(new_data, list) else [new_data]
            
            # Crear diccionario de búsqueda por ID
            data_dict = {item['id']: item for item in current_data}
            updated = False
            
            for item in items_to_update:
                if 'id' not in item:
                    continue
                    
                item_id = item['id']
                if item_id in data_dict:
                    data_dict[item_id] = item  # Actualizar el item
                    updated = True
            
            if updated:
                # Convertir de vuelta a lista y guardar
                updated_data = list(data_dict.values())
                self.save(updated_data)
            
            return updated
            
        except Exception as e:
            print(f"Error al actualizar datos: {str(e)}")
            return False

    def delete(self, ids: Union[int, List[int]]) -> int:
        try:
            data = self.read()
            
            # Asegurar que 'data' sea siempre una lista
            if not isinstance(data, list):
                data = [data] if data else []  # Convierte a lista si es un solo dict
            
            original_count = len(data)
            ids_to_delete = [ids] if isinstance(ids, int) else ids
            new_data = [item for item in data if item.get('id') not in ids_to_delete]
            deleted_count = original_count - len(new_data)
            
            if deleted_count > 0:
                # Guardar como lista, incluso si queda vacía o con un solo elemento
                self.save(new_data if new_data else [])
            
            return deleted_count
        except Exception as e:
            print(f"Error al eliminar: {str(e)}")
            return 0


    def read(self) ->List[Any]:
        try:
            with open(self.filename,'r',  encoding='utf-8') as file:
                data = json.load(file)# load:carga datos desde un archivo json
        except FileNotFoundError:
            data = []
        return data
    
    def find(self,atributo,buscado) ->list[dict[str, Any]]:
        try:
            datas = self.read()
            data = [item for item in datas if item[atributo] == buscado ]
        except FileNotFoundError:
            data = []
        return data
        
    def search(self, fields: Union[str, List[str]], sought: Any, exact_match: bool = False) -> List[Dict]:

        # Normalización de campos
        if isinstance(fields, str):
            fields = [f.strip() for f in fields.split(",")] if "," in fields else [fields]
        
        try:
            with open(self.filename, 'r') as file:
                datas = json.load(file)
                sought = str(sought).lower()
                
                return [
                    item for item in datas
                    if isinstance(item, dict) and  # Asegurar que es diccionario
                    any(
                        sought in str(item.get(field, '')).lower() if not exact_match
                        else str(item.get(field, '')).lower() == sought
                        for field in fields
                    )
                ]
                
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Error: Archivo JSON corrupto")
            return []


