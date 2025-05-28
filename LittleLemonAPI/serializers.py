from rest_framework import serializers
from .models import MenuItem,Category

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