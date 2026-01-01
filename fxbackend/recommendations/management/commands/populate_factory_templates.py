# recommendations/management/commands/populate_factory_templates.py
# This is a Django management command to populate the database with factory templates
# Run with: python manage.py populate_factory_templates

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recommendations.models import FXChainTemplate
from recommendations.comprehensive_templates import FX_CHAIN_TEMPLATES


class Command(BaseCommand):
    """
    Management command to populate database with factory templates
    
    This command takes our comprehensive template dictionary and creates
    FXChainTemplate objects in the database. This is run once during setup
    to give users a rich library of factory presets.
    """
        
    help = 'Populate database with factory FX chain templates'

    def add_arguments(self, parser):
        """
        Define command line arguments
        This allows customization when running the command
        """
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing factory templates before adding new ones',
        )

        parser.add_argument(
            '--admin-user',
            type=str,
            default='admin',
            help='Username to assign factory templates to (default: admin)',
        )

    def handle(self, *args, **options):
        """
        Main command logic - this is what runs when the command is executed
        """
        self.stdout.write('Starting factory template population...')

        # Get or create the admin user
        admin_username = options['admin_user']
        try:
            admin_user = User.objects.get(username=admin_username)
            self.stdout.write(f'Using existing user: {admin_username}')
        except User.DoesNotExist:
            # Create admin user if it doesn't exist
            admin_user = User.objects.create_user(
                username=admin_username,
                email=f'{admin_username}@fxassistant.com',
                password='factoryuser123'
            )
            self.stdout.write(f'Created new user: {admin_username}')

        # Clear existing factory templates if requested
        if options['clear']:
            deleted_count = FXChainTemplate.objects.filter(
                template_type = 'factory'
            ).delete()[0]
            self.stdout.write(f'Cleared {deleted_count} existing templates for {admin_username}')

        # Counters for reporting
        created_count = 0
        skipped_count = 0
        error_count = 0

        # Process each template with unique naming
        for (genre, instrument_type), templates in FX_CHAIN_TEMPLATES.items():

            self.stdout.write(f'Processing {genre} - {instrument_type}...')

            # Each category can have multiple named templates
            for template_name, fx_chain in templates.items():
                try:
                    # Create UNIQUE name by combining all parts
                    unique_name = f"{template_name} ({genre.title()} {instrument_type.title()})"
                    
                    # Check if template already exists with this exact name
                    existing = FXChainTemplate.objects.filter(
                        user=admin_user,
                        name=unique_name,
                        template_type='factory'
                    ).first()
                    
                    if existing:
                        # Update existing template instead of skipping
                        existing.fx_chain = fx_chain
                        existing.genre = genre
                        existing.instrument_type = instrument_type
                        existing.save()
                        self.stdout.write(f'Updated: {unique_name}')
                        skipped_count += 1
                        continue

                    # Create new template
                    template = FXChainTemplate.objects.create(
                        user=admin_user,
                        name=unique_name,   # Use the unique name
                        description=f"Professional {genre} {instrument_type} processing chain",
                        genre=genre,
                        instrument_type=instrument_type,
                        fx_chain=fx_chain,
                        template_type='factory',
                        is_public=True,     # Factory templates are always public
                        rating=4.5,         # Factory templates get good default rating
                        rating_count=10     # Simulate some ratings
                    )

                    created_count += 1
                    self.stdout.write(f'  ✓ Created: {unique_name}')

                    # Show progress every 10 templates
                    if created_count % 10 == 0:
                        self.stdout.write(f' Created {created_count} templates so far...')
                    
                except Exception as e:
                    error_count += 1
                    self.stderr.write(f'  ✗ Error creating template {template_name}: {str(e)}')

        # Report results
        self.stdout.write(
            self.style.SUCCESS(
                f'Factory template population complete!'
            )
        )
        self.stdout.write(f'Created: {created_count} templates')
        self.stdout.write(f'Updated: {skipped_count} existing templates')
        if error_count > 0:
            self.stdout.write(f'Errors: {error_count} templates failed')
        
        # Show some example templates
        self.stdout.write('\nExample factory templates:')
        recent_templates = FXChainTemplate.objects.filter(
            template_type='factory',
            user=admin_user).order_by('-created_at'
        )[:5]

        for template in recent_templates:
            chain_display = " → ".join(template.fx_chain)
            self.stdout.write(f'  • {template.name}: {chain_display}')