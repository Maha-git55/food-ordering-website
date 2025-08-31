from django.contrib import admin
from .models import Restaurant, MenuItem, Order

# Models ko register karein
admin.site.register(Restaurant)
admin.site.register(MenuItem)
admin.site.register(Order)