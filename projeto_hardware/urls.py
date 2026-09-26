from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hardware.views import LojaViewSet, ComponenteViewSet, HistoricoPrecoViewSet

router = DefaultRouter()
router.register(r'lojas', LojaViewSet)
router.register(r'componentes', ComponenteViewSet)
router.register(r'precos', HistoricoPrecoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),        
    path('api/', include(router.urls)),      
]