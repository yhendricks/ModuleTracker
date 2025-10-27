from django.core.management.base import BaseCommand
from ModuleTrack.models import PcbType

class Command(BaseCommand):
    help = 'Creates 100 dummy PCB Type entries'

    def handle(self, *args, **kwargs):
        for i in range(1, 101):
            PcbType.objects.create(name=f'Dummy PCB Type {i}', description=f'Description for Dummy PCB Type {i}')
        self.stdout.write(self.style.SUCCESS('Successfully created 100 dummy PCB Type entries.'))
