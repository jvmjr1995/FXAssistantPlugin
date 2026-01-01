# recommendations/urls.py
# Complete URL configuration for the FXAssistant template and import system

from django.urls import path
from . import views

# URL patterns for the recommendations app
# These define the API endpoints that the C++ plugin will call

urlpatterns = [
    
    # ===== CORE TEMPLATE SUGGESTION APIs =====
    # These are the main endpoints the plugin uses for getting FX suggestions
    
    path(
        'suggest-fx-chain/', 
        views.suggest_fx_chain, 
        name='suggest_fx_chain'
    ),
    # Primary endpoint: POST with genre/fx_type, returns multiple template options
    # Used by: C++ plugin main suggestion feature
    
    path(
        'recommendations/', 
        views.fx_recommendation_view, 
        name='fx_recommendations'
    ),
    # Legacy endpoint: GET with ?type=vocals, returns single recommendation
    # Used by: Backward compatibility with older plugin versions
    
    # ===== TEMPLATE MANAGEMENT APIs =====
    # These endpoints handle user's custom templates
    
    path(
        'save-template/', 
        views.save_custom_template, 
        name='save_template'
    ),
    # Save user's custom FX chain as a template
    # Used by: Plugin "Save Template" button
    
    path(
        'export-templates/', 
        views.export_user_templates, 
        name='export_templates'
    ),
    # Export all user's templates as JSON for backup
    # Used by: Plugin "Export" functionality
    
    path(
        'browse-templates/', 
        views.browse_templates, 
        name='browse_templates'
    ),
    # Browse/search public community templates
    # Used by: Plugin template browser, community features
    
    # ===== SAFE PRESET IMPORT APIs =====
    # These endpoints handle legally safe preset file imports
    
    path(
        'import-presets-safe/', 
        views.import_industry_presets_safe, 
        name='import_presets_safe'
    ),
    # Main import endpoint: Upload preset files, extract FX chains safely
    # Used by: Plugin "Import Industry Presets" feature
    
    path(
        'preview-conversion/', 
        views.preview_preset_conversion, 
        name='preview_conversion'
    ),
    # Preview what would be extracted from a preset file
    # Used by: Plugin preset preview before import
    
    path(
        'supported-formats/', 
        views.get_supported_formats, 
        name='supported_formats'
    ),
    # Get information about supported preset file formats
    # Used by: Plugin help system, format validation
    
    # ===== FUTURE ENDPOINTS =====
    # These will be implemented in future versions
    
    # path(
    #     'rate-template/<int:template_id>/', 
    #     views.rate_template, 
    #     name='rate_template'
    # ),
    # # Rate and review community templates
    # # Used by: Community rating system
    
    # path(
    #     'create-collection/', 
    #     views.create_template_collection, 
    #     name='create_collection'
    # ),
    # # Create custom template collections/folders
    # # Used by: Template organization features
    
    # path(
    #     'nft-marketplace/', 
    #     views.nft_template_marketplace, 
    #     name='nft_marketplace'
    # ),
    # # Web3 NFT template marketplace
    # # Used by: Future Web3 integration
]

"""
API Endpoint Usage Guide for C++ Plugin Development:

1. GET FX SUGGESTIONS:
   POST /api/suggest-fx-chain/
   Body: {"genre": "hip-hop", "fx_type": "vocals"}
   Returns: Multiple template options (factory/user/community)

2. SAVE USER TEMPLATE:
   POST /api/save-template/
   Headers: Authorization: Token <user_token>
   Body: {"name": "My Chain", "fx_chain": [...], "genre": "...", ...}

3. IMPORT PRESETS (SAFE):
   POST /api/import-presets-safe/
   Headers: Authorization: Token <user_token>
   Form Data: files=<multiple_preset_files>

4. BROWSE COMMUNITY:
   GET /api/browse-templates/?genre=hip-hop&min_rating=4.0
   Returns: Filtered list of public templates

5. EXPORT TEMPLATES:
   GET /api/export-templates/
   Headers: Authorization: Token <user_token>
   Returns: JSON backup of all user templates

Authentication:
- Unauthenticated: Can browse public templates, get suggestions
- Authenticated: Can save templates, import presets, access personal data
- Token format: "Authorization: Token <40-character-hex-string>"

Rate Limits:
- Suggestions: Unlimited (cached responses)
- Template saves: 100/hour per user
- Preset imports: 50 files/hour per user
- Template browsing: 1000 requests/hour per IP

Error Handling:
- All endpoints return JSON responses
- Success: HTTP 200/201 with data
- Client error: HTTP 400 with error message
- Server error: HTTP 500 with generic error
- Authentication required: HTTP 401
- Rate limited: HTTP 429

Legal Compliance:
- Import endpoints extract ONLY FX chain structure
- No copyrighted parameter values stored
- No brand names or proprietary content retained
- Users must own all imported preset files
- Clear legal disclaimers in all import responses
"""