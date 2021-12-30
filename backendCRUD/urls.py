from rest_framework import routers
from .views import CompanyViewsets

router = routers.DefaultRouter()
router.register('company',CompanyViewsets)

from django.urls import path, include

urlpatterns = [
    path('api/', include(router.urls)),
]