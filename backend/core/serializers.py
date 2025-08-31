from rest_framework import serializers
from .models import Restaurant, MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'image', 'description']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class RestaurantSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'image', 'description', 'category', 'delivery_time', 'min_order', 'rating', 'menu_items']
    
    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None