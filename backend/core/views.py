from django.http import HttpResponse
from rest_framework import generics
from .models import Restaurant, MenuItem
from .serializers import RestaurantSerializer, MenuItemSerializer
# Order views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order

# core/views.py mein yeh add karo

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
 
def home(request):
    return HttpResponse("Welcome to Food Ordering App! Go to /admin or /api/restaurants/")

class RestaurantList(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

# ✅ YEH LINE CHANGE KAR DO
    permission_classes = [permissions.IsAuthenticated]  # Sirf logged in users ko access milega
    

    def get_serializer_context(self):
        return {'request': self.request}

class RestaurantDetail(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class MenuItemList(generics.ListAPIView):
    serializer_class = MenuItemSerializer
    
    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return MenuItem.objects.filter(restaurant_id=restaurant_id)
    
    # yh bnd m ki add 
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
# CreateOrder view ko update karo

class CreateOrder(APIView):
    def post(self, request):
        try:
            # Restaurant ID bhi add karna hoga
            order = Order.objects.create(
                user=request.user,
                restaurant_id=request.data['restaurant_id'],  # yeh add karo
                items=request.data['items'],
                total=request.data['total'],
                address=request.data['address'],
                phone=request.data['phone']
            )
            return Response({"order_id": order.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


 # Signup View
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    try:
        username = request.data.get('email')  # email ko username bana rahe hain
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('name', '')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name
        )
        
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Login View
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        username = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.first_name
                }
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)       