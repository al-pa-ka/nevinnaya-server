from django.test import TestCase
from .form_order import OrderInfo, GoodInOrder, Order
from .models import Good, Material, Color
import django
# Create your tests here.



class TestOrderForm(TestCase):
    def setUp(self) -> None:
        material = Material.objects.create(material='Шёлк 100%')
        Color.objects.create(color='БЕЖЕВЫЙ')
        Color.objects.create(color='ЧЕРНЫЙ')
        test_good = Good.objects.create(good_name='пальто', price=17000, material=material, description='невероятно точное описание')
        test_good.colors.add(1)
        test_good.colors.add(2)

        return super().setUp()
    
    @django.test.utils.override_settings(
    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
    def test_order_form(self):
        data: OrderInfo = OrderInfo(need_delivery=True, delivery_type='COURIER_SERVICE', address='wwwWawa', 
                                    goods=[GoodInOrder(pk=1, size='s', color='БЕЖЕВЫЙ', quantity=10)], email='polyanin.04@mail.ru')
        order = Order(data)
        print(order.to_string())
        order.send_to_managers()

