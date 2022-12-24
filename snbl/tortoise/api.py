from rest_framework import viewsets
from tortoise.serializers import (
    PlanSerializer,
    PromotionSerializer,
    CustomerGoalsWriteSerializer,
    CustomerGoalsReadSerializer,
)
from tortoise.models import Plan, Promotion, CustomerGoals


class PlanView(viewsets.ModelViewSet):
    serializer_class = PlanSerializer
    lookup_field = "planID"
    queryset = Plan.objects.all()


class PromotionView(viewsets.ModelViewSet):
    serializer_class = PromotionSerializer
    lookup_field = "promotionID"
    queryset = Promotion.objects.all()


class CustomerGoalsView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action in {"create"}:
            return CustomerGoalsWriteSerializer
        else:
            return CustomerGoalsReadSerializer

    queryset = CustomerGoals.objects.all().select_related("plan")
