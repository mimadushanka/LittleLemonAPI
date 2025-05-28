from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import MenuItem,Category,Cart,Order,Order_item
from .serializers import MenuItemSerializer,CategorySerializer
from django.shortcuts import get_object_or_404


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
         
  
      
    