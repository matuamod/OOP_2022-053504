from xml.sax.handler import EntityResolver
from django.contrib import admin
from django.urls import path, include
from bank_service import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('account', views.AccountViewSet)
router.register('account/action', views.ActionViewSet)
router.register('account/transaction', views.TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('individual/', views.IndividualCreateView.as_view(), name='individual'),
    path('entity/', views.EntityCreateView.as_view(), name='entity'),
]
