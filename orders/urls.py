from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('add/', views.add, name='add'),
    path('list/', views.order_list, name="order_list"),
    path('control/', views.order_control, name="order_control"),
    path('approve/<int:id>/', views.order_approve, name="order_approve"),
    path('single-order/<int:id>/', views.single_order, name="single_order"),
]
