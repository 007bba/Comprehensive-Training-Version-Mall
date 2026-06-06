from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter

from apps.order import views

router=DefaultRouter()
router.register('cart',views.CartViewset,basename="cart")

urlpatterns = [
    #GenericViewSet
    path('order/',views.OrderView.as_view()),#get，Post
    path('order/<int:order_id>/pay/', views.PayOrderView.as_view()),
    path('order/<int:order_id>/mock-pay/', views.PayOrderView.as_view()),
    #router.register('indexgoods',views.IndexCategoryViewset,basename="indexgoods"),
    path("",include(router.urls))
]