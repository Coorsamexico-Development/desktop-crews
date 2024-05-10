from typing import Union


class RedNeuronal:
    def __init__(self, id:int, name:str, created_at:Union[str, None], updated_at:Union[str, None]):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

        