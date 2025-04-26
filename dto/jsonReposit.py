import json
import os
from typing import Type, TypeVar, Generic, Optional, List, Dict, Any
from pathlib import Path

T = TypeVar('T', bound='BaseModel')

class JSONRepository(Generic[T]):
    """Generic JSON repository with support for auto-increment IDs and nested detail handling"""
    
    ROOT_DB_FOLDER = "database"
    FILE_EXTENSION = ".json"
    
    def __init__(
        self,
        entity_class: Type[T],
        table_name: Optional[str] = None,
        custom_path: Optional[str] = None,
        single_file: bool = True
    ):
        self.entity_class = entity_class
        self.single_file = single_file
        self.table_name = table_name or entity_class.__name__.lower()
        
        # Configure paths
        if custom_path:
            self.base_path = os.path.join(custom_path, self.ROOT_DB_FOLDER)
        else:
            self.base_path = os.path.join(self.ROOT_DB_FOLDER, self.table_name)
        
        os.makedirs(self.base_path, exist_ok=True)
        self.single_file_path = os.path.join(self.base_path, f"{self.table_name}{self.FILE_EXTENSION}")

    def get_entity_filename(self, entity_id) -> str:
        return self.single_file_path if self.single_file else \
               os.path.join(self.base_path, f"{self.table_name}_{entity_id}{self.FILE_EXTENSION}")

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

            if self.single_file:
                existing_data = self._read_all_data()
                existing_data[item.id] = item.to_dict()
                data_to_save = list(existing_data.values())
                filename = self.single_file_path
            else:
                filename = self.get_entity_filename(item.id)
                data_to_save = item.to_dict()

            self._save_data(filename, data_to_save)
            return item
            
        except Exception as e:
            print(f"Error saving entity: {e}")
            raise

    def _assign_detail_ids(self, item: T) -> None:
        """Assign auto-increment IDs to nested details"""
        existing_details = []
        if self.single_file:
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

    def update(self, item: T) -> bool:
        if not hasattr(item, 'id') or item.id is None:
            raise ValueError("ID is required for update")

        try:
            # Handle auto-increment for nested details
            if hasattr(item, 'details') and isinstance(item.details, list):
                self._assign_detail_ids(item)

            if self.single_file:
                existing_data = self._read_all_data()
                if item.id not in existing_data:
                    return False
                existing_data[item.id] = item.to_dict()
                data_to_save = list(existing_data.values())
                filename = self.single_file_path
            else:
                filename = self.get_entity_filename(item.id)
                if not os.path.exists(filename):
                    return False
                data_to_save = item.to_dict()

            self._save_data(filename, data_to_save)
            return True
            
        except Exception as e:
            print(f"Error updating entity: {e}")
            return False

    def get(self, entity_id) -> Optional[T]:
        filename = self.get_entity_filename(entity_id)
        if not os.path.exists(filename):
            return None
            
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if self.single_file:
                    item_data = next((item for item in data if item['id'] == entity_id), None)
                    return self.entity_class.from_dict(item_data) if item_data else None
                return self.entity_class.from_dict(data)
                
        except Exception as e:
            print(f"Error loading entity {entity_id}: {e}")
            return None

    def get_all(self) -> List[T]:
        try:
            if self.single_file:
                if not os.path.exists(self.single_file_path):
                    return []
                with open(self.single_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [self.entity_class.from_dict(item) for item in data]
            else:
                pattern = f"{self.table_name}_*{self.FILE_EXTENSION}"
                return [
                    self.entity_class.from_dict(json.load(open(file, 'r', encoding='utf-8')))
                    for file in Path(self.base_path).glob(pattern)
                ]
        except Exception as e:
            print(f"Error loading all entities: {e}")
            return []

    def _read_all_data(self) -> Dict[int, Dict[str, Any]]:
        """Read all data and return as {id: item_data} dictionary"""
        if not self.single_file:
            raise NotImplementedError("This method is only for single-file mode")
            
        if not os.path.exists(self.single_file_path):
            return {}
            
        with open(self.single_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {item['id']: item for item in data}

    def _save_data(self, filename: str, data: Any) -> None:
        """Save data to file with proper formatting"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _get_existing_ids(self) -> List[int]:
        """Get all existing IDs for individual files mode"""
        if self.single_file:
            return list(self._read_all_data().keys())
            
        pattern = f"{self.table_name}_*{self.FILE_EXTENSION}"
        ids = []
        for file in Path(self.base_path).glob(pattern):
            try:
                ids.append(int(file.stem.split('_')[-1]))
            except (ValueError, IndexError):
                continue
        return ids