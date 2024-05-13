from typing import Literal
from dataclasses import dataclass


@dataclass
class GetGoodsRequestData:
    gender: Literal['male', 'female']
    sizes: list[str]
    colors: list[str]



@dataclass
class GetGoodResponseData: ...
