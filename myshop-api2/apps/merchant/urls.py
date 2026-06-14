from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('register', views.MerchantRegView, basename='merchant-register')
router.register('shop', views.ShopViewSet, basename='merchant-shop')
router.register('goods', views.MerchantGoodsViewSet, basename='merchant-goods')
router.register('categories', views.MerchantCategoryViewSet, basename='merchant-categories')
router.register('orders', views.MerchantOrderViewSet, basename='merchant-orders')
router.register('stats', views.MerchantStatsView, basename='merchant-stats')

urlpatterns = [
    path('upload-logo/', views.MerchantLogoUploadView.as_view(), name='merchant-upload-logo'),
    path('', include(router.urls)),
]
