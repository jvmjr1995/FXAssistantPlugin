from .models import Preset
from .serializers import PresetSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# We use these tools from Django REST Framework to make a simple API view
from rest_framework import viewsets

# We use Django’s ModelViewSet to handle all CRUD operations in one go.

# ViewSet provides built-in GET, POST, PUT, DELETE operations for Presets.
class PresetViewSet(viewsets.ModelViewSet):
    # This tells Django to return all Preset records, newest first.
    queryset = Preset.objects.all().order_by('-created_at')

    # This tells Django to use our serializer to convert model ↔ JSON.
    serializer_class = PresetSerializer

# This view lets new users register via POST /api/register/
@api_view(['POST'])
@permission_classes([AllowAny]) # 👈 Overrides global IsAuthenticated permission for open access
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Validate required fields
    if not username or not password:
        return Response({'error': 'Username and password required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Prevent duplicate usernames
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create the user
    user = User.objects.create_user(username=username, password=password)
    token, _ = Token.objects.get_or_create(user=user)   # Create or fetch their auth token

    return Response({
        'message': 'User created successfully',
        'token': token.key,
    }, status=status.HTTP_201_CREATED)

