from rest_framework import serializers
from tortoise.models import Plan, Promotion, CustomerGoals


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = (
            "planID",
            "planName",
            "amountOptions",
            "tenureOptions",
            "benefitPercentage",
            "benefitType",
        )


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = (
            "promotionID",
            "name",
            "max_users",
            "start_date",
            "end_date",
            "benefitPercentage",
            "plan",
        )


class CustomerGoalsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerGoals
        fields = ("plan", "userID", "selectedAmount", "selectedTenure")


class CustomerGoalsReadSerializer(serializers.ModelSerializer):
    reward = serializers.SerializerMethodField()

    class Meta:
        model = CustomerGoals
        fields = (
            "plan",
            "userID",
            "selectedAmount",
            "selectedTenure",
            "depositedAmount",
            "benefitPercentage",
            "startedDate",
            "reward",
        )

    def get_reward(self, obj):
        return f"{(obj.selectedAmount * (obj.plan.net_benefit()/100))} as {obj.plan.benefitType} once the goal is reached"
