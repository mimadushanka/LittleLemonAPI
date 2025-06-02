from rest_framework import serializers
from .models import MenuItem,Category,Cart,Order_item,Order
from django.contrib.auth.models import User

# class CategorySerializer(serializers.Serializer):
#     class Meta:
#         model=Category
#         fields=['slug','title']

# class MenuItemSerializer(serializers.Serializer):
#      id=serializers.IntegerField()
#      title=serializers.CharField(max_length=255)
#      price=serializers.DecimalField(max_digits=6,decimal_places=2,min_value=0)
#      featured=serializers.BooleanField()
#      category=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
         model=Category
         fields=['id','slug','title']

class MenuItemSerializer(serializers.ModelSerializer):
   # category=serializers.StringRelatedField()
   #category=CategorySerializer(read_only=True)
   class Meta:
        model=MenuItem
        fields=['id','title','price','featured','category']
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','username']
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields=['id','unit_price','price','user_id','menuitem','quantity']
        read_only_fields=['unit_price','price','user_id',]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order_item
        fields=['id','order','menuitem','quantity','unit_price','price']
        read_only_fields=['order','menuitem','quantity','unit_price','price']

    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['id','user','delivery_crew','status','total','date']
        read_only_fields=['id','user','total','date']

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['status']