from django.db import models
import uuid
from snbl.constants import AMOUNT_OPTIONS, TENURE_OPTIONS, BENEFIT_TYPES
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Plan(models.Model):
    planID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    planName = models.CharField(max_length=149)
    amountOptions = models.CharField(
        default="cash", max_length=15, choices=AMOUNT_OPTIONS
    )
    tenureOptions = models.IntegerField(default=1, choices=TENURE_OPTIONS)  # IN months
    benefitPercentage = models.FloatField(
        default=0, validators=[MaxValueValidator(100.0)]
    )
    benefitType = models.CharField(
        default="cashback", max_length=15, choices=BENEFIT_TYPES
    )

    def __str__(self) -> str:
        return self.planName

    def net_benefit(self):
        try:
            total = self.promotion.total_benefitpercentage()
        except:
            total = self.benefitPercentage
        return total


class Promotion(models.Model):

    promotionID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=149)
    max_users = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)
    benefitPercentage = models.FloatField(
        default=0, validators=[MaxValueValidator(100.0)]
    )
    # assumption each plan can have only one promotion
    plan = models.OneToOneField(Plan, on_delete=models.CASCADE)

    def total_benefitpercentage(self):
        # checking how many users used the promotion
        if self.max_users is not None:
            used_promotions = CustomerGoals.objects.filter(plan=self.plan).count()
            if used_promotions >= self.max_users:
                return self.plan.benefitPercentage

        if self.end_date is None:
            return self.plan.benefitPercentage + self.benefitPercentage
        # if plan has end date then check if current time is less the end date and greater than start date
        # total benfit rate will be calculated as (Plan__benefitPercentage + Promotion__benefitPercentage)
        if self.end_date and self.start_date < timezone.now() < self.end_date:
            return self.plan.benefitPercentage + self.benefitPercentage

        return self.plan.benefitPercentage


class CustomerGoals(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    userID = models.CharField(max_length=30)
    selectedAmount = models.IntegerField()
    selectedTenure = models.IntegerField(default=1)
    startedDate = models.DateField(auto_now_add=True)
    depositedAmount = models.IntegerField()
    benefitPercentage = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.depositedAmount = 0
        self.benefitPercentage = self.plan.net_benefit()
        return super(CustomerGoals, self).save(*args, **kwargs)

# extra model Amount with foreignkey CustomerGoals to and a post_save signal can be used to update depositedAmount in CustomerGoals model
# similar to tortoise app.  