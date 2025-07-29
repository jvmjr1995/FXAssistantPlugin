from django.urls import path
from .views import fx_recommendation_view, suggest_fx_chain

urlpatterns = [
        path('recommendations/', fx_recommendation_view),       # Add our new static recommendation endpoint
        path("suggest-fx-chain/", suggest_fx_chain),
]
