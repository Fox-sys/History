from django.core.management.base import BaseCommand
from ...models import MainUser
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "Preparing database"

    def handle(self, *args, **kwargs):
        self.create_moder()
        self.create_admin()
        self.create_su()

    def create_moder(self):
        try:
            Group.objects.get(name="Moder")
        except:
            moder = Group(name="Moder")
            moder.save()
            for i in self.moder_permission_ids:
                moder.permissions.add(Permission.objects.get(id=i))
            moder.save()
        
    def create_admin(self):
        try:
            Group.objects.get(name="Admin")
        except:
            admin = Group(name="Admin")
            admin.save()
            for i in self.admin_permission_ids:
                admin.permissions.add(Permission.objects.get(id=i))
            admin.save()    
            
    def create_su(self):
        user = MainUser.objects.create_superuser(username="SU", password="135790asz")
        user.last_name = "No"
        user.first_name = "Name"
        user.save()

    @property
    def moder_permission_ids(self):
        white_list = [4, 12, 8, 16, 28, 24, 32, 31, 30]        
        return white_list
        
    @property
    def admin_permission_ids(self):
        white_list = self.moder_permission_ids + [25, 26, 27, 23]
        return white_list