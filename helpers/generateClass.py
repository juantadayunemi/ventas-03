from typing import Any, Dict

def generate_class(class_name: str, attributes: Dict[str, str]) -> str:
    # separar atributos obligatorios y opcionales
    required_attrs = {}
    optional_attrs = {}
    
    for attr, attr_def in attributes.items():
        if isinstance(attr_def, tuple) and len(attr_def) == 2:
            # formato: 'attr': ('type', default_value)
            optional_attrs[attr] = attr_def
        elif '=' in str(attr_def):
            # formato: 'attr': 'type = default_value'
            attr_type, default_value = map(str.strip, attr_def.split('=', 1))
            optional_attrs[attr] = (attr_type, default_value)
        else:
            # Atributo obligatorio
            required_attrs[attr] = attr_def
    
    # generar el metodo __init__
    init_params = []
    init_body = []
    
    # parm obligatorios
    for attr, attr_type in required_attrs.items():
        init_params.append(f"{attr}: {attr_type}")
        init_body.append(f"        self.__{attr}: {attr_type} = {attr}")
    
    # parm opcionales
    for attr, (attr_type, default_value) in optional_attrs.items():
        init_params.append(f"{attr}: {attr_type} = {default_value}")
        init_body.append(f"        self.__{attr}: {attr_type} = {attr}")
    
    init_code = f"    def __init__(self, {', '.join(init_params)}) -> None:\n" + "\n".join(init_body)
    
    # Generar propiedades
    properties_code = ""
    all_attrs = {**required_attrs, **optional_attrs}
    for attr, attr_type in all_attrs.items():
        if isinstance(attr_type, tuple):  # Para atributos opcionales
            attr_type = attr_type[0]
        
        properties_code += f"""
    @property
    def {attr}(self) -> {attr_type}:
        return self.__{attr}
        
    @{attr}.setter
    def {attr}(self, value: {attr_type}) -> None:
        self.__{attr} = value
"""
    
    # Generar método getJson
    json_properties = []
    for attr in all_attrs.keys():
        json_properties.append(f'            "{attr}": self.{attr}')
    
    get_json_code = f"""
    @property
    def getJson(self) -> dict[str, Any]:
        return {{
{',\n'.join(json_properties)}
        }}
"""
    
    # Generar comentario con la estructura de atributos
    attrs_comment = "\n    # Atributos usados para generar esta clase:\n"
    attrs_comment += "    # {\n"
    for attr, attr_def in attributes.items():
        attrs_comment += f"    #     '{attr}': '{attr_def}',\n"
    attrs_comment += "    # }"
    
    # Construir la clase completa
    class_code = f"class {class_name}:\n{init_code}\n{properties_code}{get_json_code}{attrs_comment}"
    return class_code


if __name__ == "__main__":
    supplier_attrs =  {
        'id': 'int = 1',
        'fecha_pago':'date',
        'creditoVenta_id': 'int = 0',
        'valor': 'float = 0'
    }

    print('\33c')
    print(generate_class("PagoCredito", supplier_attrs))

    print()