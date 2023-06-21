from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
# this is a class that is built into django rest framework that allows us to check if a user is authenticated or not
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from base.serializers import UserSerializer, UserSerializerWithToken, IngredientSerializer, MenuItemSerializer, MenuIngredientSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password 

from base.models import UserProfile, Ingredient, MenuItem, MenuIngredient
# this is a function that is built into django that allows us to hash a password
from rest_framework import status

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):  # no need decode token, will show username and email in postman
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data


# this class is used in urls.py
class MyTokenObtainPairView(TokenObtainPairView):
    # serializer_class is a class variable of TokenObtainPairView, a class variable is a variable that is shared by all instances of a class.
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password']) #this is a function that is built into django that allows us to hash a password
        )

        userprofile = UserProfile.objects.create(
            user = user,
            isSupplier = True if data['isSupplier'] == 'true' else False
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST) #check rest_framework  
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    # this is a user object from request object that is passed in from the frontend
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createIngredient(request):
    serializer = IngredientSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save(user=request.user)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateIngredient(request):
    data = request.data
    try:
        ingredient = Ingredient.objects.filter(user = request.user).get(pk=data['_id'])
        serializer = IngredientSerializer(instance=ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"status": "error", "data": 'Ingredient does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getIngredients(request):
    ingredients = Ingredient.objects.filter(user = request.user)
    serializer = IngredientSerializer(ingredients, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteIngredient(request):
    data = request.data
    try:
        ingredient = Ingredient.objects.filter(user = request.user).get(pk=data['_id'])
        ingredient.delete()
        return Response({"status": "success", "data": 'Ingredient deleted.'}, status=status.HTTP_200_OK)
    except:
        return Response({"status": "error", "data": 'Ingredient does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createMenuItem(request):
    serializer = MenuItemSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save(user=request.user)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateMenuItem(request):
    data = request.data
    try:
        menuItem = MenuItem.objects.filter(user = request.user).get(pk=data['_id'])
        serializer = MenuItemSerializer(instance=menuItem, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            except:
                return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"status": "error", "data": 'Menu Item does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMenuItems(request):
    menuItems = MenuItem.objects.filter(user = request.user)
    serializer = MenuItemSerializer(menuItems, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteMenuItem(request):
    data = request.data
    try:
        menuItem = MenuItem.objects.filter(user = request.user).get(pk=data['_id'])
        menuItem.delete()
        return Response({"status": "success", "data": 'Menu Item deleted.'}, status=status.HTTP_200_OK)
    except:
        return Response({"status": "error", "data": 'Menu Item does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createMenuIngredient(request):
    data = request.data
    try:
        menuItem = MenuItem.objects.filter(user = request.user).get(pk=data['menuItem'])
        ingredient = Ingredient.objects.filter(user = request.user).get(pk=data['ingredient'])

        serializer = MenuIngredientSerializer(data=request.data)
        if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"status": "error", "data": 'Menu Item or Ingredient does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    

# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def updateMenuIngredient(request):
#     data = request.data
#     try:
#         menuIngredient = MenuIngredient.objects.get(pk=data['_id'])
#         newQuantity = { k:v for k,v in data.items() if 'quantity' in k }
#         serializer = MenuIngredientSerializer(instance=menuIngredient, data=newQuantity, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
#         else:
#             return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  
#     except:
#         return Response({"status": "error", "data": 'Menu Ingredient does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateMenuIngredient(request):
    data = request.data
    try:
        menuItem = MenuItem.objects.filter(user = request.user).get(pk=data['menuItem_id'])
        ingredients = menuItem.menuingredient_set.all()
        for add_ingredient in data['add']:
            if ingredients.filter(ingredient=add_ingredient['ingredient']).exists():
                menuIngredient = ingredients.get(ingredient=add_ingredient['ingredient'])
                menuIngredient.quantity = add_ingredient['quantity']
                menuIngredient.save()
            else:
                add_ingredient['menuItem'] = menuItem._id
                serializer = MenuIngredientSerializer(data=add_ingredient)
                if serializer.is_valid():
                    serializer.save(menuItem=menuItem)
                else:
                    return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        for remove_ingredient in data['remove']:
            if ingredients.filter(ingredient=remove_ingredient['ingredient']).exists():
                menuIngredient = ingredients.get(ingredient=remove_ingredient['ingredient'])
                menuIngredient.delete()

        return Response({"status": "success", "data": 'Menu Ingredients updated.'}, status=status.HTTP_200_OK)
    
    except Exception as err:
        return Response({"status": "error", "data": str(err)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMenuIngredients(request):
    try:
        menuIngredients = MenuItem.objects.filter(user = request.user).get(pk=request.data['_id']).menuingredient_set.all()
        serializer = MenuIngredientSerializer(menuIngredients, many=True)
        return Response(serializer.data)
    except:
        return Response({"status": "error", "data": 'Menu Item does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteMenuIngredient(request):
    data = request.data
    try:
        menuIngredient = MenuItem.objects.filter(user = request.user).get(pk=data['menuItem_id']).menuingredient_set.get(pk=data['_id'])
        menuIngredient.delete()
        return Response({"status": "success", "data": 'Menu Ingredient deleted.'}, status=status.HTTP_200_OK)
    except:
        return Response({"status": "error", "data": 'Menu Ingredient does not exist.'}, status=status.HTTP_400_BAD_REQUEST)