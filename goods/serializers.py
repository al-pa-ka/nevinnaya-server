from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
    CharField,
    SerializerMethodField,
)
from rest_framework import serializers
from .models import (
    Color,
    DeliveryAndReturn,
    Good,
    Material,
    Photo,
    Size,
    FabricCare,
    Category,
)
from .form_order import DELIVERY_TYPE_MAP


class ColorSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = ["pk", "color"]


class DeliveryAndReturnSerializer(ModelSerializer):
    option = StringRelatedField(source="point_name")

    class Meta:
        model = DeliveryAndReturn
        fields = ["pk", "option", "description", "extra"]


class FabricCareSerializer(ModelSerializer):
    care = StringRelatedField(source="fabric_care")

    class Meta:
        model = FabricCare
        fields = ["pk", "care"]


class MaterialSerializer(ModelSerializer):
    class Meta:
        model = Material
        fields = ["pk", "material"]


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = ["pk", "photo"]


class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = ["pk", "size"]


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["pk", "name", "gender"]


class GoodSerializer(ModelSerializer):
    sizes = StringRelatedField(many=True)
    # photos = StringRelatedField(many=True)
    photos = SerializerMethodField("build_photo_urls")
    colors = StringRelatedField(many=True)
    material = StringRelatedField()
    goodName = CharField(source="good_name")
    deliveryAndReturn = SerializerMethodField("delivery_and_return")
    fabricCares = StringRelatedField(source="fabric_cares.all", many=True)
    matchWith = SerializerMethodField("match_with")

    def build_photo_urls(self, obj):
        photos = []
        for photo in obj.photos.all():
            photo_url = self.context["request"].build_absolute_uri(str(photo))
            photos.append(photo_url)
        return photos

    def match_with(self, obj):
        print(obj.match_with.all())
        ids = [obj.pk for obj in obj.match_with.all()]
        print(ids)
        return ids

    def delivery_and_return(self, obj):
        return DeliveryAndReturnSerializer(
            obj.delivery_and_return.all(), many=True
        ).data

    class Meta:
        fields = [
            "sizes",
            "photos",
            "colors",
            "goodName",
            "price",
            "description",
            "features",
            "material",
            "deliveryAndReturn",
            "pk",
            "fabricCares",
            "matchWith",
        ]
        model = Good


class GoodInOrderSerializer(serializers.Serializer):
    pk: int = serializers.IntegerField()
    size: str = serializers.CharField()
    color: str = serializers.CharField()
    quantity: int = serializers.IntegerField()

    def validate(self, attrs):
        super().validate(attrs)
        print(self)
        good_sizes = map(
            lambda size: size.size, Good.objects.get(pk=attrs["pk"]).sizes.all()
        )
        good_sizes = list(good_sizes)
        print(good_sizes)
        print(attrs["size"])
        if attrs["size"] not in good_sizes:
            raise serializers.ValidationError("There is no such size")
        return attrs

    def validate_pk(self, value):
        ids = Good.objects.all().values_list("id", flat=True)
        if value not in ids:
            raise serializers.ValidationError("There is no good with such a pk")
        return value


class OrderFormSerializer(serializers.Serializer):
    goods = serializers.ListField(child=GoodInOrderSerializer())
    need_delivery = serializers.BooleanField()
    email = serializers.EmailField()
    delivery_type = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    def validate_delivery_type(self, value):
        if value not in DELIVERY_TYPE_MAP.keys():
            raise serializers.ValidationError("There is no such delivery type")

    def validate(self, attrs):
        need_delivery = attrs.get("need_delivery", None)
        delivery_type = attrs.get("delivery_type", None)
        super().validate(attrs)
        if need_delivery and not delivery_type:
            raise serializers.ValidationError(
                "delivery_type must be passed if need_delivery is true"
            )
        return attrs
