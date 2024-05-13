from abc import ABC
from django.db.models import Model
from django.db.models import Manager
from .models import Good, Color, Size, FabricCare, Feature, Photo, DeliveryAndReturn, Material, Category
from .serializers import SizeSerializer, ColorSerializer, GoodSerializer, DeliveryAndReturnSerializer, MaterialSerializer, PhotoSerializer, FabricCareSerializer, CategorySerializer
from .filters_factory import FilterFactory, GoodFilterFactory, DefaultFilterFactory




class ModelPrototype:
    def __init__(self, filter_factory, model, serializer, **data) -> None:
        self.filter_factory: FilterFactory = filter_factory
        self.model: Model = model
        self.serializer = serializer
        self.data = data
        
    def serialize(self, model_instances: Manager[Model], **kwargs) -> dict:
        return self.serializer(model_instances, many=True, context=kwargs).data

    def get(self) -> Manager[Model]:
        filters = self.filter_factory.get_filters(self.data)
        print(filters)
        return self.model.objects.filter(**filters)


class ModelAbstractFactory:
    def build(self, **data) -> ModelPrototype: ...



class GoodFactory(ModelAbstractFactory):
    def build(self, **data) -> ModelPrototype:
        filter_factory = GoodFilterFactory()
        return ModelPrototype(filter_factory, Good, GoodSerializer, **data)

class SizeFactory(ModelAbstractFactory):
    def build(self, **data) -> ModelPrototype:
        filter_factory = DefaultFilterFactory()
        return ModelPrototype(filter_factory, Size, SizeSerializer, **data)
    
class PhotosFactory(ModelAbstractFactory):
    def build(self, **data) -> ModelPrototype:
        filter_factory = DefaultFilterFactory()
        return ModelPrototype(filter_factory, Photo, PhotoSerializer, **data)
    
class ColorFactory(ModelAbstractFactory):
    def build(self, **data) -> ModelPrototype:
        filter_factory = DefaultFilterFactory()
        return ModelPrototype(filter_factory, Color, ColorSerializer, **data)

class DeliveryAndReturnFactory(ModelAbstractFactory):
    def build(self, **data) -> ModelPrototype:
        filter_factory = DefaultFilterFactory()
        return ModelPrototype(filter_factory, DeliveryAndReturn, DeliveryAndReturnSerializer, **data)
    
class MaterialFactory(ModelAbstractFactory):
    def build(self, **data) -> ModelPrototype:
        filter_factory = DefaultFilterFactory()
        return ModelPrototype(filter_factory, Material, MaterialSerializer, **data)

class CaresFactory(ModelAbstractFactory):
    def build(self, **data) -> ModelPrototype:
        filter_factory = DefaultFilterFactory()
        return ModelPrototype(filter_factory, FabricCare, FabricCareSerializer, **data)    

class CategoryFactory(ModelAbstractFactory):
    def build(self, **data) -> ModelPrototype:
        filter_factory = DefaultFilterFactory()
        return ModelPrototype(filter_factory, Category, CategorySerializer, **data)    


class ModelsGetter:
    MODEL_NAME_MAP : dict[str, ModelAbstractFactory] = {
        'delivery_and_return': DeliveryAndReturnFactory(),
        'color': ColorFactory(),
        'material': MaterialFactory(),
        'photo': PhotosFactory(),
        'good': GoodFactory(),
        'size': SizeFactory(),
        'category': CategoryFactory(),
        'care': CaresFactory()
    }

    def get(self, model_name: str, **data) -> ModelPrototype:
        return self.MODEL_NAME_MAP[model_name].build(**data)
    