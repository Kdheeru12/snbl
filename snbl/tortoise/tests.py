from django.test import TestCase
from tortoise.models import Promotion, Plan,CustomerGoals
from django.utils import timezone

# Create your tests here.
class PromotionTestCase(TestCase):
    def setUp(self):
        self.plan1 = Plan.objects.create(planName="ipad",benefitPercentage=10)
        self.plan2 = Plan.objects.create(planName="macbook",benefitPercentage=4)
        self.promotion = Promotion.objects.create(plan= self.plan1, name="sbicard", max_users=1,benefitPercentage=5)
    def test_net_benefit_percentage(self):
        # as of now no user has claimed the promotion so the total benefit should be 10 + 5
        goal = CustomerGoals.objects.create(plan=self.plan1,userID='11', selectedAmount=10000)
        self.assertEquals(goal.benefitPercentage, 15)
    
    def test_net_benefit_percentage_with_end_date(self):
        # as of now no user has claimed the promotion so the total benefit should be 10 + 5
        self.promotion.end_date = timezone.now() + timezone.timedelta(seconds=10)
        goal = CustomerGoals.objects.create(plan=self.plan1,userID='11', selectedAmount=10000)
        self.assertEquals(goal.benefitPercentage, 15)
    def test_net_benefit_percentage_after_users_claimed(self):
        CustomerGoals.objects.create(plan=self.plan1,userID='1', selectedAmount=10000)
        goal2 =CustomerGoals.objects.create(plan=self.plan1,userID='2', selectedAmount=10000)
        # as max_users is 1 so now user 2 will not be able to claim the benefits of promotion total benefit = 10
        self.assertEquals(goal2.benefitPercentage, 10)
    def test_net_benefit_after_promotion_as_completed(self):
        self.promotion.end_date = timezone.now()
        goal = CustomerGoals.objects.create(plan=self.plan1,userID='1', selectedAmount=10000)
        self.assertEqual(goal.benefitPercentage, 10)
    def test_net_benefit_with_no_promotion(self):
        goal=CustomerGoals.objects.create(plan=self.plan2,userID='1', selectedAmount=10000)
        self.assertEquals(goal.benefitPercentage, 4)
    
        