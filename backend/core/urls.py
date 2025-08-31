from django.urls import path
from .views import home, RestaurantList, RestaurantDetail, MenuItemList, CreateOrder
from .views import signup, login


urlpatterns = [
    path('', home),
    path('api/restaurants/', RestaurantList.as_view()),
    path('api/restaurants/<int:pk>/', RestaurantDetail.as_view()),
    path('api/restaurants/<int:restaurant_id>/menu/', MenuItemList.as_view(),  name='menu-items'),
    path('orders/create/', CreateOrder.as_view()),
    path('api/signup/', signup, name='signup'),  # yeh add karo
    path('api/login/', login, name='login'),     # yeh add karo
]