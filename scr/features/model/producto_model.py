from typing import Union

from scr.features.model.red_neuronal_model import RedNeuronal

class Producto:
    def __init__(self, id:int, ean:str, 
                    name:str, 
                    foto:Union[str, None],
                    volumetira:str, created_at:Union[str, None], 
                    updated_at:Union[str, None],
                    red_neuronal_id:Union[str, None],
                    red_neuronal:Union[RedNeuronal, None]
                    ):
        self.id = id
        self.ean = ean
        self.name = name
        self.foto = foto
        self.volumetira = volumetira
        self.created_at = created_at
        self.updated_at = updated_at
        self.red_neuronal_id = red_neuronal_id
        self.red_neuronal = red_neuronal