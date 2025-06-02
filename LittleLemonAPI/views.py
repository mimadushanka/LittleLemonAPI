from django.utils import timezone
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes,throttle_classes
from rest_framework.permissions import IsAuthenticated
from .models import MenuItem,Category,Cart,Order,Order_item,User
from .serializers import MenuItemSerializer,CategorySerializer,UserSerializer,CartSerializer,OrderItemSerializer,OrderSerializer,OrderStatusUpdateSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User,Group
from django.db import transaction
from django.core.paginator import Paginator,EmptyPage
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle

################################################################  




@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle,UserRateThrottle])  
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
            ##filtering the items
            category_name=request.query_params.get('category')
            to_price=request.query_params.get('to_price')
            search=request.query_params.get('search')
            ordering=request.query_params.get('ordering')
            
            perpage=request.query_params.get('perpage',default=10)
            page=request.query_params.get('page',default=1)
            if category_name:
                items=items.filter(category__title=category_name)
            if to_price:
                items=items.filter(price__lte=to_price)
            if search:
                items=items.filter(title__contains=search)
            if ordering:
                ordering_fields=ordering.split(",")
                items=items.order_by(*ordering_fields)
             #pagination
            paginator=Paginator(items,per_page=perpage)
            try:
                    items=paginator.page(number=page)
            except EmptyPage:
                     items=[]

            serialized_item=MenuItemSerializer(items,many=True)
            return Response(serialized_item.data,status=status.HTTP_200_OK)
        
    


@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle,UserRateThrottle])  
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
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle,UserRateThrottle])  
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
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle,UserRateThrottle])  
def revoke_manager(request,id):
    if request.user.groups.filter(name='Manager').exists():
        user=get_object_or_404(User,pk=id)
        manager_group=Group.objects.get(name='Manager')
        if manager_group in user.groups.all():
            user.groups.remove(manager_group)
            return Response({'message':'User removed from Manager Group'},status=status.HTTP_200_OK)
    return Response({'detail':'Unauthorized'},status=status.HTTP_403_FORBIDDEN)





@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle,UserRateThrottle])  
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
@throttle_classes([AnonRateThrottle,UserRateThrottle])  
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
@throttle_classes([AnonRateThrottle,UserRateThrottle])  

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


#create order item for perticular user 

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle,UserRateThrottle])  

def order_item(request):
    if request.method=='POST':
        if not request.user.groups.filter(name__in=['Manager', 'Delivery_crew']).exists():
            user=request.user
            cart_items=Cart.objects.filter(user=user)
            
            if not cart_items.exists():
                return Response({"message":"Cart is empty, There is no items in the Cart"},status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():
              total = sum(item.price for item in cart_items)
              order = Order.objects.create(
              user=user,
              total=total,
              date=timezone.now().date()
            )
                # Create order items from cart
            order_items = [
                Order_item(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
                )for item in cart_items
            ]
            Order_item.objects.bulk_create(order_items)  
            cart_items.delete()
            return Response({"detail": "Order placed successfully!"}, status=status.HTTP_201_CREATED)
        return Response({'detail':'Unauthorized'},status=status.HTTP_403_FORBIDDEN)
    

    if request.method=='GET':
          if not request.user.groups.filter(name__in=['Manager', 'Delivery_crew']).exists():
            orders = Order.objects.filter(user=request.user)
            items = Order_item.objects.filter(order__in=orders)
            if not items.exists():
             return Response({"message": "No order items found."}, status=status.HTTP_400_BAD_REQUEST)
            serialized_item=OrderItemSerializer(items,many=True)
            return Response(serialized_item.data)
          elif  request.user.groups.filter(name='Manager').exists():
              items = Order_item.objects.all()
              if not items.exists():
               return Response({"message": "No order items found."}, status=status.HTTP_400_BAD_REQUEST)
              serialized_item=OrderItemSerializer(items,many=True)
              return Response(serialized_item.data)
          
          elif  request.user.groups.filter(name='Delivery_crew').exists():##check the logic again
               orders = Order.objects.filter(delivery_crew=request.user)
               items = Order_item.objects.filter(order__in=orders)
               if not items.exists():
                return Response({"message": "No order items found."}, status=status.HTTP_400_BAD_REQUEST)
               serialized_item=OrderItemSerializer(items,many=True)
               return Response(serialized_item.data)
              
         # elif request.user.groups.filter(name=['Delivery_crew']).exists():
    return Response({'detail':'Unauthorized'},status=status.HTTP_403_FORBIDDEN)



@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])  
@throttle_classes([AnonRateThrottle,UserRateThrottle])  

def order_management(request,id):
    order=get_object_or_404(Order,pk=id)
    if request.method=='GET':
       if request.user.groups.filter(name__in=['Manager', 'Delivery_crew']).exists():
        return Response({'detail': 'Only customers can access this endpoint.'}, status=status.HTTP_403_FORBIDDEN)
       
       elif order.user != request.user:
        return Response({'detail': 'Unauthorized access to this order.'}, status=status.HTTP_403_FORBIDDEN)
       
       serializer = OrderSerializer(order)
       return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method=='PUT':
        if request.user.groups.filter(name='Manager').exists():
            serialized_item=OrderSerializer(order,data=request.data)
            if serialized_item.is_valid():
                serialized_item.save()
                return Response(serialized_item.data, status.HTTP_200_OK)
            return Response(serialized_item.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    elif request.method=='PATCH':
        if request.user.groups.filter(name='Delivery_crew').exists():
            serialized_item=OrderStatusUpdateSerializer(order,data=request.data,partial=True)
            if serialized_item.is_valid():
              serialized_item.save()
              return Response(serialized_item.data, status=status.HTTP_201_CREATED)
            return Response(serialized_item.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    elif request.method=='DELETE':
         if request.user.groups.filter(name='Manager').exists():
            order.delete()
            return Response({'detail': 'Order deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
         return Response({'detail': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)



             


















    