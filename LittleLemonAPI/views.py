from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import MenuItem,Category,Cart,Order,Order_item,User
from .serializers import MenuItemSerializer,CategorySerializer,UserSerializer,CartSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User,Group


# Create your views here.
@api_view()
def books(reqest):
    return Response('message is displayed',status=status.HTTP_200_OK)

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
     return Response({"Message":"Only Manager should see this"})
    else:
       return Response({'Message':'you dont have access to this view'},403)


################################################################  
#display the items in the menu item category
@api_view()
def category(request):
   #if request.method=='GET':
    items=Category.objects.all()
    serialized_item=CategorySerializer(items,many=True)
    return Response(serialized_item.data)
    

@api_view(['GET','POST'])
def menu_items(request):
   if request.method=='POST':
       if request.user.groups.filter(name='Manager').exists():
                serialized_item=MenuItemSerializer(data=request.data)
                serialized_item.is_valid(raise_exception=True)
                serialized_item.save()
                return Response(serialized_item.data, status.HTTP_201_CREATED)
       else:
            return Response({"detail": "Unauthorised"}, status.HTTP_403_FORBIDDEN)   
   if request.method=='GET':
            items=MenuItem.objects.select_related('category').all()
            serialized_item=MenuItemSerializer(items,many=True)
            return Response(serialized_item.data,status=status.HTTP_200_OK)
        
    


@api_view(['GET','PUT','PATCH','DELETE'])
def single_item(request,id):
   item=get_object_or_404(MenuItem,pk=id)
       
   if request.method=='PUT':
        if request.user.groups.filter(name='Manager').exists():
            serialized_item=MenuItemSerializer(item,data=request.data)
            if serialized_item.is_valid():
                serialized_item.save()
                return Response(serialized_item.data, status.HTTP_200_OK)
            return Response(serialized_item.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
   

   elif request.method=='PATCH':
       if request.user.groups.filter(name='Manager').exists():
          serialized_item=MenuItemSerializer(item,data=request.data,partial=True)
          if serialized_item.is_valid():
             serialized_item.save()
          return Response(serialized_item.data,status.HTTP_201_CREATED)
       
       return Response({'detail':'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
   
   elif request.method=='DELETE':
      if request.user.groups.filter(name='Manager').exists():
         item.delete()
         return Response({"detail": "Deleted successfully."},status=status.HTTP_200_OK)
      return Response({'detail':'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
      
   elif request.method=='GET': 
    serialized_item=MenuItemSerializer(item)
    return Response (serialized_item.data,status=status.HTTP_200_OK)
         
  
@api_view(['GET','POST'])
def managers(request):
    managers_group=Group.objects.get(name='Manager')
    if request.method=='POST':
        username=request.data['username']
        if request.user.groups.filter(name='Manager').exists():
            if username:
                user=get_object_or_404(User,username=username)
                managers_group.user_set.add(user)
                return Response({'message':'ok'},status=status.HTTP_200_OK)
            return Response({"message":"error"},status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Unauthorized'},status=status.HTTP_403_FORBIDDEN)
    elif request.method=='GET':
        if request.user.groups.filter(name='Manager').exists():
            managers=managers_group.user_set.all()
            serializer=UserSerializer(managers,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'detail':'Unauthorized'},status=status.HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
def revoke_manager(request,id):
    if request.user.groups.filter(name='Manager').exists():
        user=get_object_or_404(User,pk=id)
        manager_group=Group.objects.get(name='Manager')
        if manager_group in user.groups.all():
            user.groups.remove(manager_group)
            return Response({'message':'User removed from Manager Group'},status=status.HTTP_200_OK)
    return Response({'detail':'Unauthorized'},status=status.HTTP_403_FORBIDDEN)





@api_view(['GET','POST'])

def delivery_crew(request):
    delivery_group=Group.objects.get(name='Delivery_crew')
    if request.method=='POST':
        username=request.data['username']
        if request.User.group.filter(name='Manager').exists():
             if username:
                user=get_object_or_404(User,username=username)
                delivery_group.user_set.add(user)
                return Response({'message':'ok'},status=status.HTTP_200_OK)
             return Response({"message":"error"},status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Unauthorized'},status=status.HTTP_403_FORBIDDEN)
   
    elif request.method=='GET':
        if request.user.groups.filter(name='Manager').exists():
            delivery_crew=delivery_group.user_set.all()
            serializer=UserSerializer(delivery_crew,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'detail':'Unauthorized'},status=status.HTTP_403_FORBIDDEN)

@api_view(['DELETE'])
def revoke_delivery_crew(request,id):
    if request.user.groups.filter(name='Manager').exists():
        user=get_object_or_404(User,pk=id)
        delivery_group=Group.objects.get(name='Delivery_crew')
        if delivery_group in user.groups.all():
            user.groups.remove(delivery_group)
            return Response({'message':'User removed from delivery Crew'},status=status.HTTP_200_OK)
    return Response({'detail':'Unauthorized'},status=status.HTTP_403_FORBIDDEN)



@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def add_cart_items(request):
    if not request.user.groups.filter(name__in=['Manager', 'Delivery_crew']).exists():
        if request.method=='GET':
            items = Cart.objects.filter(user=request.user)
            serialized_item=CartSerializer(items,many=True)
            return Response(serialized_item.data)
        elif request.method=='POST':
            user=request.user
            menu_item_id=request.data.get('menuitem')
            quantity=request.data.get('quantity')
            if not menu_item_id or not quantity:
                return Response({"message":"error"},status.HTTP_400_BAD_REQUEST)
            menuitem=get_object_or_404(MenuItem,pk=menu_item_id)

            try: 
                quantity=int(quantity)
                if quantity<1:
                    raise ValueError
            except ValueError:
                return Response({"detail": "Quantity must be a positive integer."},status=status.HTTP_400_BAD_REQUEST)
            
            unit_price=menuitem.price
            price=unit_price*quantity

            cart_items=Cart.objects.create(
                user_id=request.user.id,
                menuitem=menuitem,
                quantity=quantity,
                unit_price=unit_price,
                price=price
            )
            
            serialized_item=CartSerializer(cart_items)
            return Response(serialized_item.data, status.HTTP_201_CREATED)
        

        elif request.method=='DELETE':
            items = Cart.objects.filter(user=request.user)
            items.delete()
            return Response({"detail": "All the cart items are deleted!"},status=status.HTTP_200_OK)
        
    return Response({'detail':'Unauthorized'},status=status.HTTP_403_FORBIDDEN)









    