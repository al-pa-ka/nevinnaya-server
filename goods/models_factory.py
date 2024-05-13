from .good_create import ColorCreation, SizeCreation, MaterialCreation, PhotoCreation, DeliveryAndReturnCreation, GoodCreation
from .rest_models.create import CreateGoodRequestData

class ModelsFactory:
    def create(self, model_name: str, data) -> int:
        if model_name == 'color':
            return ColorCreation().create(data)
        elif model_name == 'size':
            return SizeCreation().create(data)
        elif model_name == 'material':
            return MaterialCreation().create(data)
        elif model_name == 'photo':
            return PhotoCreation().create(data)
        elif model_name == 'delivery_and_return':
            return DeliveryAndReturnCreation().create(data)
        elif model_name == 'good':
            data = CreateGoodRequestData(**data)
            return GoodCreation(data).create()


