# recommendations/management/commands/create_test_users.py
# Management command to create test users for development

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    """
    Create test users for development and testing
    """

    help = 'Create test users with API tokens for development'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of test users to create (default: 5)',
        )

    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(f'Creating {count} test users...')

        created_users = []

        for i in range(1, count + 1):
            username = f'testuser{i}'
            email = f'testuser{i}@fxassistant.com'
            password = 'testpass123'

            # Create user if it doesn't exist
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': f'Test',
                    'last_name': f'User {i}',
                }
            )

            if created:
                user.set_password(password)
                user.save()

                # Create API token
                token, _ = Token.objects.get_or_create(user=user)

                created_users.append({
                    'username': username,
                    'password': password,
                    'email': email,
                    'token': token.key
                })
                
                self.stdout.write(f'Created user: {username}')

        if created_users:
            self.stdout.write('\n' + '='*50)
            self.stdout.write('TEST USER CREDENTIALS:')
            self.stdout.write('='*50)
            
            for user_info in created_users:
                self.stdout.write(f"Username: {user_info['username']}")
                self.stdout.write(f"Password: {user_info['password']}")
                self.stdout.write(f"Email: {user_info['email']}")
                self.stdout.write(f"API Token: {user_info['token']}")
                self.stdout.write('-' * 30)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(created_users)} test users')
        )