from django.contrib import admin
from .models import Category,MenuItem,Cart,Order_item,Order

# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order_item)
admin.site.register(Order)


