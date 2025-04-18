from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutosViewSet, ClientesViewSet, VendasViewSet, CarrinhoViewSet
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'produtos', ProdutosViewSet)
router.register(r'clientes', ClientesViewSet)
router.register(r'vendas', VendasViewSet)
router.register(r'carrinho', CarrinhoViewSet)

urlpatterns = [

    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Página de logout
    path('register/', views.register, name='register'),  # Página de cadastro
    path('login/', views.login_view, name='login'),  # Página de login
    path('accounts/', include('allauth.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  

    path('api/', include(router.urls)),


    path('', views.index, name='index'),
    path('produtos/', views.produtos_usuario, name='produtos_usuario'),
    path('produtos/adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('produtos/excluir/<int:id>/', views.excluir_produto, name='excluir_produto'),
    path('produtos/editar/<int:id>/', views.editar_produto, name='editar_produto'),


    path('produtos/adicionar-ao-carrinho/<int:id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/remover/<int:item_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),
    path('carrinho/', views.carrinho, name='carrinho'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

