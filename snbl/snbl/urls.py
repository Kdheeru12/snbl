"""snbl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from tortoise.api import PlanView, PromotionView, CustomerGoalsView

router = DefaultRouter()
router.register("plan", PlanView, "plan")
router.register("promotion", PromotionView, "promotion")
router.register("goals", CustomerGoalsView, "goals")


urlpatterns = [path("admin/", admin.site.urls), url(r"^", include(router.urls))]
