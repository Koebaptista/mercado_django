from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutosViewSet, ClientesViewSet, VendasViewSet, CarrinhoViewSet
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'produtos', ProdutosViewSet)
router.register(r'clientes', ClientesViewSet)
router.register(r'vendas', VendasViewSet)
router.register(r'carrinho', CarrinhoViewSet)

urlpatterns = [

    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Página de logout
    path('register/', views.register, name='register'),  # Página de cadastro
    path('login/', views.login_view, name='login'),  # Página de login

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  

    path('api/', include(router.urls)),


    path('', views.index, name='index'),
    path('produtos/', views.produtos, name='produtos'),
]

