from django.urls import path
from . import views  # . means current directory

urlpatterns = [
    path('', views.display_all_products, name='products'),
    path('<product_id>', views.display_product_detail,
         name='display_product_detail')
]