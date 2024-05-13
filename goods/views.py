from rest_framework.request import Request
from rest_framework.response import Response
from .models_factory import ModelsFactory
from .models_getter import ModelsGetter, ModelPrototype
from rest_framework.views import APIView
from .form_order import Order, OrderInfo, GoodInOrder

from .serializers import OrderFormSerializer

from users.users import Admin

# Create your views here.


class Test(APIView):
    @Admin.is_aunteficated
    def post(self, request):
        return Response("authentificated")


class NewOrder(APIView):
    def post(self, request: Request):
        print(request.data["order_info"])
        validator = OrderFormSerializer(data=request.data["order_info"])
        validator.is_valid(raise_exception=True)
        validated_data = validator.validated_data
        goods = validated_data["goods"]
        validated_data["goods"] = [GoodInOrder(**good) for good in goods]
        order_info = OrderInfo(**(validated_data))
        order = Order(order_info)
        order.send_to_managers()
        return Response()


class Read(APIView):
    def post(self, request: Request, model_name: str):
        print(request.data)
        reader = ModelsGetter()
        model: ModelPrototype = reader.get(model_name, **request.data)
        instances = model.get()
        return Response(model.serialize(instances, request=request))


class Create(APIView):
    # @Admin.is_aunteficated
    def post(self, request: Request, model_name: str):
        factory = ModelsFactory()
        instance_id = factory.create(model_name, request.data)
        return Response({"pk": instance_id})
