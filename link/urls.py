from django.urls import path
from link import views

urlpatterns = [
    path('create', views.create_vpa_link),
    path('pay/<str:payId>', views.linkpage),
    path('pay-data/<str:payId>', views.data_view)
]
