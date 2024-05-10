from scr.features.model.mappers.red_neuronal_mapper import RedNeuronalMapper
from scr.features.model.producto_model import Producto

class ProductoMapper: 
    @staticmethod
    def from_json(dict): 
        
        return Producto(
            id=dict['id'],
            name=dict['name'],
            ean=dict['ean'],
            foto=dict['foto'],
            volumetira=dict['volumetria'],
            created_at=dict['created_at'],
            updated_at=dict['updated_at'],
            red_neuronal_id=dict['red_neuronal_id'],
            red_neuronal= None if dict['red_neuronal'] == None else RedNeuronalMapper.from_json(dict['red_neuronal']),
        )