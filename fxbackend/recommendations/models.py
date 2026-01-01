# This file defines the database structure for our FX templates and user management

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import json

class FXChainTemplate(models.Model):
    
    """
    Core model for storing FX chain templates
    
    This represents a single FX processing chain that users can save, share, and reuse.
    Think of it like a "preset" but for entire FX chains rather than individual plugin settings.
    
    Example: A hip-hop vocal chain might be ['EQ', 'De-esser', 'Compressor', 'Reverb']
    """

    # Template Type Choices - These define where the template came from
    TEMPLATE_TYPES = [
        ('factory', 'Factory Preset'),      # Built-in templates we provide
        ('user', 'User Created'),           # Templates created by users in the plugin
        ('community', 'Community Shared'),  # User templates shared publicly
        ('imported', 'Imported'),           # Templates imported from other software (safely)  
    ]

    # Genre Choices - Musical genres for categorization
    # These help users find relevant templates for their music style
    GENRE_CHOICES = [
        ('hip-hop', 'Hip-Hop'),
        ('edm', 'EDM'),
        ('rock', 'Rock'),
        ('pop', 'Pop'),
        ('rnb', 'R&B'),
        ('jazz', 'Jazz'),
        ('country', 'Country'),
        ('reggae', 'Reggae'),
        ('ambient', 'Ambient'),
        ('lofi', 'Lo-Fi'),
        ('trap', 'Trap'),
        ('drill', 'Drill'),
        ('afrobeats', 'Afrobeats'),
        ('other', 'Other'),
    ]

    # Instrument Type Choices - What kind of audio this template is designed for
    # This helps users find templates appropriate for their source material
    INSTRUMENT_CHOICES = [
        ('vocals', 'Vocals'),
        ('guitar', 'Guitar'),
        ('bass', 'Bass'),
        ('drums', 'Drums'),
        ('piano', 'Piano'),
        ('synth', 'Synthesizer'),
        ('keys', 'Keys'),
        ('saxophone', 'Saxophone'),
        ('percussion', 'Percussion'),
        ('pad', 'Pad'),
        ('full_mix', 'Full Mix'),
        ('hi_hats', 'Hi-Hats'),
        ('other', 'Other'),
    ]

    # === CORE FIELDS ===
    
    # Every template belongs to a user (the creator)
    # CASCADE means if user is deleted, their templates are deleted too
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='fx_templates',
        help_text="The user who created this template"
    )

    # Template name - what the user calls this template
    name = models.CharField(
        max_length=100,
        help_text="User-friendly name for this template (e.g., 'Warm Vocal Chain')"
    )

    # Optional description explaining what this template does
    description = models.TextField(
        blank=True,
        help_text="Optional description of what this template is good for"
    )

    # === CLASSIFICATION FIELDS ===
    
    # What genre of music this template works best with
    genre = models.CharField(
        max_length=20,
        choices=GENRE_CHOICES,
        help_text="Musical genre this template is designed for"
    )

    # What type of instrument/audio this template is designed for
    instrument_type = models.CharField(
        max_length=20,
        choices=INSTRUMENT_CHOICES,
        help_text="Type of audio source this template works best with"
    )

    # How this template was created
    template_type = models.CharField(
        max_length=20,
        choices=TEMPLATE_TYPES,
        default='user',
        help_text="Origin of this template (factory, user-created, community shared, or imported)"
    )

    # === FX CHAIN DATA ===
    
    # The actual FX chain - stored as JSON array
    # Example: ["EQ", "Compressor", "Reverb", "Delay"]
    fx_chain = models.JSONField(
        help_text="Array of FX plugin names in processing order"
    )

    # Optional: Parameters for each FX (for future use)
    # This could store specific settings, but we start with just the chain structure
    parameters = models.JSONField(
        blank=True,
        null=True,
        help_text="Optional parameter settings for each FX (future feature)"
    )

    # === COMMUNITY FEATURES ===
    
    # Whether other users can see and use this template
    is_public = models.BooleanField(
        default=False,
        help_text="Allow other users to see and use this template"
    )

    # How many times this template has been downloaded/used by others
    downloads = models.IntegerField(
        default=0,
        help_text="Number of times this template has been used by other users"
    )

    # Average user rating (1-5 stars)
    rating = models.FloatField(
        default=0.0,
        help_text="Average user rating (0.0 to 5.0 stars)"
    )

    # Number of ratings (for calculating averages)
    rating_count = models.IntegerField(
        default=0,
        help_text="Number of users who have rated this template"
    )

    # Searchable tags (comma-separated)
    # Example: "warm, vintage, radio, broadcast"
    tags = models.CharField(
        max_length=200,
        blank=True,
        help_text="Comma-separated tags for searching"
    )

    # === METADATA ===
    
    # When this template was created
    created_at = models.DateTimeField(auto_now_add=True)

    # When this template was last modified
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Users can't have two templates with the same name
        unique_together = ['user', 'name']

        # Default ordering: newest first
        ordering = ['-created_at']

        # Database indexes for faster queries
        indexes = [
            models.Index(fields=['genre', 'instrument_type']),  # Fast genre/instrument lookup
            models.Index(fields=['is_public', 'rating']),       # Fast public template queries
            models.Index(fields=['template_type']),             # Fast filtering by type
        ]
    
    def __str__(self):
        """
        String representation for admin interface and debugging
        """
        return f"{self.name} ({self.genre} - {self.instrument_type})"
    
    def clean(self):
        """
        Data validation - called before saving to ensure data integrity
        This is like a "sanity check" on the data before it goes into the database
        """
        # Ensure fx_chain is a list (array)
        if not isinstance(self.fx_chain, list):
            raise ValidationError("FX chain must be a list of plugin names")
        
        # Ensure fx_chain isn't empty
        if not self.fx_chain:
            raise ValidationError("FX chain cannot be empty")
        
        # Validate each FX name in the chain
        for fx in self.fx_chain:
            if not isinstance(fx, str) or not fx.strip():
                raise ValidationError("Each FX must be a non-empty string")
            
        # Ensure rating is within valid range
        if not (0.0 <= self.rating <= 5.0):
            raise ValidationError("Rating must be between 0.0 and 5.0")
        
    def get_tags_list(self):
        """
        Convert comma-separated tags string into a Python list
        This makes it easier to work with tags in templates and API responses
        """
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def increment_downloads(self):
        """
        Safely increment the download counter
        This is called whenever someone uses this template
        """
        self.downloads += 1
        self.save(update_fields=['downloads'])

    def update_rating(self, new_rating: float, is_new_rating: bool = True):
        """
        Update the average rating when a user rates this template
        
        Args:
            new_rating: The new rating (1-5)
            is_new_rating: Whether this is a new rating (vs updating existing)
        """
        if is_new_rating:
            # Calculate new average with additional rating
            total_points = (self.rating * self.rating_count) + new_rating
            self.rating_count += 1
            self.rating = total_points / self.rating_count
        else:
            # Recalculate average (when user changes their rating)
            # This would require more complex logic to track old rating
            pass

        self.save(update_fields=['rating', 'rating_count'])
    

class TemplateRating(models.Model):
    """
    User ratings for community templates
    
    This tracks who rated which template and what rating they gave.
    It prevents users from rating the same template multiple times.
    """

    # The user who gave the rating
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="User who gave this rating"
    )

    # The template being rated
    template = models.ForeignKey(
        FXChainTemplate,
        on_delete=models.CASCADE,
        related_name='ratings',
        help_text="Template being rated"
    )

    # The rating (1-5 stars)
    rating = models.IntegerField(
        choices=[(i, f"{i} stars") for i in range(1, 6)],
        help_text="Rating from 1 to 5 stars"
    )
    
    # Optional written review
    review = models.TextField(
        blank=True,
        help_text="Optional written review"
    )

    # When this rating was given
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Each user can only rate each template once
        unique_together = ['user', 'template']

        # Default ordering: newest ratings first
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} rated {self.template.name}: {self.rating} stars"
    

class TemplateCollection(models.Model):
    """
    User-created collections/folders of templates
    
    This allows users to organize their templates into custom groups.
    Think of it like playlists for music, but for FX templates.
    
    Examples:
    - "My Vocal Chains"
    - "Lo-Fi Hip-Hop Pack"
    - "Client Project Templates"
    """

    # The user who owns this collection
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='template_collections',
        help_text="User who owns this collection"
    )

    # Collection name
    name = models.CharField(
        max_length=100,
        help_text="Name of this collection"
    )

    # Optional description
    description = models.TextField(
        blank=True,
        help_text="Optional description of this collection"
    )

    # Templates in this collection (many-to-many relationship)
    # A template can be in multiple collections, and a collection can have multiple templates
    templates = models.ManyToManyField(
        FXChainTemplate,
        blank=True,
        help_text="Templates included in this collection"
    )

    # Whether other users can see this collection
    is_public = models.BooleanField(
        default=False,
        help_text="Allow other users to see this collection"
    )

    # When this collection was created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Users can't have two collections with the same name
        unique_together = ['user', 'name']

        # Default ordering: newest first
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
    def get_template_count(self):
        # Get the number of templates in this collection
        return self.templates.count()
    

class ImportLog(models.Model):
    """
    Log of preset import operations
    
    This tracks when users import presets and what happened.
    Useful for debugging and understanding user behavior.
    """

    # User who performed the import
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="User who performed this import"
    )

    # Number of files processed
    files_processed = models.IntegerField(
        default=0,
        help_text="Number of files user tried to import"
    )

    # Number of successful conversions
    successful_imports = models.IntegerField(
        default=0,
        help_text="Number of files successfully converted and imported"
    )

    # Number of failed conversions
    failed_imports = models.IntegerField(
        default=0,
        help_text="Number of files that failed to import"
    )

    # Types of files imported (JSON field to store array)
    # Example: ["vst", "xml", "json"]
    file_types = models.JSONField(
        default=list,
        help_text="Types of files that were imported"
    )

    # Any error messages (for debugging)
    error_messages = models.JSONField(
        default=list,
        blank=True,
        help_text="Error messages from failed imports"
    )

    # When this import happened
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} import: {self.successful_imports}/{self.files_processed} successful"
    

# === SIGNAL HANDLERS ===
# These are "hooks" that automatically run when certain events happen

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Automatically create an API token for every new user
    
    This runs every time a User is saved. If it's a new user (created=True),
    we create an authentication token they can use for API calls.
    
    The token allows the C++ plugin to authenticate with our Django API.
    """

    if created:
        # Create a token for the new user
        # get_or_create() ensures we don't create duplicates
        Token.objects.get_or_create(user=instance)

@receiver(post_save, sender=TemplateRating)
def update_template_rating(sender, instance, created, **kwargs):
    """
    Automatically update template's average rating when someone rates it
    
    This runs every time a TemplateRating is saved.
    If it's a new rating, we update the template's average rating.
    """
    if created:
        # This is a new rating, update the template's average
        template = instance.template

        # Calculate new average rating
        all_ratings = TemplateRating.objects.filter(template=template)
        total_ratings = all_ratings.count()
        average_rating = sum(rating.rating for rating in all_ratings) / total_ratings

        #Update the template
        template.rating = average_rating
        template.rating_count = total_ratings
        template.save(update_fields=['rating', 'rating_count'])