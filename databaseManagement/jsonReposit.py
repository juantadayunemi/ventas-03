import json
import os
from typing import Type, TypeVar, Generic, Optional, List, Dict, Any
from pathlib import Path

T = TypeVar('T', bound='BaseModel') # type: ignore

class JSONRepository(Generic[T]):
    """Generic JSON repository with support for auto-increment IDs and nested detail handling"""
    
    ROOT_DB_FOLDER = "database"
    FILE_EXTENSION = ".json"
    
    def __init__(self,entity_class: Type[T],table_name: Optional[str] = None,custom_path: Optional[str] = None )->None:
        self.entity_class = entity_class
        self.table_name = table_name or entity_class.__name__.lower()
        
        # Configure paths
        if custom_path:
            self.base_path = os.path.join(custom_path, self.ROOT_DB_FOLDER)
        else:
            self.base_path = os.path.join(self.ROOT_DB_FOLDER, self.table_name)
        
        os.makedirs(self.base_path, exist_ok=True) # crea la carpeta en caso de que no exista
        self._file_path = os.path.join(self.base_path, f"{self.table_name}{self.FILE_EXTENSION}")


    def add(self, item: T) -> T:
        try:
            # Handle auto-increment for main entity
            if getattr(item, 'id', None) is None or item.id <= 0:
                existing_data = self._read_all_data()
                new_id = max(existing_data.keys(), default=0) + 1
                item.id = new_id

            # Handle auto-increment for nested details if they exist
            if hasattr(item, 'details') and isinstance(item.details, list):
                self._assign_detail_ids(item)

                   # Auto-increment para pagos si existen
            if hasattr(item, 'payments') and isinstance(item.payments, list):
                self._assign_payment_ids(item)

       
            existing_data = self._read_all_data()
            existing_data[item.id] = item.to_dict()
            data_to_save = list(existing_data.values())
            filename = self._file_path

            self._save_data(filename, data_to_save)
            return item
            
        except Exception as e:
            print(f"Error saving entity: {e}")
            raise

    def update(self, item: T) -> bool:
        if not hasattr(item, 'id') or item.id is None:
            raise ValueError("ID is required for update")

        try:
            # Handle auto-increment for nested details
            if hasattr(item, 'details') and isinstance(item.details, list):
                self._assign_detail_ids(item)
                
            if hasattr(item, 'payments') and isinstance(item.payments, list):
                self._assign_payment_ids(item)


            existing_data = self._read_all_data()
            if item.id not in existing_data:
                return False
            existing_data[item.id] = item.to_dict()
            data_to_save = list(existing_data.values())
            filename = self._file_path
         

            self._save_data(filename, data_to_save)
            return True
            
        except Exception as e:
            print(f"Error updating entity: {e}")
            return False

    def remove(self, entity_id: int) -> bool:
            """Elimina una entidad por su ID. Retorna True si se eliminó correctamente."""
            try:
                existing_data = self._read_all_data()
                
                if entity_id not in existing_data:
                    return False
                    
                del existing_data[entity_id]
                self._save_data(self._file_path, list(existing_data.values()))
                return True
                
            except Exception as e:
                print(f"Error removing entity {entity_id}: {e}")
                return False
            
    def get(self, entity_id) -> Optional[T]:
        """busqueda de entidades  po id (primary key)"""
        if not os.path.exists(self._file_path):
            return None
            
        try:
            with open(self._file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

                item_data = next((item for item in data if item['id'] == entity_id), None)
                return self.entity_class.from_dict(item_data) if item_data else None
      
                
        except Exception as e:
            print(f"Error loading entity {entity_id}: {e}")
            return None

    def find(self, field: str, value: Any) -> List[T]:
        """Busca entidades donde el campo coincida con el valor"""
        all_entities = self.get_all()
        return [
            entity for entity in all_entities 
            if getattr(entity, field, None) == value
        ]
        
    def search(self, fields: List[str], search_term: str) -> List[T]:
        """Busca entidades donde el término aparezca en cualquiera de los campos especificados"""
        search_term = search_term.lower()
        return [
            entity for entity in self.get_all()
            if any(
                search_term in str(getattr(entity, field, '')).lower()
                for field in fields
            )
        ]

    def get_all(self) -> List[T]:
        try:
           
            if not os.path.exists(self._file_path):
                return []
            
            with open(self._file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [self.entity_class.from_dict(item) for item in data]
         
        except Exception as e:
            print(f"Error loading all entities: {e}")
            return []
     
    def _assign_detail_ids(self, item: T) -> None:
        """Assign auto-increment IDs to nested details"""
        existing_details = []
        
        existing_data = self._read_all_data()
        existing_details = [
            detail for entity in existing_data.values() 
            for detail in entity.get('details', [])
        ]
        
        # Get max detail ID from existing data or from current item's details
        max_detail_id = max(
            [d.get('id', 0) for d in existing_details] +
            [d.id for d in item.details if hasattr(d, 'id') and d.id > 0],
            default=0
        )
        
        # Assign IDs to details without IDs
        next_id = max_detail_id + 1
        for detail in item.details:
            if getattr(detail, 'id', None) is None or detail.id <= 0:
                detail.id = next_id
                next_id += 1

    def _assign_payment_ids(self, item: T) -> None:
        """Asigna IDs autoincrementales a los pagos"""

        existing_data = self._read_all_data()
        existing_payments = [
            payment for entity in existing_data.values() 
            for payment in entity.get('payments', [])
        ]

        max_payment_id = max(
                [p.get('id', 0) for p in existing_payments] +
                [p.id for p in item.payments if hasattr(p, 'id') and p.id > 0],
                default=0
            )
        
        next_id = max_payment_id + 1
        for payment in item.payments:
            if getattr(payment, 'id', None) is None or payment.id <= 0:
                payment.id = next_id
                next_id += 1
                
    def _read_all_data(self) -> Dict[int, Dict[str, Any]]:
        """Read all data and return as {id: item_data} dictionary"""
              
        if not os.path.exists(self._file_path):
            return {}
            
        with open(self._file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {item['id']: item for item in data}

    def _save_data(self, filename: str, data: Any) -> None:
        """Save data to file with proper formatting"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _get_existing_ids(self) -> List[int]:
        """Get all existing IDs for individual files mode"""
        return list(self._read_all_data().keys())
            
    
