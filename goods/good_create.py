from .models import DeliveryAndReturn, Material, Color, Good, Feature, FabricCare, Photo, Size, Category
from .rest_models.create import CreateGoodRequestData


class CreateTemplateMethod():
    def get_create_data(self, data) -> dict:
        init_data = {}
        for key, value in data.items():
            init_data[key] = value
        return init_data

    def create(self, data) -> int:
        data_ready_for_unpack = self.get_create_data(data)
        model_instance = self.model(**data_ready_for_unpack)
        model_instance.save()
        return model_instance.pk
    

class MaterialCreation(CreateTemplateMethod):
    def __init__(self) -> None:
        super().__init__()
        self.model = Material


class ColorCreation(CreateTemplateMethod):
    def __init__(self) -> None:
        super().__init__()
        self.model = Color


class PhotoCreation(CreateTemplateMethod):
        
    def __init__(self) -> None:
        super().__init__()
        self.model = Photo


class SizeCreation(CreateTemplateMethod):
    def __init__(self) -> None:
        super().__init__()
        self.model = Size


class DeliveryAndReturnCreation(CreateTemplateMethod):
    def __init__(self) -> None:
        super().__init__()
        self.model = DeliveryAndReturn


class GoodCreation:
    def __init__(self, data: CreateGoodRequestData) -> None:
        self.data = data
        self.model_instanse = Good()

    def set_good_name(self):
        self.model_instanse.good_name = self.data.good_name

    def set_price(self):
        self.model_instanse.price = self.data.price

    def set_material(self):
        material = Material.objects.get_or_create(material = self.data.material, defaults={'material': self.data.material})
        material[0].save()
        self.model_instanse.material = material[0]

    def set_description(self):
        self.model_instanse.description = self.data.description

    def set_colors(self):
        for color in self.data.colors:
            color = Color.objects.get_or_create(color=color, defaults={'color': color})
            self.model_instanse.colors.add(color[0])
    
    def set_match_with(self):
        for match_id in self.data.match_with or []:
            self.model_instanse.match_with.add(
                Good.objects.get(id=match_id)
            )
    
    def set_sizes(self):
        for size in self.data.sizes:
            size = Size.objects.get_or_create(size=size)[0]
            self.model_instanse.sizes.add(size)

    def set_delivery_and_return(self):
        for delivery_and_return_id in self.data.delivery_and_return or []:
            self.model_instanse.sizes.add(
                DeliveryAndReturn.objects.get(id=delivery_and_return_id)
            )

    def set_features(self):
        for feature in self.data.features:
            feature = Feature(good=self.model_instanse, feature=feature)
            feature.save()

    def set_category(self):
        category = Category.objects.get_or_create(name=self.data.category['name'], defaults={'name': self.data.category['name'], 'gender': self.data.category['gender']})
        self.model_instanse.category = category[0]

    def set_fabric_cares(self):
        for fabric_care in self.data.fabric_cares:
            care = FabricCare(good=self.model_instanse, fabric_care=fabric_care)
            care.save()

    def set_photos(self):
        for photo in self.data.photos:
            photo = Photo.objects.get(pk = photo)
            self.model_instanse.photos.add(photo)

    def create(self) -> int:
        self.set_good_name()
        self.set_price()
        self.set_material()
        self.set_description()
        self.set_category()
        self.model_instanse.save()
        self.set_photos()
        self.set_features()
        self.set_colors()
        self.set_match_with()
        self.set_sizes()
        self.set_fabric_cares()
        self.set_delivery_and_return()
        self.model_instanse.save()
        return self.model_instanse.pk
