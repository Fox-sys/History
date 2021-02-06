from django.core.management.base import BaseCommand
from ...models import MainUser
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "Preparing database"

    def handle(self, *args, **kwargs):
        print("Preparing database...")
        print("creating moder group...")
        try:
            self.create_moder()
            print("moder group created")
        except Exception as e:
            print("can't create moder group")
            print(e)
        print("creating admin group...")
        try:
            self.create_admin()
            print("admin group created")
        except Exception as e:
            print("can't create admin group")
            print(e)
        print("creating superuser group...")
        try:
            self.create_su()
            print("superuser created")
            print("login: SU")
            print("password: 135790asz")
        except Exception as e:
            print("can't create superuser")
            print(e)
        

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