from django.db import models
import enum

# Create your models here.


class Genders(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    UNISEX = "UNISEX"


class Color(models.Model):
    color = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.color


class Size(models.Model):
    size = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.size


class Feature(models.Model):
    feature = models.CharField(max_length=200)
    good = models.ForeignKey("Good", on_delete=models.CASCADE, related_name="features")

    def __str__(self) -> str:
        return self.feature


class Material(models.Model):
    material = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.material


class FabricCare(models.Model):
    fabric_care = models.CharField(max_length=200)
    good = models.ForeignKey(
        "Good", on_delete=models.CASCADE, related_name="fabric_cares"
    )

    def __str__(self) -> str:
        return self.fabric_care


class Photo(models.Model):
    photo = models.ImageField(upload_to="static/photos")
    gender = models.CharField(max_length=50, default=Genders.UNISEX.value)

    def __str__(self):
        return self.photo.url


class DeliveryAndReturn(models.Model):
    point_name = models.CharField(max_length=200)
    description = models.TextField()
    extra = models.TextField()


class Category(models.Model):
    gender = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    name_for_women = models.CharField(max_length=100, null=True)
    name_for_men = models.CharField(max_length=100, null=True)


class Good(models.Model):
    good_name = models.CharField(max_length=100)
    price = models.IntegerField()
    material = models.ForeignKey(Material, on_delete=models.DO_NOTHING)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    colors = models.ManyToManyField(to=Color, related_name="colors")
    match_with = models.ManyToManyField(to="Good")
    photos = models.ManyToManyField(Photo, related_name="photos")
    sizes = models.ManyToManyField(Size, related_name="sizes")
    delivery_and_return = models.ManyToManyField(
        DeliveryAndReturn, related_name="delivery_and_returns"
    )
