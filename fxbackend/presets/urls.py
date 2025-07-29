from django.urls import path, include                       # Import Django's routing functions
from rest_framework.routers import DefaultRouter            # Used for generating RESTful routes for ModelViewSet
from .views import PresetViewSet, register_user   # We import our new view function here
from rest_framework.authtoken.views import obtain_auth_token

# Create a router to automatically handle API endpoint routes
router = DefaultRouter()
router.register(r'presets', PresetViewSet) # Registers /api/presets/ endpoint - Connect our PresetViewSet to /presets/


# This file defines how URLs in this app are routed to views.
urlpatterns = [
    path('', include(router.urls)), # Includes all auto-routed endpoints from the router
    path('token-auth/', obtain_auth_token), # POST username + password → token
    path('register/', register_user),
]
