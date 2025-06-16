from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PresetViewSet

# Create a router to automatically handle API endpoint routes
router = DefaultRouter()
router.register(r'presets', PresetViewSet) # Registers /api/presets/ endpoint

# This file defines how URLs in this app are routed to views.
urlpatterns = [
    path('', include(router.urls)), # Includes all auto-routed endpoints from the router
]
