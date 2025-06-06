from .import views
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('token/login/',obtain_auth_token),
    path('menu-items/',views.menu_items),
    #path('category/',views.category),
    path('menu-items/<int:id>',views.single_item),
    path('groups/manager/users/',views.managers),
    path('groups/manager/users/<int:id>',views.revoke_manager),
    path('groups/delivery-crew/users/',views.delivery_crew),
    path('groups/delivery-crew/users/<int:id>',views.revoke_delivery_crew),
    path('cart/menu-items/',views.add_cart_items),
    path('orders/',views.order_item),
    path('orders/<int:id>',views.order_management),


]
