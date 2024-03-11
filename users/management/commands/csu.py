from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User(
            email='njutcka@yandex.ru',
            first_name='test',
            last_name='test',
            phone='+79080159099',
            role='admin',
            is_active=True
        )

        user.set_password("12345")

        user.save()
