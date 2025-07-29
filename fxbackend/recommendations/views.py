from django.shortcuts import render
# We use these tools from Django REST Framework to make a simple API view
from rest_framework.decorators import api_view  # Lets us define a function as an API endpoint
from rest_framework.response import Response    # Lets us send structured JSON responses back to the client
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


# This is a hardcoded dictionary of recommended FX chains by type
# Each "type" (e.g. vocals, drums) has its own FX plugin chain and settings
FX_CHAIN_TEMPLATES = {
    'vocals': [
        {
            'name': 'Clean Pop Vocals',
            'chain': [
                {'plugin': 'EQ', 'settings': {'highpass': 80, 'lowpass': 12000}},           # Remove low frequencies below 80Hz & high frequencies above 12000Hz
                {'plugin': 'Compressor', 'settings': {'threshold': -18, 'ratio': 4.0}},     # Start compressing at -18 dB & compress at a 4:1 ratio
                {'plugin': 'Reverb', 'settings': {'decay': 2.5, 'mix': 0.35}}               # 2.5 seconds of reverb tail & 35% wet signal
            ]
        },
        {
            'name': 'Vintage Radio Voice',
            'chain': [
                {'plugin': 'EQ', 'settings': {'highpass': 200, 'lowpass': 4500}},           # Remove low frequencies below 200Hz & high frequencies above 4500Hz
                {'plugin': 'Saturation', 'settings': {'drive': 0.6}},     
                {'plugin': 'Compressor', 'settings': {'threshold': -12, 'ratio': 2.5}}
            ]
        }
    ],
    'drums': [
        {
            'name': 'Punchy Kit',
            'chain': [
                {'plugin': 'TransientShaper', 'settings': {'attack': 0.9}},                # Emphasize the initial hit of drum sounds
                {'plugin': 'Saturation', 'settings': {'drive': 0.4}},                      # Add harmonic distortion
                {'plugin': 'Compressor', 'settings': {'threshold': -10, 'ratio': 5.0}}
            ]
        },
        {
            'name': 'Lo-Fi Percussion',
            'chain': [
                {'plugin': 'Bitcrusher', 'settings': {'rate': 12, 'depth': 8}},
                {'plugin': 'TapeHiss', 'settings': {'noise_level': 0.3}},                      
                {'plugin': 'Reverb', 'settings': {'decay': 1.8, 'mix': 0.3}}
            ]
        }
    ],

    'lofi': [
        {
            'name': 'Dusty Chillwave',
            'chain': [
                {'plugin': 'Vinyl', 'settings': {'noise': 0.4}},        # Add vinyl crackle noise
                {'plugin': 'Chorus', 'settings': {'depth': 0.6}},
                {'plugin': 'Reverb', 'settings': {'decay': 3.2, 'mix': 0.4}}
            ]
        },
        {
            'name': 'Crushed Nostalgia',
            'chain': [
                {'plugin': 'Bitcrusher', 'settings': {'rate': 8, 'depth': 6}},      # Lower sample rate to 8kHz & reduce bit depth to 6 bits
                {'plugin': 'EQ', 'settings': {'highpass': 120, 'lowpass': 5000}},           
                {'plugin': 'Delay', 'settings': {'time': 0.3, 'feedback': 0.5}}
            ]
        }
    ]
}

# This is the actual view function Django will call when the user requests a recommendation
@api_view(['GET'])      # Only allow GET requests like /api/recommendations/?type=vocals
def fx_recommendation_view(request):
    """
    This view receives a 'type' query string and returns a recommended FX chain.
    Example: GET /api/recommendations/?type=drums
    """

    # Pull the value of 'type' from the URL query parameters
    fx_type = request.GET.get('type')

    # Check if the user gave us a valid type like 'vocals' or 'drums'
    if fx_type not in FX_CHAIN_TEMPLATES:
        return Response(
            {'error': 'Invalid type. Choose from: vocals, drums, lofi'},
            status=400 # This is an HTTP 400 "Bad Request" error
        )
    
    # If it's valid, send back the recommended FX chain
    return Response({
        'type': fx_type,
        'count': len(FX_CHAIN_TEMPLATES[fx_type]),  # Show how many results returned
        'recommendation': FX_CHAIN_TEMPLATES[fx_type]   # Return the full list
    })

@csrf_exempt
def suggest_fx_chain(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            genre = data.get('genre', '').lower()
            fx_type = data.get('fx_type', '').lower()

            if fx_type in FX_CHAIN_TEMPLATES:
                results = FX_CHAIN_TEMPLATES[fx_type]
            else:
                return JsonResponse({'error': 'Invalid fx_type'}, status=400)
            
            return JsonResponse({'suggestions': results}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
    return JsonResponse({'error': 'Invalid request method'}, status=405)
