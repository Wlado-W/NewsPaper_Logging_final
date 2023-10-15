from django.urls import path
from .views import AppointmentView

app_name = 'appointments'

urlpatterns = [
    path('make_appointment/', AppointmentView.as_view(), name="make_appointment"),
]