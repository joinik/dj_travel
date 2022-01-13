from django.urls import path

from apps.verifications.views import MsmCodeView



urlpatterns = [
    path('sms/codes/<mobile>/', MsmCodeView.as_view())
]
