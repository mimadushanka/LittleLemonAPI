from .import views
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('books/',views.books),
    path('manager-view/',views.manager_view),
    path('api-token-auth/',obtain_auth_token),
    path('menu-items/',views.menu_items),
    path('category/',views.category),
    path('menu-items/<int:id>',views.single_item),

]
