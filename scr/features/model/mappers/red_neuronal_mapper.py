from model.red_neuronal_model import RedNeuronal

class RedNeuronalMapper: 
    @staticmethod
    def from_json(dict): 
        return RedNeuronal(
            id=dict['id'],
            name=dict['name'],
            created_at=dict['created_at'],
            updated_at=dict['updated_at'],
        )