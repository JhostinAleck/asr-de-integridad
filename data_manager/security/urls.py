from django.urls import path
from .views import TestDataView

urlpatterns = [
    path('data/', TestDataView.as_view(), name='test-data'),
]