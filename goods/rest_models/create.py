from dataclasses import dataclass


@dataclass
class DeliveryAndReturn:
    option: str
    extra: str
    description: str

@dataclass
class CreateGoodRequestData:
    description: str
    colors: list[str] 
    good_name: str
    fabric_cares: list[str]
    features: list[str]
    material: str 
    photos: list[int]
    sizes: list[str]
    price: int
    category: dict
    delivery_and_return: list[str] | None = None
    match_with: list[int] | None = None
