from dataclasses import dataclass
from .models import Good
from django.db.models import Manager
from django.core.mail import EmailMessage

DELIVERY_TYPE_MAP = {
    "DELIVERY_SERVICE": "службой доставки (СДЭК)",
    "COURIER_SERVICE": "курьером",
    "SELF_SERIVICE": "самовывоз",
}


@dataclass
class GoodInOrder:
    pk: int
    size: str
    color: str
    quantity: int


@dataclass
class OrderInfo:
    goods: list[GoodInOrder]
    need_delivery: bool
    email: str
    delivery_type: str | None = None
    address: str | None = None


class Order:
    def __init__(self, order_info: OrderInfo) -> None:
        self.order_info = order_info

    def send_to_managers(self):  # test
        print("in send message")
        # send_mail('subject', self.to_string(), 'polyanin.aleksey.00@mail.ru',  recipient_list=['polyanin.aleksey.00@mail.ru'], fail_silently=False)
        message = EmailMessage(
            "Новый заказ",
            self.to_string(),
            "polyanin.aleksey.00@mail.ru",
            to=["polyanin.aleksey.00@mail.ru"],
        )
        message.send(fail_silently=False)

    def get_goods_models(self) -> Manager[Good]:
        return Good.objects.filter(
            pk__in=list(map(lambda x: x.pk, self.order_info.goods))
        )

    def get_good_by_pk(self, pk: int):
        return Good.objects.get(pk=pk)

    def to_string(self):
        result = ""
        for good in self.order_info.goods:
            result += f"Наименование товара {self.get_good_by_pk(good.pk).good_name}\nЦвет {good.color}\nКоличество {good.quantity}\nРазмер {good.size}\n"
        if self.order_info.need_delivery:
            result += f"Адрес доставки {self.order_info.address}, {DELIVERY_TYPE_MAP[self.order_info.delivery_type]}\n"
        result += f"email покупателя {self.order_info.email}\n"
        result += f"Общая стоимость {self.calculate_total_price()}\n"
        return result

    def get_quantity(self, good_pk: int):
        for good in self.order_info.goods:
            if good_pk == good.pk:
                return good.quantity

    def calculate_total_price(self) -> int:
        goods = self.get_goods_models()
        price = 0
        for good in goods:
            price += good.price * self.get_quantity(good.pk)
        if self.order_info.need_delivery:
            price += 690
        return price
