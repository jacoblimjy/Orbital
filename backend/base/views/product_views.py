from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
# this is a class that is built into django rest framework that allows us to check if a user is authenticated or not
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from base.models import Product
from base.serializers import ProductSerializer

# this is a function that is built into django that allows us to hash a password
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):  # pk is passed in from the url from urls.py
    product = None
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
#@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response('Product Deleted')

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def createProduct(request):
    user = request.user
    supplier = user.supplier_set.get() 
    
    data = request.data
    name = data.get('name', '')
    price = data.get('price', 0)
    countInStock = data.get('countInStock', 0)
    category = data.get('category', '')
    description = data.get('description', '')
    expirationDate = data.get('expirationDate', '')
    unit = data.get('unit', '')
    

    product = Product.objects.create(
        supplier=supplier,
        name=name,
        price=price,
        countInStock=countInStock,
        category=category,
        description=description,
        expirationDate=expirationDate,
        unit=unit,
        image = request.FILES.get('image')
    )

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
# @permission_classes([IsAdminUser])
def updateProduct(request, pk):
    data = request.data
    product = Product.objects.get(_id=pk)

    product.name = data['name']
    product.price = data['price']
    product.countInStock = data['countInStock']
    product.category = data['category']
    product.description = data['description']
    product.expirationDate = data['expirationDate']
    product.unit = data['unit']

    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def uploadImage(request):
    data = request.data
    product_id = data['product_id']
    product = Product.objects.get(_id=product_id)

    product.image = request.FILES.get('image')
    product.save()
    return Response('Image was uploaded')
