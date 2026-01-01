from django.shortcuts import render, get_object_or_404
# We use these tools from Django REST Framework to make a simple API view
from rest_framework.decorators import api_view, permission_classes, parser_classes  # Lets us define a function as an API endpoint
from rest_framework.response import Response    # Lets us send structured JSON responses back to the client
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.db.models import Q, Avg
from django.conf import settings
import json
import os
import tempfile
import logging
from pathlib import Path
from typing import Dict, List, Any

# Import our models and systems
from .models import FXChainTemplate, TemplateRating, TemplateCollection, ImportLog
from .comprehensive_templates import FX_CHAIN_TEMPLATES, get_template_by_category, get_random_template
from .safe_preset_converter import SafeFXChainExtractor, LegalComplianceManager

# Set up logging
logger = logging.getLogger(__name__)

# Simple FX chain templates for quick responses
QUICK_FX_TEMPLATES = {
    'hip-hop': ['EQ Eight', 'Compressor', 'Saturator', 'Reverb'],
    'edm': ['EQ Eight', 'Multiband Dynamics', 'Chorus', 'Delay', 'Reverb'],
    'lo-fi': ['EQ Eight', 'Vintage Electric Pianos', 'Vinyl', 'Chorus', 'Reverb'],
    'vocals': ['EQ Eight', 'Compressor', 'DeEsser', 'Chorus', 'Reverb'],
    'drums': ['EQ Eight', 'Transient Shaper', 'Compressor', 'Saturator'],
    'bass': ['EQ Eight', 'Compressor', 'Saturator', 'Sub']
}

# ===== CORE TEMPLATE SUGGESTION API =====

@csrf_exempt
def suggest_fx_chain(request):
    """
    Enhanced FX chain suggestion using comprehensive template system
    POST /api/suggest-fx-chain/
    {"genre": "hip-hop", "fx_type": "vocals"}
    """
    if request.method != "POST":
        return JsonResponse(['EQ Eight', 'Compressor', 'Reverb'], safe=False)
    
    try:
        # Parse request
        data = json.loads(request.body)
        genre = data.get('genre', '').lower().strip()
        fx_type = data.get('fx_type', '').lower().strip()
        
        logger.info(f"FX request: genre={genre}, fx_type={fx_type}")
        
        # Strategy 1: Try comprehensive templates first (your full library!)
        templates = get_template_by_category(genre, fx_type)
        if templates:
            # Get first template from comprehensive system
            template_name, fx_chain = list(templates.items())[0]
            logger.info(f"Found comprehensive template: {template_name}")
            return JsonResponse(fx_chain, safe=False)
        
        # Strategy 2: Try database templates
        try:
            db_template = FXChainTemplate.objects.filter(
                genre=genre,
                instrument_type=fx_type,
                is_public=True
            ).first()
            
            if db_template:
                logger.info(f"Found database template: {db_template.name}")
                return JsonResponse(db_template.fx_chain, safe=False)
        except Exception as e:
            logger.debug(f"Database query failed: {str(e)}")
        
        # Strategy 3: Try genre-only from comprehensive templates
        for (template_genre, template_fx_type), template_dict in FX_CHAIN_TEMPLATES.items():
            if template_genre == genre:
                template_name, fx_chain = list(template_dict.items())[0]
                logger.info(f"Found genre-only template: {template_name}")
                return JsonResponse(fx_chain, safe=False)
        
        # Strategy 4: Try fx_type-only from comprehensive templates  
        for (template_genre, template_fx_type), template_dict in FX_CHAIN_TEMPLATES.items():
            if template_fx_type == fx_type:
                template_name, fx_chain = list(template_dict.items())[0]
                logger.info(f"Found fx_type-only template: {template_name}")
                return JsonResponse(fx_chain, safe=False)
        
        # Strategy 5: Try quick templates
        if fx_type in QUICK_FX_TEMPLATES:
            result = QUICK_FX_TEMPLATES[fx_type]
            logger.info(f"Found quick fx_type template: {result}")
            return JsonResponse(result, safe=False)
        
        if genre in QUICK_FX_TEMPLATES:
            result = QUICK_FX_TEMPLATES[genre]
            logger.info(f"Found quick genre template: {result}")
            return JsonResponse(result, safe=False)
        
        # Strategy 6: Default fallback
        result = ['EQ Eight', 'Compressor', 'Reverb']
        logger.info(f"Using fallback template: {result}")
        return JsonResponse(result, safe=False)
        
    except Exception as e:
        logger.error(f"Error in suggest_fx_chain: {str(e)}")
        return JsonResponse(['EQ Eight', 'Compressor', 'Reverb'], safe=False)
    
def get_factory_templates(genre: str, fx_type: str) -> List[Dict]:
    """
    Get factory templates from our comprehensive template library
    
    Args:
        genre: Musical genre (e.g., 'hip-hop', 'edm')
        fx_type: Instrument type (e.g., 'vocals', 'guitar')
    
    Returns:
        List of factory template objects with metadata
    """

    try:
        # Get templates from our comprehensive library
        templates = get_template_by_category(genre, fx_type)
        
        if templates:
            # Convert to API format with metadata
            factory_list = []
            for name, fx_chain in templates.items():
                factory_list.append({
                    'name': name,
                    'fx_chain': fx_chain,
                    'type': 'factory',
                    'rating': 4.5,  # Factory templates get high default ratings
                    'description': f'Professional {genre} {fx_type} processing chain',
                    'chain_length': len(fx_chain),
                    'popularity': 'high'  # Factory templates are always popular
                })
            
            logger.debug(f"Found {len(factory_list)} factory templates for {genre}/{fx_type}")
            return factory_list
        
        # Try broader search if exact match not found
        else:
            # Look for genre-only matches
            all_matches = []
            for (template_genre, template_fx_type), template_dict in FX_CHAIN_TEMPLATES.items():
                if template_genre == genre:
                    for name, fx_chain in template_dict.items():
                        all_matches.append({
                            'name': f"{name} (adapted for {fx_type})",
                            'fx_chain': fx_chain,
                            'type': 'factory',
                            'rating': 4.2,
                            'description': f'Adapted {genre} processing chain',
                            'chain_length': len(fx_chain),
                            'popularity': 'medium'
                        })
            
            # Return up to 3 matches
            return all_matches[:3] if all_matches else get_default_factory_templates()
    
    except Exception as e:
        logger.error(f"Error getting factory templates: {str(e)}")
        return get_default_factory_templates()
    
def get_user_templates(user, genre: str, fx_type: str) -> List[Dict]:
    """
    Get user's custom templates matching the requested criteria
    
    Args:
        user: Django User object
        genre: Musical genre
        fx_type: Instrument type
    
    Returns:
        List of user template objects
    """
    try:
        # Query user's templates with exact match
        templates = FXChainTemplate.objects.filter(
            user=user,
            genre=genre,
            instrument_type=fx_type
        ).order_by('-updated_at')[:5]  # Get 5 most recent
        
        user_list = []
        for template in templates:
            user_list.append({
                'name': template.name,
                'fx_chain': template.fx_chain,
                'type': 'user',
                'description': template.description,
                'rating': 5.0,  # User's own templates get max rating
                'chain_length': len(template.fx_chain),
                'created_date': template.created_at.isoformat(),
                'id': template.id
            })
        
        logger.debug(f"Found {len(user_list)} user templates for {user.username}")
        return user_list
        
    except Exception as e:
        logger.error(f"Error getting user templates: {str(e)}")
        return []
    
def get_community_templates(genre: str, fx_type: str) -> List[Dict]:
    """
    Get highly-rated community templates
    
    Args:
        genre: Musical genre
        fx_type: Instrument type
    
    Returns:
        List of community template objects
    """

    try:
        # Query public templates with good ratings
        templates = FXChainTemplate.objects.filter(
            genre=genre,
            instrument_type=fx_type,
            is_public=True,
            template_type__in=['user', 'community'],
            rating__gte=3.5  # Only show well-rated templates
        ).order_by('-rating', '-downloads')[:3]  # Top 3 by rating and popularity
        
        community_list = []
        for template in templates:
            community_list.append({
                'name': template.name,
                'fx_chain': template.fx_chain,
                'type': 'community',
                'rating': template.rating,
                'downloads': template.downloads,
                'author': template.user.username,
                'description': template.description,
                'chain_length': len(template.fx_chain),
                'id': template.id
            })
        
        logger.debug(f"Found {len(community_list)} community templates")
        return community_list
        
    except Exception as e:
        logger.error(f"Error getting community templates: {str(e)}")
        return []
    
def get_quick_pick_chain(factory_templates: List[Dict]) -> List[str]:
    """
    Return a single FX chain for simple UI implementations
    
    Args:
        factory_templates: List of available factory templates
    
    Returns:
        Single FX chain as list of strings
    """

    if factory_templates:
        # Return the first (usually best) factory template chain
        return factory_templates[0]['fx_chain']
    else:
        # Return safe default
        return ['EQ', 'Compressor', 'Reverb']

def get_default_factory_templates() -> List[Dict]:
    """
    Get default factory templates when specific search fails
    
    Returns:
        List of generic factory templates
    """

    return [
        {
            'name': 'Basic Processing',
            'fx_chain': ['EQ', 'Compressor', 'Reverb'],
            'type': 'factory',
            'rating': 4.0,
            'description': 'Universal processing chain suitable for any source',
            'chain_length': 3,
            'popularity': 'high'
        },
        {
            'name': 'Enhanced Processing',
            'fx_chain': ['EQ', 'Compressor', 'Chorus', 'Reverb'],   
            'type': 'factory',
            'rating': 4.2,
            'description': 'Enhanced processing with modulation',
            'chain_length': 4,
            'popularity': 'medium'
        }
    ]

def get_fallback_response() -> Dict:
    """
    Safe fallback response when everything fails
    
    Returns:
        Minimal safe response
    """

    return {
        'factory': get_default_factory_templates(),
        'user': [],
        'community': [],
        'quick_pick': ['EQ', 'Compressor', 'Reverb'],
        'total_suggestions': 2,
        'status': 'fallback'
    }

# ===== TEMPLATE MANAGEMENT APIs =====

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_custom_template(request):
    """
    Save user's custom FX chain template
    
    Expected POST data:
    {
        "name": "My Vocal Chain",
        "description": "Custom vocal processing",
        "genre": "hip-hop",
        "instrument_type": "vocals",
        "fx_chain": ["EQ", "Compressor", "Reverb"],
        "is_public": false,
        "tags": "warm, vintage, vocal"
    }
    """
    
    try:
        data = request.data
        
        # Validate required fields
        required_fields = ['name', 'genre', 'instrument_type', 'fx_chain']
        for field in required_fields:
            if not data.get(field):
                return Response({'error': f'{field} is required'}, status=400)
        
        # Validate FX chain format
        fx_chain = data['fx_chain']
        if not isinstance(fx_chain, list) or not fx_chain:
            return Response({'error': 'fx_chain must be a non-empty list'}, status=400)
        
        # Check for duplicate names
        if FXChainTemplate.objects.filter(
            user=request.user, 
            name=data['name']
        ).exists():
            return Response({'error': 'Template name already exists'}, status=400)
        
        # Create template
        template = FXChainTemplate.objects.create(
            user=request.user,
            name=data['name'],
            description=data.get('description', ''),
            genre=data['genre'],
            instrument_type=data['instrument_type'],
            fx_chain=fx_chain,
            parameters=data.get('parameters', None),
            is_public=data.get('is_public', False),
            tags=data.get('tags', ''),
            template_type='user'
        )
        
        logger.info(f"User {request.user.username} saved template: {template.name}")
        
        return Response({
            'message': 'Template saved successfully',
            'template_id': template.id,
            'name': template.name,
            'fx_chain': template.fx_chain
        }, status=201)
        
    except Exception as e:
        logger.error(f"Error saving template: {str(e)}")
        return Response({'error': 'Failed to save template'}, status=500)

# ===== SAFE PRESET IMPORT APIs =====


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def import_industry_presets_safe(request):
    """
    LEGALLY SAFE import of industry presets
    
    This endpoint extracts ONLY FX chain structure from preset files.
    NO copyrighted content, parameter values, or brand names are stored.
    
    Expected form data:
    - files: Multiple preset files
    - auto_categorize: Boolean (optional)
    - make_public: Boolean (optional) 
    - add_source_prefix: Boolean (optional)
    """

    try:
        logger.info(f"Safe preset import request from user: {request.user.username}")
        
        # Validate request
        if 'files' not in request.FILES and 'file' not in request.FILES:
            return Response({'error': 'No files provided'}, status=400)
        
        # Get files list
        files = request.FILES.getlist('files') if 'files' in request.FILES else [request.FILES['file']]
        
        # Validate import request
        file_paths = [file.name for file in files]
        is_valid, error_msg = LegalComplianceManager.validate_import_request(file_paths, request.user.id)
        
        if not is_valid:
            return Response({'error': error_msg}, status=400)
        
        # Get import options
        import_options = {
            'auto_categorize': request.data.get('auto_categorize', 'true').lower() == 'true',
            'make_public': request.data.get('make_public', 'false').lower() == 'true',
            'add_source_prefix': request.data.get('add_source_prefix', 'true').lower() == 'true',
        }
        
        logger.info(f"Processing {len(files)} files with options: {import_options}")
        
        # Initialize extraction system
        extractor = SafeFXChainExtractor()
        compliance = LegalComplianceManager()
        
        # Track results
        results = {
            'success_count': 0,
            'error_count': 0,
            'imported_templates': [],
            'errors': [],
            'warnings': []
        }
        
        # Process each file
        for uploaded_file in files:
            try:
                logger.debug(f"Processing file: {uploaded_file.name}")
                
                # Save file temporarily for analysis
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                    # Write uploaded file to temp location
                    for chunk in uploaded_file.chunks():
                        tmp_file.write(chunk)
                    tmp_file_path = tmp_file.name
                
                # Extract FX chain structure (legally safe)
                extraction_result = extractor.extract_fx_chain_structure(tmp_file_path)
                
                # Clean up temp file immediately
                os.unlink(tmp_file_path)
                
                if extraction_result:
                    # Sanitize result for legal compliance
                    safe_result = compliance.sanitize_extraction_result(extraction_result)
                    
                    # Create database template from safe result
                    template = create_template_from_safe_extraction(
                        safe_result, 
                        request.user, 
                        import_options,
                        uploaded_file.name
                    )
                    
                    if template:
                        results['success_count'] += 1
                        results['imported_templates'].append({
                            'name': template.name,
                            'fx_chain': template.fx_chain,
                            'source_file': uploaded_file.name,
                            'chain_length': len(template.fx_chain),
                            'id': template.id
                        })
                        
                        logger.debug(f"Successfully imported: {template.name}")
                    else:
                        results['error_count'] += 1
                        results['errors'].append(f"Failed to create template from {uploaded_file.name}")
                else:
                    results['error_count'] += 1
                    results['errors'].append(f"Could not extract FX chain from {uploaded_file.name}")
                    
            except Exception as e:
                results['error_count'] += 1
                results['errors'].append(f"Error processing {uploaded_file.name}: {str(e)}")
                logger.error(f"File processing error: {str(e)}")
        
        # Log import activity
        ImportLog.objects.create(
            user=request.user,
            files_processed=len(files),
            successful_imports=results['success_count'],
            failed_imports=results['error_count'],
            file_types=[Path(f.name).suffix.lower() for f in files],
            error_messages=results['errors']
        )
        
        # Create response
        response_data = {
            'success': True,
            'message': f'Import completed: {results["success_count"]} successful, {results["error_count"]} failed',
            'legal_disclaimer': 'Only FX chain structure extracted. No copyrighted content stored.',
            **results
        }
        
        logger.info(f"Import complete: {results['success_count']}/{len(files)} successful")
        
        return Response(response_data, status=200)
        
    except Exception as e:
        logger.error(f"Import system error: {str(e)}")
        return Response({
            'error': 'Import system error',
            'legal_disclaimer': 'Only FX chain structure extracted. No copyrighted content stored.'
        }, status=500)

def create_template_from_safe_extraction(safe_result: Dict, user, import_options: Dict, original_filename: str) -> FXChainTemplate:
    """
    Create FXChainTemplate from safely extracted data
    
    Args:
        safe_result: Legally compliant extraction result
        user: Django User object
        import_options: Import configuration options
        original_filename: Original file name for reference
    
    Returns:
        Created FXChainTemplate object or None if creation fails
    """
    try:
        # Generate safe template name
        base_name = safe_result.get('name', 'Imported Chain')
        
        if import_options['add_source_prefix']:
            source_type = safe_result.get('source_type', 'imported')
            base_name = f"{base_name} ({source_type})"
        
        # Ensure unique name for this user
        name = base_name
        counter = 1
        while FXChainTemplate.objects.filter(user=user, name=name).exists():
            name = f"{base_name} ({counter})"
            counter += 1
        
        # Create template with only safe data
        template = FXChainTemplate.objects.create(
            user=user,
            name=name,
            description=safe_result.get('description', f'Imported from {original_filename}'),
            genre=safe_result.get('genre', 'imported'),
            instrument_type=safe_result.get('instrument_type', 'generic'),
            fx_chain=safe_result['fx_chain'],  # This is the safe FX chain structure
            parameters=None,  # Never store parameters (legal safety)
            template_type='imported',
            is_public=import_options.get('make_public', False),
            tags=f"imported, {safe_result.get('source_type', 'preset')}"
        )
        
        logger.debug(f"Created template: {template.name} with chain: {template.fx_chain}")
        return template
        
    except Exception as e:
        logger.error(f"Error creating template: {str(e)}")
        return None

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def preview_preset_conversion(request):
    """
    Preview what a preset file would look like when converted (safely)
    
    This allows users to see the FX chain structure that would be extracted
    without actually importing the preset.
    """
    try:
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=400)
        
        uploaded_file = request.FILES['file']
        
        # Validate file
        file_paths = [uploaded_file.name]
        is_valid, error_msg = LegalComplianceManager.validate_import_request(file_paths, request.user.id)
        
        if not is_valid:
            return Response({'error': error_msg}, status=400)
        
        # Save file temporarily for analysis
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            for chunk in uploaded_file.chunks():
                tmp_file.write(chunk)
            tmp_file_path = tmp_file.name
        
        # Extract FX chain structure safely
        extractor = SafeFXChainExtractor()
        extraction_result = extractor.extract_fx_chain_structure(tmp_file_path)
        
        # Clean up temp file
        os.unlink(tmp_file_path)
        
        if extraction_result:
            # Sanitize for legal compliance
            compliance = LegalComplianceManager()
            safe_result = compliance.sanitize_extraction_result(extraction_result)
            
            return Response({
                'success': True,
                'preview': {
                    'name': safe_result.get('name', 'Imported Chain'),
                    'fx_chain': safe_result['fx_chain'],
                    'chain_length': safe_result['chain_length'],
                    'source_type': safe_result.get('source_type', 'unknown'),
                    'extraction_method': safe_result.get('extraction_method', 'structure_analysis')
                },
                'supported': True,
                'legal_status': 'safe_extraction',
                'legal_disclaimer': 'Only FX chain structure shown. No copyrighted content extracted.'
            }, status=200)
        else:
            return Response({
                'success': False,
                'supported': False,
                'message': 'Could not extract FX chain structure from this file',
                'legal_disclaimer': 'Only FX chain structure extracted. No copyrighted content processed.'
            }, status=200)
            
    except Exception as e:
        logger.error(f"Preview error: {str(e)}")
        return Response({
            'error': 'Preview failed', 
            'legal_disclaimer': 'Only FX chain structure extracted. No copyrighted content processed.'
        }, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_supported_formats(request):
    """
    Return information about supported preset formats
    
    This endpoint provides information about what file types we can import
    and legal guidelines for users.
    """
    try:
        extractor = SafeFXChainExtractor()
        
        supported_formats = {
            '.xml': {
                'name': 'Generic XML Presets',
                'description': 'XML-based preset files from various plugins',
                'safety_level': 'high',
                'extraction_method': 'structure_analysis'
            },
            '.xps': {
                'name': 'XML-Style Presets',
                'description': 'XML preset format (structure only)',
                'safety_level': 'high', 
                'extraction_method': 'structure_analysis'
            },
            '.ffp': {
                'name': 'Generic Plugin Presets',
                'description': 'Plugin preset files (structure only)',
                'safety_level': 'high',
                'extraction_method': 'structure_analysis'
            },
            '.json': {
                'name': 'JSON Presets',
                'description': 'JSON-based preset files',
                'safety_level': 'high',
                'extraction_method': 'structure_analysis'
            },
            '.fxp': {
                'name': 'VST Presets',
                'description': 'Standard VST preset format (structure only)',
                'safety_level': 'medium',
                'extraction_method': 'header_analysis'
            },
            '.fxb': {
                'name': 'VST Banks',
                'description': 'VST preset bank files (structure only)',
                'safety_level': 'medium',
                'extraction_method': 'header_analysis'
            }
        }
        
        return Response({
            'supported_formats': supported_formats,
            'total_formats': len(supported_formats),
            'legal_compliance': {
                'extraction_method': 'structure_only',
                'copyrighted_content': False,
                'parameter_values': False,
                'brand_names': False,
                'user_owns_files': True
            },
            'usage_guidelines': {
                'file_ownership': 'You must own or have rights to all imported files',
                'extraction_scope': 'Only FX chain structure is extracted',
                'no_redistribution': 'Do not redistribute extracted chains commercially',
                'personal_use': 'Imported chains are for personal use only'
            },
            'legal_disclaimer': LegalComplianceManager.create_legal_disclaimer()
        }, status=200)
        
    except Exception as e:
        logger.error(f"Error getting supported formats: {str(e)}")
        return Response({'error': 'Could not retrieve format information'}, status=500)

# ===== TEMPLATE BROWSING & COMMUNITY APIs =====

@api_view(['GET'])
@permission_classes([AllowAny])
def browse_templates(request):
    """
    Browse all public templates with filtering and search
    
    Query parameters:
    - genre: Filter by genre
    - instrument: Filter by instrument type
    - search: Search in names, descriptions, tags
    - min_rating: Minimum rating (default 3.0)
    - template_type: Filter by type (factory, user, community, imported)
    - limit: Number of results (default 20, max 100)
    """
    try:
        # Get query parameters
        genre = request.GET.get('genre', '').lower()
        instrument = request.GET.get('instrument', '').lower()
        search = request.GET.get('search', '')
        min_rating = float(request.GET.get('min_rating', 3.0))
        template_type = request.GET.get('template_type', '')
        limit = min(int(request.GET.get('limit', 20)), 100)  # Max 100 results
        
        logger.debug(f"Browse request: genre={genre}, instrument={instrument}, search='{search}'")
        
        # Build base query for public templates
        queryset = FXChainTemplate.objects.filter(is_public=True)
        
        # Apply filters
        if genre and genre != 'all':
            queryset = queryset.filter(genre=genre)
        if instrument and instrument != 'all':
            queryset = queryset.filter(instrument_type=instrument)
        if template_type and template_type != 'all':
            queryset = queryset.filter(template_type=template_type)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(tags__icontains=search)
            )
        
        # Filter by rating
        queryset = queryset.filter(rating__gte=min_rating)
        
        # Order by popularity and rating
        queryset = queryset.order_by('-rating', '-downloads', '-created_at')
        
        # Limit results
        templates = queryset[:limit]
        
        # Format results
        template_list = []
        for template in templates:
            template_list.append({
                'id': template.id,
                'name': template.name,
                'description': template.description,
                'genre': template.genre,
                'instrument_type': template.instrument_type,
                'fx_chain': template.fx_chain,
                'chain_length': len(template.fx_chain),
                'rating': template.rating,
                'downloads': template.downloads,
                'author': template.user.username,
                'template_type': template.template_type,
                'tags': template.get_tags_list(),
                'created_at': template.created_at.isoformat()
            })
        
        return Response({
            'templates': template_list,
            'count': len(template_list),
            'total_available': queryset.count(),
            'filters_applied': {
                'genre': genre or 'all',
                'instrument': instrument or 'all',
                'search': search,
                'min_rating': min_rating,
                'template_type': template_type or 'all',
                'limit': limit
            }
        }, status=200)
        
    except Exception as e:
        logger.error(f"Error browsing templates: {str(e)}")
        return Response({'error': 'Could not retrieve templates'}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_user_templates(request):
    """
    Export user's templates as JSON for backup/sharing
    
    Returns all of the user's templates in a portable JSON format.
    """
    try:
        # Get all user's templates
        templates = FXChainTemplate.objects.filter(user=request.user)
        
        # Format for export
        export_data = {
            'version': '1.0',
            'exported_by': request.user.username,
            'export_date': __import__('datetime').datetime.now().isoformat(),
            'template_count': templates.count(),
            'templates': []
        }
        
        for template in templates:
            export_data['templates'].append({
                'name': template.name,
                'description': template.description,
                'genre': template.genre, 
                'instrument_type': template.instrument_type,
                'fx_chain': template.fx_chain,
                'template_type': template.template_type,
                'tags': template.tags,
                'is_public': template.is_public,
                'created_at': template.created_at.isoformat(),
                'updated_at': template.updated_at.isoformat()
            })
        
        logger.info(f"Exported {len(export_data['templates'])} templates for {request.user.username}")
        
        return Response(export_data, status=200)
        
    except Exception as e:
        logger.error(f"Export error: {str(e)}")
        return Response({'error': 'Export failed'}, status=500)

# ===== LEGACY API SUPPORT =====

@api_view(['GET'])
def fx_recommendation_view(request):
    """
    Legacy API endpoint for backward compatibility
    
    This maintains compatibility with older versions of the plugin
    that might still use the original recommendation system.
    """
    try:
        fx_type = request.GET.get('type', '').lower()
        
        # Map old types to new system
        type_mapping = {
            'vocals': ('default', 'vocals'),
            'drums': ('default', 'drums'),
            'lofi': ('lofi', 'full_mix')
        }
        
        if fx_type in type_mapping:
            genre, instrument = type_mapping[fx_type]
            templates = get_template_by_category(genre, instrument)
            
            if templates:
                # Return first template in old format
                first_template = list(templates.items())[0]
                return Response({
                    'type': fx_type,
                    'recommendation': {
                        'name': first_template[0],
                        'chain': first_template[1]
                    },
                    'count': 1
                })
        
        return Response({
            'error': 'Invalid type. Use: vocals, drums, lofi',
            'available_types': ['vocals', 'drums', 'lofi']
        }, status=400)
        
    except Exception as e:
        logger.error(f"Legacy API error: {str(e)}")
        return Response({'error': 'Legacy API error'}, status=500)